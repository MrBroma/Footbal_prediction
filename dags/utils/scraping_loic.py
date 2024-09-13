import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def scrape_data():
    # Define the full path for the 'data' folder
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data")

    # Create the 'data' folder if it doesn't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # URL of the website to scrape
    root_url = "https://www.football-data.co.uk/belgiumm.php"

    # Check if the request was successful
    response = requests.get(root_url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Get all the URLs containing a CSV file to download on this webpage
    urls = []

    # Find all the <a> tags in the HTML soup related to the links
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith(".csv"):
            full_url = urljoin(root_url, href)
            urls.append(full_url)

    # Loop through the URLs and download the first 5 CSV files
    for link in urls[0:5]:
        # Request the CSV file
        response = requests.get(link)
        print(link)
        # Save the CSV file
        filename = link.split("/")[-2] + ".csv"
        filepath = os.path.join(data_folder, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
            print(f"File {filename} saved in {data_folder} folder")

