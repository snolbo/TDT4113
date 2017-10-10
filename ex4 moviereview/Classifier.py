import utils
import os
from collections import Counter
import math

class Classifier:
    def __init__(self, pos_dir, neg_dir, prune_threshold, N):

        num_pos_reviews = len(os.listdir(pos_dir))
        num_neg_reviews = len(os.listdir(neg_dir))
        num_total_reviews = num_pos_reviews + num_neg_reviews
        
        print("Getting positive ngram dict")
        pos_ngram_dict = utils.get_ngram_dict_from_directory(pos_dir, N)
        print()

        print("Getting negative ngram dict")
        neg_ngram_dict = utils.get_ngram_dict_from_directory(neg_dir, N)
        print()

        total_ngram_dict = utils.get_joined_dict(pos_ngram_dict, neg_ngram_dict)

        pos_pruned_ngram_dict = utils.get_pruned_dict(pos_ngram_dict, prune_threshold, num_total_reviews)
        neg_pruned_ngram_dict = utils.get_pruned_dict(neg_ngram_dict, prune_threshold, num_total_reviews)

        pos_pruned_info_dict = utils.get_information_value_dict(pos_pruned_ngram_dict, total_ngram_dict)
        neg_pruned_info_dict = utils.get_information_value_dict(neg_pruned_ngram_dict, total_ngram_dict)

        # DEBUG
        NUM = 25
        pos_pruned_most_info = dict(Counter(pos_pruned_info_dict).most_common(NUM))
        neg_pruned_most_info = dict(Counter(neg_pruned_info_dict).most_common(NUM))

        print(pos_pruned_most_info)
        print(neg_pruned_most_info)
        print()

        self.prune_threshold_ = prune_threshold
        self.N_ = N
        self.neg_data_dict_ = neg_pruned_info_dict
        self.pos_data_dict_ = pos_pruned_info_dict
        return


    def classify_document(self, file_path):
        clean_test_words = utils.get_cleaned_words(file_path)
        test_ngrams = utils.get_ngram_from_list(clean_test_words, self.N_)
        pos_score = 0
        neg_score = 0
        epsilon = math.log10(self.prune_threshold_)
        # Calculate membership in pos and neg

        for ngram in test_ngrams:
            in_pos = ngram in self.pos_data_dict_
            in_neg = ngram in self.neg_data_dict_

            if in_pos:
                pos_score += math.log10(self.pos_data_dict_[ngram])
            else:
                pos_score += epsilon

            if in_neg:
                neg_score += math.log10(self.neg_data_dict_[ngram])
            else:
                neg_score += epsilon

        return pos_score >= neg_score

    def classify_directory(self, dir_path):
        file_list = os.listdir(dir_path)
        total_predictions = len(file_list)
        num_pos_predicted = 0
        num_neg_predicted = 0
        total_files = len(file_list)
        i = 0
        for file_name in file_list:
            file_path = dir_path + file_name
            is_positive = self.classify_document(file_path)
            if is_positive:
                num_pos_predicted += 1
            else:
                num_neg_predicted += 1
            i += 1
            if i % 1000 == 0:
                print("Progress classifying directory: " + str(i) + " : " + str(total_files))


        pos_prediction = num_pos_predicted / total_predictions
        neg_prediction = num_neg_predicted / total_predictions
        print()
        print("Prediction directory is positive: " + str(pos_prediction))
        print("Prediction directory is negative: " + str(neg_prediction))
        print()
        return