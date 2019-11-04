import json
import os

from data.models import *
from data.pokehelper import find_pokemon_api, find_evolves_from


class Transform:

    def __init__(self, config, image_downloader):
        """
        Constructor for Transform command
        :param config: the Rotom configuration
        :param image_downloader: the ImageDownloader implementation
        """
        self.config = config
        self.image_downloader = image_downloader

    def run(self, source, destination, output, only_difference):
        print('Transforming!!! %s ==> %s' % (source, destination))

        source_path = os.path.join(self.config['source_path'], source) if 'source_path' in self.config else source
        dst_path = os.path.join(self.config['dest_path'], destination) if 'dest_path' in self.config else destination

        with open(source_path, 'r') as src:
            with open(dst_path, 'r') as dst:
                src_json = json.load(src)
                dst_json = json.load(dst)

                # map the json to our jsonmodel class objs
                src_cards = list(map(lambda data: DataCard(**data), src_json))
                dst_cards = list(map(lambda data: Card(**data), dst_json))

                # Now that we have our card objects, validate the format
                for card in src_cards:
                    card.validate()

                for card in dst_cards:
                    card.validate()

                # Now we need to ascertain the global missing fields such as set, series
                print(dst_cards)
                origin_card = dst_cards[0]
                card_set = origin_card.set
                series = origin_card.series
                set_code = origin_card.setCode

                # Now we need to find what cards from source aren't in the destination, then add them to the dest
                destination_ids = map(lambda c: c.id, dst_cards)
                missing_cards = list(filter(lambda c: c.id not in destination_ids, src_cards))

                # get the image url format from config, or use the default
                image_url_format = self.config['image_format'] if 'image_format' in self.config \
                    else "https://images.pokemontcg.io/%s/%s.png"

                # Attach missing data to source cards
                for card in missing_cards:
                    card.imageUrl = image_url_format % (card.setCode, card.number)
                    card.imageUrlHiRes = image_url_format % (card.setCode, card.number + "_hires")
                    card.set = card_set
                    card.series = series

                    # Grab text and break it up
                    if card.text:
                        if '\\n\\n' in card.text[0]:
                            flat_text = []
                            for text in card.text:
                                parts = text.split('\\n\\n')
                                flat_text = flat_text + parts
                            card.text = flat_text
                            print(flat_text)

                    if card.supertype == 'Pokémon':
                        print("Getting extra info for %s" % card.name)
                        # API was a bust, so see if we can find an existing one in our destination
                        existing = next(c for c in dst_cards if c.name == card.name)
                        if existing:
                            print("Found existing card from dest (ndn=%s, evolves=%s, artist=%s" %
                                  (existing.nationalPokedexNumber, existing.evolvesFrom, existing.artist))
                            card.nationalPokedexNumber = existing.nationalPokedexNumber
                            card.evolvesFrom = existing.evolvesFrom
                            # card.artist = existing.artist
                        else:
                            api_pokemon = find_pokemon_api(card)
                            if api_pokemon:
                                card.nationalPokedexNumber = api_pokemon.id
                                card.evolvesFrom = find_evolves_from(api_pokemon)
                                print("Api info found (npn=%d, evolves_from=%s)" %
                                      (card.nationalPokedexNumber, card.evolvesFrom))

                new_cards = []
                if only_difference:
                    new_cards = list(map(lambda c: c.to_struct(), missing_cards))
                else:
                    new_cards = list(map(lambda c: c.to_struct(), dst_cards)) + \
                        list(map(lambda c: c.to_struct(), missing_cards))

                stream = open(output, 'w+')
                json.dump(new_cards, stream, indent=2, ensure_ascii=False)

                print("Data Transformed @ %d" % len(new_cards))
                print("Downloading %d images" % len(missing_cards))

                missing_card_numbers = list(map(lambda c: c.number, missing_cards))
                self.image_downloader.download(set_code, missing_card_numbers)

                print("Download finished")
