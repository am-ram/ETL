from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
# Function to extract Product Title
# def get_title(soup):

#     try:
#         # Outer Tag Object
#         title = soup.find("span", attrs={"id":'productTitle'})
        
#         # Inner NavigatableString Object
#         title_value = title.text

#         # Title as a string value
#         title_string = title_value.strip()

#     except AttributeError:
#         title_string = ""

#     return title_string

# # Function to extract Product Price
# def get_price(soup):

#     try:
#         price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

#     except AttributeError:

#         try:
#             # If there is some deal price
#             price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

#         except:
#             price = ""

#     return price

# # Function to extract Product Rating
# def get_rating(soup):

#     try:
#         rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
#     except AttributeError:
#         try:
#             rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
#         except:
#             rating = ""	

#     return rating

# # Function to extract Number of User Reviews
# def get_review_count(soup):
#     try:
#         review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

#     except AttributeError:
#         review_count = ""	

#     return review_count

# # Function to extract Availability Status
# def get_availability(soup):
#     try:
#         available = soup.find("div", attrs={'id':'availability'})
#         available = available.find("span").string.strip()

#     except AttributeError:
#         available = "Not Available"	

#     return available
# if __name__ == '__main__':

#     # # add your user agent 
#     # HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

#     # # The webpage URL
#     # URL = "https://www.amazon.in/s?k=mobiles"

#     URL = 'https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
#     HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})


#     # HTTP Request
#     webpage = requests.get(URL, headers=HEADERS)

#     # Soup Object containing all data
#     soup = BeautifulSoup(webpage.content, "html.parser")

#     # Fetch links as List of Tag Objects
#     links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

#     # Store the links
#     links_list = []

#     # Loop for extracting links from Tag Objects
#     for link in links:
#             links_list.append(link.get('href'))

#     d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
    
#     # Loop for extracting product details from each link 
#     for link in links_list:
#         new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

#         new_soup = BeautifulSoup(new_webpage.content, "html.parser")

#         # Function calls to display all necessary product information
#         d['title'].append(get_title(new_soup))
#         d['price'].append(get_price(new_soup))
#         d['rating'].append(get_rating(new_soup))
#         d['reviews'].append(get_review_count(new_soup))
#         d['availability'].append(get_availability(new_soup))

    
#     amazon_df = pd.DataFrame.from_dict(d)
#     amazon_df['title'].replace('', np.nan, inplace=True)
#     amazon_df = amazon_df.dropna(subset=['title'])
#     amazon_df.to_csv("amazon_data.csv", header=True, index=False)

# url = 'https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
# HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
# webpage = requests.get(url,headers=HEADERS)

def scrape_page(url):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    webpage = requests.get(url, headers=HEADERS)
    if webpage.status_code == 200:
        # Parsing the HTML content
        soup = BeautifulSoup(webpage.content, "html.parser")

        product_name_divs = soup.find_all("div", class_="KzDlHZ")
        price_divs = soup.find_all("div", class_="Nx9bqj _4b5DiR")
        product_info_divs = soup.find_all("ul", class_='G4BRas')

        star_div = soup.find("div", class_="XQDdHH")
        star_rating = star_div.text.strip() if star_div else None

        ratings_span = soup.find("span", class_="Wphh3N")
        ratings_reviews_text = ratings_span.text.strip() if ratings_span else None
        ratings_count = None
        reviews_count = None
        if ratings_reviews_text:
            ratings_text, reviews_text = ratings_reviews_text.split("&")
            ratings_count = ratings_text.strip().split()[0]
            reviews_count = reviews_text.strip().split()[0]

        product_data = []

        # Extract the text of each product name, price, and info
        for product_name_div, price_div, product_info_div in zip(product_name_divs, price_divs, product_info_divs):
            product_name = product_name_div.text.strip()
            price = price_div.text.strip()
            product_info_items = product_info_div.find_all("li", class_="J+igdf")

            product_info = {
                "RAM_ROM": product_info_items[0].text.strip() if len(product_info_items) > 0 else None,
                "Display": product_info_items[1].text.strip() if len(product_info_items) > 1 else None,
                "Battery": product_info_items[3].text.strip() if len(product_info_items) > 3 else None,
                "Processor": product_info_items[4].text.strip() if len(product_info_items) > 4 else None
            }

            product_data.append({"PhoneName": product_name, "Price": price, **product_info, "Stars": star_rating, "Ratings Count": ratings_count, "Reviews Count": reviews_count})
        return product_data
    else:
        print("Failed to fetch the webpage. Status code:", webpage.status_code)
        return []


base_url = 'https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
all_product_data = []
all_product_data += scrape_page(base_url)

# Determine the number of pages to scrape
num_pages = 3  
for page in range(2, num_pages + 1):
    page_url = f"{base_url}&page={page}"
    all_product_data += scrape_page(page_url)

df = pd.DataFrame(all_product_data)
print(df)