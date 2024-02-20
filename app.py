import streamlit as st
from urllib.parse import urlparse, urlunparse
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="SentiMeter📈")

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://drive.google.com/file/d/1JuXabMvn0ZGtlNGRUQhTkx91yD3KHetl/view?usp=sharing");
    }
   </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .st-emotion-cache-zt5igj{
        font-family: Bricolage Grotesk;
        font-size: 30px;
        min-height: 40px;
    }

    
   </style>
    """,
    unsafe_allow_html=True
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def get_url_up_to_last_slash(url):
    parsed_url = urlparse(url)
    url_up_to_last_slash = urlunparse((parsed_url.scheme, parsed_url.netloc, "/".join(parsed_url.path.split('/')[:-1]), '', '', ''))
    return url_up_to_last_slash


# Increase the size of the title text using HTML
st.title(":trophy: Senti-Meter :rocket:")


st.write("Your perfect Review Analyst")

# User input for the URL
url_input = st.text_input("Enter the URL:")

# Convert the URL and display the result
if st.button("Convert"):
    if url_input:
        result_url = get_url_up_to_last_slash(url_input)+"/"
        st.success(f"The converted URL is: {result_url}")
    else:
        st.warning("Please enter a valid URL.")


st.header("Ask your CSV 📈")

user_csv = st.file_uploader("Upload your CSV file", type="csv")

if user_csv is not None:
    user_question = st.text_input("Ask your questions about your CSV.")


    llm = OpenAI(temperature=0)
    agent = create_csv_agent(llm,user_csv, verbose=True)

    if user_question is not None and user_question is not "":
        response = agent.run(user_question)
        st.write(response)

st.sidebar.header("Play with the tool here!")
years = st.sidebar.selectbox("What would you like to do?","")
