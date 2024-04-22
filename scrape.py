from flask import Flask, jsonify, request
from app import scrape_page  # Import your web scraping script function

app = Flask(__name__)

@app.route('/scrape', methods=['GET','POST'])
def scrape():
    base_url = 'https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    all_product_data = []
    all_product_data += scrape_page(base_url)

    # Determine the number of pages to scrape
    num_pages = 12 
    for page in range(2, num_pages + 1):
        page_url = f"{base_url}&page={page}"
        all_product_data += scrape_page(page_url)

    return jsonify(all_product_data)

if __name__ == '__main__':
    app.run(host=0.0.0.0,port=5000)
