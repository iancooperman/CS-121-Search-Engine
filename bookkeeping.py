import json
import re
from pathlib import Path


class Book:
    def __init__(self, root):
        self.root = root
        self.dictionary = self.load_bookkeeping_file()

    def load_bookkeeping_file(self) -> dict:
        with open(Path(self.root) / Path("bookkeeping.json"), "r") as f:
            dictionary = json.load(f)

        return dictionary

    def retrieve_url(self, path: str) -> str:
        return self.dictionary[path]

    def retrieve_document_content(self, folder_name, file_name) -> str:
        with open(Path(self.root) / Path(folder_name) / Path(file_name)) as f:
            content = f.read()

        return content


