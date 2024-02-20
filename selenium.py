import browsercookie
import requests
from bs4 import BeautifulSoup
import csv
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv('HF')
print(HF_TOKEN)
API_URL = "https://api-inference.huggingface.co/models/lxyuan/distilbert-base-multilingual-cased-sentiments-student"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
# Get cookies for Chrome browser
chrome_cookies = browsercookie.chrome()

# Print the cookies
for cookie in chrome_cookies:
    print(cookie)

def scrape(cookies, review_link, filename):
    fields = ['stars', 'month', 'year', 'sentiment', 'review']
    my_master_list = []

    for i in range(2, pages + 1):
        product_link = f"{review_link}{i}"
        print(product_link)

        response = requests.get(product_link, cookies=cookies)
        while response.status_code != 200:
            response = requests.get(product_link, cookies=cookies)

        html_data = response.text
        soup = BeautifulSoup(html_data, 'html.parser')
        review_box = soup.find_all('div', class_='a-section celwidget')
            
        for r in review_box:
            try:
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
                my_master_list.append([stars, month, year, best_label, review_text])
            except:
                pass

    with open(f"DATASET/{filename}.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(my_master_list)


with open("URLS/tb.txt", "r") as file:
    for d in file:
        d = d.split()
        pages = min((int(d[0]) + 9) // 10, 22)
        filename = d[1]
        review_link = d[2][:-1]

        # scrape(pages, review_link, filename)


# Example usage
pages = 2  # replace with the desired number of pages
filename = 'output'
review_link = 'https://www.amazon.in/Oral-Health-Care-Soft-Free/product-reviews/B00U7EEARI/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber='  # replace with the actual review link

# Replace 'your_cookies' with the actual cookies obtained from the previous step
your_cookies = browsercookie.chrome()

scrape(your_cookies, review_link, filename)
