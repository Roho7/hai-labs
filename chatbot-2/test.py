from nltk import corpus

word_list = ["hey", "this", "is", "so", "fun"]


class SpellChecker:
    def __init__(self, sentence: list) -> None:
        self.sentence = sentence

    def find_matches(self, word) -> list[str]:
        matches = []
        for lst_word in self.sentence:
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
                matches.append(lst_word)
        if matches != []:
            return matches
        else:
            return False

    def autocorrect_word(self, word):
        match = self.find_matches(word)
        match = sorted(match)
        return match[0]


# user_input = input("Enter: ")
p1 = SpellChecker(["cat", "cap", "cag", "boy", "boi", "goy", "gay"]).autocorrect_word(
    "boys"
)
print(p1)
