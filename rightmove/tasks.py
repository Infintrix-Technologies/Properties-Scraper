from celery import shared_task
from rightmove.script import RightMoveScraper


@shared_task
def scrape_properties():
    print("scraping properties")
    # Your task logic here
    scraper = RightMoveScraper()
    scraper.initiate()
