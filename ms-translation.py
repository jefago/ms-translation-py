#!/usr/bin/python

import os
import sys
import codecs
import urllib
from xml.etree import ElementTree

import requests

TRANSLATE_URI = "http://api.microsofttranslator.com/v2/Http.svc/Translate?{}"
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
    sys.stderr.write("Translating")
    # Iterate over all languages to translate
    for to_lang in LANGUAGES:
        sys.stderr.write(".")

        # Translate line by line because otherwise the translation API messes up line breaks
        lines = text_to_translate.split("\n")
        translated_lines = []
        for line_to_translate in lines:
            # MS Translation API request
            line_to_translate = line_to_translate.rstrip()
            if (len(line_to_translate) > 0):

                uri_to_call = TRANSLATE_URI.format(urllib.urlencode({
                    'text' : line_to_translate,
                    'from' : from_lang,
                    'to' : to_lang
                }))

                response = requests.get(uri_to_call, headers=headers)

                translation_xml_tree = ElementTree.fromstring(response.text.encode('utf-8'))
                translated_lines.append(translation_xml_tree.text)
            else:
                translated_lines.append("")

            translation = '\n'.join(translated_lines)
        # Add translation to dictionary that we will return
        retval[to_lang] = translation

    sys.stderr.write("done\n")
    # Return the dictionariy of translations
    return retval

# Main script
if __name__ == "__main__":
    API_KEY = os.environ.get('MS_TRANSLATION_API_KEY')

    if API_KEY is None:
        print "Missing environment variable MS_TRANSLATION_API_KEY"
        exit(1)

    arg_list = list(sys.argv)
    del arg_list[0]

    if len(arg_list) >= 1:
        input_string = ' '.join(arg_list)
    else:
        sys.stderr.write("No text to translate given as command line parameter, reading from stdin\n")
        input_string = sys.stdin.read()

    translations = translate(API_KEY, "en-us", input_string)

    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    for lang in translations:
        sys.stdout.write(
            u"<{0}>\n{1}\n</{0}>\n".format(lang, translations[lang])
        )
