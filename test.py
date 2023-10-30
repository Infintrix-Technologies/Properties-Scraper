import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
}

response = requests.get(
    "https://www.rightmove.co.uk/properties/141320084", headers=headers
)


# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the script tag containing the JSON data
    tenure = soup.select_one("_1hV1kqpVceE9m-QrX_hWDN _2SpNNVW0fTYoFvPDmhKSt8 ")
    print(tenure)
