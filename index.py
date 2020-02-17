import pickle
from collections import defaultdict
from collections import deque
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer


class Index:
    def __init__(self):
        self.inverted_index = defaultdict(deque)
        self.lemmatizer = WordNetLemmatizer()

    # save the index to a file
    def save_to_file(self):
        with open("index.PICKLE", "wb") as f:
            pickle.dump(self.inverted_index, f)

    # load the index from a file
    def load_from_file(self):
        with open("index.PICKLE", "rb") as f:
            self.inverted_index = pickle.load(f)

    # given a document, add it to appropriate places in the index
    def add_document(self, docid, content):
        doc = BeautifulSoup(content, features='lxml')
        doc_text = doc.get_text()

        for word in set(tokenize(doc_text)):
            lemmatized = self.lemmatizer.lemmatize(word)
            self.inverted_index[lemmatized].append(docid)

    # given a query, return a list of relevant documents
    def query(self, q: str) -> list:
        result = []
        tokenized_query = tokenize(q)
        for word in tokenized_query:
            root_word = self.lemmatizer.lemmatize(word)
            for url in self.inverted_index[root_word]:
                result.append(url)

        return result


def tokenize(text: str) -> list:
    # O(1), as checking containment with a hash-set is.
    def is_ascii(c: str) -> bool:
        # for practicality's sake, single-quote is considered alphanumeric
        return c in {'R', 'z', 'p', 'T', 'A', 'H', 'E', 'X', '8', 'J', 'k', 'g', '1', '5', 'e', 'C', 'f', 'd', 'a',
                     'l', 'B', 'c',
                     'q', 'x', '9', 'Y', 'G', 'u', '6', 'D', '4', 'v', 'U', 't', 'i', 'Q', 'L', 'h', '2', 'Z', 'I',
                     'o', 'F', 'O',
                     'm', '0', 's', 'n', 'b', 'K', 'V', 'y', 'S', 'W', 'M', 'r', 'j', 'w', '3', 'N', 'P', '7', "'"}

    word_list = []
    character_list = []
    for char in text:
        if is_ascii(char):
            character_list.append(char.lower())
        else:
            if len(character_list) > 0:
                # Per Piazza question "what is considered a word?", ignoring "words" less than 2 characters long
                if len(character_list) >= 2:
                    word_list.append("".join(character_list))
                character_list = []

    # Per Piazza question "what is considered a word?", ignoring "words" less than 2 characters long
    if len(character_list) >= 2:
        word_list.append("".join(character_list))

    return word_list