import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils import *
import tempfile
import os
#from dotenv import load_dotenv

#load_dotenv()

#groq_api_key = os.environ.get("GROQ_API_KEY")


st.set_page_config(layout='wide')
# Custom CSS to keep the title at the top
st.markdown("""
    <style>
        .title {
            position: fixed;
            top: 30px;
            left: 750px;
            width: 100%;
            background-color: white;
            padding: 10px;
            z-index: 1000;
        }
    </style>
""", unsafe_allow_html=True)

# Display title
st.markdown('<h1 class="title">Invoice Reader</h1>', unsafe_allow_html=True)
#st.markdown("<h1 style='text-align: center;'>Invoice Reader</h1>", unsafe_allow_html=True)
with st.sidebar:
    uploaded_file = st.file_uploader("Upload an invoice image.",type=[".png",".jpg",".jpeg"])
    groq_api_key = st.text_input("Enter your Groq API Key", type="password")

if uploaded_file:
    images = Image.open(uploaded_file)
    bytes_data = uploaded_file.getvalue()
    fig1,fig2 = st.columns(2)

    with fig1:
        with st.container(height=900):
            st.image(bytes_data,use_container_width=True)

    with fig2:
        st.header("**User Prompt**")
        user_input = st.text_area(label="Enter your Query",placeholder ="Ask me anything...",height=250)\
# Button to submit text
        if st.button("Submit"):
            with st.spinner("Wait for it...", show_time=True):
                full_text = analyse_image(bytes_data)
                answer = generate_llm_response(full_text,user_input,groq_api_key)
            with st.container(border=True):
                st.header("Output")
                st.text(answer)

             

