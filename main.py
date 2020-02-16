import sys
from bookkeeping import Book
from nltk.stem import WordNetLemmatizer
from index import Index


def main():
    book = Book("WEBPAGES_CLEAN")
    home = book.retrieve_document("fano.ics.uci.edu/cites/Publication/Cha-SODA-02-cp.html")
    print(home)



    index = Index()



if __name__ == "__main__":
    main()
