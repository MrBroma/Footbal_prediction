# import of the different libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os

def scrape_data():
    # url of the website to scrape
    root_url = "https://www.football-data.co.uk/belgiumm.php"

    # check if the request was successful
    response = requests.get("https://www.football-data.co.uk/belgiumm.php")

    # parse the html content
    soup = BeautifulSoup(response.content, "html.parser")

    # get all the URL which contain a csv file to d ownload on this webpage
    urls = []


    # Find all the <> tags in the HTML soup related to the links

    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith(".csv"):
            full_url = urljoin(root_url, href)
            urls.append(full_url)

    # create the data folder if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    for link in urls[0:5]:
        # request the csv file
        response = requests.get(link)
        print(link)
        # save the csv file
        filename = link.split("/")[-2] + ".csv"
        filepath = os.path.join("data", filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
            print(f"File {filename} saved in data folder")

