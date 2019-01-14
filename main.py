"""
main.py
Scrapes IG profiles, saves images matching description and corresponding captions,
and generates Markov chains based on captions.
"""

from markov import MarkovText
from scrape import InstaScraper

def main():
    """
    Scrapes profiles and generates Markov captions.
    """
    InstaScraper(out='scraped').scrape_all(profiles='profiles.txt')
    MarkovText(file='scraped/captions.json').gen_text((1, 20), 10000)

if __name__ == '__main__':
    main()
