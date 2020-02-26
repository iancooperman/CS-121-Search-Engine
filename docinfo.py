from bs4 import BeautifulSoup
import math


class DocInfo:
    def __init__(self, docid, term_frequency, relative_importance):
        self._docid = docid
        self._term_frequency = term_frequency
        self._relative_importance = relative_importance

        self._normalized_term_frequency = self._calculate_normalized_term_frequency(self._term_frequency)

        self._document_frequency = 0

        self._inverse_document_frequency = 0.0
        self._priority = 0

    def _calculate_normalized_term_frequency(self, tf) -> float:
        if tf > 0:
            return 1 + math.log(tf, 10)
        return 0.0

    def calculate_inverse_document_frequency(self, N, df) -> None:
        self._inverse_document_frequency = math.log((N/df), 10)

    def tfidf(self) -> float:
        return self._normalized_term_frequency * self._inverse_document_frequency
