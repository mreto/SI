import pandas as pd

def keywords_with_the_most_important_words(n=5):
    if n == 50:
        file = open("./analyze_after_cut/catastrophy_keywords_50.txt", "w")
        #file = open("./analyze_after_cut/assasination_keywords_50.txt", "w")
        #file = open("./analyze_after_cut/neutral_keywords_50.txt", "w")
    else:
        file = open("./analyze_after_cut/catastrophy_keywords_5.txt", "w")
        #file = open("./analyze_after_cut/assasination_keywords_5.txt", "w")
        #file = open("./analyze_after_cut/neutral_keywords_5.txt", "w")
    # data = pd.read_csv('./analyze_after_cut/vector_catastrophy')
    data = pd.read_csv('./analyze_after_cut/vector_assasination')
    for index, row in data.iterrows():
        file.write("\n\nKLUCZOWE SŁOWO: {}\n".format(row[0]))
        row[0] = 0
        file.write(row.sort_values(ascending=False)[0:n].to_string())
    file.close()


def analyze_similarity_of_keywords_vectors():
    file = open("./analyze_after_cut/catastrophy_similarity.txt", "w")
    #file = open("./analyze_after_cut/assasination_similarity.txt", "w")
    #file = open("./analyze_after_cut/neutral_similarity.txt", "w")

    data = pd.read_csv('./analyze_after_cut/vector_catastrophy')
    #data = pd.read_csv('./analyze_after_cut/vector_assasination')
    #data = pd.read_csv('./analyze_after_cut/vector_neutral')

    list = []
    cnt, cnt2 = 0, 0
    for column in data:
        file.write("\n"+column+"\n")
        if data[column].max() != 'zdrad':
            x = float(data[column].max())/float(data[column].sum())
            x *= 100
            list.append(x)
            if x < 50:
                cnt+=1
            if x < 50 and data[column].sum() > 10:
                cnt2+=1
            file.write("{}".format(x)+"%\n")
    print("Srednio: ",sum(list)/len(list),"%")
    print("Mniej niz 50%: ", cnt/len(list)*100,"%")
    print("Mniej niz 50% i waga min. 10: ", cnt2/len(list)*100,"%")

if __name__ == "__main__":
    keywords_with_the_most_important_words(5)
    keywords_with_the_most_important_words(50)
    analyze_similarity_of_keywords_vectors()
