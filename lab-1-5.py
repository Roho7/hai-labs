# lm generate
from nltk.lm import Laplace

lm = Laplace(2)

print(lm.generate(20, text_seed=["i"], random_seed=1))
