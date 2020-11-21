import re
import pickle
from collections import Counter
fp = open(r"C:\Users\ANKIT\PycharmProjects\NLPAssign3\Training set_HMM.txt","r",encoding="utf8")
text = fp.read()

sentences = text.split("\n\n")
print(len(sentences))
#Finding initial probablities of POS tags
beg_pos = []
for sent in sentences:
    tokens = re.split("\t|\n",sent)
    len_tokens = len(tokens)
    len_tokens = len_tokens - 2
    if len_tokens >= 2:
        beg_pos.append(tokens[1])
len_beg_pos= len(beg_pos)
beg_pos_count = Counter(beg_pos)
pie_dict = {}
for key in beg_pos_count:
    prob = beg_pos_count[key]/len_beg_pos
    pie_dict[key] = prob

#the above dictionary pie_dict conatisn the initial probabilities
#Finding the tag transmission probablities
pos_bigrams = []
all_pos = []
word_tags = []
word_list = []
for sent in sentences:
    tokens = re.split("\t|\n",sent)
    len_tokens = len(tokens)
    len_tokens = len_tokens - 2
    pos_list = []
    for i in range(1,len_tokens,+2):
        pos_list.append(tokens[i])
    for k in range(0,len_tokens-1,+2):
        word_list.append(tokens[k])
        group = (tokens[k], tokens[k+1])
        word_tags.append(group)
    all_pos.extend(pos_list)
    len_pos_list = len(pos_list)
    for j in range(len_pos_list-1):
        pair = (pos_list[j], pos_list[j + 1])
        pos_bigrams.append(pair)

count_pos_bigrams = Counter(pos_bigrams)
count_all_pos = Counter(all_pos)

prob_pos_bigrams = {}

for key in count_pos_bigrams:
    prob = count_pos_bigrams[key] / count_all_pos[key[0]]
    prob_pos_bigrams[key] = prob

#the above dictionary prob_pos_bigrams contains the tag emission probablities i.e A

#Now finding the emission probabilities i.e B
count_word_tags = Counter(word_tags)

prob_word_tags = {}
for key in count_word_tags:
    prob = count_word_tags[key] / count_all_pos[key[1]]
    prob_word_tags[key] = prob

#The dictionary prob_word_tags contains the emission probabilities i.e B

#Now to handle OOV words finding the POS tag with the highest probability for words
# that occured only once in the training set
count_word_list = Counter(word_list)

unique_pos_list = count_all_pos.keys()

hapax_tags_avg = {}
for tag in unique_pos_list:
    prob_sum = 0
    count = 0
    for key in prob_word_tags:
        if key[1] == tag and count_word_list[key[0]] == 1:
            prob_sum = prob_sum + prob_word_tags[key]
            count = count + 1
    if count != 0:
        prob = prob_sum / count
        hapax_tags_avg[tag] = prob

#The dictionary hapax_tags_avg contains the average probabilities for tags assigned to hapax words

all_pos_list = []
for x in unique_pos_list:
    all_pos_list.append(x)

Picklefile1 = open('ListPos', 'wb')
pickle.dump(all_pos_list, Picklefile1)
Picklefile1.close()

Picklefile2 = open('InitialProb', 'wb')
pickle.dump(pie_dict, Picklefile2)
Picklefile2.close()

Picklefile3 = open('PosTransmissionA', 'wb')
pickle.dump(prob_pos_bigrams, Picklefile3)
Picklefile3.close()

Picklefile4 = open('ProbEmissionB', 'wb')
pickle.dump(prob_word_tags, Picklefile4)
Picklefile4.close()

Picklefile5 = open('HapaxProb', 'wb')
pickle.dump(hapax_tags_avg, Picklefile5)
Picklefile5.close()

Picklefile6 = open('WordsList', 'wb')
pickle.dump(count_word_list, Picklefile6)
Picklefile6.close()
