#!/usr/bin/env python3

import os
import xml.etree.ElementTree as ET
from multiprocessing import Pool
from tts import gcloud_tts
from urllib.request import urlretrieve

# make sure that cache files are there
cache = f"{os.getenv('HOME')}/.cache/decks"
media_cache = f"{os.getenv('HOME')}/.cache/decks/media"
kelly_cache = f"{cache}/kelly.xml"
kelly_url = "https://svn.spraakdata.gu.se/sb-arkiv/pub/lmf/kelly/kelly.xml"
folkets_cache = f"{cache}/folkets.xml"
folkets_url = "http://folkets-lexikon.nada.kth.se/folkets/folkets_sv_en_public.xml"

if not os.path.exists(cache):
    os.makedirs(cache)
if not os.path.exists(media_cache):
    os.makedirs(media_cache)
if not os.path.exists(kelly_cache):
    urlretrieve(kelly_url, kelly_cache)
if not os.path.exists(folkets_cache):
    urlretrieve(folkets_url, folkets_cache)

folkets = ET.parse(folkets_cache)
kelly = ET.parse (kelly_cache)

def mk_fokets_map():
    """Builds a word -> card map for words, collects the following fields:

    - translation with word class and comment;
    - list of synonyms;
    - list of inflextions;
    - example and translation.

    Only translation is mandatory, others are omitted if not found;
    words with multiple meanings / rolse are connected in one card.
    """
    folkets_word_map = {}
    for word in folkets.iter("word"):
        wkey = word.attrib['value'].lower().replace("|", "")
        card = ''
        if 'class' in word.attrib and word.attrib['class']:
            wclass = word.attrib['class']
            if wclass == 'jj': wclass='av'
            card += f"[{wclass}] "
        if (wtrans := word.find('translation')) is None:
            continue
        else:
            card += f"{wtrans.attrib['value']}"
        if 'comment' in word.attrib:
            card += f" <i>({word.attrib['comment']})</i>"
        if word.find('synonym') is not None:
            card += f"<br>synon. {', '.join([s.attrib['value'] for s in word.findall('synonym')])}"

        if word.find('inflection') is not None:
            card += f"<br>infle. {', '.join([s.attrib['value'] for s in word.findall('inflection')])}"

        if (wexmpl := word.find('example')) is not None:
            card += f"<br>exmpl. {wexmpl.attrib['value']}"
            if (etrans:=wexmpl.find('translation')) is not None:
                card += f"<br>trans. {etrans.attrib['value']}"
        if wkey in folkets_word_map:
            folkets_word_map[wkey].append(card)
        else:
            folkets_word_map[wkey] = [card]
    return folkets_word_map

def mk_kelly_deck():
    """makes a csv of Swedish words by frequency."""
    done, tts_all = set(), []
    folkets_map = mk_fokets_map()
    lemma_all = kelly.getroot().findall('./Lexicon/LexicalEntry/Lemma')
    f = open("kelly.csv", "w")
    for lemma in lemma_all:
        word = lemma.find(".//feat[@att='writtenForm']").attrib['val']
        prefix = ""
        if (gram := lemma.find(".//feat[@att='gram']")) is not None:
            prefix = f"({gram.attrib['val']}) "

        kidx = lemma.find(".//feat[@att='kellyID']").attrib['val']
        wkey = word.lower()

        if wkey in done:
            continue
        elif wkey in folkets_map:
            front = f"{prefix}{word} [sound:sv-kelly-{kidx}.mp3]"
            tts_all.append((f"{media_cache}/sv-kelly-{kidx}.mp3", word))
            done.add(wkey)
            back = ("<ol>" +
                    ''.join(
                        [f'<li>{card}</li>' for card in folkets_map[wkey]]) +
                    "</ol>")
            f.write(f"{front}\t{back}\t{kidx}\n")
            print(f'\r kelly cnt.: {kidx}', end='')
    f.close()
    print(f', done.')
    with Pool(4) as p:
        p.starmap(gcloud_tts, tts_all)

def mk_idioms_deck():
    """makes a csv of Swedish idioms."""
    idiom_all = folkets.getroot().iter('idiom')
    idx, tts_all = 0, []
    with open(f'{cache}/idiom.csv', 'w') as f:
        for idiom in idiom_all:
            text = idiom.attrib["value"]
            if (t := idiom.find("./translation")) is not None:
                idx += 1
                front = f"{text} [sound:sv-idiom-{idx}.mp3]"
                tts_all.append((f"{media_cache}/sv-idiom-{idx}.mp3", text))
                back = t.attrib["value"]
                entry = f"{front}\t{back}\t{idx}\n"
                f.write(entry)
        print(f"\r idiom cnt.: {idx}", end = "")
    print(", done.")
    with Pool(4) as p:
        p.starmap(gcloud_tts, tts_all)

mk_kelly_deck()
mk_idioms_deck()
