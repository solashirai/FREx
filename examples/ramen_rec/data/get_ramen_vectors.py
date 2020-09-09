import rdflib
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def convert():
    """
    One-off code to make some dummy "similarity" ratings between ramens.
    Using a super simple jaccard index for similarity. Don't look at this code as an example of a good
    similarity metric...
    """
    ramen_data = []
    with open('ramen-ratings.csv', 'r', encoding='utf-8') as f:
        next(f) #skip first line, header for CSV
        for line in f:
            #Review #,Brand,Variety,Style,Country,Stars,Top Ten
            ramen_content = line.strip().lower().split(",")[:-1]
            ramen_content = [c.strip() for c in ramen_content]
            if len(ramen_content) != 6:
                continue
            ramen_data.append(tuple(ramen_content))

    ramen_ns = rdflib.Namespace('http://www.frex.com/examples/ramen/')
    uri_to_items = dict()

    for ramen_content in ramen_data:
        ramen_uri = ramen_ns[ramen_content[0]]
        # use brand, label, style, and country
        uri_to_items[ramen_uri] = [ramen_content[1], ramen_content[2], ramen_content[3], ramen_content[4]]

    vectorizer = CountVectorizer(tokenizer=lambda doc: doc, preprocessor=lambda doc: doc)
    vectorizer.fit(uri_to_items.values())
    uri_to_items = {key: vectorizer.transform([val])[0] for key, val in uri_to_items.items()}
    with open('ramen-vectors.pkl', 'wb') as f:
        pickle.dump(uri_to_items, f)

if __name__ == '__main__':
    convert()
