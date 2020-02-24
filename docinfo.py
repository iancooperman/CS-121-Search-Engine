from bs4 import BeautifulSoup


class DocInfo:
    def __init__(self, docid, term_frequency, relative_importance):
        self._docid = docid
        self._term_frequency = term_frequency
        self._relative_importance = relative_importance