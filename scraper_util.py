import requests
from bs4 import BeautifulSoup
import nltk
import re

URL = "https://en.wikipedia.org/wiki/Holly_Willoughby"
TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')
MATCH_BRACKETS_REGEX = "[\[].*?[\]]"

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

	h2s = content_div.find_all("h2")

	early_life_span = None
	for h2 in h2s:
		span = h2.find(id="Early_life")
		if span is not None:
			early_life_span = span.parent
			break

	if early_life_span is not None:
		for sibling in early_life_span.next_siblings:
			if sibling is not None and sibling.name == "p" and sibling.text is not None and len(sibling.text.strip()) > 0:
				sentences.extend(clean_paragraphs_to_sentences(sibling.text))

	return sentences

def clean_paragraphs_to_sentences(text):
	return TOKENIZER.tokenize(re.sub(MATCH_BRACKETS_REGEX, "", text.strip("\n")))
