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

        unique_docids = set()
        for postings_list in self.inverted_index.values():
            for doc_info in postings_list:
                unique_docids.add(doc_info.docid)

        self.num_documents = len(unique_docids)

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
                doc_info.calculate_tfidf(self.num_documents, len(postings_list))

    # given a query, return a list of relevant documents
    def query(self, q: str) -> list:
        # tokenize and lemmatize the query
        lemmatized_query = []
        for word in tokenize(q):
            lemmatized_word = self.lemmatizer.lemmatize(word)
            lemmatized_query.append(lemmatized_word)

        if len(lemmatized_query) > 1:
            # calculate term frequencies of words in query
            query_term_frequency = defaultdict(int)
            for word in lemmatized_query:
                query_term_frequency[word] += 1

            # Cosine Similarity

            # dictionary for storing the cosine similarity between the query vector and all document vectors
            doc_scores = defaultdict(float)

            # dictionary for storing lengths of document vectors
            doc_lengths = defaultdict(float)

            # variable for storing the length of the query vector
            query_length = 0.0  # sqrt(x1 ** 2 + x2 ** 2 + ... + xN ** 2)
            # for each unique lemmatized term in the query
            for term in set(lemmatized_query):
                # calculate tf-idf for term in query
                tf = 1 + math.log(query_term_frequency[word], 10)
                # if the term isn't in the index, set its idf to 0
                if len(self.inverted_index[term]) <= 0:
                    idf = math.inf
                else:
                    idf = math.log(self.num_documents / len(self.inverted_index[term]), 10)
                query_weight = tf * idf

                # build up query length by adding tf-idf squared, in accordance with Pythagorean theorem
                query_length += math.pow(query_weight, 2)

                tag_importance = defaultdict(float)

                # for each document the lemmatized word is in...
                for doc_info in self.inverted_index[term]:
                    # add the query word tf-idf times the document word tf-idf to the total score for the document
                    # (NOTE: documents not in this word's postings list but not in another word's posting list
                    # don't affect the score because the tf-idf for this term in those document would be 0 anyway)
                    doc_scores[doc_info.docid] += query_weight * doc_info.tf_idf
                    doc_lengths[doc_info.docid] += doc_info.tf_idf ** 2

                    if tag_importance[doc_info.docid] < doc_info.relative_importance:
                        tag_importance[doc_info.docid] = doc_info.relative_importance

            # finalize lengths of doc vectors by finding the square roots of the sums of the squared tf-idfs
            for docid in doc_lengths.keys():
                doc_lengths[docid] = math.sqrt(doc_lengths[docid])

            # finalize length of query vector by finding the square root of the sum of the squared tf-idfs
            query_length = math.sqrt(query_length)

            # divide all scores by the lengths of the query vector and the corresponding document vector
            for docid in doc_scores.keys():
                doc_scores[docid] = doc_scores[docid] / query_length

                # if the length of the relevant vector is 0, don't bother with it
                if doc_lengths[docid] != 0:
                    doc_scores[docid] = doc_scores[docid] / doc_lengths[docid]

            # Sort list of query results by Cosine Similarity value
            # return list of reverse-sorted docid/score pairs
            return sorted(doc_scores.items(), key=lambda x: x[1] + tag_importance[x[0]], reverse=True)

        else:
            # rank by tf-idf
            query_word = lemmatized_query[0]
            search_results = []
            for doc_info in self.inverted_index[query_word]:
                search_results.append((doc_info.docid, doc_info.tf_idf + doc_info.relative_importance))
            # Sort list of query results by tf-idf value + relative importance
            search_results.sort(key=lambda x: x[1], reverse=True)

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
