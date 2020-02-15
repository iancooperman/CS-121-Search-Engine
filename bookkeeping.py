import json
import re
from pathlib import Path


class Book:
    def __init__(self, root):
        self.root = root
        self.dictionary = self.load_bookkeeping_file()
        self.inverted_dictionary = self.invert_bookkeeping_dictionary()

    def load_bookkeeping_file(self) -> dict:
        with open(Path(self.root) / Path("bookkeeping.json") , "r") as f:
            dictionary = json.load(f)

        return dictionary

    def invert_bookkeeping_dictionary(self) -> dict:
        return {url: path for path, url in self.dictionary.items()}

    def retrieve_document_location(self, url: str) -> str:
        return self.inverted_dictionary[url]

    def retrieve_url(self, path: str) -> str:
        return self.dictionary[path]

    def retrieve_document(self, url) -> str:
        file_location = self.retrieve_document_location(url)
        match = re.match(r"(.*)/(.*)", file_location)
        if match:
            folder_name = match.group(1)
            file_name = match.group(2)
        else:
            return ""

        with open(Path(self.root) / Path(folder_name) / Path(file_name)) as f:
            content = f.read()

        return content


