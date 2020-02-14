import json


class Book:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dictionary = self.load_bookkeeping_file()

    def load_bookkeeping_file(self) -> dict:
        with open(self.file_path, "r") as f:
            dictionary = json.load(f)

        return dictionary

    def invert_bookkeeping_dictionary(self) -> dict:
        pass

    def retrieve_document_location(self, url: str) -> str:
        pass

    def retrieve_url(self) -> str:
        pass

    def retrieve_document(self, url) -> str:
        pass


