import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage,HumanMessage
from dotenv import load_dotenv
load_dotenv()

import os
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")


# Page Configuration
st.set_page_config(page_title= "AI Chatbot ", layout="wide")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(r".\Coforge.jpg")
with col2:
    #st.markdown("<h1 style='text-align: left;'>",self.config.get_page_title(),"</h1>", unsafe_allow_html=True)
    st.header("AI Chatbot - MySQL Agent")


user_message = st.chat_input("Enter your message:")
if user_message:
    template = """Based on the table schema below, write a SQL query that would answer the user's question:
    {schema}
    Question: {question}
    SQL Query:"""
    prompt = ChatPromptTemplate.from_template(template)
    prompt.format(schema="my schema",question="how many users are there?")


    mysql_uri = 'mysql+mysqlconnector://root:Mohan%40123@localhost:3306/chinook'
    db = SQLDatabase.from_uri(mysql_uri)

    def get_schema(db):
        schema = db.get_table_info()
        return schema

    llm = ChatOpenAI()

    sql_chain = (
        RunnablePassthrough.assign(schema=lambda _:get_schema)
        | prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )

    def run_query(query):
        return db.run(query)

    template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
    {schema}
    Question: {question}
    SQL Query: {query}
    SQL Response: {response}"""
    prompt_response = ChatPromptTemplate.from_template(template)

    full_chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _:get_schema,
            response=lambda vars: run_query(vars["query"]),
        )
        | prompt_response
        | llm
    )

    user_question = user_message
    response=full_chain.invoke({"question": user_question})
    st.subheader("Agent Response:")
    if hasattr(response, "content"):
        response_text = response.content  # Extract content from AIMessage
    else:
        response_text = str(response)  # Fallback to string conversion

    #st.subheader("Generated Response:")
    st.write(response_text)
    #message=response.get("messages")
   # ai_message=[message.content for message in message if isinstance(message,AIMessage)]  

    print(response)