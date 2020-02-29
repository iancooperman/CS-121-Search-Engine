import pickle
from index import Index
import pathlib
from bookkeeping import Book

def main():
    index = Index()
    index.load_from_file()

    book = Book("WEBPAGES_RAW")

    print("Searching...")
    query_result = index.query("Informatics")
    num_results = len(query_result)

    print(f"{num_results} results:")

    for docinfo in query_result[0:20]:
        print(book.retrieve_url(docinfo._docid), docinfo.tfidf())



if __name__ == "__main__":
    main()