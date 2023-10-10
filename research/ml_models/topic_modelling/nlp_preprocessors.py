import pandas as pd
import numpy as np
import spacy

nlp = spacy.load('de_core_news_sm')

def clean_text(text):

    # lemmatization
    allowed_postags = ['NOUN', 'VERB', 'ADJ', 'ADV', 'PROPN']
    nlp_text = nlp(text)
    text = ' '.join([token.lemma_ for token in nlp_text if token.pos_ in allowed_postags])
    
    return text