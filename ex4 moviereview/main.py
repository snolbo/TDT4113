import utils
import os
from collections import Counter
import Classifier


directory = "./data/subset/train/"
pos_dir = directory + "pos/"
neg_dir = directory + "neg/"

pos_test_filename = "0_9.txt"
neg_test_filename = "0_3.txt"


# Number of positive, negative and total reviews
num_pos_reviews = len(os.listdir(pos_dir))
num_neg_reviews = len(os.listdir(neg_dir))
num_total_reviews = num_pos_reviews + num_neg_reviews


# PART 1 & PART 3. Get list of cleaned words from file. Cleaned of symbols and stop words
pos_clean_words = utils.get_cleaned_words(pos_dir + pos_test_filename)
neg_clean_words = utils.get_cleaned_words(neg_dir + neg_test_filename)

print(pos_clean_words)
print(neg_clean_words)
print()

# PART 2 and PART 6. Change N for n-grams, N = 1 is 1 word. Read all files from training set, create n-gram words, print N most popular and their percentages
NUM = 25
N = 1
pos_ngram_dict = utils.get_ngram_dict_from_directory(pos_dir, N)
neg_ngram_dict = utils.get_ngram_dict_from_directory(neg_dir, N)

pos_most_pop = dict(Counter(pos_ngram_dict).most_common(NUM))
neg_most_pop = dict(Counter(neg_ngram_dict).most_common(NUM))
for key in pos_most_pop:
    pos_most_pop[key] /= num_total_reviews
for key in neg_most_pop:
    neg_most_pop[key] /= num_total_reviews

print(pos_most_pop)
print(neg_most_pop)
print()


# PART 4 find informationvalue of words
total_ngram_dict = utils.get_joined_dict(pos_ngram_dict, neg_ngram_dict)

pos_info_dict = utils.get_information_value_dict(pos_ngram_dict, total_ngram_dict)
neg_info_dict = utils.get_information_value_dict(neg_ngram_dict, total_ngram_dict)

pos_most_info = dict(Counter(pos_info_dict).most_common(NUM))
neg_most_info = dict(Counter(neg_info_dict).most_common(NUM))

print(pos_most_info)
print(neg_most_info)
print()


# PART 5 pruning lists before finding informatino values
prune_threshold = 0.05
pos_pruned_ngram_dict = utils.get_pruned_dict(pos_ngram_dict, prune_threshold, num_total_reviews)
neg_pruned_ngram_dict = utils.get_pruned_dict(neg_ngram_dict, prune_threshold, num_total_reviews)

pos_pruned_info_dict = utils.get_information_value_dict(pos_pruned_ngram_dict, total_ngram_dict)
neg_pruned_info_dict = utils.get_information_value_dict(neg_pruned_ngram_dict, total_ngram_dict)

pos_pruned_most_info = dict(Counter(pos_pruned_info_dict).most_common(NUM))
neg_pruned_most_info = dict(Counter(neg_pruned_info_dict).most_common(NUM))

print(pos_pruned_most_info)
print(neg_pruned_most_info)
print()


# PART 7 nad PART 8
print("START PART 7. CLASSIFIER")
N = 1
prune_threshold = 0.01  # 0.01 good for N = 1, N = 2 0.001
train_dir = "./data/alle/train/"
pos_train_dir = train_dir + "pos/"
neg_train_dir = train_dir + "neg/"

test_dir = "./data/alle/test/"
pos_test_dir = test_dir + "pos/"
neg_test_dir = test_dir + "neg/"

print("Initializing classifier...")
cls = Classifier.Classifier(pos_train_dir, neg_train_dir, prune_threshold, N)

print("Classifying directory...")
cls.classify_directory(pos_test_dir)