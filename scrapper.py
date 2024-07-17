import requests
from bs4 import BeautifulSoup
import json
import uuid

def scrape_website_data(url):
    """
    Scrapes various data (images, videos, text, links) from a webpage
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {
            'videos': [],
            'images': [],
            'text': [],
            'links': []
        }
        
        # Scraping videos
        for video_tag in soup.find_all('video'):
            video_url = video_tag.get('src')
            if video_url:
                video_id = str(uuid.uuid4())  # Generate a unique ID for each video entry
                data['videos'].append({
                    'id': video_id,
                    'url': video_url
                })
        
        # Scraping images
        for img_tag in soup.find_all('img'):
            image_url = img_tag.get('src')
            if image_url and image_url.startswith('https://'):
                image_title = img_tag.get('title', '')
                image_alt = img_tag.get('alt', '')
                image_id = str(uuid.uuid4())  # Generate a unique ID for each image entry
                data['images'].append({
                    'id': image_id,
                    'url': image_url,
                    'title': image_title,
                    'alt': image_alt
                })
        
        # Scraping text
        for p_tag in soup.find_all('p'):
            paragraph_text = p_tag.get_text().strip()
            if paragraph_text:
                data['text'].append(paragraph_text)
        
        # Scraping links
        for a_tag in soup.find_all('a', href=True):
            link_url = a_tag['href']
            if link_url:
                data['links'].append(link_url)
        
        return data
    else:
        raise Exception(f"Failed to fetch webpage. Status code: {response.status_code}")

def save_to_json(data, filename):
    """
    Saves data to a JSON file
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    webpage_url = "https://www.icc-cricket.com/tournaments/t20cricketworldcup/index"  # Replace with the URL of the website you want to scrape
    output_filename = "pixabay.json"
    
    try:
        website_data = scrape_website_data(webpage_url)
        save_to_json(website_data, output_filename)
        print(f"Data saved to {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
