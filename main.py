import time
from medium_scraper.scraper import MediumScraper          

def main():
    tag = "deep-learning"
    MediumScraper(article_tag=tag).scrape_from_tags()

if __name__ == "__main__":
    main()
