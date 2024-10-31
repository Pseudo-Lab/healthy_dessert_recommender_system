from konlpy.tag import Okt
import pandas as pd


def create_title(x):
    return str(x['option']) + ' ' + str(x['title'])


def add_spaces(text):
    okt = Okt()
    tokens = okt.morphs(text)  # 형태소로 분리
    return ' '.join(tokens)  # 공백으로 결합


# Removes spaces and converts to lowercase
def sanitize(x):
    if isinstance(x, list):
        # Strip spaces and convert to lowercase
        return [str.lower(i.replace(" ","")) for i in x]
    else:
        # Check if an item exists. If not, return empty string
        if isinstance (x, str):
            return str.lower(x.replace(" ",""))
        else:
            return ''


def create_soup(x):
    return str(x['option_price']) + ' ' + str(x['category']) + ' ' + x['gluten_free_tag'] + ' ' + x['high_protein_tag'] + ' ' + x['sugar_free_tag'] + ' ' + x['vegan_tag'] + ' ' + x['ketogenic_tag']    


        