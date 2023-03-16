import csv
import ast
from collections import defaultdict,OrderedDict
import stanza
import re
from urduhack.preprocessing  import remove_punctuation

def read_stop_words()->list:
    words=[]
    with open('stop_words_urdu.txt', 'rt', encoding="utf-8") as f:
        reader = csv.reader(f)
        doc_list = list(reader)
    for d in doc_list:
        words.append(d[0])

    return words


def clean_text(doc_text)->list:
    cleaned_text = remove_punctuation(doc_text)
    cleaned_text = re.findall(r'[\u0600-\u06ff]+', cleaned_text)
    return cleaned_text

def remove_stopwords(words:list):
    stopwords=read_stop_words()
    for w in stopwords:
        print(w)
        if w in words:
            words.remove(w)
    return words

def read_data():
    term_keys=[]
    dict = defaultdict(lambda: defaultdict(list))
    with open('dictionary.txt', 'rt', encoding="utf-8") as f:
        reader = csv.reader(f)
        terms = list(reader)
    for term in terms:
        pair=term[0].split()
        tup=(pair[0],pair[1])
        term_keys.append(tup)

    # read posting list
    doc_ids=[]
    posting=[]
    with open('postings.txt', 'r') as file:
        for line in file:
            line = line.strip()
            start_number_str, lst_str = line.split(' ', 1)
            doc_ids.append( int(start_number_str))
            posting.append(ast.literal_eval(lst_str))
    #create hash table
    index=0
    for k in term_keys:

        dict[k[0]]['document frequency'] = k[1]
        for i in range(index,index+int(k[1])):
            dict[k[0]][doc_ids[i]]+=posting[i]
        index+=int(k[1])

    return dict
#checks posting list for words in
def test(dictionary):
    nlp = stanza.Pipeline(lang='ur', processors='tokenize', tokenize_no_ssplit=True)
    doc_text=str()
    words=[]
    with open('testdata.txt', 'rt', encoding="utf-8") as f:
        reader = csv.reader(f)
        doc_list = list(reader)
    f.close()
    for i in range(0, len(doc_list)):
        doc_text = doc_text + (doc_list[i][0])

    doc = nlp(clean_text(doc_text))
    for sentence in doc.sentences:
        words = words + ([token.text for token in sentence.tokens])
    tokens = list(OrderedDict.fromkeys(words))
    tokens = remove_stopwords(tokens)
    for t in tokens:
        if len(dictionary[t]) == 0:
            print(t + " not found !")
        else:
            print("term: "+t)
            print("Posting List:")
            for k in dictionary[t]:
                print(str(k)+": ",dictionary[t][k])
        print("-------------------------------------------")

dictionary=read_data()
test(dictionary)