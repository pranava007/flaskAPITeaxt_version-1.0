from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith('http') and 'api' in href:
            links.append(href)
    return links

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                text_content = response.text
                api_links = extract_links_from_html(text_content)
                return render_template('result.html', text_content=text_content, api_links=api_links)
            except requests.RequestException as e:
                error_message = str(e)
                return render_template('index.html', error=error_message)
        else:
            return render_template('index.html', error='Please enter a URL')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
