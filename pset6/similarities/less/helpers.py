from nltk.tokenize import sent_tokenize, word_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    same_lines = set(a.splitlines()) & set(b.splitlines())
    return (same_lines)


def sentences(a, b):
    """Return sentences in both a and b"""
    same_sentences = list(set(sent_tokenize(a)) & set(sent_tokenize(b)))
    return (same_sentences)


# takes in string and number of letters to parse
def extract_substrings(s, n):
    parsed_list = []
    for i in range(len(s) - n + 1):
        parsed_list.append(s[i: n + i])
    return (parsed_list)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    same_substrings = list(set(extract_substrings(a, n)) & set(extract_substrings(b, n)))
    return (same_substrings)