import requests
from bs4 import BeautifulSoup
import time

base_link = "https://www.amazon.in/Colgate-Gentle-Enamel-Ultra-Toothbrush/dp/B08G5GPXHR/ref=sr_1_7_mod_primary_new?crid=6B854ZBXJ8D2&dib=eyJ2IjoiMSJ9._E22AlTRFznBb_xtw6hmR5LcyJqwq8h5b69VBWpTySLsgQI_f0f3RnHFhlFn6itjwkkhiEei0yJn2tGwCR_JbP2v8wWsG7NLctfw0LDU0RRkM5shq0CTTL8tlvxNulKt1x_SKVYtmjlCTxRX4Ju8kIAHXVY3acXNcdNeYn_3HshBuee62qmMgriYQW4yVLzuXyEShPed_gdh3AFus7l--et7oH4lLYHUAQrKAZaC3R-3oQwzTlJ88LVwAv0LG5eWQy5hczGmJoXq7GQXC7KgNok2v_PskzEBknVEN-9CbQs.hOQllPsQxzy0ug2shgPk4CHsOIxLIMEWHP0v5QYy5LQ&dib_tag=se&keywords=toothbrush&qid=1708438370&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=tooth%2Caps%2C201&sr=8-7&th=1"

# connnect to base link
response = requests.get(base_link)
while response.status_code != 200:
    print("f")
    time.sleep(5)
    response = requests.get(base_link)

html_data = response.text
soup = BeautifulSoup(html_data, "html.parser")
element = soup.find("a", {"data-hook": "see-all-reviews-link-foot"})['href']
print(element)
