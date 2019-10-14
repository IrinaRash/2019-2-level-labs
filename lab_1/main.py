"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""
def calculate_frequences(text: str) -> dict:
    """
    Calculates number of times each word appears in the text
    """
    if isinstance(text, int):
        return {}
    if text is None or text == (''):
        return {}
    result = ''
    for word in text:
        if word.isalpha() or word == ' ' or word == '\n':
            result += word.lower()
    splitted = result.split()
    dictionary = {}
    for key in splitted:
        if key in dictionary:
            dictionary[key] += 1
        else:
            dictionary [key] = 1
    return dictionary

def filter_stop_words(dictionary: dict, stop_words: tuple) -> dict:

    """
    Removes all stop words from the given frequencies dictionary
    """
    if dictionary is None or stop_words is None:
        return {}
    if dictionary is None and stop_words is None:
        return {}
    if not stop_words:
        return dictionary
    if not dictionary:
        return {}
    keys_list = list(dictionary.keys())
    for word in stop_words:
        if word in dictionary:
            del (dictionary[word])
    return dictionary

def get_top_n(dictionary: dict, top_n: int) -> tuple:
    if dictionary == {}:
        return ()
    if top_n < 0:
        return ()
    else:
        frequency_list = dictionary.items()
        sorted_list = sorted(frequency_list, key=lambda tup: tup[1], reverse=True)
        top_n = (sorted_list[0:top_n])
        result = []
        for w in top_n:
            result.append(w[0])
        result = tuple(result)
        return result