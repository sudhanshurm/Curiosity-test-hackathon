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
from prompts import template, viz_suggestion_template, response_template

st.set_page_config(page_title="📊 Curiosity: AI Assistant for Cost", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

def config_env_variables():
    os.environ['AWS_CONFIG_FILE'] = r'C:\Users\223149195\.aws\credentials'
    os.environ['REQUESTS_CA_BUNDLE'] = r'C:\Users\223149195\cacert.pem'
    os.environ['HTTPS_PROXY'] = "http://PITC-Zscaler-ASPAC-Bangalore3PR.proxy.corporate.ge.com:80"
    os.environ['AWS_DEFAULT_PROFILE'] = 'mfa'

def extract_sql_query(explanation_text):
    sql_pattern = r"```sql\n([\s\S]*?)```"
    matches = re.findall(sql_pattern, explanation_text)
    
    if matches:
        return matches[0].strip()

    code_pattern = r"```([\s\S]*?)```"
    matches = re.findall(code_pattern, explanation_text)
    
    if matches:
        code = matches[0].strip()
        if any(keyword in code.lower() for keyword in ['select', 'from', 'where', 'group by', 'order by', 'join', 'having']):
            return code

    return None

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

def execute_query(self, query):
    try:
        with self._engine.connect() as connection:
            result = connection.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        # You could add logging here
        raise Exception(f"Database query failed: {str(e)}")
    
def get_visualization_suggestion(query, results_df, question):

    results_str = results_df.head(10).to_string()

    suggestion_response = llm.invoke(
        viz_suggestion_prompt.format(
            query=query,
            results=results_str,
            question=question
        )
    )

    try:
        response_text = suggestion_response.content
        
        json_pattern = r'\{[\s\S]*?\}'
        json_matches = re.findall(json_pattern, response_text, re.DOTALL)
        
        if json_matches:
            for json_str in json_matches:
                try:
                    suggestion = json.loads(json_str)
                    if "visualization_type" in suggestion:
                        return suggestion
                except:
                    continue
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

def generate_sql_response(question, session_id="default_session"):
    response = sql_chain_with_history.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}}
    )
    return response

def truncate_message_history(history, max_pairs=5):
    """Keep only the most recent conversation pairs."""
    messages = history.messages
    if len(messages) > max_pairs:
        # Keep only the most recent pairs
        history.messages = messages[-max_pairs:]
    return history

def display_message_history():
    st.sidebar.subheader("Message History Contents")
    
    message_history = get_session_history("default_session")

    if message_history and message_history.messages:
        for i, msg in enumerate(message_history.messages):
            role = "User" if msg.type == "human" else "Assistant"
            content = msg.content[:300] + "..." if len(msg.content) > 300 else msg.content
            st.sidebar.text(f"{i+1}. {role}:")
            st.sidebar.text_area(f"Content {i+1}", content, height=100, key=f"hist_{i}")
    else:
        st.sidebar.info("No messages in history")
    
    # Display token count estimate (rough estimate)
    if message_history and message_history.messages:
        total_chars = sum(len(msg.content) for msg in message_history.messages)
        est_tokens = total_chars // 4
        st.sidebar.info(f"Estimated token count: ~{est_tokens}")

@st.cache_resource
def initialize_resources():

    config_env_variables()
    
    llm = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_kwargs=dict(temperature=0, max_tokens=8000),
        credentials_profile_name="mfa"
    )

    sqlite_db_uri = "sqlite:///publish_layer_1.db"
    db = SQLDatabase.from_uri(sqlite_db_uri)

    schema_info = db.get_table_info()

    message_histories = {}
    
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in message_histories:
            message_histories[session_id] = ChatMessageHistory()
        message_histories[session_id] = truncate_message_history(message_histories[session_id])
        return message_histories[session_id]
    
    def run_query(query):
        return db.run(query)
    
    viz_suggestion_prompt = ChatPromptTemplate.from_template(viz_suggestion_template)

    prompt_response = ChatPromptTemplate.from_template(response_template)
    
    prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", template + "\n\nDatabase Schema:\n" + schema_info),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
    ])

    inner_chain = prompt_with_history | llm | StrOutputParser()
    
    sql_chain_with_history = RunnableWithMessageHistory(
        inner_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history"
    )
    
    full_chain = (
    RunnablePassthrough.assign(query=lambda x: extract_sql_query(x["sql_explanation"])).assign(
        schema=lambda _: schema_info,
        response=lambda vars: run_query(vars["query"]),
        question=lambda x: x["question"]
    )
    | prompt_response
    | llm
    )

    return sql_chain_with_history, db, llm, viz_suggestion_prompt, full_chain, get_session_history

sql_chain_with_history, db, llm, viz_suggestion_prompt, full_chain, get_session_history = initialize_resources()

st.title("📊 Curiosity: AI Assistant for Cost")
st.markdown("Ask questions about your database in natural language")

for message in st.session_state.messages:

    with st.expander(f"Debug: Message Structure ({message['role']})"):
        st.json(message)
    
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant" and "visualization" in message:
            viz = message["visualization"]
            if viz:
                st.plotly_chart(viz, use_container_width=True, key=f"viz_{id(message)}")

if prompt := st.chat_input("Ask a question about your data"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)
   
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            sql_explanation = generate_sql_response(prompt)

            st.markdown(sql_explanation)

            sql_query = extract_sql_query(sql_explanation)

            if sql_query:
                try:
                    df_result = db.execute_query(sql_query)

                    if not df_result.empty:
                        st.dataframe(df_result)
                    else:
                        st.info("Query returned no results.")

                    visualization = None
                    if not df_result.empty:
                        try:
                            viz_suggestion = get_visualization_suggestion(sql_query, df_result, prompt)

                            if viz_suggestion["visualization_type"] != "none":
                                x_axis = viz_suggestion.get("x_axis")
                                y_axis = viz_suggestion.get("y_axis")
                                color_by = viz_suggestion.get("color_by")
                                title = viz_suggestion.get("title", "Query Results")

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

                    response = full_chain.invoke({"question": prompt, "sql_explanation": sql_explanation})
                    st.write(response.content)
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response.content,  
                        "visualization": visualization if 'visualization' in locals() else None
                    })
                    
                    message_history = get_session_history("default_session")
                    if len(message_history.messages) >= 2:  
                        message_history.messages[-1].content = response.content
                    
                except Exception as e:
                    st.error(f"Error executing query: {str(e)}")
                    st.error(f"Failed SQL query: {sql_query}")

                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"I encountered an error while executing the SQL query: {str(e)}"
                    })
                    
                    message_history = get_session_history("default_session")
                    if len(message_history.messages) >= 2:
                        message_history.messages[-1].content = f"I encountered an error while executing the SQL query: {str(e)}"
            else:
                st.warning("No SQL query was found in the response. The model didn't generate executable SQL code.")
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": sql_explanation,
                    "visualization": None
                })

                message_history = get_session_history("default_session")
                if len(message_history.messages) >= 2:
                    message_history.messages[-1].content = sql_explanation

if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    # Also clear the LangChain message history
    message_history = get_session_history("default_session")
    message_history.clear()
    st.rerun()

if st.sidebar.button("Show Message History"):
    display_message_history()
