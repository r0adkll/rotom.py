import os
from pathlib import PurePosixPath
from urllib.parse import unquote, urlparse

import requests
from PIL import Image

from bs4 import BeautifulSoup
from resizeimage import resizeimage

from images.images import ImageDownloader


def get_last_url_part(url):
    parts = PurePosixPath(
        unquote(
            urlparse(
                url
            ).path
        )
    ).parts
    return parts[len(parts) - 1]


def download_image(image_url, destination):
    try:
        response = requests.get(
            url=image_url
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))

        fd = open(destination, 'wb+')
        fd.write(response.content)
        fd.close()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def resize_image(file_path, output_path):
    with open(file_path, 'r+b') as f:
        with Image.open(f) as image:
            new_width = image.width / 3
            low_res = resizeimage.resize_width(image, new_width)
            low_res.save(output_path)


class MalieImageDownloader(ImageDownloader):

    def download(self, set_code, numbers):
        """
        Trigger the download of images from the malie hosting site
        :param numbers: the list of card number strings to download the image of
        :param set_code: the set code that the cards belong to
        """
        site_url = "https://malie.io/static/listings/%s.html" % set_code.upper()
        result = requests.get(site_url)
        soup = BeautifulSoup(result.text, 'html.parser')

        card_list = soup.body.div.article.ul
        output_path = os.path.join(str(os.path.curdir), set_code)
        delimited_keys = list(map(lambda n: "%s-%s" % (set_code.upper(), str(n).zfill(3)), numbers))

        def _find_english_urls(tag):
            return tag.name == 'a' and tag.has_attr('href') and \
                   tag.string == 'en_US' and tag['href'].endswith('.png') and \
                   (any(key in tag['href'] for key in delimited_keys) or len(numbers) == 0)

        for t in card_list.find_all(_find_english_urls):
            print("Downloading => %s" % t['href'])
            set_key = "%s-" % set_code.upper()
            download_url = get_last_url_part(t['href']).replace('.png', '_hires.png')
            thumbnail_url = get_last_url_part(t['href'])
            for dkey in delimited_keys:
                if dkey in t['href']:
                    download_url = "%s_hires.png" % dkey.replace(set_key, '').lower()
                    thumbnail_url = "%s.png" % dkey.replace(set_key, '').lower()

            output_file = os.path.join(output_path, download_url)
            thumbnail_output_file = os.path.join(output_path, thumbnail_url)

            if not os.path.exists(output_path):
                os.mkdir(output_path)

            download_image(t['href'], output_file)
            resize_image(output_file, thumbnail_output_file)
            print("Finished downloading %s" % download_url)
