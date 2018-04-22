import glob
import numpy as np
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

    return Counter(dict(zip(sentence_vector, count)))


def count_occurence(vector, keywords, margin=5):
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
    dictionary = {}
    for keyword in keywords:
        dictionary[keyword] = Counter({})
        indices, = np.where(np.char.find(vector, keyword) == 0)
        # all the indices of elements that contain keyword
        # example vector = ['qaa', 'eea', 'jjdaa'], keyword = 'aa'
        # -> indices = [0, 2]

        for index in indices:
            left_margin = vector[max(0, index - margin):index]
            right_margin = vector[index + 1:min(index + margin, length)]
            dictionary[keyword] += count_distance(
                left_margin, margin_before=True)
            dictionary[keyword] += count_distance(
                right_margin, margin_before=False)

    return dictionary


def write_to_file(data_frame, file_name):
    file = open(file_name, 'w')
    output_string = ''
    output_string = str(data_frame.shape[1]) + '\n'
    output_string += "#n"
    columns_lables = data_frame.columns
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

    # dir_data = [
    #     './articles/assasination_plus_catastrophy/*',
    #     './articles/assasination/*', './articles/catastrophy/*'
    # ]
    # dir_output = [
    #     './data/new_generated_data/assasination_plus_catastrophy.dat',
    #     './data/new_generated_data/correct_assasination.dat',
    #     './data/new_generated_data/correct_catastrophy.dat'
    # ]

    # dir_data = ['./articles/random_wiki/*']
    # dir_output = ['./data/shorter_generated_data/neut.dat']

    # dir_data = ['./p/*']
    # dir_output = ['./data/new_generated_data/neut.dat']

    # dir_data = ['./articles/catastrophy/*']
    # dir_output = ['./data/shorter_generated_data/catastrophy.dat']
    dir_data = ['./articles/assasination/*']
    dir_output = ['./data/shorter_generated_data/assasination.dat']


    keywords = [line.rstrip('\n') for line in open('keywords')]

    for single_dir_data, single_dir_output in zip(dir_data, dir_output):
        print('generating data from ', single_dir_data)
        vector = get_raw_vector(single_dir_data)
        vector_basis, _ = convert_to_basis(vector)
        if vector_basis is not None:
            dictionary = count_occurence(vector_basis, keywords, 6)

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
            shorter_data_frame.to_csv('./analyze_after_cut/vector_assasination')
            #shorter_data_frame.to_csv('./analyze_after_cut/vector_neutral')
            #shorter_data_frame.to_csv('./analyze_after_cut/vector_catastrophy')
            write_to_file(shorter_data_frame, single_dir_output)


def delete_vector_tail(data_frame):
    for column in data_frame:
        m = float(data_frame[column].max())
        s = float(data_frame[column].sum())
        similarity = (m/s)*100
        if s <= 10 or similarity >= 50:
            data_frame.pop(column)
    return data_frame


def get_combined_raw_vector_without_interpunction(
        directory_neutral, directory_biased, number_to_add):
    list_of_vectors = []

    dir_neutral_articles = glob.glob(directory_neutral)
    for article in dir_neutral_articles:
        f = open(article)
        read = f.read()
        list_of_vectors.append(np.array(re.findall(r"[\w']+|[.!?;]", read)))
        f.close()

    dir_biased_articles = glob.glob(directory_biased)
    for article in dir_biased_articles[:number_to_add]:
        f = open(article)
        read = f.read()
        list_of_vectors.append(np.array(re.findall(r"[\w']+|[.!?;]", read)))
        f.close()

    if list_of_vectors != []:
        vec = np.hstack(list_of_vectors)
        return np.char.lower(vec)
    return None


def get_combined_raw_vector(directory_neutral, directory_biased,
                            number_to_add):
    list_of_vectors = []
    dir_neutral_articles = glob.glob(directory_neutral)
    for article in dir_neutral_articles:
        list_of_vectors.append(np.genfromtxt(article, dtype='str'))

    dir_biased_articles = glob.glob(directory_biased)
    i = 0
    for article in dir_biased_articles:
        list_of_vectors.append(np.genfromtxt(article, dtype='str'))
        i += 1
        if i >= number_to_add:
            break

    if list_of_vectors != []:
        return np.concatenate(list_of_vectors)
    return None


def get_combined_som_data(n):
    dir_neutral = './neutral_articles/*'
    dir_biased = './biased_articles/*'
    dir_output = './output/'

    keywords = [line.rstrip('\n') for line in open('keywords')]

    number_of_biased_articles = len(glob.glob(dir_biased))
    portion_to_add = number_of_biased_articles / n

    for i in range(1, n):
        print('generating data from ', dir_neutral, ' and ', dir_biased)
        vector = get_combined_raw_vector(dir_neutral, dir_biased,
                                         portion_to_add * i)
        if vector is not None:
            dictionary = count_occurence(vector, keywords, 6)
            data_frame = pd.DataFrame(dictionary).T.fillna(0)
            shorter_data_frame = delete_single_words(data_frame)
            write_to_file(shorter_data_frame,
                          dir_output + 'output' + str(i) + '.dat')


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
    # get_combined_som_data(4)