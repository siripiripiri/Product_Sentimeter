import streamlit as st
from urllib.parse import urlparse, urlunparse
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import altair as alt
load_dotenv()
import pandas as pd
import spacy
import random
import requests
import os
from bs4 import BeautifulSoup
from transformers import pipeline
import matplotlib.pyplot as plt
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm


pipe = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")
nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])

headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

def get_html_pages(url, len_page):
    soups = []

    for page_no in range(1, len_page + 1):
        params = {
            'ie': 'UTF8',
            'reviewerType': 'all_reviews',
            'filterByStar': 'critical',
            'pageNumber': page_no,
        }
        
        response = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        soups.append(soup)

    return soups

def get_reviews(html_data):
    data_dicts = []
    boxes = html_data.select('div[data-hook="review"]')

    for r in boxes:
        try:
            stars = r.find('i', {'data-hook': 'review-star-rating'})
            stars = stars.find('span', {'class': 'a-icon-alt'}).text.split()[0]
            # print(stars)
        except:
            stars = ""
    
        try:
            d = r.find('span',{'data-hook':'review-date'}).text
            d = d.split()[4:]
            date, month, year = d[0], d[1], d[2]
            # print(date, month, year)
        except:
            month = "January"
            year = "2024"

        try:
            review = r.find('span', {'data-hook': 'review-body'})
            review_text = review.find('span').text
        except:
            review_text = ""
        try:
            output = pipe(review_text)
            result_label = output[0]['label']
        except:
            result_label = "positive"
            

        # create Dictionary with al review data 
        data_dict = {
            'Stars' : stars,
            'Month': month,
            'Year': year,
            'Sentiment_label': result_label,
            'Review_text': review_text
        }

        # Add Dictionary in master empty List
        data_dicts.append(data_dict)
    
    return data_dicts


st.set_page_config( page_icon=":cookie:", page_title="Senti-Meter📈",layout="wide")
# Load the dataset)


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
nav_pages = ["Main Page", "Conversational Analysis","Interactive Dashboard", "Brand Wars"]
selected_page = st.sidebar.selectbox("Navigate to:", nav_pages)

# Main Page
if selected_page == "Main Page":
    st.title("📈 Senti-Meter :rocket:")
    st.write("Your Virtual Product Analyst")

    # User input for the URL
    url_input = st.text_input("Enter the URL:")
    # file_path ='Dataset_new/Eltb_new/oralb_el_tb_3.csv'
    file_path = 'realtime.csv'

    # Convert the URL and display the result
    if st.button("Fetch!"):
        if url_input:
            result_url = get_url_up_to_last_slash(url_input)+"/"
            st.success(f"The converted URL is: {result_url}")
            html_pages = get_html_pages(result_url, 10)
            reviews = []
            for html_data in html_pages:
                review = get_reviews(html_data)
                reviews += review
            df_reviews = pd.DataFrame(reviews)
            df_reviews.to_csv("realtime.csv", index=False)
            data = pd.read_csv(file_path)

            downloadable_file = ""
            for index, row in df_reviews.iterrows():
                downloadable_file += row
                downloadable_file += "\n"
        else:
            st.warning("Please enter a valid URL.")

        st.download_button(
            "Download generated file",
            data = "realtime.csv",
            file_name= "download.csv",
            mime = "text/csv",
            help = "Click here to download a CSV file"
        )

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
        positivity_rate = (positive_count) / (positive_count + negative_count + neutral_count)
        number_of_reviews = data.shape[0]
        neutrality_rate = (neutral_count/(positive_count + negative_count + neutral_count))
        negativity_rate = (negative_count/(positive_count + negative_count + neutral_count))



        display_adjectives = []
        for i in range(7):
            choice = random.choice(adjective_list)
            if choice not in display_adjectives:
                display_adjectives.append(choice)

        total1, total2, total3, total4 = st.columns(4)
        with total1:
            st.info('Total Number of Reviews', icon="⭐")
            st.metric("Overall Reviews", round(number_of_reviews,2))
        with total2:
            st.info('Average Positivity Rate', icon="😄")
            st.metric("Positivity Rate", round(positivity_rate,2))
        with total3:
            st.info('Average Neutrality Rate', icon="😐")
            st.metric("Neutrality Rate", round(neutrality_rate,2))
        with total4:
            st.info('Average Negativity Rate', icon="😔")
            st.metric("Negativity Rate",round(negativity_rate,2))
# Add a rectangle around each outer list element
        st.markdown('<div style="display: flex; flex-wrap: wrap;">', unsafe_allow_html=True)

# Add a rectangle around each outer list element with specific background colors
        for aspect, sentiment in display_adjectives:
            if sentiment == "positive":
                bg_color = "#3d7eba"
            elif sentiment == "negative":
                bg_color = "#fa897f"
            else:
                bg_color = "#858282"
            
            st.markdown(f'<div style="border: 2px solid #e2cbcb; border-radius:1rem; padding: 10px; margin: 10px;">{aspect}<span style="background-color: {bg_color}; color:#FFFFFF;margin-left:10px; border-radius: 0.7rem; padding:5px; font-size:16px">{sentiment}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col11, col12 = st.columns(2)

        with col11:
            sum = 0.0
            st.write("Average Ratings\n")
            for i in data['Stars']:
                sum = sum+i
                
            avg = sum/len(data['Stars'])
            st.write(f'{avg} Stars')








        labels = ["Positive", "Negative", "Neutral"]
        colors = ['#3d7eba', '#fa897f', '#858282'] 
        sizes = [positive_count, negative_count, neutral_count]
        with col12:
            # Create the pie chart with custom colors
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
            ax.set_aspect('equal')
            fig.patch.set_facecolor('none')  # Equal aspect ratio ensures the pie chart is circular

            # Display the plot in Streamlit
            st.pyplot(fig)
            labels=["Postive","Negative","Neutral"] 
            sizes=[positive_count, negative_count, neutral_count]





# Page 2
elif selected_page == "Conversational Analysis":
    st.title("AI Insights")
    
    st.header("Ask your CSV 📈")

    user_csv = st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        user_question = st.text_input("Ask your questions about your CSV.")

        llm = OpenAI(temperature=0)
        agent = create_csv_agent(llm, user_csv, verbose=True)

        if user_question is not None and user_question is not "":
            response = agent.run(user_question)
            st.write(response)


#Page 2
elif selected_page == "Brand Wars":
    st.title("Brand Wars")


elif selected_page == "Interactive Dashboard":
    st.title("Interactive Dashboard")
 
    # Get an instance of pygwalker's renderer. You should cache this instance to effectively prevent the growth of in-process memory.
    @st.cache_resource
    def get_pyg_renderer() -> "StreamlitRenderer":
        df = pd.read_csv("realtime.csv")
        # When you need to publish your app to the public, you should set the debug parameter to False to prevent other users from writing to your chart configuration file.
        return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
    
    renderer = get_pyg_renderer()
    
    # Render your data exploration interface. Developers can use it to build charts by drag and drop.
    renderer.render_explore()

    