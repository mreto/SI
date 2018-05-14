import glob
import numpy as np
import math
import pandas as pd
import re
import unidecode
from collections import Counter


def get_raw_vector(directory):
    """
    Giving the files directory, returns numpy vector containing all words in
    unchanged order.
      - The punctation marks '?' '!' '.' are treated as words
      - Other interpunction is deleted
      - All words are converted to lower case.
    Example of directory : "./articles/*"
    Example of returned data:
    ['smolensk"' 'jest' ... 'przez' 'zespol' 'macierewicza', '.']
    """

    dir_all_files = glob.glob(directory)
    list_of_vectors = []
    for article in dir_all_files:
        f = open(article)
        read = f.read()
        list_of_vectors.append(np.array(re.findall(r"[\w']+|[.!?;]", read)))
        f.close()
    if list_of_vectors != []:
        vec = np.hstack(list_of_vectors)
        return np.char.lower(vec)
    return None


def count_distance(vector, max_distance=5, margin_before=True):
    """
    Returns the distance from the beginning or end of the vector.

    Example situation, we have found the keyword in the main vector,
    vector = ['aa', 'bb', '?', 'cc', 'dd', 'KEYWORD', 'ee', 'ff', 'gg', '?', 'hh']
    we would use function count_distance to get distance from keyword.
    so
    vector_beginning = ['aa', 'bb', '?', 'cc', 'dd']
    count_distance(vector_beginning, margin_before=True)
    returns dictionary {'dd':5, 'cc':4'}

    vector_end = ['ee', 'ff', 'gg', '?', 'hh']
    count_distance(vector_end, margin_before=False)
    returns dictionary {'ee':5, 'ff':4', 'gg': 3}

    function stops counting after founding '?', '!', '.' (another sentence).

    """
    count = []
    sentence_vector = []
    if margin_before is False:
        vector = reversed(vector)
    for i, word in enumerate(reversed(list(vector))):
        if word in {'?', '!', '.'}:
            break
        count.append(max_distance - i)
        sentence_vector.append(word)

    return dict(zip(sentence_vector, count))


def count_occurence(vector, keywords, keywords_full, margin=5):
    """
    Giving the vector of words, returns dictionary of occurences with distance
    from KEYWORD in marigin.
    Example:
    vector = ['This', 'is', 'very', 'short', 'very', 'sentence']
    keywords = ['is', 'short', 'very']
    margin = 2
    return -> {'is': {'This': 2, 'very':2"},
                'short': {'very': 2, 'is': 1, 'sentence':1}
                'very': {'This': 1, 'is': 2, 'short': 4, 'sentence': 2}}
    """
    length = vector.shape[0]
    dictionary = Counter({})
    for keyword_beginning, keyword_full in zip(keywords, keywords_full):
        dictionary[keyword_full] = Counter({})
        indices, = np.where(np.char.find(vector, keyword_beginning) == 0)
        # all the indices of elements that contain keyword
        # example vector = ['qaa', 'eea', 'jjdaa'], keyword = 'aa'
        # -> indices = [0, 2]

        for index in indices:
            left_margin = vector[max(0, index - margin):index]
            right_margin = vector[index + 1:min(index + margin, length)]
            dictionary[keyword_full] += count_distance(
                left_margin, margin_before=True)
            dictionary[keyword_full] += count_distance(
                right_margin, margin_before=False)

    return dictionary


def write_to_file(data_frame, file_name):
    file = open(file_name, 'w')
    output_string = ''
    output_string = str(data_frame.shape[1]) + '\n'
    output_string += "#n"
    columns_lables = data_frame.columns
    # row_labels = pd.DataFrame(np.genfromtxt('./keywords_full', dtype=str))
    row_labels = data_frame.index
    for column in columns_lables:
        output_string += ' ' + column
    output_string += "\n"
    file.writelines(output_string)
    file.close()
    # zzzz to ensure that it is the last column
    data_frame['zzzz'] = row_labels
    data_frame.to_csv(file_name, sep=' ', header=False, index=False, mode='a')


def get_som_data():

    dir_data = [
        './articles/assasination_plus_catastrophy/*',
        './articles/assasination/*', './articles/catastrophy/*',
        './articles/neural_from_wiki/*'
    ]
    dir_output = [
        './data/new_generated_data/assasination_plus_catastrophy.dat',
        './data/new_generated_data/correct_assasination.dat',
        './data/new_generated_data/correct_catastrophy.dat',
        './data/new_generated_data/neutral_from_wiki.dat'
    ]

    keywords = [line.rstrip('\n') for line in open('keywords')]
    keywords_full = [line.rstrip('\n') for line in open('./keywords_full')]

    for single_dir_data, single_dir_output in zip(dir_data, dir_output):
        print('generating data from ', single_dir_data)
        vector = get_raw_vector(single_dir_data)
        vector_basis, _ = convert_to_basis(vector)
        if vector_basis is not None:
            dictionary = count_occurence(vector_basis, keywords, keywords_full,
                                         6)

            # transforms from:
            # {'is': {'This': 1, 'very':1},
            #  'short': {'very': 2}
            #  'very': {'is': 1, 'short': 2, 'sentence': 1}}
            # to:
            #        This   very    is   short  sentence
            # is      1      1       0     0       0
            # short   0      2       0     0       0
            # very    0      0       1     2       1
            data_frame = pd.DataFrame(dictionary).T.fillna(0)
            shorter_data_frame = delete_vector_tail(data_frame)
            shorter_data_frame.to_csv(
                './analyze_after_cut/vector_assasination')
            # shorter_data_frame.to_csv('./analyze_after_cut/vector_neutral')
            # shorter_data_frame.to_csv('./analyze_after_cut/vector_catastrophy')
            write_to_file(shorter_data_frame, single_dir_output)


def delete_vector_tail(data_frame):
    for column in data_frame:
        m = float(data_frame[column].max())
        s = float(data_frame[column].sum())
        similarity = (m / s) * 100
        if s <= 10 or similarity >= 50:
            data_frame.pop(column)
    return data_frame


def get_part_vector(directory, number_to_add):

    list_of_vectors = []
    number_to_add = math.floor(number_to_add)
    if number_to_add < 1:
        number_to_add = 1
    dir_all_files = glob.glob(directory)
    list_of_vectors = []
    for article in dir_all_files[:number_to_add]:
        f = open(article)
        read = f.read()
        list_of_vectors.append(np.array(re.findall(r"[\w']+|[.!?;]", read)))
        f.close()
    if list_of_vectors != []:
        vec = np.hstack(list_of_vectors)
        return np.char.lower(vec)
    return None


def get_parted_som_data(n):
    dir_neutral = './articles/neural_from_wiki/*'
    dir_biased = './articles/catastrophy/*'
    dir_output = './data/biased_catastrophy/neutral_plus_part_catastrophy/'

    keywords = [line.rstrip('\n') for line in open('keywords')]
    keywords_full = [line.rstrip('\n') for line in open('keywords_full')]

    number_of_biased_articles = len(glob.glob(dir_biased))
    portion_to_add = number_of_biased_articles / n

    for i in range(1, n):
        print('generating data from ', dir_neutral, ' and ', dir_biased)
        print('loop element: ', i, ', of total:', n)
        vector_biased = get_part_vector(dir_biased, i * portion_to_add)
        vector_neutral = get_raw_vector(dir_neutral)
        dictionary_biased = count_occurence(vector_biased, keywords,
                                            keywords_full, 6)
        dictionary_neutral = count_occurence(vector_neutral, keywords,
                                             keywords_full, 6)

        data_frame_biased = pd.DataFrame(dictionary_biased).T.fillna(0)
        data_frame_neutral = pd.DataFrame(dictionary_neutral).T.fillna(0)

        shorter_biased = delete_vector_tail(data_frame_biased)
        shorter_neutral = delete_vector_tail(data_frame_neutral)
        data_frame = shorter_neutral.add(shorter_biased, fill_value=0)
        write_to_file(
            data_frame,
            dir_output + 'biased_fraction' + str(i).zfill(2) + '.dat')


def get_multiply_som_data(n):

    dir_neutral = './articles/neural_from_wiki/*'
    dir_biased = './articles/catastrophy/*'
    dir_output = './data/biased_catastrophy/neutral_plus_multiply_catastrophy/'

    keywords = [line.rstrip('\n') for line in open('keywords')]
    keywords_full = [line.rstrip('\n') for line in open('keywords_full')]

    for i in range(1, n):
        print('generating data from ', dir_neutral, 'x', 1, ' and ',
              dir_biased, 'x', i)
        vector_biased = get_raw_vector(dir_biased)
        vector_neutral = get_raw_vector(dir_neutral)
        dictionary_biased = count_occurence(vector_biased, keywords,
                                            keywords_full, 6)
        dictionary_neutral = count_occurence(vector_neutral, keywords,
                                             keywords_full, 6)
        data_frame_biased = pd.DataFrame(dictionary_biased).T.fillna(0)
        biased_short = delete_vector_tail(data_frame_biased)
        biased_multiplied = biased_short.apply(lambda x: x * i)
        data_frame_neut = pd.DataFrame(dictionary_neutral).T.fillna(0)
        neut_short = delete_vector_tail(data_frame_neut)
        data_frame = biased_multiplied.add(neut_short, fill_value=0)
        write_to_file(data_frame,
                      dir_output + 'neutral_plus_catastrophy_times_' +
                      str(i).zfill(2) + '.dat')


def get_basis(word):
    answer = ''
    with open('dictionaries/' + word[0] + '.tab') as f:
        for line in f:
            if line.split()[0] == word:
                answer = line.split()[1]
                break
    if answer == '':
        answer = word
    return answer


def convert_to_basis(vector):
    """
    Giving the vector with natural polish text, returns bases
    ['smolenskie', 'sprawy'] -> ['smolenski', 'sprawa']

    words_not_in_vectors are usefull to debugging which words are not in
    dictionary, e.g there is no 'Kaczynski' in dictionary and we should
    probably add it.
    """

    # load directory containing all Polish words
    dic = {}
    all_data_dic = glob.glob('./dictionaries/*')
    for dict_file in all_data_dic:
        with open(dict_file) as f:
            for line in f:
                dic[unidecode.unidecode(
                    line.split()[0])] = unidecode.unidecode(line.split()[1])
    converted_vector = []
    words_not_in_vectors = []
    for word in vector:
        if word in dic:
            converted_vector.append(dic[word])
        else:
            converted_vector.append(word)
            if word not in '!.?':
                words_not_in_vectors.append(word)
    return np.array(converted_vector), words_not_in_vectors


if __name__ == "__main__":
    get_som_data()
    get_parted_som_data(30)
    get_multiply_som_data(30)
