import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk import ne_chunk, word_tokenize, pos_tag


sent = "Washington is a dirty, filthy place ruled by Osama Bin Laden."
tokens = word_tokenize(sent)
pos = pos_tag(tokens)

# chunk = ne_chunk(pos)
print(pos)

grammer = r"NP: {<DT>?<JJ>*<NN>}"
chunk = nltk.RegexpParser(grammer)

result = chunk.parse(pos)
print(result)