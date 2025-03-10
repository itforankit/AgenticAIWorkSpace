import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
# os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])




def main():
    # Page Configuration
    st.set_page_config(page_title= "AI Chatbot ", layout="wide")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(r".\img\Coforge.jpg")
    with col2:
        #st.markdown("<h1 style='text-align: left;'>",self.config.get_page_title(),"</h1>", unsafe_allow_html=True)
        st.header("AI Chatbot - Pdf Summarizer Agent")

    #user_question = st.text_input("Ask a Question from the PDF Files uploaded .. ✍️📝")
    user_question = st.chat_input("Enter your message:")
    if user_question:
        user_input(user_question)

    with st.sidebar:

        st.image("img/Image1.png")
        st.write("---")
        
        st.title("📁 PDF File's Section")
        pdf_docs = st.file_uploader("Upload your PDF Files & \n Click on the Submit & Process Button ", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."): # user friendly message.
                raw_text = get_pdf_text(pdf_docs) # get the pdf text
                text_chunks = get_text_chunks(raw_text) # get the text chunks
                get_vector_store(text_chunks) # create vector store
                st.success("Done")
        
        # st.write("---")
        #st.image("img/Image2.jpg")
        #st.write("AI App created by @ Ankit Singhal")  # add this line to display the image


    # st.markdown(
    #     """
    #     <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #ff6262; padding: 15px; text-align: center;">
    #         © <a href="https://www.linkedin.com/in/ankit0777/" target="_blank">Ankit Singhal</a> 
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

if __name__ == "__main__":
    main()
