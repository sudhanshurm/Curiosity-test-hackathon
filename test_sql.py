import os
import re
import json
import time
import boto3
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import text
from langchain_aws import ChatBedrock
from langchain_experimental.sql.base import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from prompts import template

# Configure page
st.set_page_config(page_title="📊 Curiosity: AI Assistant for Cost", layout="wide")

# Initialize session state for chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

def config_env_variables():
    os.environ['AWS_CONFIG_FILE'] = r'C:\Users\223149195\.aws\credentials'
    os.environ['REQUESTS_CA_BUNDLE'] = r'C:\Users\223149195\cacert.pem'  # Set the location of the cacert
    # Turn off proxy if the request hangs
    os.environ['HTTPS_PROXY'] = "http://PITC-Zscaler-ASPAC-Bangalore3PR.proxy.corporate.ge.com:80"
    os.environ['AWS_DEFAULT_PROFILE'] = 'mfa'


# Function to extract SQL query from explanation text
def extract_sql_query(explanation_text):
    """Extract SQL query from explanation text that includes SQL code blocks.
    Returns None if no SQL code block is found."""
    # Look for SQL code between triple backticks
    sql_pattern = r"```sql\n([\s\S]*?)```"
    matches = re.findall(sql_pattern, explanation_text)
    
    if matches:
        return matches[0].strip()
    
    # Fallback: try to find any code block if sql-specific not found
    code_pattern = r"```([\s\S]*?)```"
    matches = re.findall(code_pattern, explanation_text)
    
    if matches:
        # Check if this looks like SQL code (contains common SQL keywords)
        code = matches[0].strip()
        if any(keyword in code.lower() for keyword in ['select', 'from', 'where', 'group by', 'order by', 'join', 'having']):
            return code
    
    # If no code blocks found or the code doesn't look like SQL, return None
    return None

# Function to create visualizations based on query results
def create_visualization(df, viz_type, x_axis, y_axis, color_by, title):
    if df.empty:
        return None
    
    try:
        if viz_type == "bar_chart":
            if color_by and color_by in df.columns:
                fig = px.bar(df, x=x_axis, y=y_axis, color=color_by, title=title)
            else:
                fig = px.bar(df, x=x_axis, y=y_axis, title=title)
            return fig
        
        elif viz_type == "line_chart":
            if color_by and color_by in df.columns:
                fig = px.line(df, x=x_axis, y=y_axis, color=color_by, title=title)
            else:
                fig = px.line(df, x=x_axis, y=y_axis, title=title)
            return fig
        
        elif viz_type == "pie_chart":
            fig = px.pie(df, names=x_axis, values=y_axis, title=title)
            return fig
        
        elif viz_type == "scatter_plot":
            if color_by and color_by in df.columns:
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by, title=title)
            else:
                fig = px.scatter(df, x=x_axis, y=y_axis, title=title)
            return fig
        
        else:
            return None
    except Exception as e:
        st.error(f"Error creating visualization: {e}")
        return None

# Function to truncate message history to prevent token limit issues
def truncate_message_history(history, max_pairs=5):
    """Keep only the most recent conversation pairs."""
    messages = history.messages
    if len(messages) > max_pairs:
        # Keep only the most recent pairs
        history.messages = messages[-max_pairs:]
    return history

# Initialize LLM and database only once
@st.cache_resource
def initialize_resources():
    config_env_variables()
  
    llm = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_kwargs=dict(temperature=0, max_tokens=8000),  # Set reasonable max tokens
        credentials_profile_name="mfa"
    )
  
    sqlite_db_uri = "sqlite:///publish_layer_1.db"
    db = SQLDatabase.from_uri(sqlite_db_uri)
    
    message_histories = {}
    
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in message_histories:
            message_histories[session_id] = ChatMessageHistory()
        # Truncate history to prevent token limit issues
        message_histories[session_id] = truncate_message_history(message_histories[session_id])
        return message_histories[session_id]
    
    schema_info = db.get_table_info()
    
    # Create visualization suggestion prompt template
    viz_suggestion_template = """
    Analyze the SQL query and its results to recommend an appropriate visualization.

    SQL Query: {query}
    Query Results (first 10 rows): {results}
    Question: {question}

    Return ONLY a valid JSON object with this exact structure:
    {{
      "visualization_type": "bar_chart|line_chart|pie_chart|scatter_plot|table|none",
      "x_axis": "column name for x-axis",
      "y_axis": "column name for y-axis",
      "color_by": "column for color differentiation (optional)",
      "title": "suggested title for the visualization",
      "description": "brief explanation of why this visualization is appropriate"
    }}

    Choose visualization_type based on these guidelines:
    - bar_chart: For comparing categories or showing counts/sums
    - line_chart: For time series or trends
    - pie_chart: For showing proportions of a whole (limit to <10 categories)
    - scatter_plot: For showing relationships between two numeric variables
    - table: For detailed data that's better viewed as a table
    - none: If no visualization is appropriate

    Return ONLY the JSON object and nothing else.
    """
    
    viz_suggestion_prompt = ChatPromptTemplate.from_template(viz_suggestion_template)
    
    # Create response template
    response_template = """Based on the table schema, question, sql query, and sql response, 
    write a natural language response
    Make a table as well and always make the full table from the sql data.
    Question: {question}
    SQL Query: {query}
    SQL Response: {response}"""
    
    prompt_response = ChatPromptTemplate.from_template(response_template)
    
    # Create prompt with history
    prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", template + "\n\nDatabase Schema:\n" + schema_info),  # Include schema in system message
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
    ])
    
    # Create SQL chain with history
    inner_chain = prompt_with_history | llm | StrOutputParser()
    
    sql_chain_with_history = RunnableWithMessageHistory(
        inner_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history"
    )
    
    # Create full chain for response generation
    def run_query(query):
        return db.run(query)
    
    full_chain = (
    RunnablePassthrough.assign(query=lambda x: extract_sql_query(x["sql_explanation"])).assign(
        schema=lambda _: schema_info,  # Use cached schema
        response=lambda vars: run_query(vars["query"]),
        question=lambda x: x["question"]
    )
    | prompt_response
    | llm
    )
    
    return sql_chain_with_history, db, llm, viz_suggestion_prompt, full_chain, get_session_history

# Get the resources
sql_chain_with_history, db, llm, viz_suggestion_prompt, full_chain, get_session_history = initialize_resources()

# Function to get visualization suggestion
def get_visualization_suggestion(query, results_df, question):
    # Convert DataFrame to string representation for the prompt
    # Limit the size to avoid overwhelming the model
    results_str = results_df.head(10).to_string()
    
    # Get suggestion from LLM
    suggestion_response = llm.invoke(
        viz_suggestion_prompt.format(
            query=query,
            results=results_str,
            question=question
        )
    )
    
    # Extract JSON from response
    try:
        # Get the response text
        response_text = suggestion_response.content
        
        # Try to find a JSON object in the text
        json_pattern = r'\{[\s\S]*?\}'
        json_matches = re.findall(json_pattern, response_text, re.DOTALL)
        
        if json_matches:
            # Try each match until we find valid JSON
            for json_str in json_matches:
                try:
                    suggestion = json.loads(json_str)
                    # Check if it has the required keys
                    if "visualization_type" in suggestion:
                        return suggestion
                except:
                    continue
        
        # If we couldn't parse JSON or find the required keys, create a default response
        st.warning("Could not parse visualization suggestion. Defaulting to table view.")
        return {
            "visualization_type": "none",
            "description": "Could not parse visualization suggestion from LLM response"
        }
    except Exception as e:
        st.error(f"Error in visualization suggestion: {str(e)}")
        return {
            "visualization_type": "none",
            "description": f"Error: {str(e)}"
        }

# Display chat header
st.title("📊 Curiosity: AI Assistant for Cost")
st.markdown("Ask questions about your database in natural language")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        # Display visualization if available
        if message["role"] == "assistant" and "visualization" in message:
            viz = message["visualization"]
            if viz:
                st.plotly_chart(viz, use_container_width=True, key=f"viz_{id(message)}")

# Function to generate response
def generate_sql_response(question, session_id="default_session"):
    response = sql_chain_with_history.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}}
    )
    return response

# Get user input
if prompt := st.chat_input("Ask a question about your data"):
    # Add user message to chat history for UI display
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Get SQL explanation with embedded query
            sql_explanation = generate_sql_response(prompt)
            
            # Display the full explanation
            st.markdown(sql_explanation)
            
            # Extract just the SQL query for execution
            sql_query = extract_sql_query(sql_explanation)

            # Check if a valid SQL query was extracted
            if sql_query:
                # Execute query and get results as DataFrame
                try:
                    # Get the SQLAlchemy engine from the database
                    engine = db._engine
                    
                    # Execute the query and get results as DataFrame
                    with engine.connect() as connection:
                        result = connection.execute(text(sql_query))
                        df_result = pd.DataFrame(result.fetchall(), columns=result.keys())

                    # Display the results table
                    if not df_result.empty:
                        st.dataframe(df_result)
                    else:
                        st.info("Query returned no results.")
                    
                    # Only attempt visualization if we have results
                    visualization = None
                    if not df_result.empty:
                        try:
                            # Get visualization suggestion
                            viz_suggestion = get_visualization_suggestion(sql_query, df_result, prompt)
                            
                            # Create visualization if appropriate
                            if viz_suggestion["visualization_type"] != "none":
                                x_axis = viz_suggestion.get("x_axis")
                                y_axis = viz_suggestion.get("y_axis")
                                color_by = viz_suggestion.get("color_by")
                                title = viz_suggestion.get("title", "Query Results")
                                
                                # Verify columns exist in the dataframe
                                if x_axis and x_axis not in df_result.columns:
                                    st.warning(f"Column '{x_axis}' not found in results. Skipping visualization.")
                                elif y_axis and y_axis not in df_result.columns:
                                    st.warning(f"Column '{y_axis}' not found in results. Skipping visualization.")
                                else:
                                    visualization = create_visualization(
                                        df_result,
                                        viz_suggestion["visualization_type"],
                                        x_axis,
                                        y_axis,
                                        color_by,
                                        title
                                    )
                                    
                                    if visualization:
                                        st.plotly_chart(visualization, use_container_width=True, key=f"new_viz_{int(time.time())}")
                        except Exception as viz_error:
                            st.warning(f"Could not create visualization: {str(viz_error)}")

                    # Get and display full response
                    response = full_chain.invoke({"question": prompt, "sql_explanation": sql_explanation})
                    st.write(response.content)
                    
                    # Add assistant response to chat history for UI display
                    # Only include the final response content, not SQL or technical details
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response.content,  # Only include the final response content
                        "visualization": visualization if 'visualization' in locals() else None
                    })
                    
                    # Update the LangChain message history to replace the assistant's response with just the clean final response
                    message_history = get_session_history("default_session")
                    # We don't need to manually add messages here as RunnableWithMessageHistory handles that,
                    # but we can ensure the last message (the assistant's response) is clean
                    if len(message_history.messages) >= 2:  # If there are messages (should be at least user + assistant)
                        # Replace the last message (assistant's) with just the clean response
                        message_history.messages[-1].content = response.content
                    
                except Exception as e:
                    st.error(f"Error executing query: {str(e)}")
                    st.error(f"Failed SQL query: {sql_query}")
                    
                    # Add assistant response to chat history without visualization
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"I encountered an error while executing the SQL query: {str(e)}"
                    })
                    
                    # Update message history with error message
                    message_history = get_session_history("default_session")
                    if len(message_history.messages) >= 2:
                        message_history.messages[-1].content = f"I encountered an error while executing the SQL query: {str(e)}"
            else:
                # No SQL query was found
                st.warning("No SQL query was found in the response. The model didn't generate executable SQL code.")
                
                # Add the explanation as the response
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": sql_explanation,
                    "visualization": None
                })
                
                # Update message history
                message_history = get_session_history("default_session")
                if len(message_history.messages) >= 2:
                    message_history.messages[-1].content = sql_explanation

# Add a button to clear the conversation
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    # Also clear the LangChain message history
    message_history = get_session_history("default_session")
    message_history.clear()
    st.rerun()

# Add function to display message history
def display_message_history():
    st.sidebar.subheader("Message History Contents")
    
    # Get the LangChain message history
    message_history = get_session_history("default_session")
    
    # Display the contents
    if message_history and message_history.messages:
        for i, msg in enumerate(message_history.messages):
            role = "User" if msg.type == "human" else "Assistant"
            # Truncate long messages for display
            content = msg.content[:300] + "..." if len(msg.content) > 300 else msg.content
            st.sidebar.text(f"{i+1}. {role}:")
            st.sidebar.text_area(f"Content {i+1}", content, height=100, key=f"hist_{i}")
    else:
        st.sidebar.info("No messages in history")
    
    # Display token count estimate (rough estimate)
    if message_history and message_history.messages:
        total_chars = sum(len(msg.content) for msg in message_history.messages)
        # Very rough estimate: ~4 chars per token
        est_tokens = total_chars // 4
        st.sidebar.info(f"Estimated token count: ~{est_tokens}")

# Add button to show message history
if st.sidebar.button("Show Message History"):
    display_message_history()
