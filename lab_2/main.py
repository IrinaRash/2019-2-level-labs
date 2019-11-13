"""
Labour work #2. Levenshtein distance.
"""
def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    matrix = []
    if not isinstance(num_rows, int) or not isinstance(num_cols, int):
        return matrix
    if num_cols <= 0 or num_rows <= 0:
        return matrix
    for i in range(num_rows):
        matrix.append([0] * num_cols)
    return matrix

def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    edit_matrix = list(edit_matrix)
    if not isinstance(add_weight, int) or not isinstance(remove_weight, int):
        return edit_matrix
    if len(edit_matrix) == 0:
        return edit_matrix
    if edit_matrix[0] == []:
        return edit_matrix
    i = 0
    j = 0
    for _ in edit_matrix:
        edit_matrix [0][0] = 0
        edit_matrix [i][0] = edit_matrix [i-1][0] + remove_weight
        i += 1
    for _ in edit_matrix[0]:
        edit_matrix [0][0] = 0
        edit_matrix [0][j] = edit_matrix [0] [j-1] + add_weight
        j += 1
    return edit_matrix

def minimum_value(numbers: tuple) -> int:
    numbers = list(numbers)
    for i in range(len(numbers)):
        if not isinstance(numbers[i], int):
            numbers[i] = -1
    return min(numbers)


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    if isinstance (add_weight, int) and isinstance (remove_weight, int) and isinstance (substitute_weight, int) and isinstance (original_word, str):
        for i in range(1, len(edit_matrix)):
            for j in range(1, len(edit_matrix[0])):
                if original_word[i - 1] != target_word[j - 1]:
                    edit_matrix[i][j] = minimum_value((edit_matrix[i - 1][j] + remove_weight,
                                                    edit_matrix[i][j - 1] + add_weight,
                                                    edit_matrix[i - 1][j - 1] + substitute_weight))
                else:
                    edit_matrix[i][j] = minimum_value((edit_matrix[i - 1][j] + remove_weight,
                                                    edit_matrix[i][j - 1] + add_weight,
                                                    edit_matrix[i - 1][j - 1]))
    return list (edit_matrix)

def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if not isinstance(original_word, str) or not isinstance(target_word, str):
        return -1
    if not isinstance(add_weight, int) or not isinstance(remove_weight, int) or not isinstance(substitute_weight, int):
        return -1
    original_word.lower()
    target_word.lower()
    matrix = tuple(generate_edit_matrix(len(original_word) + 1, len(target_word) + 1))
    matrix = tuple(initialize_edit_matrix(matrix, add_weight, remove_weight))
    result = fill_edit_matrix(matrix, add_weight, remove_weight, substitute_weight, original_word, target_word)
    return result [-1][-1]

def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    with open(path_to_file, 'w') as file:
        for line in edit_matrix:
            for i, num in enumerate(line):
                line[i] = str(num)
            file.write(','.join(line) + '\n')

def load_from_csv(path_to_file: str) -> list:
    with open(path_to_file) as matrix:
        matrix = matrix.readlines()
        for i, string in enumerate(matrix):
            matrix[i] = string.split(',')
            for j, num in enumerate(matrix[i]):
                matrix[i][j] = int(num)
    return matrix

