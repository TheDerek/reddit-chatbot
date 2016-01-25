import re

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.stem import *

stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')


def stem(word):
    word = word.lower()
    word = stemmer.stem(word)
    return word


def tokenize(text, stopwords=None):
    if stopwords is None:
        stopwords = []

    words = word_tokenize(text)
    words = [stem(word) for word in words]
    words = list(filter(lambda word: re.match(r'^[a-zA-Z0-9]*$', word), words))
    words = list(filter(lambda word: word not in stopwords, words))
    return words
