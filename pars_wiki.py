import wikipedia
import unidecode

wikipedia.set_lang("pl")
f = open("keywords")

keys = f.readlines()

for key in keys:
    # find list of possible articles titles simmilar to key
    # sometimes it finds entirely not connected articles
    articles_title = wikipedia.search(key, results=10)
    print(articles_title)
    for title in articles_title:
        try:
            ar = wikipedia.page(title)
        except wikipedia.exceptions.DisambiguationError:
            continue
        # remove accents
        without_accent = unidecode.unidecode(ar.content)
        without_new_line = without_accent.replace('\n', ' ')

        try:
            new_file = open("neutralne/" + key + "_" + title, "w")
        except:
            continue
        new_file.write(without_new_line)
