import streamlit as st
from bs4 import BeautifulSoup
import requests

def scrape_and_clean_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        doc = BeautifulSoup(response.text, 'html.parser')
        content = doc.find('div', id='page-content')
        
        # Remove unwanted parts
        unwanted_selectors = [
            "div.infobox",
            "th:contains('Other Pages By This Author')",
            "th:contains('Rooms')",
            "th:contains('Entitles')",
            "th:contains('Objects')",
            "th:contains('GOIs')",
            "th:contains('POIs')",
            "th:contains('Tales')",
            "th:contains('Themes')"
        ]
        
        for selector in unwanted_selectors:
            for tag in content.select(selector):
                tag.decompose()

        return content
    else:
        return None

st.title('Web Scraper')

# Input for URL
name = st.text_input('Enter the level,entity,object of the page to scrape. E.G level-101 or level 1-1.', '')

if name:
    # Scrape the content
    url_text = f'http://backrooms-wiki.wikidot.com/{name}'
    st.write(url_text)
    content = scrape_and_clean_content(f'{url_text}')
    if content:
        

        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error('Failed to retrieve content. Please check the URL and try again.')
