import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import google.generativeai as genai

import time
from pathlib import Path

import tempfile

from dotenv import load_dotenv
load_dotenv()

import os

#os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page Configuration
st.set_page_config(page_title= "AI Chatbot ", layout="wide")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(r".\Coforge.jpg")
with col2:
    #st.markdown("<h1 style='text-align: left;'>",self.config.get_page_title(),"</h1>", unsafe_allow_html=True)
    st.header("AI Chatbot - Video AI Summarizer Agent")

#st.title("AI Chatbot - Video AI Summarizer Agent")


@st.cache_resource
def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )
## Initial the agent
multimodal_Agent=initialize_agent()

#File Uploader
video_file = st.file_uploader(
    "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI Analysis"
)

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name
    col1, col2,col3 = st.columns([1, 2,3])
    with col1:
        pass
    with col2:
        #st.markdown("<h1 style='text-align: left;'>",self.config.get_page_title(),"</h1>", unsafe_allow_html=True)
        st.video(video_path, format="video/mp4", start_time=0) 
    with col3:
        pass
    
    
    user_query = st.text_area(
        "What insights are you seeking from this video?",
        placeholder="Ask anything about the video content. The AI agent will analyze and gather additional ",
        help="Provide specific questions or insights you want from the video."
    )
    if st.button("🎤 Analyze video ", key="analyze video button"):
        if not user_query:
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            try:
                with st.spinner("Processing video and gathering insights..."):
                    # Upload and process video file
                    processed_video = upload_file(video_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)
                        
                    # Prompt generation for analaysis
                    analysis_prompt = (
                        f"""
                        Analyze the uploaded video for content and context.
                        Respond to the following query using insights and supplementary web research
                        {user_query}
                            
                        Provide a detailed , user-friendly, and actionable response.
                        """                         
                    )
                        
                    # AI Agent processing
                    response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])
                        
                # Display the result
                st.subheader("Analysis Result")
                st.markdown(response.content)
                    
            except Exception as error:
                st.error(f"An error occured during the analysis: {error}")
            finally:
                # Clean up temporary video file
                Path(video_path).unlink(missing_ok=True)
else:
    st.info("Upload a video file to begin analysis.")

# Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#streamlit run app.py