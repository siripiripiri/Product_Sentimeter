import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# HUGGING FACE
# load_dotenv()
# HF_TOKEN = os.getenv('HF')
# print(HF_TOKEN)
# API_URL = "https://api-inference.huggingface.co/models/lxyuan/distilbert-base-multilingual-cased-sentiments-student"
# headers = {"Authorization": f"Bearer {HF_TOKEN}"}
# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()
# # output = query({
# # 	"inputs": review_text,
# # })
from transformers import pipeline
pipe = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")



# Bypass scraper captcha
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

reviews_url = 'https://www.amazon.in/Colgate-Gentle-Enamel-Ultra-Toothbrush/product-reviews/B08G5GPXHR/'
len_pages = 10


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
            print(stars)
        except:
            stars = ""
    
        try:
            d = r.find('span',{'data-hook':'review-date'}).text
            d = d.split()[4:]
            date, month, year = d[0], d[1], d[2]
            print(date, month, year)
        except:
            month = "January"
            year = "2024"

        try:
            review = r.find('span', {'data-hook': 'review-body'})
            review_text = review.find('span').text
        except:
            review_text = ""
        # output = query({
        #     "inputs": review_text,
        # })
        # best_score = -1
        # best_label = ''
        # print(output)
        # for l in output[0]:
        #     if l['score'] > best_score:
        #         best_score = l['score']
        #         best_label = l['label']
        # print(best_label)
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


with open("Urls_new/floss_new.txt", "r") as file:
    for d in file:
        d = d.split()
        pages = min((int(d[0]) + 9) // 10, 22)
        filename = d[1]
        review_link = d[2][:-1]

        # scrape(pages, review_link, filename)
        
        html_pages = get_html_pages(review_link, pages)
        reviews = []
        for html_data in html_pages:
            review = get_reviews(html_data)
            reviews += review
        
        df_reviews = pd.DataFrame(reviews)
        df_reviews.to_csv(f"Dataset_new/Floss_new/{filename}.csv", index=False)