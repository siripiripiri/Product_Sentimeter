import requests
from bs4 import BeautifulSoup

# product_link = "https://www.amazon.in/Oral-B-Pro-Expert-Premium-Dental-Floss/product-reviews/B00E601GJE/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=2"
# product_link = "https://www.amazon.in/Oral-B-1-2-3-Fluoride-Toothpaste/product-reviews/B06XYMW1FY/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"
product_link = "https://www.amazon.in/Pepsodent-Germicheck-Toothpaste-150-Pack/product-reviews/B00R1BOIJU/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"
def scrape(product_link):

    response = requests.get(product_link)
    while response.status_code != 200:
        response = requests.get(product_link)

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
            # print(stars)
        
            d = r.find('span',{'data-hook':'review-date'}).text
            d = d.split()[4:]
            date, month, year = d[0], d[1], d[2]
            # print(date, month, year)


            
            # review_text = r.find()


    except:
        print("except")
        return -1

scrape(product_link)