import os
def config_env_variables():
    os.environ['AWS_CONFIG_FILE'] = r'C:\Users\223149195\.aws\credentials'
    os.environ['REQUESTS_CA_BUNDLE'] = r'C:\Users\223149195\cacert.pem'
    os.environ['HTTPS_PROXY'] = "http://PITC-Zscaler-ASPAC-Bangalore3PR.proxy.corporate.ge.com:80"
    os.environ['AWS_DEFAULT_PROFILE'] = 'mfa'

import re

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

import streamlit as st
import plotly as px

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

def truncate_message_history(history, max_pairs=5):
    messages = history.messages
    if len(messages) > max_pairs:
        history.messages = messages[-max_pairs:]
    return history


import pandas as pd
from sqlalchemy import text

def execute_query(self, query):
    try:
        with self._engine.connect() as connection:
            result = connection.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        # You could add logging here
        raise Exception(f"Database query failed: {str(e)}")

def generate_sql_response(question, session_id="default_session"):
    response = sql_chain_with_history.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}}
    )
    return response

from prompts import viz_suggestion_template
from langchain_core.prompts import ChatPromptTemplate
import json

viz_suggestion_prompt = ChatPromptTemplate.from_template(viz_suggestion_template)

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

import os
from langchain_aws import ChatBedrock
from langchain_experimental.sql.base import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from prompts import response_template, template

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




