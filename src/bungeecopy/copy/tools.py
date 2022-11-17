from bungeecopy.copy.search import search_filepairs

def bungeecopy(**kwds):
    search = search_filepairs(**kwds)
    for path, matches in search.items():
        print(path)
        for match in matches:
            print(match)
