import requests
import json
from bs4 import BeautifulSoup
from typing import List
import pandas as pd
from datetime import datetime
import os
from rightmove import models
import time

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
input_file_name = "input.xlsx"
output_file_name = "output.xlsx"
columns_to_remove = [
    "summary",
    "countryCode",
    "propertyImages",
    "distance",
    "listingUpdate",
    "productLabel",
    "feesApplyText",
    "displaySize",
    "displayStatus",
    "enquiredTimestamp",
    "heading",
    "formattedDistance",
    "enhancedListing",
    "customer",
    "contactUrl",
    "staticMapUrl",
    "saved",
    "hidden",
    "onlineViewingsAvailable",
    "lozengeModel",
    "numberOfVirtualTours",
    "keywords",
    "keywordMatchType",
    "hasBrandPlus",
    "transactionType",
    "channel",
]

column_names = [
    "id",
    "bedrooms",
    "bathrooms",
    "numberOfImages",
    "numberOfFloorplans",
    "displayAddress",
    "location",
    "propertySubType",
    "premiumListing",
    "featuredProperty",
    "price",
    "commercial",
    "development",
    "residential",
    "students",
    "auction",
    "feesApply",
    "showOnMap",
    "propertyUrl",
    "firstVisibleDate",
    "propertyTypeFullDescription",
    "formattedBranchName",
    "addedOrReduced",
    "isRecent",
    "phoneNumber",
    "listingUpdateReason",
    "listingUpdateDate",
    "branchDisplayName",
    "Area",
    "ZIP",
]


class RightMoveScraper:
    def __init__(self):
        self.BASE_URL = "https://www.rightmove.co.uk"
        self.session = requests.Session()

    def get_soup(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup

    def get_location_identifier(self, searchLocation) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }

        params = {
            "searchLocation": searchLocation,
            "useLocationIdentifier": "false",
            "locationIdentifier": "",
            "buy": "For sale",
        }

        response = requests.get(
            "https://www.rightmove.co.uk/property-for-sale/search.html",
            params=params,
            # cookies=cookies,
            headers=headers,
        )
        soup = self.get_soup(response.text)

        locationIdentifier = soup.select_one(
            'input[type="hidden"][name="locationIdentifier"]'
        )

        return locationIdentifier.get("value", None)

    def get_pages(self, area: models.Area):
        locationIdentifier = self.get_location_identifier(area.zip)
        index = 0
        page_number = 1

        params = {
            "locationIdentifier": locationIdentifier,
            "minBedrooms": "3",
            "maxPrice": "200000",
            "numberOfPropertiesPerPage": "24",
            "radius": "0.0",
            "sortType": "1",
            "index": str(index),
            "viewType": "LIST",
            "channel": "BUY",
            "areaSizeUnit": "sqft",
            "currencyCode": "GBP",
            "isFetching": "false",
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }

        properties_listing = []

        while True:
            params["index"] = str(index)

            response = self.session.get(
                "https://www.rightmove.co.uk/api/_search",
                params=params,
                headers=headers,
            )
            # Check if the request was successful
            if response.status_code == 200:
                json_response = response.json()
                total_result_count = json_response["resultCount"]
                pagination: dict = json_response["pagination"]
                api_properties: List[dict] = json_response["properties"]
                # print(f"\tTotal result count: {total_result_count}")

                for api_property in api_properties:
                    property_id = api_property.get("id")
                    print(f"\tScraping: {property_id} for area {area}")
                    defaults = {
                        "bedrooms": api_property.get("bedrooms"),
                        "bathrooms": api_property.get("bathrooms"),
                        "displayAddress": api_property.get("displayAddress"),
                        "propertySubType": api_property.get("propertySubType"),
                        "price": api_property.get("price")["amount"],
                        "propertyUrl": self.BASE_URL + api_property.get("propertyUrl"),
                        "firstVisibleDate": api_property.get("firstVisibleDate"),
                        "propertyTypeFullDescription": api_property.get(
                            "propertyTypeFullDescription"
                        ),
                        "addedOrReduced": api_property.get("addedOrReduced"),
                        "phoneNumber": api_property.get("customer").get(
                            "contactTelephone"
                        ),
                        "branchDisplayName": api_property.get("customer").get(
                            "branchDisplayName"
                        ),
                        "area": area,
                        "image": api_property.get("propertyImages").get("mainImageSrc"),
                    }
                    (
                        new_property,
                        created,
                    ) = models.RightMoveProperty.objects.update_or_create(
                        property_id=property_id, defaults=defaults
                    )

                # properties_listing.extend(properties)

                index = pagination.get("next")
                if int(pagination.get("total", 0)) == int(pagination.get("page", 0)):
                    # print(
                    #     f"Last page ending now {page_number}. Status Code: {response.status_code}"
                    # )
                    break

            else:
                print(
                    f"Failed to fetch page {page_number}. Status Code: {response.status_code}"
                )
                break

        return properties_listing

    def initiate(self):
        areas = models.Area.objects.all()
        for area in areas:
            try:
                print(f"Current Area: {area.zip}")
                self.get_pages(area)
            except Exception as e:
                print(e)
                pass


if __name__ == "__main__":
    rm = RightMoveScraper()
    # rm.initiate()
