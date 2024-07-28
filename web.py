import requests
from bs4 import BeautifulSoup

def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        return None
    
def extract_title(soup):
    title = soup.find('h1', {'id': 'firstHeading'})
    return title.text if title else None

def extract_article_content(soup):
    content = {}
    for heading in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
        heading_text = heading.text.strip()
        paragraphs = []
        sibling = heading.find_next_sibling()
        while sibling and sibling.name == 'p':
            paragraphs.append(sibling.text.strip())
            sibling = sibling.find_next_sibling()
        if paragraphs:
            content[heading_text] = paragraphs
    return content

def extract_wikipedia_links(soup):
    base_url = "https://en.wikipedia.org"
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/') and ':' not in href:
            full_url = base_url + href
            links.append(full_url)
    return links

def scrape_wikipedia_page(url):
    soup = get_html_content(url)
    if not soup:
        return None

    data = {
        "title": extract_title(soup),
        "content": extract_article_content(soup),
        "links": extract_wikipedia_links(soup)
    }
    return data
