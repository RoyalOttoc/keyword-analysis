from nltk.tokenize import word_tokenize
import pandas as pd
import nltk
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import filtering

nltk.download('punkt')
nltk.download('stopwords')

df = pd.read_csv('./data/NDIS_private.csv').dropna()

keywordList = []

post_values = df["post"].values

tokenized_sents = [word_tokenize(word) for word in post_values]
for word in tokenized_sents:
    keywordList += word

lower_keywords = [word.lower() for word in keywordList]

wordlist = filtering.removeStopwords(lower_keywords, filtering.stopwords)
dictionary = filtering.wordListToFreqDict(wordlist)
sorteddict = filtering.sortFreqDict(dictionary)

filtered_keywords = pd.DataFrame(sorteddict,
                                 columns=['counts', 'word']).head(15)

keys = filtered_keywords["counts"]
values = filtered_keywords["word"]
plt.bar(values, keys)
plt.title('Top 15 keywords')
plt.xlabel('word')
plt.ylabel('counts')
# it shows a graph about Top 15 keywords
plt.show()

# it shows the top 15 keywords
# print(filtered_keywords)
