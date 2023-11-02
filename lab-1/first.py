import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist

text = """this is human ai interaction. i am in this class."""

tokenWord = word_tokenize(text)
print(FreqDist(tokenWord))
