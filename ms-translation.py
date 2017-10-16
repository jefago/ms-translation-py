#!/usr/bin/python

import os
import sys
from xml.etree import ElementTree

import requests

TRANSLATE_URI = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&from={}&to={}"
LANGUAGES = [
    "en-US", 
    "ar", "de-DE", "en-AU", "en-CA", "en-GB", "es-419", "es-ES", "es-US", "fr-CA", "fr-FR",
    "hr", "it-IT", "ja-JP", "ko-KR", "nl-NL", "pl-PL", "pt-BR", "pt-PT", "ru-RU", "sr", "zh-CN"
]


def translate(api_key, from_lang, text_to_translate):
    # Headers contain API key
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    # Dictionary of translations to return
    retval = {}

    # Iterate over all languages to translate
    for to_lang in LANGUAGES:

        # Include original copy if this is the language we are translating from
        if to_lang == from_lang:
            translation = text_to_translate
        else:
            # MS Translation API request
            uri_to_call = TRANSLATE_URI.format(text_to_translate, from_lang, to_lang)
            response = requests.get(uri_to_call, headers=headers)

            translation_xml_tree = ElementTree.fromstring(response.text.encode('utf-8'))
            translation = translation_xml_tree.text
        # Add translation to dictionary that we will return
        retval[to_lang] = translation

    # Return the dictionariy of translations
    return retval

if __name__ == "__main__":
    API_KEY = os.environ.get('MS_TRANSLATION_API_KEY')

    if API_KEY is None:
        print "Missing environment variable MS_TRANSLATION_API_KEY"
        exit(1)

    arg_list = list(sys.argv)
    del arg_list[0]

    if len(arg_list) < 1:
        print "Syntax: {} [text to translate]".format(sys.argv[0])
        exit(2)

    translations = translate(API_KEY, "en-us", ' '.join(arg_list))

    for lang in translations:
        print u"<{0}>\n{1}\n</{0}>\n".format(lang, translations[lang])
