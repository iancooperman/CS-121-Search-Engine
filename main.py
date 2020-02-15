import sys
from bookkeeping import Book
from nltk.stem import WordNetLemmatizer


def main():
    book = Book("WEBPAGES_CLEAN")
    document = book.retrieve_document("www.ics.uci.edu/~pattis/common/handouts/macpythoneclipsejava/images/java?C=D;O=A")
    print(document)
    # print(lemmatization("caresses"))


if __name__ == "__main__":
    main()
