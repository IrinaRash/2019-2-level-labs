"""
Labour work #3
Building an own N-gram model
"""

import math

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()

class WordStorage:
    def __init__(self):
        self.storage = {}
    def put(self, word: str) -> int:
        if not isinstance(word, str):
            return -1
        if word not in self.storage:
            if self.storage:
                identifier = max(self.storage.values()) + 1
            else:
                identifier = 1
            self.storage[word] = identifier
        return self.storage[word]

    def get_id_of(self, word: str) -> int:
        if word not in self.storage:
            return self.storage.get(word)
        return -1

    def get_original_by(self, id: int) -> str:
        id_index = -1
        if id in self.storage.values():
            id_index = list(self.storage.values()).index(id)
        if id_index != -1:
            return list (self.storage.keys())[id_index]
        return "UNK"

    def from_corpus(self, corpus: tuple):
        if isinstance(corpus, tuple):
            for word in corpus:
                code_word = hash(word)
                self.storage[word] = code_word

        return self.storage

class NGramTrie:
    def __init__(self, n):
        self.size = n
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}
        self.gram_frequencies_all = {}
        self.sentence_code_list = []

    def fill_from_sentence(self, sentence: tuple) -> str:
        if not isinstance(sentence, tuple) or not sentence:
            return 'ERROR'
        patterns = []
        for i in range(len(sentence)):
            if len(sentence) - i > self.size:
                patterns.append(sentence[i: i + self.size])
            elif len(sentence) - i == self.size:
                patterns.append(sentence[i:])
        for element in patterns:
            if element not in self.gram_frequencies:
                self.gram_frequencies[element] = 1
            else:
                self.gram_frequencies[element] += 1
        return 'OK'

    def calculate_log_probabilities(self):
        for gramm in self.gram_frequencies:
            summ = 0
            for base_gramm in self.gram_frequencies:
                if gramm[:-1] == base_gramm[:-1]:
                    summ += self.gram_frequencies[base_gramm]
                    self.gram_log_probabilities[gramm] = math.log(self.gram_frequencies[gramm] / summ)

    def predict_next_sentence(self, prefix: tuple) -> list:
        if isinstance(prefix, tuple) and len(prefix) == self.size - 1:
            for k in range(round(len(self.gram_log_probabilities) / 2)):
                maximum = -32000
                prefix = list(prefix)
                for i, j in self.gram_log_probabilities.items():
                    i = list(i)
                    if prefix[k:] == i[:self.size - 1]:
                        if j > maximum:
                            maximum = j
                if maximum == -32000:
                    return prefix
                for i, j in self.gram_log_probabilities.items():
                    if j == maximum:
                        prefix.append(i[-1])
            return prefix
        return []

def encode(storage_instance, corpus) -> list:
    code_sentences = []

    for sentence in corpus:
        code_sentence = []
        for word in sentence:
            code_word = storage_instance.get_id_of(word)
            code_sentence += [code_word]
        code_sentences += [code_sentence]

    return code_sentences

def split_by_sentence(text: str) -> list:
    if not text:
        return []
    ord_list = (33, 63, 46)
    if ord(text[-1]) not in ord_list:
        return []

    text = text.replace('\n', " ")
    while "  " in text:
        text = text.replace("  ", " ")
    words = text.split(" ")
    while "" in words:
        words.remove("")
    sentences = []
    symbol_count = 0
    ord_list = (33, 63, 46)

    for index, word in enumerate(words):
        if symbol_count == len(sentences):
            sentences += [['<s>']]
        if not word[-1].isalpha() and index == (len(words) - 1):
            sentences[symbol_count].append(word[:-1])
            sentences[symbol_count].append("</s>")
            symbol_count += 1
        elif ord(word[-1]) in ord_list and words[index + 1][0].isupper():
            sentences[symbol_count].append(word[:-1])
            sentences[symbol_count].append("</s>")
            symbol_count += 1
        else:
            sentences[symbol_count].append(word)

    new_sentences = []

    for sentence in sentences:
        new_words = []
        for index, word in enumerate(sentence):
            new_word = ""
            if not word.isalpha() and (not word == '<s>' and not word == "</s>"):
                for i in word:
                    if i.isalpha():
                        new_word += i
                if new_word:
                    new_words.append(new_word.lower())
            else:
                new_words.append(word.lower())
        new_sentences += [new_words]

    if new_sentences[0] == ["<s>", "</s>"]:
        return []

    return new_sentences

def initialize():
    ref_txt = ''
    if __name__ == '__main__':
        with open('not_so_big_reference_text.txt', 'r') as example:
            ref_txt = example.read()
    ref_txt = split_by_sentence(ref_txt)
    print(str(len(ref_txt)) + " sentences in corpus")
    for sentence in ref_txt:
        for word in sentence:
            WS.put(word)
    print(str(len(WS.storage)) + " unique words")
    ref_txt = encode(WS, ref_txt)
    for sentence in ref_txt:
        NGR.fill_from_sentence(tuple(sentence))
    NGR.calculate_log_probabilities()


def predict(words: str) -> list:
    final = []
    if not isinstance(words, str):
        return final
    test = []
    words = words.split()
    initialize()
    test.append(words)
    words = encode(WS, test)
    words = words[0]
    if len(words) != NGR.size - 1:
        return final
    for element in words:
        if element == -1:
            return final
    print(str(NGR.prefixes[tuple(words)]) + ' times right combination in corpus was found')
    code = NGR.predict_next_sentence(tuple(words))
    for element in code:
        final.append(WS.get_original_by(element))
    return final


WS = WordStorage()
NGR = NGramTrie(2)