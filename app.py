from flask import Flask, jsonify, request
from scrape import scrape_page  # Import your web scraping script function

app = Flask(__name__)

@app.route('/scrape', methods=['GET','POST'])
def scrape():
    base_url = 'https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    user_agent = request.headers.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')

    all_product_data = []
    all_product_data += scrape_page(base_url,user_agent)

    # Determine the number of pages to scrape
    num_pages = 3  
    for page in range(2, num_pages + 1):
        page_url = f"{base_url}&page={page}"
        all_product_data += scrape_page(page_url)

    return jsonify(all_product_data)

# if __name__ == '__main__':
#     app.run(debug=True)
