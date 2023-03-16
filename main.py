import os
from urduhack.preprocessing  import remove_punctuation
import csv
import stanza
import re
from collections import defaultdict,OrderedDict

def print_dictionary(inverted_index:defaultdict):
    for key in inverted_index:
        print(key)
        for k in inverted_index[key]:
            print(k," : ",inverted_index[key][k])

def write_files(dict):

    #writing terms and doc frequency
    with open("dictionary.txt", "a", encoding="utf-8") as f:
        for key in dict:
            f.writelines(str(key[0])+" "+str(key[1])+"\n")
    f.close()

    # writing posting list
    with open("postings.txt", "a", encoding="utf-8") as f:
        for key in dict:
            for k in dict[key]:
                f.writelines(str(k)+" "+str(dict[key][k]) + "\n")

    f.close()



def add_doc_frequency(dict:defaultdict)->defaultdict:
    doc_freq_dictionary = defaultdict(lambda: defaultdict(list))
    for term in dict:
        doc_freq =len(dict[term])
        doc_freq_dictionary[(term,doc_freq)] =dict[term]
    dict.clear()
    return doc_freq_dictionary

# mapping of term to doc frequency;memory issue
def add_doc_frequency2(dict:defaultdict)->defaultdict:
    doc_freq_dictionary = defaultdict(lambda: 0)
    for term in dict:
        doc_freq =len(dict[term])
        doc_freq_dictionary[term] =doc_freq
    return doc_freq_dictionary

# adding doc freq to posting list hash table
def add_doc_frequency3(dict:defaultdict)->defaultdict:

    for term in dict:
        doc_freq =len(dict[term])
        dict[term]['frequency'] =doc_freq
    return dict

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

def remove_stopwords(words:list,stopwords:list):
    for w in stopwords:
        if w in words:
            words.remove(w)
    return words

def read_files(stopwords:list):
    nlp = stanza.Pipeline(lang='ur', processors='tokenize', tokenize_no_ssplit=True)
    files = os.listdir("Urdu Corpus")
    files=files[1:]
    all_text=str()
    all_tokens=[()]
    doc_id=1
    #Data structured used: hash table aka dictionary
    inverted_index = defaultdict(lambda: defaultdict(list))
    #loop here
    for a_file in files:
        doc_text = str()
        tokens=[]
        words = []

        with open('Urdu Corpus//'+a_file, 'rt', encoding="utf-8") as f:
            reader = csv.reader(f)
            doc_list = list(reader)
        f.close()

        for i in range(0, len(doc_list)):
            doc_text=doc_text+(doc_list[i][0])

        splitted=re.split(r"۔| ", doc_text)

        doc = nlp(clean_text(doc_text))

        for  sentence in doc.sentences:
            words =words+([token.text for token in sentence.tokens])
            # reomove dups
        tokens = list(OrderedDict.fromkeys(words))
        # remove stopwords
        tokens = remove_stopwords(tokens, stop_words)
        flag=True
        for t in tokens:
            indices=[]

            if flag:
                indices += [i for i, x in enumerate(splitted) if x == '﻿'+t]
                indices += [i for i, x in enumerate(splitted) if x == t]
                flag=False
            else:
                indices += [i for i, x in enumerate(splitted) if x == t]
            inverted_index[t][doc_id]+=indices


        doc_id+=1

    return inverted_index


stop_words=read_stop_words()
dicionary=read_files(stop_words)
# print(add_doc_frequency2(dicionary))
dicionary=add_doc_frequency(dicionary)
print_dictionary(dicionary)
write_files(dicionary)

