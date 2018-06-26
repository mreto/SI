import glob
import random
import numpy as np
import math
import pandas as pd
import re
import os
import unidecode
import dill
from collections import Counter
import sklearn.feature_selection as sk

stopwords = [
    'a', 'aby', 'ach', 'acz', 'aczkolwiek', 'aj', 'albo', 'ale', 'alez',
    'alez', 'ani', 'az', 'az', 'bardziej', 'bardzo', 'beda', 'bedzie', 'bez',
    'deda', 'beda', 'bede', 'bedę', 'bedzie', 'bo', 'bowiem', 'by', 'byc',
    'byc', 'byl', 'byla', 'byli', 'bylo', 'byly', 'byl', 'byla', 'bylo',
    'byly', 'bynajmniej', 'cala', 'cali', 'caly', 'cala', 'caly', 'ci', 'cie',
    'ciebie', 'cie', 'co', 'cokolwiek', 'cos', 'cos', 'czasami', 'czasem',
    'czemu', 'czy', 'czyli', 'daleko', 'dla', 'dlaczego', 'dlatego', 'do',
    'dobrze', 'dokad', 'dokad', 'dosc', 'dosc', 'duzo', 'duzo', 'dwa', 'dwaj',
    'dwie', 'dwoje', 'dzis', 'dzisiaj', 'dzis', 'gdy', 'gdyby', 'gdyz', 'gdyz',
    'gdzie', 'gdziekolwiek', 'gdzies', 'gdzies', 'go', 'i', 'ich', 'ile', 'im',
    'inna', 'inne', 'inny', 'innych', 'iz', 'iz', 'ja', 'jak', 'jakas',
    'jakas', 'jakby', 'jaki', 'jakichs', 'jakichs', 'jakie', 'jakis', 'jakis',
    'jakiz', 'jakiz', 'jakkolwiek', 'jako', 'jakos', 'jakos', 'ja', 'je',
    'jeden', 'jedna', 'jednak', 'jednakze', 'jednakze', 'jedno', 'jego', 'jej',
    'jemu', 'jesli', 'jest', 'jestem', 'jeszcze', 'jesli', 'jezeli', 'jezeli',
    'juz', 'juz', 'kazdy', 'kazdy', 'kiedy', 'kilka', 'kims', 'kims', 'kto',
    'ktokolwiek', 'ktora', 'ktore', 'ktorego', 'ktorej', 'ktory', 'ktorych',
    'ktorym', 'ktorzy', 'ktos', 'ktos', 'ktora', 'ktore', 'ktorego', 'ktorej',
    'ktory', 'ktorych', 'ktorym', 'ktorzy', 'ku', 'lat', 'lecz', 'lub', 'ma',
    'maja', 'malo', 'mam', 'mi', 'miedzy', 'miedzy', 'mimo', 'mna', 'mna',
    'mnie', 'moga', 'moga', 'moi', 'moim', 'moj', 'moja', 'moje', 'moze',
    'mozliwe', 'mozna', 'moze', 'mozliwe', 'mozna', 'moj', 'mu', 'musi', 'my',
    'na', 'nad', 'nam', 'nami', 'nas', 'nasi', 'nasz', 'nasza', 'nasze',
    'naszego', 'naszych', 'natomiast', 'natychmiast', 'nawet', 'nia', 'nia',
    'nic', 'nich', 'nie', 'niech', 'niego', 'niej', 'niemu', 'nigdy', 'nim',
    'nimi', 'niz', 'niz', 'no', 'o', 'obok', 'od', 'okolo', 'on', 'ona', 'one',
    'oni', 'ono', 'oraz', 'oto', 'owszem', 'pan', 'pana', 'pani', 'po', 'pod',
    'podczas', 'pomimo', 'ponad', 'poniewaz', 'poniewaz', 'powinien',
    'powinna', 'powinni', 'powinno', 'poza', 'prawie', 'przeciez', 'przeciez',
    'przed', 'przede', 'przedtem', 'przez', 'przy', 'roku', 'rowniez',
    'rowniez', 'sam', 'sama', 'sa', 'sie', 'sie', 'skad', 'skad', 'soba',
    'soba', 'sobie', 'sposob', 'sposob', 'swoje', 'ta', 'tak', 'taka', 'taki',
    'takie', 'takze', 'takze', 'tam', 'te', 'tego', 'tej', 'ten', 'teraz',
    'tez', 'to', 'toba', 'toba', 'tobie', 'totez', 'totez', 'totoba', 'trzeba',
    'tu', 'tutaj', 'twoi', 'twoim', 'twoj', 'twoja', 'twoje', 'twoj', 'twym',
    'ty', 'tych', 'tylko', 'tym', 'u', 'w', 'wam', 'wami', 'was', 'wasz',
    'wasza', 'wasze', 'we', 'wedlug', 'wiele', 'wielu', 'wiec', 'wiecej',
    'wlasnie', 'wlasnie', 'wszyscy', 'wszystkich', 'wszystkie', 'wszystkim',
    'wszystko', 'wtedy', 'wy', 'z', 'za', 'zaden', 'zadna', 'zadne', 'zadnych',
    'zapewne', 'zawsze', 'ze', 'zeby', 'zeznowu', 'zl', 'znow', 'znowu',
    'znow', 'zostal', 'zostal', 'zaden', 'zadna', 'zadne', 'zadnych', 'ze',
    'zeby'
]


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
        filtered_words = [
            word for word in np.char.lower(
                np.array(re.findall(r"[\w']+|[.!?;]", read)))
            if word not in stopwords
        ]
        list_of_vectors.append(filtered_words)
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
    """
    write data_frame to file in som format
    """
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
    del data_frame['zzzz']


def get_single_articles_data():
    """
    Generates som data from for every article in dir_source. The function
    generates separate data for every single article.
    (it doesnt sum it in contrast to get_som_data)
    The data are beeing normalized as in the final report.
    """

    data = [('./articles/catastrophy/*',
             './data/single_articles_data/catastrophy/', 0),
            ('./articles/assasination/*',
             './data/single_articles_data/assasination/', 1)]

    # super important
    dic = None

    scores = [[] for i in data]
    for Tuple in data:
        (source, out, y) = Tuple
        dir_all_files = glob.glob(source)
        keywords = [line.rstrip('\n') for line in open('keywords')]
        keywords_full = [line.rstrip('\n') for line in open('./keywords_full')]
        for article in dir_all_files:
            base = os.path.basename(article)
            print('generating data from ', article)
            print('to file ', out + (os.path.splitext(base)[0]) + '.dat')
            if dic is None:
                print(
                    'SUPER ERROR are you sure dictionaries are at ./dictionaries/?',
                    'not using dictionaries')

            f = open(article)
            read = f.read()
            vector = [
                word for word in np.char.lower(
                    np.array(re.findall(r"[\w']+|[.!?;]", read)))
                if word not in stopwords
            ]
            f.close()
            vector_basis, dic = convert_to_basis(vector, dic)
            dictionary = count_occurence(vector_basis, keywords, keywords_full,
                                         6)
            data_frame = pd.DataFrame(dictionary).T.fillna(0)
            normalized = normalize(delete_vector_tail(data_frame))
            scores[y].append(normalized)
            base = os.path.basename(article)
            write_to_file(normalized,
                          out + (os.path.splitext(base)[0]) + '.dat')
    return scores


def get_som_data():
    """
    Sums all articles in single dir in 'dir_data' and generate data in som
    format.
    The data are beeing normalized as in the final report.
    """

    dir_data = [
        './articles/assasination_plus_catastrophy/*',
        './articles/assasination/*', './articles/catastrophy/*',
        './articles/neural_from_wiki/*'
    ]
    dir_output = [
        './data/basic_data/assasination_plus_catastrophy.dat',
        './data/basic_data/correct_assasination.dat',
        './data/basic_data/correct_catastrophy.dat',
        './data/basic_data/neutral_from_wiki.dat'
    ]

    keywords = [line.rstrip('\n') for line in open('keywords')]
    keywords_full = [line.rstrip('\n') for line in open('./keywords_full')]

    # super important
    dic = None
    out = []
    for single_dir_data, single_dir_output in zip(dir_data, dir_output):
        print('generating data from ', single_dir_data)
        vector = get_raw_vector(single_dir_data)
        vector_basis, dic = convert_to_basis(vector, dic)
        if dic is None:
            print(
                'SUPER ERROR are you sure dictionaries are at ./dictionaries/?',
                'not using dictionaries')
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
            normalized = normalize(delete_vector_tail(data_frame))
            # shorter_data_frame.to_csv('./analyze_after_cut/vector_assasination')
            write_to_file(normalized, single_dir_output)
            out.append(normalized)
    return out


def normalize(data_frame):
    """
    normalize each row of matrix, within range 0 and 1.
    """
    df_max = data_frame.max(axis=1)
    data_frame = data_frame.divide(df_max, axis=0)
    return data_frame.fillna(0)


def delete_vector_tail(data_frame, minimum=50):
    """
    delete the column of data_frame that has little impact on the word and can
    be percived as a noise
    """

    for column in data_frame:
        m = float(data_frame[column].max())
        s = float(data_frame[column].sum())
        similarity = (m / s) * 100
        if s <= 10 or similarity >= minimum:
            data_frame.pop(column)
    return data_frame


def get_part_vector(directory, number_to_add):
    """
    returns the vector with only portion of data in directory
    """
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
    """
    Sums all articles in dir_neutral with part of the articles
    from dir_biased. It allows us to see how the neutral data
    become biased. It start with portion 0 and finish with
    neutral + biased data. n is the number of steps.
    The data are beeing normalized as in the final report.
    """
    dir_neutral = './articles/neural_from_wiki/*'
    dir_biased = ['./articles/catastrophy/*', './articles/assasination/*']
    dir_output = [
        './data/biased_catastrophy/part/catastrophy_',
        './data/biased_assasination/part/assasination_'
    ]

    keywords = [line.rstrip('\n') for line in open('keywords')]
    keywords_full = [line.rstrip('\n') for line in open('./keywords_full')]

    for biased, output in zip(dir_biased, dir_output):
        number_of_biased_articles = len(glob.glob(biased))
        portion_to_add = number_of_biased_articles / n

        for i in range(1, n):
            print('generating parted data from ', dir_neutral, ' and ', biased)
            print('to file ',
                  output + 'parted' + str(i).zfill(2) + '_' + str(n) + '.dat')
            print('loop element: ', i, ', of total:', n)
            vector_biased = get_part_vector(biased, i * portion_to_add)
            vector_neutral = get_raw_vector(dir_neutral)
            dictionary_biased = count_occurence(vector_biased, keywords,
                                                keywords_full, 6)
            dictionary_neutral = count_occurence(vector_neutral, keywords,
                                                 keywords_full, 6)

            data_frame_biased = pd.DataFrame(dictionary_biased).T.fillna(0)
            data_frame_neutral = pd.DataFrame(dictionary_neutral).T.fillna(0)

            shorter_biased = delete_vector_tail(data_frame_biased)
            shorter_neutral = delete_vector_tail(data_frame_neutral)
            data_frame = normalize(
                shorter_neutral.add(shorter_biased, fill_value=0))
            write_to_file(
                data_frame,
                output + 'parted' + str(i).zfill(2) + '_' + str(n) + '.dat')


def get_multiply_som_data(n):
    """
    Sums all articles in dir_neutral with multiplied by i
    scores of articles in dir_biased. It allows us to see how the neutral data
    become fully transform to biased. It start with multipling by 1 and finish
    with neutral + n * biased data.
    The data are beeing normalized as in the final report.
    """

    dir_neutral = './articles/neural_from_wiki/*'
    dir_biased = ['./articles/catastrophy/*', './articles/assasination/*']
    dir_output = [
        './data/biased_catastrophy/multiply/catastrophy_',
        './data/biased_assasination/multiply/assasination_'
    ]

    keywords = [line.rstrip('\n') for line in open('keywords')]
    keywords_full = [line.rstrip('\n') for line in open('keywords_full')]

    for biased, output in zip(dir_biased, dir_output):
        for i in range(1, n):

            print('generating data from ', dir_neutral, 'x', 1, ' and ',
                  biased, 'x', i)
            print(
                'to file ',
                output + 'multiply_' + str(i).zfill(2) + '_' + str(n) + '.dat')

            vector_biased = get_raw_vector(biased)
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
            data_frame = normalize(
                biased_multiplied.add(neut_short, fill_value=0))
            write_to_file(
                data_frame,
                output + 'multiply_' + str(i).zfill(2) + '_' + str(n) + '.dat')


def convert_to_basis(vector, dic=None):
    """
    Giving the vector with natural polish text, returns bases
    ['smolenskie', 'sprawy'] -> ['smolenski', 'sprawa']

    words_not_in_vectors are usefull to debugging which words are not in
    dictionary, e.g there is no 'Kaczynski' in dictionary and we should
    probably add it.
    """

    # load directory containing all Polish words
    if dic is None:
        dic = {}
        all_data_dic = glob.glob('./dictionaries/*')
        for dict_file in all_data_dic:
            with open(dict_file) as f:
                for line in f:
                    dic[unidecode.unidecode(
                        line.split()[0])] = unidecode.unidecode(
                            line.split()[1])
    converted_vector = []
    words_not_in_vectors = []
    for word in vector:
        if word in dic:
            converted_vector.append(dic[word])
        else:
            converted_vector.append(word)
            if word not in '!.?':
                words_not_in_vectors.append(word)
    if not dic:
        return np.array(converted_vector), None
    return np.array(converted_vector), dic


def filtr(scores):
    X = pd.DataFrame()
    max_occurence = 0
    for list_of_scores in scores:
        if len(list_of_scores) > max_occurence:
            max_occurence = len(list_of_scores)

    for class_id, scores_in_class in enumerate(scores):
        for i, score in enumerate(scores_in_class):
            score['score'] = class_id
            X = X.append(score, sort=True)
        while i < max_occurence:
            X = X.append(
                scores_in_class[random.randint(0,
                                               len(scores_in_class) - 1)],
                sort=True)
            i += 1
    X = X.fillna(0)
    # round to [0.2, 0.4, 0.6, 0.8, 1]
    X = (X * 5).round(0) / 5

    y = X['score']
    del X['score']
    print("start mutual information")
    mi = sk.mutual_info_classif(X, y)
    mi = mi / np.amax(mi)
    columns = X.columns
    usefull_feature = mi != 0
    print("uzyteczne: ", columns[usefull_feature].tolist(),
          columns[usefull_feature].shape)
    print("bexuzyteczne: ", columns[np.invert(usefull_feature)].tolist(),
          columns[np.invert(usefull_feature)].shape)
    print("najlepsze , ", columns[mi > 0].tolist())

    return columns[usefull_feature]


def get_filtered_single_articles_data(scores, usefull_feature):
    data = [('./articles/catastrophy/*',
             './data/single_articles_data_filtered/catastrophy/'),
            ('./articles/assasination/*',
             './data/single_articles_data_filtered/assasination/')]

    for dir_tuple, score_list in zip(data, scores):
        (source, out) = dir_tuple
        dir_all_files = glob.glob(source)
        for article, normalized in zip(dir_all_files, score_list):
            base = os.path.basename(article)
            indices = np.intersect1d(usefull_feature, normalized.columns)
            if indices.size > 0:
                filtered = normalized[indices]
                write_to_file(filtered,
                              out + (os.path.splitext(base)[0]) + '.dat')
    return scores


def get_filtered_som_data(scores, usefull_features):
    dir_output = [
        './data/basic_data/fassasination_plus_catastrophy.dat',
        './data/basic_data/fcorrect_assasination.dat',
        './data/basic_data/fcorrect_catastrophy.dat',
        './data/basic_data/fneutral_from_wiki.dat'
    ]

    i = 0
    for single_dir_output in dir_output:
        normalized = scores[i]
        i += 1
        # shorter_data_frame.to_csv('./analyze_after_cut/vector_assasination')
        indices = np.intersect1d(usefull_feature, normalized.columns)
        filtered = normalized[indices]
        write_to_file(filtered, single_dir_output)


if __name__ == "__main__":
    scores_single = get_single_articles_data()
    scores_basic = get_som_data()
    usefull_feature = filtr(scores_single)
    get_filtered_single_articles_data(scores_single, usefull_feature)
    get_filtered_som_data(scores_basic, usefull_feature)
