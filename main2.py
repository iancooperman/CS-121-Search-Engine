import pickle
from index import Index
import pathlib
from bookkeeping import Book

def main():
    index = Index()
    index.load_from_file()
    print("Loading index...")

    book = Book("WEBPAGES_RAW")

    while True:
        query = input("Enter a query: ")

        print("Searching...")
        query_result = index.query(query)
        num_results = len(query_result)

        print(f"{num_results} results:")

        for docid_score_pair in query_result[0:20]:
            print(book.retrieve_url(docid_score_pair[0]), docid_score_pair[1])
        print()



if __name__ == "__main__":
    main()