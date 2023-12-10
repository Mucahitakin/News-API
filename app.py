from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

url = 'https://www.haberturk.com/son-dakika-haberleri/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
option_values = [option['value'].split('/', 3)[-1] for option in soup.find_all('option')]
del option_values[0]
@app.route("/")
def index():
    return jsonify(option_values)
@app.route("/get-datas/<category>")
def get_news(category):
    if category in option_values:
        category_in_url = f'https://www.haberturk.com/son-dakika-haberleri/{category}'
        response_category = requests.get(category_in_url)
        soup_category = BeautifulSoup(response_category.text, 'html.parser')
        news_urls = soup_category.find_all('div', {'class': 'w-full relative pb-5 border-b dark:border-gray-800'})
        links = [url.find('a')['href'] for url in news_urls] if news_urls else []
        news_data = []
        for index, link in enumerate(links, start=1):
            content_title = news_urls[index - 1].find('span', {'data-name': 'title'}).get_text(strip=True) if news_urls[index - 1].find('span', {'data-name': 'title'}) else None
            date = news_urls[index - 1].find('span', {'data-name': 'date'}).get_text(strip=True) if news_urls[index - 1].find('span', {'data-name': 'date'}) else None
            
            data = {
                "id": index,
                "category": category,
                "title": content_title,
                "date":date,
                "link": link
            }
            news_data.append(data)
        
        return jsonify(news_data), 200
    else:
        return jsonify({"error": "Category not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
