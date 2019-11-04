from pathlib import PurePosixPath

import pokepy
from urllib.parse import urlparse, unquote


def clean_card_name(card):
    """
    Clean the card name to be only of the first pokemon name on the card
    :param card:
    :return:
    """
    clean_name = card.name.replace('-GX', '')
    clean_name = clean_name.replace('Mega', '')
    clean_name = clean_name.split(' & ')[0] if '&' in clean_name else clean_name
    return clean_name.strip()


def find_pokemon_api(card):
    """
    Find the pokemon object from the Pokeapi using a given card
    :param card:
    :return:
    """
    name = clean_card_name(card)
    try:
        client = pokepy.V2Client()
        return client.get_pokemon(name)
    except:
        print("Couldn't find pokemon for %s" % name)
        return


def find_evolves_from(pokemon):
    """
    Find the pokemon that this evolves from baed on the API pokemon model
    :param pokemon:
    :return:
    """
    if pokemon.species:
        species_url = pokemon.species.url
        species_id = get_species_id(species_url)
        parent_species = get_species(species_id)
        if parent_species:
            evolves_species_spec = parent_species.evolves_from_species
            if evolves_species_spec:
                evolves_url = evolves_species_spec.url
                evolves_species_id = get_species_id(evolves_url)
                evolves_species = get_species(evolves_species_id)
                if evolves_species:
                    names = evolves_species.names
                    english_name = next(name for name in names if name.language.name == 'en').name
                    return english_name
        return
    else:
        return


def get_species_id(url):
    parts = PurePosixPath(
        unquote(
            urlparse(
                url
            ).path
        )
    ).parts
    return parts[len(parts) - 1]


def get_species(species_id):
    try:
        client = pokepy.V2Client()
        return client.get_pokemon_species(species_id)
    except:
        print("Couldn't find species for %d" % species_id)
        return
