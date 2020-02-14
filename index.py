import pickle

class Index:
    def __init__(self):
        self.inverted_index = dict()

    # save the index to a file
    def save_to_file(self):
        with open("index.PICKLE", "w") as f:
            pickle.dump(self.inverted_index, f)

    # load the index from a file
    def load_from_file(self):
        with open("index.PICKLE", "r") as f:
            self.inverted_index = pickle.load(f)

    # given a document, add it to appropriate places in the index
    def add_document(self):
        pass

    # given a query, return a list of relevant documents
    def query(self, q: str) -> list:
        pass