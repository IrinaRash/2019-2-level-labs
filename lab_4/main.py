import math
REFERENCE_TEXTS = []

def clean_tokenize_corpus(texts: list) -> list:
    if not texts or not isinstance(texts, list):
        return []
    clean_token_corpus = []
    for one_text in texts:
        if one_text and isinstance(one_text, str):
            while '<br />' in one_text:
                one_text = one_text.replace("<br />", " ")
            clean_token_text = []
            words = one_text.split(" ")
            for word in words:
                new_word = ""
                if not word.isalpha():
                    for i in word.lower():
                        if i.isalpha():
                            new_word += i
                    if new_word:
                        clean_token_text.append(new_word.lower())
                else:
                    clean_token_text.append(word.lower())
            clean_token_corpus += [clean_token_text]
    return clean_token_corpus

class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []
        self.file_names = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']

    def calculate_tf(self):
        if self.corpus:
            for one_text in self.corpus:
                if not one_text:
                    continue
                tf_values = {}
                if one_text:
                    len_text = len(one_text)
                    for word in one_text:
                        if not isinstance(word, str):
                            len_text -= 1
                for word in one_text:
                    if isinstance(word, str) and word not in tf_values:
                        count_word = one_text.count(word)
                        tf_values[word] = count_word / len_text
                self.tf_values.append(tf_values)
        return self.tf_values

    def calculate_idf(self):
        if isinstance(self.corpus, list):
            total_documents = 0
            docs_where_present = {}
            for document in self.corpus:
                if not isinstance(document, list):
                    continue
                total_documents += 1
                for word_occurrence in document:
                    if not isinstance(word_occurrence, str):
                        continue
                    if word_occurrence in docs_where_present:
                        continue
                    for doc in self.corpus:
                        if isinstance(doc, list) and word_occurrence in doc:
                            docs_where_present[word_occurrence] = docs_where_present.get(word_occurrence, 0) + 1
            for word in docs_where_present:
                self.idf_values[word] = math.log(total_documents / docs_where_present[word])
    def calculate(self):
        if not self.tf_values or not self.idf_values:
            return
        for element in self.tf_values:
            dictionary = {}
            for word, value in element.items():
                dictionary[word] = value * self.idf_values[word]
            self.tf_idf_values.append(dictionary)
    def report_on(self, word, document_index):
        if not self.tf_idf_values or document_index >= len(self.tf_idf_values):
            return ()
        tf_idf_dict = self.tf_idf_values[document_index]
        if not word in tf_idf_dict:
            return ()
        list_tf_idf = sorted(tf_idf_dict, key=tf_idf_dict.__getitem__, reverse=True)
        return tf_idf_dict.get(word.lower()), list_tf_idf.index(word.lower())

if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
    test_texts = clean_tokenize_corpus(REFERENCE_TEXTS)
    tf_idf = TfIdfCalculator(test_texts)
    tf_idf.calculate_tf()
    tf_idf.calculate_idf()
    tf_idf.calculate()
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))