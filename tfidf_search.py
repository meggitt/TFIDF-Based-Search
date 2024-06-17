import os
import sys
import traceback
from collections import Counter
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math

#nltk.download() <-- uncomment when the program is run for the first time and then comment out to avoid repeated downloads

porter = PorterStemmer()

class TFIDFSearch:
    def __init__(self, corpus_root):
        self.corpus_root = corpus_root
        self.document_tf = {}
        self.term_df = Counter()
        self.idf = {}
        self.normalized_tfidf = {}

    def preProcessDocuments(self):
        tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
        stop_words = set(stopwords.words('english'))

        for filename in os.listdir(self.corpus_root):
            if filename.endswith(".txt"):
                try:
                    with open(os.path.join(self.corpus_root, filename), "r", encoding='windows-1252') as file:
                        doc = file.read().lower()

                    tokens = tokenizer.tokenize(doc)
                    filtered_tokens = [porter.stem(token) for token in tokens if token.lower() not in stop_words]

                    self.document_tf[filename] = filtered_tokens

                    unique_terms = set(filtered_tokens)
                    self.term_df.update(unique_terms)

                except OSError:
                    print("Could not open/read file:", filename)
                    sys.exit()
                except Exception:
                    traceback.print_exception(*sys.exc_info())

    def getidf(self):
        total_documents = len(self.document_tf)
        for term, df in self.term_df.items():
            if df > 0:
                self.idf[term] = math.log10(total_documents / df)
            else:
                self.idf[term] = -1

    def tfidf(self):
        for filename, tokens in self.document_tf.items():
            term_frequency = Counter(tokens)
            total_terms = len(tokens)
            tfidf_dict = {}
            for term, freq in term_frequency.items():
                tf = 1 + math.log10(freq)
                tfidf = tf * self.idf[term] if tf > 0 else 0
                tfidf_dict[term] = tfidf
            norm_factor = math.sqrt(sum(tfidf**2 for tfidf in tfidf_dict.values()))
            normalized_tfidf_dict = {term: tfidf / norm_factor if norm_factor != 0 else 0 for term, tfidf in tfidf_dict.items()}
            self.normalized_tfidf[filename] = normalized_tfidf_dict

    def get_weight(self, filename, token):
        token = porter.stem(token)
        if filename in self.normalized_tfidf:
            normalized_tfidf_dict = self.normalized_tfidf[filename]
            normalized_tfidf_score = normalized_tfidf_dict.get(token, 0)
            return normalized_tfidf_score
        else:
            print("File not found")
            return 0

    def get_idf(self, token):
        token = porter.stem(token)
        print(token)
        return self.idf.get(token, -1)

    def query(self, query):
        total = -1
        query = query.split()
        for filename in self.normalized_tfidf:
            d_weight = []
            q_weight = []
            for token in query:
                tf_q = self.get_weight_q(query, token)
                q_weight.append(tf_q)
                tf_d = self.get_weight(filename, token)
                d_weight.append(tf_d)
            q_norm = [x / max(math.sqrt(sum(x**2 for x in q_weight)),1) for x in q_weight]
            value = [x * y for x, y in zip(q_norm, d_weight)]
            if sum(value) > total:
                total = sum(value)
                doc = filename
        return doc, total

    def get_weight_q(self, query, term):
        query = [porter.stem(token) for token in query]
        term = porter.stem(term)
        tf_d = query.count(term)
        if tf_d > 0:
            return 1 + math.log10(tf_d)
        else:
            return 0

search = TFIDFSearch("./US_Inaugural_Addresses")
search.preProcessDocuments()
search.getidf()
search.tfidf()

def getidf(token):
    return search.get_idf(token)
def getweight(filename,token):
    return search.get_weight(filename,token)
def query(q):
    return search.query(q)

print("%.12f" % getidf('children'))
print("%.12f" % getidf('foreign'))
print("%.12f" % getidf('people'))
print("%.12f" % getidf('honor'))
print("%.12f" % getidf('great'))
print("--------------")
print("%.12f" % getweight('19_lincoln_1861.txt','constitution'))
print("%.12f" % getweight('23_hayes_1877.txt','public'))
print("%.12f" % getweight('25_cleveland_1885.txt','citizen'))
print("%.12f" % getweight('09_monroe_1821.txt','revenue'))
print("%.12f" % getweight('05_jefferson_1805.txt','press'))
print("--------------")
print("(%s, %.12f)" % query("pleasing people"))
print("(%s, %.12f)" % query("war offenses"))
print("(%s, %.12f)" % query("british war"))
print("(%s, %.12f)" % query("texas government"))
print("(%s, %.12f)" % query("cuba government"))
print("--------------")
print("\n\nspecial Cases , Incorrect input\n\n")
print("%.12f" % getidf('AT&T'))
print("%.12f" % getweight('007_JJ.txt', 'UTA'))
print("%.12f" % getweight('05_jefferson_1805.txt', 'AT&T'))
print("(%s, %.12f)" % query("arlington texas"))
