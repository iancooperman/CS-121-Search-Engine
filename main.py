import sys
from bookkeeping import Book
from nltk.stem import WordNetLemmatizer
from index import Index
import pathlib
from urllib.parse import urlparse
import re
from collections import defaultdict


searched_urls = defaultdict(int)
downloaded_urls = set()

def is_valid(url):
    """
    Function returns True or False based on whether the url has to be fetched or not. This is a great place to
    filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
    in this method
    """
    parsed_url = urlparse(url)
    url_directories = parsed_url.path.split("/")

    # limit how deep the url goes, keep path from going down greater than 6 directories
    if len(url_directories) > 6:
        return False

    url_directory_set = set()
    for directory in url_directories[:-1]:
        directory_lower = directory.lower()
        if directory_lower == "files":
            return False
        # limit length of directory names
        if len(directory) > 30:
            return False

        # eliminate urls with repeated directory names
        if directory_lower in url_directory_set:
            return False
        else:
            url_directory_set.add(directory_lower)

    # restrict the number of similar queries
    try:
        match = re.fullmatch(r"(.+)\?.+", url)
        base_url = match.group(1)
        searched_urls[base_url] += 1

        if searched_urls[base_url] > 500:
            return False
    except AttributeError as e:
        pass

    # keep links to somewhere in the same page to a minimum
    try:
        match = re.fullmatch(r"(.+)#.*", url)
        base_url = match.group(1)
        if base_url in downloaded_urls:
            return False
        else:
            downloaded_urls.add(base_url)
    except AttributeError as e:
        pass

    # what was here before. NO TOUCHIE
    parsed = urlparse(url)
    # print(parsed)
    try:
        return ".ics.uci.edu" in parsed.path \
               and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1|mat" \
                                + "|thmx|mso|arff|rtf|jar|csv" \
                                + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

    except TypeError as e:
        # print("TypeError for ", parsed)
        print(e)
        return False



def main():
    index = Index()
    book = Book("WEBPAGES_RAW")

    count = 0
    for folder in pathlib.Path("WEBPAGES_RAW").iterdir():
        if "." not in str(folder):  # If the file is a File type without any extensions (i.e. .json, .tsv, etc.)
            for file in folder.iterdir():
                docid = folder.parts[-1] + "/" + file.parts[-1]
                valid = is_valid(book.retrieve_url(docid))
                if valid:
                    open_file = file.open("r", encoding='utf-8')
                    content = open_file.read()
                    index.add_document(docid, content)
                    count += 1

    index.update_document_frequencies()

    index.save_to_file()




    book = Book("WEBPAGES_CLEAN")


if __name__ == "__main__":
    main()
