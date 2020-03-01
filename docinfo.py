from bs4 import BeautifulSoup
import math


class DocInfo:
    def __init__(self, docid, term_frequency, relative_importance):
        self.docid = docid
        self._term_frequency = term_frequency
        self.relative_importance = relative_importance

        # initialize a value for this because PyCharm was complaining
        self.tf_idf = 0.0

    def _calculate_normalized_term_frequency(self, tf) -> float:
        if tf > 0:
            return 1 + math.log(tf, 10)
        return 0.0

    def _calculate_inverse_document_frequency(self, n: int, df: int) -> float:
        return math.log((n/df), 10)

    def calculate_tfidf(self, num_documents: int, document_frequency: int) -> float:
        self.tf_idf = self._calculate_normalized_term_frequency(self._term_frequency) * self._calculate_inverse_document_frequency(num_documents, document_frequency)
