"""
Title: News Headline Scraper

Subject: Static Web Scraping and Data Extraction

Components: requests, BeautifulSoup

Requirements:
- Fetch HTML from the specified news website's homepage using requests
- Extract news headlines and relevant URLs from the fetched HTML using BeautifulSoup with CSS selectors
- Convert extracted data into a Python list of dictionaries
"""
from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)


def fetch_news():
    try:
        url = "https://www.bbc.com/news"

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        news_data = []

        headlines = soup.select('h2[data-testid="card-headline"]')

        for idx, headline in enumerate(headlines):
            link_tag = headline.find_parent('a')

            if link_tag and headline.get_text(strip=True):
                title = headline.get_text(strip=True)
                link = link_tag.get('href', '')

                if link.startswith('/'):
                    link = f'https://www.bbc.com{link}'

                news_data.append({
                    'id': idx,
                    'title': title,
                    'url': link,
                    'source': 'BBC News'
                    })
        print(f'Fetched {len(news_data)} headlines.')
        return news_data
    
    except requests.RequestException as error:
        print(f'Error fetching news data: {error}')
        return []
    except Exception as error:
        print(f'Error parsing news data: {error}')
        return []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/news')
def get_news():
    news_data = fetch_news()
    return jsonify({
        'success': True,
        'count': len(news_data),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': news_data
        })


if __name__ == '__main__':
    app.run(debug=True)
