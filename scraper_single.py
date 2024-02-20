import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# HUGGING FACE
load_dotenv()
HF_TOKEN = os.getenv('HF')
print(HF_TOKEN)
API_URL = "https://api-inference.huggingface.co/models/lxyuan/distilbert-base-multilingual-cased-sentiments-student"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
# output = query({
# 	"inputs": review_text,
# })
# print(output)


# product_link = "https://www.amazon.in/Oral-B-Pro-Expert-Premium-Dental-Floss/product-reviews/B00E601GJE/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"
product_link = "https://www.amazon.in/Oral-B-Pro-Expert-Premium-Dental-Floss/product-reviews/B00E601GJE/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber=3"
# product_link = "https://www.amazon.in/Oral-B-Pro-Expert-Premium-Dental-Floss/product-reviews/B00E601GJE/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=2"

def scrape(product_link):

    response = requests.get(product_link)
    print("w")
    while response.status_code != 200:
        print('f', end="")
        response = requests.get(product_link)
    print("w2")

    try:
        # print(response.status_code)
        # if response.status_code != 200:
        #     print("-1")
        #     return -1

        html_data = response.text
        soup = BeautifulSoup(html_data, 'html.parser')
        review_box = soup.find_all('div', class_='a-section celwidget')
        
        for r in review_box:
            stars = r.find('i', {'data-hook': 'review-star-rating'})
            stars = stars.find('span', {'class': 'a-icon-alt'}).text.split()[0]
            print(stars)
        
            d = r.find('span',{'data-hook':'review-date'}).text
            d = d.split()[4:]
            date, month, year = d[0], d[1], d[2]
            print(date, month, year)

            review = r.find('span', {'data-hook': 'review-body'})
            review_text = review.find('span').text
            output = query({
	            "inputs": review_text,
            })
            best_score = -1
            best_label = ''
            for l in output[0]:
                # print(l)
                if l['score'] > best_score:
                    best_score = l['score']
                    best_label = l['label']
            print(best_label)

    except:
        print("except")
        return -1

scrape(product_link)
    
# review_text = "I earliar used the oral b essential floss and Colgate floss and both of them had plastic string which caused bleeding inside the gums. This one is very soft and is professional in quality and does not injure the gums. This was made in USA and oral b should make the same thing available in India. Excellent quality and must buy. This is what floss should be like. Good minty taste as well. Does not shred."




# with file.open
