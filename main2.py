import pickle
from index import Index
import pathlib
from bookkeeping import Book

def main():
    index = Index()
    index.load_from_file()

    book = Book("WEBPAGES_CLEAN")

    print("Unique Words: " + str(len(index.inverted_index)))
    query_result = index.query("Irvine")
    num_results = len(query_result)

    print(f"{num_results} results:")

    for docid in query_result[0:20]:
        print(book.retrieve_url(docid))



if __name__ == "__main__":
    main()