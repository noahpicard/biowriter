import requests
from bs4 import BeautifulSoup
import nltk
import re
# nltk.download('punkt')

URL = "https://en.wikipedia.org/wiki/Holly_Willoughby"
TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')
MATCH_BRACKETS_REGEX = "[\[].*?[\]]"
WIKIPEDIA_URL_BASE = "https://en.wikipedia.org"

# Top level web scraper. Takes in a URL of the bio page to scrape and returns
# a tuple of the name of the subject of the bio along with a list of sentences composing the bio.
def parse_bio_from_url(url):
	page = requests.get(url)

	soup = BeautifulSoup(page.content, "html.parser")

	# Get Bio owner's name
	name = scrape_bio_name(soup)

	# Get all sentences as a list from the bio, starting with the Early Life section
	sentences = scrape_bio_sentences(soup)

	return name, sentences

def parse_bio_urls_from_url(url):
	page = requests.get(url)

	soup = BeautifulSoup(page.content, "html.parser")

	births = find_specific_h2(soup, "Births")

	bio_urls = []
	if births is not None:
		for sibling in births.next_siblings:
			if sibling is not None and sibling.name == "ul":
				for li in sibling.find_all("li"):
					urls = li.find_all('a', href=True)
					url = None
					if len(urls) == 1:
						url = urls[0]['href']
					elif len(urls) == 2: 
						url = urls[1]['href']
					if url is not None and not url.startswith("#cite_note"):
						bio_urls.append(WIKIPEDIA_URL_BASE + url)
			if sibling is not None and sibling.name == "h2":
				break

	return bio_urls

def scrape_bio_name(soup):
	name = None
	first_heading = soup.find("h1", id="firstHeading")
	if first_heading is not None:
		name = first_heading.text
	return name

def scrape_bio_sentences(soup):
	sentences = []
	results = soup.find(id="bodyContent")
	if results is None:
		return sentences

	content_div = results.find("div", id="mw-content-text")
	if content_div is None:
		return sentences

	early_life_span = find_specific_h2(content_div, "Early_life")

	if early_life_span is not None:
		for sibling in early_life_span.next_siblings:
			if sibling is not None and sibling.name == "p" and sibling.text is not None and len(sibling.text.strip()) > 0:
				sentences.extend(clean_paragraphs_to_sentences(sibling.text))

	return sentences

# Returns None if the h2 with that specific id is not found
def find_specific_h2(div_to_search, h2_id):
	specific_h2 = None
	h2s = div_to_search.find_all("h2")
	for h2 in h2s:
		span = h2.find(id=h2_id)
		if span is not None:
			specific_h2 = span.parent
			break
	return specific_h2

def clean_paragraphs_to_sentences(text):
	return TOKENIZER.tokenize(re.sub(MATCH_BRACKETS_REGEX, "", text.strip("\n")))
