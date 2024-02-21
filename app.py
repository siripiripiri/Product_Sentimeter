import streamlit as st
from urllib.parse import urlparse, urlunparse
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import spacy
import random

nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])
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
    file_path ='Dataset_new/Eltb_new/oralb_el_tb_3.csv'

    data = pd.read_csv(file_path)
    # Convert the URL and display the result
    if st.button("Fetch!"):
        if url_input:
            result_url = get_url_up_to_last_slash(url_input)+"/"
            st.success(f"The converted URL is: {result_url}")
        else:
            st.warning("Please enter a valid URL.")

        positive = ""
        positive_count = 0
        negative = ""
        negative_count = 0
        neutral_count = 0
        adjective_list = []

        for index, row in data.iterrows():
            if str(row['Sentiment_label']) == 'positive':
                positive_count += 1
                if positive_count <= 20:
                    positive += str(row['Review_text'])
            elif str(row['Sentiment_label']) == 'negative':
                negative_count += 1
                if negative_count <= 20:
                    negative += str(row['Review_text'])
            else:
                neutral_count += 1
            # adjective
            doc = nlp(str(row['Review_text']))
            for token in doc:
                if token.pos_ == "ADJ" and [token.text.lower(), row['Sentiment_label']] not in adjective_list:
                    adjective_list.append([token.text.lower(), row['Sentiment_label']])
        
        sentiment_score = (positive_count + neutral_count - negative_count) / (positive_count + negative_count + neutral_count)
        positivity_rate = (positive_count + neutral_count) / (positive_count + negative_count + neutral_count)
        number_of_reviews = data.shape[0]
        neutrality_rate = (neutral_count/(positive_count + negative_count + neutral_count))
        negativity_rate = (negative_count/(positive_count + negative_count + neutral_count))



        display_adjectives = []
        for i in range(7):
            choice = random.choice(adjective_list)
            if choice not in display_adjectives:
                display_adjectives.append(choice)
        # print(display_adjectives)
        total1, total2, total3, total4 = st.columns(4)
        with total1:
            st.info('Total Number of Reviews', icon="⭐")
            st.metric("Overall Reviews", number_of_reviews)
        with total2:
            st.info('Average Positivity Rate', icon="😄")
            st.metric("Positivity Rate", positivity_rate)
        with total3:
            st.info('Average Neutrality Rate', icon="😐")
            st.metric("Neutrality Rate", neutrality_rate)
        with total4:
            st.info('Average Negativity Rate', icon="😔")
            st.metric("Negativity Rate",negativity_rate)







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
