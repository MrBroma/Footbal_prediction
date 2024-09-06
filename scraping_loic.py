# import of the different libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os


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

# find the common columns in all csv files from data folder and put it in a variable
common_columns = set()
for filename in os.listdir("data"):
    filepath = os.path.join("data", filename)
    df = pd.read_csv(filepath)
    common_columns = common_columns.intersection(set(df.columns)) if common_columns else set(df.columns)

print(common_columns)



########################################################################################################


dfs = []
first_file = True
common_columns = None

# Iterate over all files in the "data" folder
for filename in os.listdir("data"):
    filepath = os.path.join("data", filename)
    
    # Read each CSV file into a DataFrame
    df = pd.read_csv(filepath)
    
    if first_file:
        # For the first file, save the columns to be used as reference
        common_columns = df.columns
        df = df[common_columns]  # Keep the columns in the order of the first file
        first_file = False
    else:
        # For subsequent files, retain only the columns present in the first file
        df = df.reindex(columns=common_columns)
    
    dfs.append(df)  # Add the processed DataFrame to the list

# Concatenate all DataFrames, ignoring the index to reset it
merged_df = pd.concat(dfs, ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_filepath = os.path.join("data", "merge.csv")
merged_df.to_csv(merged_filepath, index=False)

print(f"Merged file saved as merge.csv in data folder")
