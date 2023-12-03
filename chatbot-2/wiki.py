from cleanup import clean_up_sentence
from nltk import pos_tag
import wikipediaapi


def get_wiki(sentence):
    clean_sent = clean_up_sentence(sentence)
    if "a" in clean_sent:
        clean_sent.remove("a")
    if "an" in clean_sent:
        clean_sent.remove("an")
    pos = pos_tag(clean_sent)
    if pos[0][1] == "WP" or pos[0][0].lower() in [
        "what",
        "who",
        "where",
        "when",
        "how",
    ]:
        try:
            if "is" in clean_sent:
                is_index = clean_sent.index("is")
            elif "was" in clean_sent:
                is_index = clean_sent.index("was")
            else:
                is_index = 1
            search_query_arr = clean_sent[is_index + 1 : len(clean_sent)]
            query = " ".join(search_query_arr)
        except (ValueError, IndexError):
            print("No word found in the query.")
    try:
        wiki_wiki = wikipediaapi.Wikipedia(
            "Zeitkonig (roho.bhattacharya@gmail.com)", "en"
        )
        page_py = wiki_wiki.page(query)
        if not page_py.summary:
            return "Couldn't find anything. Could you try that again?"
    except:
        return "I didn't get that, come again?"
    return f"According to wikipedia, {page_py.summary[0:1000]}...To learn more you can go to {page_py.fullurl}"
