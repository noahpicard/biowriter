from scraper_util import parse_bio_from_url
from scraper_util import parse_bio_urls_from_url
from datetime import date

def generate_bio_map(urls):
	bio_map = {}
	for url in urls:
		print("Processing url: " + url)
		result = parse_bio_from_url(url)
		bio_map[result[0]] = result[1]
	return bio_map

def get_bio_urls_for_today():
	today = date.today()
	dt_for_url = today.strftime("%B_%d")
	wikipedia_today_url = "https://en.wikipedia.org/wiki/" + dt_for_url
	return parse_bio_urls_from_url(wikipedia_today_url)
	