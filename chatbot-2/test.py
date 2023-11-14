from nltk import corpus

word_list = ["hey", "this", "is", "so", "fun"]


class SpellChecker:
    def __init__(self, word: str, sentence: list) -> None:
        self.word = word
        self.sentence = sentence

    def find_matches(self, word: str, sentence: list) -> list[str]:
        matches = []
        for lst_word in sentence:
            count = 0
            for i in range(len(lst_word)):
                try:
                    if word[i] == lst_word[i]:
                        pass
                    else:
                        count += 1
                except:
                    pass
            if count > 1:
                pass
            else:
                matches.append(word)
                return matches
        else:
            return False


p1 = SpellChecker("girls", ["cat", "dog", "girl"])
p1.find_matches()
