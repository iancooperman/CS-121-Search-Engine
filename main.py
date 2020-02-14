import sys
import bookkeeping



def main():
    book = bookkeeping.load_bookkeeping_file(sys.argv[1] + "/bookkeeping.json")
    print(type(book))
    # print(book)




if __name__ == "__main__":
    main()
