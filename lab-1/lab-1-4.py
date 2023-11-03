# the LM function

import nltk, re, pprint, string
from collections import Counter
from nltk import word_tokenize, sent_tokenize
from nltk.util import ngrams, bigrams
from nltk.lm import MLE
from nltk.lm.preprocessing import pad_both_ends, padded_everygram_pipeline
from nltk.lm import Laplace

lm = Laplace(2)

custom_punctuation = string.punctuation + "’" + "-" + "‘" + "-"
custom_punctuation = custom_punctuation.replace(".", "")

with open("lab-1/dataset.txt", encoding=" utf8 ") as file:
    file_content = file.read()

file_nl_removed = file_content.replace("\n", " ")
file_p = "".join([char for char in file_nl_removed if char not in custom_punctuation])

n_param = 4

tokenized_text = nltk.word_tokenize(file_p)
padded_text = [list(pad_both_ends(tokenized_text, n=n_param))]
corpus, vocab = padded_everygram_pipeline(n_param, padded_text)

lm = MLE(n_param)
lm.fit(corpus, vocab)

# Create a Counter object to get the vocabulary
vocabulary = Counter(tokenized_text)

# Print the vocabulary
for word, count in vocabulary.items():
    print(f"{ word }: { count }")

print(lm.generate(20, text_seed=["so"], random_seed=2))
