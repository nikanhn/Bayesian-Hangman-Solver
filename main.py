# part b
def prob_next(dict_evidence, list_evidence, char):
    global corpus
    normal_dict = {word: value for word, value in corpus.items() 
                   if set(list_evidence) & set([c for c in word]) == set({}) and all([word[i] == dict_evidence[i] 
                                                                                      for i in dict_evidence.keys()]) and 
                                                                                      set(dict_evidence.values()) & set([c for idx, c in enumerate(word) 
                                                                                                                         if idx not in list(dict_evidence.keys())]) == set({})}
    joint_list_evidence = list_evidence + [char]
    joint_dict = {word: value for word, value in corpus.items() 
                  if set(joint_list_evidence) & set([c for c in word]) == set({}) and all([word[i] == dict_evidence[i] 
                                                                                           for i in dict_evidence.keys()]) and 
                                                                                           set(dict_evidence.values()) & set([c for idx, c in enumerate(word) 
                                                                                                                              if idx not in list(dict_evidence.keys())]) == set({})}
    return 1 - (sum([count for _, count in joint_dict.items()])) / sum([count for _, count in normal_dict.items()])


file_path = '/Users/Surface/Desktop/CSE250A - HW1/hw1_word_counts_05.txt'
corpus = {}
with open(file_path, 'r') as file:
    for line in file:
        corpus[line[0:5]] = int(line[6:-1])

# part a

sum_over_all = sum([count for _, count in corpus.items()])
frequency_corpus = {word: count/sum_over_all for word, count in corpus.items()}

frequency_corpus_sorted_descending = sorted({count: word for word, count in frequency_corpus.items()}.items(), reverse=True)
print()
fifteen_most_probable = [word for _, word in list(frequency_corpus_sorted_descending)[:15]]
print("15 Most Frequent: ",fifteen_most_probable)
fourteen_least_probable = [word for _, word in list(frequency_corpus_sorted_descending)[-14:]]
print ("14 Least Frequent: ",fourteen_least_probable)
print("\n", "--------")

# part b continue
dict_evidence = {}
list_of_evidence = []
list_of_chars = [chr(i) for i in range(65, 91, 1)]
list_of_probs_for_letters = [(c, prob_next(dict_evidence, list_of_evidence, c)) for c in list_of_chars]
print(list_of_probs_for_letters)
print("\n", "--------")


dict_evidence_1 = {}
list_of_evidence_1 = ['E', 'A']
list_of_chars = [chr(i) for i in range(65, 91, 1)]
list_of_probs_for_letters_1 = [(c, prob_next(dict_evidence_1, list_of_evidence_1, c)) for c in list_of_chars]
print(list_of_probs_for_letters_1)
print("\n", "--------")

dict_evidence_2 = {0:'A', 4:'S'}
list_of_evidence_2 = []
list_of_chars = [chr(i) for i in range(65, 91, 1)]
list_of_probs_for_letters_2 = [(c, prob_next(dict_evidence_2, list_of_evidence_2, c)) for c in list_of_chars]
print(list_of_probs_for_letters_2)
print("\n", "--------")

dict_evidence_3 = {0:'A', 4:'S'}
list_of_evidence_3 = ['I']
list_of_chars = [chr(i) for i in range(65, 91, 1)]
list_of_probs_for_letters_3 = [(c, prob_next(dict_evidence_3, list_of_evidence_3, c)) for c in list_of_chars]
print(list_of_probs_for_letters_3)
print("\n", "--------")

dict_evidence_4 = {2:'O'}
list_of_evidence_4 = ['A','E','M','N','T']
list_of_chars = [chr(i) for i in range(65, 91, 1)]
list_of_probs_for_letters_4 = [(c, prob_next(dict_evidence_4, list_of_evidence_4, c)) for c in list_of_chars]
print(list_of_probs_for_letters_4)
