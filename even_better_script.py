import glob
import numpy as np
import pandas as pd


def get_raw_vector(directory):
    """
    Giving the files directory, returns numpy vector containing all words in unchanged
    order.
    Example of directory : "./articles/*"
    Example of returned data:
    ['Smolensk"' 'jest' ... 'przez' 'zespol' 'Macierewicza.']
    """

    dir_all_files = glob.glob(directory)
    list_of_vectors = []
    for article in dir_all_files:
        list_of_vectors.append(np.genfromtxt(article, dtype='str'))
    if list_of_vectors != []:
        return np.concatenate(list_of_vectors)
    return None


def count_occurence(vector, keywords, margin=5):
    """
    Giving the vector of words, returns dictionary of occurences of words in marigin in vector.
    Example:
    vector = ['This', 'is', 'very', 'short', 'very', 'sentence']
    keywords = ['is', 'short', 'very']
    margin = 1
    return -> {'is': {'This': 1, 'very':1"},
                'short': {'very': 2}
                'very': {'is': 1, 'short': 2, 'sentence': 1}}
    The capitalized keywords are also tested.
    """
    length = vector.shape[0]
    dictionary = {}
    for keyword in keywords:
        indices, = np.where(np.char.find(vector, keyword) == 0)
        # all the indices of elements that contain keyword
        # example vector = ['qaa', 'eea', 'jjdaa'], keyword = 'aa'
        # -> indices = [0, 2]

        indices_capitalize, = np.where(
            np.char.find(vector, keyword.capitalize()) == 0)
        single_vector = []
        for index in indices:
            left_margin = vector[max(0, index - margin):index]
            right_margin = vector[index + 1:min(index + margin, length)]
            single_vector.append(left_margin)
            single_vector.append(right_margin)

        for index in indices_capitalize:
            left_margin = vector[max(0, index - margin):index]
            right_margin = vector[index + 1:min(index + margin, length)]
            single_vector.append(left_margin)
            single_vector.append(right_margin)

        if single_vector != []:
            words_around = np.concatenate(single_vector)
            unique, counts = np.unique(words_around, return_counts=True)
            # sums across vector,
            # words_around =['s1', 's2', s1'] becomes
            # -> unique = ['s1', s2'], -> counts = [2, 1]

            dictionary[keyword] = dict(zip(unique, counts))
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

def delete_single_words(data_frame):
    for column in data_frame:
        if data_frame[column].sum()<=1.0:
            data_frame.pop(column)
    return data_frame

def get_som_data():

    dir_data = ['./random_wiki/*', './assasination/*', './catastrophy/*']
    dir_output = [
        'shorter_generated_data/random_wiki.dat',
        'shorter_generated_data/assasination.dat',
        'shorter_generated_data/catastrophy.dat'
    ]

    # dir_data = ['./neutralne/*']
    # dir_output = ['new_generated_data/neut.dat']

    keywords = [line.rstrip('\n') for line in open('keywords')]

    for single_dir_data, single_dir_output in zip(dir_data, dir_output):
        print('generating data from ', single_dir_data)
        vector = get_raw_vector(single_dir_data)
        if vector is not None:
            dictionary = count_occurence(vector, keywords, 6)

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
            shorter_data_frame=delete_single_words(data_frame)
            write_to_file(shorter_data_frame, single_dir_output)


if __name__ == "__main__":
    get_som_data()
