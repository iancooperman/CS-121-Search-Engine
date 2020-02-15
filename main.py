import sys
import bookkeeping
from nltk.stem import WordNetLemmatizer
import nltk


def main():
    # nltk.download('wordnet')

    lemmatizer = WordNetLemmatizer()

    print(lemmatizer.lemmatize(""))

    # print(lemmatization("caresses"))


if __name__ == "__main__":
    main()
