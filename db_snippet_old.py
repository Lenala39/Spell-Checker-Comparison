import sqlite3
from hunspell import Hunspell

conn = sqlite3.connect("corpus.sqlite3")
c = conn.cursor()
c.execute("SELECT * FROM Posts WHERE ID_Post <= 4")
data = c.fetchall()

h = Hunspell('de-DE', hunspell_data_dir="C:\\Users\\Lena_Langholf\\Downloads\\million_post_corpus\\dictionaries")

for elem in data:
    print("Post number: ", elem[0])
    elem = list(elem)
    elem[7] = elem[7].replace("=\r\n", "")
    elem[7] = elem[7].replace("\r", "")
    elem[7] = elem[7].replace("\n", " ")
    elem[7] = elem[7].replace ("(", "").replace(")", "")
    elem[7] = elem[7].replace (",", "")
    if elem[7]:
        single_words = elem[7].split(" ")
        print(single_words)
        for word in single_words:
            if not h.spell(word) and word is not "":
                print("suggestion for: {}".format(word), h.suggest(word))
