import streamlit as st
from urllib.parse import urlparse, urlunparse
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()
import pandas as pd

st.set_page_config(page_title="SentiMeter📈")

# CSS styles
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

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to get URL up to the last slash
def get_url_up_to_last_slash(url):
    parsed_url = urlparse(url)
    url_up_to_last_slash = urlunparse((parsed_url.scheme, parsed_url.netloc, "/".join(parsed_url.path.split('/')[:-1]), '', '', ''))
    return url_up_to_last_slash

# Navigation bar
nav_pages = ["Main Page", "Brand Wars"]
selected_page = st.sidebar.selectbox("Navigate to:", nav_pages)

# Main Page
if selected_page == "Main Page":
    st.title(":trophy: Senti-Meter :rocket:")
    st.write("Your perfect Review Analyst")

    # User input for the URL
    url_input = st.text_input("Enter the URL:")
    file_path ='Dataset_new/Eltb_new/col_eltb_1.csv'

    data = pd.read_csv(file_path)
    # Convert the URL and display the result
    if st.button("Fetch!"):
        if url_input:
            result_url = get_url_up_to_last_slash(url_input)+"/"
            st.success(f"The converted URL is: {result_url}")
        else:
            st.warning("Please enter a valid URL.")

        
        total1, total2, total3, total4 = st.columns(4)
        with total1:
            st.info('Total Number of Reviews', icon="⭐")
            st.metric("Overall Reviews", f"{data.shape()[0]:,.0f}")
        with total2:
            st.info('Positivity Rate', icon="😄")
            st.metric("Positivity Rate", f"{positivity_rate:,.0f}")
        with total3:
            st.info('Neutrality Rate', icon="😐")
            st.metric("Neutrality Rate", f"{neutrality_rate:,.0f}")
        with total4:
            st.info('Negativity Rate', icon="😔")
            st.metric("Negativity Rate", f"{negativity_rate:,.0f}")







    st.header("Ask your CSV 📈")

    user_csv = st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        user_question = st.text_input("Ask your questions about your CSV.")

        llm = OpenAI(temperature=0)
        agent = create_csv_agent(llm, user_csv, verbose=True)

        if user_question is not None and user_question is not "":
            response = agent.run(user_question)
            st.write(response)

# Page 1
elif selected_page == "Brand Wars":
    st.title("Brand Wars")
    st.write("Brands...")

# # Page 2
# elif selected_page == "Page 2":
#     st.title("Page 2")
#     st.write("Content for Page 2 goes here.")
