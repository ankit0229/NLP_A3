import re
import pickle
from collections import Counter

Picklefile1 = open('ListPos', 'rb')
all_pos_list = pickle.load(Picklefile1)

Picklefile2 = open('InitialProb', 'rb')
pie_dict = pickle.load(Picklefile2)
pie_dict = Counter(pie_dict)

Picklefile3 = open('PosTransmissionA', 'rb')
prob_pos_bigrams = pickle.load(Picklefile3)
prob_pos_bigrams = Counter(prob_pos_bigrams)

Picklefile4 = open('ProbEmissionB', 'rb')
prob_word_tags = pickle.load(Picklefile4)
prob_word_tags = Counter(prob_word_tags)

Picklefile5 = open('HapaxProb', 'rb')
hapax_tags_avg = pickle.load(Picklefile5)
hapax_tags_avg = Counter(hapax_tags_avg)

Picklefile6 = open('WordsList', 'rb')
count_word_list = pickle.load(Picklefile6)

def ViterbiAlgo(sentence):
    len_sentence = len(sentence)
    len_sentence = len_sentence - 1
    len_all_pos_list = len(all_pos_list)
    vitrerbi = []
    backpointer = []
    probability = 0

    for i in range(len_all_pos_list):
         vitrerbi.append([])
         current  = all_pos_list[i]
         word = sentence[0]
         group = (word,current)
         probability = prob_word_tags[group]
         if probability == 0 and count_word_list[word] == 0:
             probability = hapax_tags_avg[current]
         value = (pie_dict[current] * probability)
         vitrerbi[i].append(value)
         for j in range(1,len_sentence):
            vitrerbi[i].append(0)

    for i in range(len_all_pos_list):
        backpointer.append([])
        backpointer[i].append(0)
        for j in range(1, len_sentence):
            backpointer[i].append(0)

    for t in range(1,len_sentence):
        word = sentence[t]
        for s in range(len_all_pos_list):
            values = []
            current = all_pos_list[s]
            for k in range(len_all_pos_list):
                prev = all_pos_list[k]
                pair = (prev,current)
                group = (word,current)
                prob = prob_word_tags[group]
                if prob == 0 and count_word_list[word] == 0:
                    prob = hapax_tags_avg[current]
                x = vitrerbi[k][t-1] * prob_pos_bigrams[pair] * prob
                values.append(x)
            vitrerbi[s][t] = max(values)
            parent_pos = values.index(max(values))
            backpointer[s][t] = parent_pos + 1
    last_col_values = []
    for z in range(len_all_pos_list):
        last_col_values.append(vitrerbi[z][len_sentence-1])
    best_path_prob = max(last_col_values)
    best_path_pointer = last_col_values.index(max(last_col_values))
    predicted_pos_tags = []
    predicted_pos_tags.append(all_pos_list[best_path_pointer])
    best = best_path_pointer
    for x in range(len_sentence-1,0,-1):
        current = backpointer[best][x]
        predicted_pos_tags.append(all_pos_list[current-1])
        best = current-1
    len_predicted_pos_tags = len(predicted_pos_tags)
    wd = 0
    for w in range(len_predicted_pos_tags-1,-1,-1):
        fp2 = open(r"C:\Users\ANKIT\PycharmProjects\NLPAssign3\PredictedTags.txt","a")
        fp2.write(sentence[wd]+"\t"+predicted_pos_tags[w]+"\n" )
        wd = wd + 1
    fp2.write("."+"\t"+"."+"\n\n")
    fp2.close()

print("Enter the path of test file to be :")
test_file = input()
fp = open(test_file,"r",encoding="utf8")
text = fp.read()
fp.close()
sentences = text.split("\n\n")
for sent in sentences:
    tokens = re.split("\n",sent)
    ViterbiAlgo(tokens)
print("Predicted tags file created successfully")







