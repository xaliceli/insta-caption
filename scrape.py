"""
scrape.py
Scrapes facial images and caption text from supplied IG profiles.
"""

import json
import io
import os

from bs4 import BeautifulSoup
import cv2
import requests
from scipy import misc

class InstaScraper():
    """
    Scrapes list of IG profiles, saving images and captions for posts where
    accessibility caption contains requested descriptors.
    """

    def __init__(self, out='scraped', caption_file='captions.json'):
        self.profiles = None
        self.out_dir = out
        if caption_file:
            with open(os.path.join(out, caption_file), 'r') as filehandle:
                self.captions = json.load(filehandle)
        else:
            self.captions = []

    def read_profiles(self, file):
        """
        Reads in profiles from txt file, removing duplicates.
        """
        profiles = open(file).read().split()
        unread = profiles[:profiles.index('===')]
        read = profiles[profiles.index('===') + 1:]
        self.profiles = list(set(unread) - set(read))

    def meets_logic(self, check, params=('1 person', 'closeup')):
        """
        Checks whether accessibility caption exists and if so,
        whether desired descriptions are present.
        """
        logic = bool('accessibility_caption' in check)
        if logic:
            for param in params:
                logic = logic and param in check['accessibility_caption']
        return logic

    def scrape_one(self, profile, scrape_img, scrape_caption):
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
            image_response = requests.get(post['node']['display_url'], stream=True)
            image = misc.imread(io.BytesIO(image_response.content))
            if self.meets_logic(post['node']):
                if scrape_img:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(os.path.join(self.out_dir, profile + str(num) + '.png'), image)
                if scrape_caption:
                    if post['node']['edge_media_to_caption']['edges']:
                        if 'text' in post['node']['edge_media_to_caption']['edges'][0]['node']:
                            self.captions.append(post['node']['edge_media_to_caption']['edges'][0]['node']['text'])

    def scrape_all(self, profiles='profiles.txt', scrape_img=True, scrape_caption=True):
        """
        Scrapes all profiles supplied.
        """
        self.read_profiles(profiles)
        for profile in self.profiles:
            print('Scraping profile: ' + profile)
            self.scrape_one(profile, scrape_img, scrape_caption)
        if scrape_caption:
            with open(os.path.join(self.out_dir, 'captions.json'), 'w+') as file:
                json.dump(self.captions, file)

if __name__ == '__main__':
    InstaScraper().scrape_all()
