import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import urllib.request

class Scraper:
    def __init__(self, base_url, output_directory):
        self.base_url = base_url
        self.output_directory = output_directory

    def scrape_and_download(self):
                
        response = requests.get(self.base_url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        link_elements = soup.find_all('a', string='Jupiler League')

        csv_files = []
        
        for index, element in enumerate(link_elements):
            if index < 5:
                href = element.get('href')
                full_url = urllib.parse.urljoin(self.base_url, href)
                csv_files.append(full_url)
        
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        
        for index, url in enumerate(csv_files):
            file_name = os.path.join(self.output_directory, f"{url.split('/')[-2]}.csv")
            urllib.request.urlretrieve(url, file_name)        
        print("All files downloaded successfully")









