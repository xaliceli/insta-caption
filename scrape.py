"""
scrape.py
Scrapes facial images and caption text from supplied IG profiles.
"""

import json
import io
import os
import sys

from bs4 import BeautifulSoup
import cv2
import numpy as np
import requests
from scipy import misc

class InstaScraper():
    """
    Scrapes list of IG profiles, saving images and captions for posts where
    accessibility caption contains requested descriptors.
    """

    def __init__(self, out='scraped', file='profiles.txt'):
        self.profiles = open(file).read().split()
        self.captions = []
        self.out_dir = out

    def meets_logic(self, check, params=['1 person', 'closeup']):
        """
        Checks whether accessibility caption exists and if so,
        whether desired descriptions are present.
        """
        logic = bool('accessibility_caption' in check)
        if logic:
            for param in params:
                logic = logic and param in check['accessibility_caption']
        return logic

    def scrape_one(self, profile):
        """
        Scrapes first 12 posts of a single IG profile for image and caption.
        """
        response = requests.get('http://www.instagram.com/' + profile)
        soup = BeautifulSoup(response.text, features='html.parser')
        prof_json = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
        json_content = prof_json.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(json_content)
        post_data = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for num, post in enumerate(post_data):
            image_url = post['node']['display_url']
            image_response = requests.get(image_url, stream=True)
            image = misc.imread(io.BytesIO(image_response.content))
            meets_logic = self.meets_logic(post['node'])
            if meets_logic:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imwrite(os.path.join(self.out_dir, profile + str(num) + '.png'), image)
                if post['node']['edge_media_to_caption']['edges']:
                    if 'text' in post['node']['edge_media_to_caption']['edges'][0]['node']:
                        self.captions.append(post['node']['edge_media_to_caption']['edges'][0]['node']['text'])

    def scrape_all(self):
        """
        Scrapes all profiles supplied.
        """
        for profile in self.profiles:
            self.scrape_one(profile)
        with open(os.path.join(self.out_dir, 'captions.json'), 'w+') as file:
            json.dump(self.captions, file)

if __name__ == '__main__':
    InstaScraper().scrape_all()
