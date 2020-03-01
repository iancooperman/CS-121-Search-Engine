import pickle
from collections import defaultdict
from collections import deque
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from docinfo import DocInfo
import math


class Index:
    def __init__(self):
        self.inverted_index = defaultdict(deque)  # defaultdict< str, deque<DocInfo> >
        self.lemmatizer = WordNetLemmatizer()
        self.num_documents = 0

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
        word_priorities = dict()  # dict<str, float>
        term_frequencies = defaultdict(int)
        doc = BeautifulSoup(content, features='lxml')

        def tag_parse(tag_type: str, importance: float) -> None:
            try:
                tags = doc.find_all(tag_type)
                for tag in tags:
                    tag_text = tag.get_text()
                    for term in tokenize(tag_text):
                        lemmatized_term = self.lemmatizer.lemmatize(term)
                        word_priorities[lemmatized_term] = importance
            except AttributeError as e:
                pass

        # set all words to importance 1
        doc_text = doc.get_text()
        for word in tokenize(doc_text):
            lemmatized_word = self.lemmatizer.lemmatize(word)
            word_priorities[lemmatized_word] = 0/8
            term_frequencies[lemmatized_word] += 1

        tag_parse('b', 1/8)
        tag_parse('strong', 1/8)
        tag_parse('h6', 2/8)
        tag_parse('h5', 3/8)
        tag_parse('h4', 4/8)
        tag_parse('h3', 5/8)
        tag_parse('h2', 6/8)
        tag_parse('h1', 7/8)
        tag_parse('title', 8/8)

        for word, word_importance in word_priorities.items():
            info = DocInfo(docid, term_frequencies[word], word_importance)
            self.inverted_index[word].append(info)

        self.num_documents += 1

    def update_document_frequencies(self):
        for word, postings_list in self.inverted_index.items():
            for doc_info in postings_list:
                doc_info.calculate_inverse_document_frequency(self.num_documents, len(postings_list))

    # given a query, return a list of relevant documents
    def query(self, q: str) -> list:
        query_term_frequency = defaultdict(int)
        lemmatized_query = []
        for word in tokenize(q):
            self.lemmatizer.lemmatize(word)
            lemmatized_query.append(word)
            query_term_frequency[word] += 1

        if len(lemmatized_query) > 1:
            # Cosine Similarity
            doc_scores = defaultdict(float)
            doc_lengths = defaultdict(float)
            query_length = 0.0 # sqrt(x1 ** 2 + x2 ** 2 + ... + xN ** 2)
            for term in lemmatized_query:
                # calculate tfidf for query
                tf = 1 + math.log(query_term_frequency[word], 10)
                idf = math.log((self.num_documents/len(self.inverted_index[term])), 10)
                query_weight = tf * idf
                query_length += tf ** 2
                for doc in self.inverted_index[term]:
                    doc_scores[doc] += query_weight * doc.tfidf()
                    # doc_lengths[doc] ? in add_document maybe?
            search_results = []
            query_length = math.sqrt(query_length)
            for term in lemmatized_query:
                for docInfo in self.inverted_index[term]:
                    doc_scores[docInfo] = doc_scores[docInfo]/(doc_lengths[docInfo] * query_length) # doc_lengths not done yet
                    search_results.append(docInfo)
            # Sort list of query results by Cosine Similarity value
            search_results.sort(key=lambda x: doc_scores[docInfo] + x._relative_importance, reverse=True)
        else:
            # rank by tf-idf
            query_word = lemmatized_query[0]
            search_results = []
            for docInfo in self.inverted_index[query_word]:
                search_results.append(docInfo)
            # Sort list of query results by tfidf value
            search_results.sort(key=lambda x: x.tfidf() + x._relative_importance, reverse=True)

            return search_results


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
