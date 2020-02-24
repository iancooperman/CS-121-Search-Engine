import sys
from bookkeeping import Book
from nltk.stem import WordNetLemmatizer
from index import Index
import pathlib


def main():
    index = Index()

    count = 0
    for folder in pathlib.Path("WEBPAGES_CLEAN").iterdir():
        if "." not in str(folder):  # If the file is a File type without any extensions (i.e. .json, .tsv, etc.)
            for file in folder.iterdir():
                docid = folder.parts[-1] + "/" + file.parts[-1]
                open_file = file.open("r", encoding='utf-8')
                content = open_file.read()
                index.add_document(docid, content)
                count += 1

    print(count)

    index.save_to_file()



---



    book = Book("WEBPAGES_CLEAN")


if __name__ == "__main__":
    main()
