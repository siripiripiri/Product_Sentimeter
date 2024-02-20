import requests
from bs4 import BeautifulSoup

product_link = "https://www.amazon.in/Oral-B-Pro-Expert-Premium-Dental-Floss/product-reviews/B00E601GJE/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"

def scrape(product_link):
    try:
        response = requests.get(product_link)
        if response.status_code != 200:
            print("-1")
            return -1

        html_data = response.text
        soup = BeautifulSoup(html_data, 'html.parser')
        review_box = soup.find_all('div', class_='a-section celwidget')
        # print(review_box)
        for r in review_box:
            stars = r.find('i', {'data-hook': 'review-star-rating'})
            stars = stars.find('span', {'class': 'a-icon-alt'}).text.split()[0]
            print(stars)
            # pass


    except:
        return -1

scrape(product_link)