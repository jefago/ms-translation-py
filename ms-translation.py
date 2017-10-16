#!/usr/bin/python

import os
import sys
# import requests






if __name__ == "__main__":
    API_KEY = os.environ.get('MS_TRANSLATION_API_KEY')

    if API_KEY is None:
        print "Missing environment variable MS_TRANSLATION_API_KEY"
        exit(1)

    if len(sys.argv) < 2:
        print "Syntax: {} [text to translate]".format(sys.argv[0])

    print "Main"
