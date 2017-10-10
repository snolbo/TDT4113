import re
import os
from collections import Counter
import numpy


ONLY_WORD_REGEX = "[^A-Za-z0-9 ]+"  # Keep letters numbers and spaces

def get_pruned_dict(dict_to_prune, prune_threshold, reference_count):
    pruned_dict = {}
    for key in dict_to_prune:
        if dict_to_prune[key]/reference_count > prune_threshold:
            pruned_dict[key] = dict_to_prune[key]
    return pruned_dict

# Returns words cleaned for symbols and stop-words from the specified file path
def get_cleaned_words(filename):
    file_object = open(filename, encoding="utf8")
    content = file_object.read();
    file_object.close()
    # Clean content
    content = content.lower()
    # Clean text of symbols and  tags
    content = re.sub('<[^>]*>', ' ', content)  # remove all tags replace with space
    content = re.sub(ONLY_WORD_REGEX, '', content)
    content_list = content.split()
    cleaned_words = []
    # REMOVE STOP WORDS. OK TO DO IT HERE?
    stop_words = get_stop_words()
    for word in content_list:
        if word in stop_words:
            continue
        cleaned_words.append(word)
    return cleaned_words


# Returns an n-gram representation from the list of words, with max number of words joined from max_n
def get_ngram_from_list(word_list, n):
    ngrams = set()
    for j in range(0, len(word_list) - n + 1):  #all words that can be joined with consecutive ones
        ngram_word = ""
        for k in range(0, n): # join i words together to create 1,2,3 gram
            ngram_word += word_list[j+k] + "-"
        ngram_word = ngram_word[:-1]  # Remove last "-" at end of word
        ngrams.add(ngram_word)  # Removes duplicates
    return ngrams


# # Return a set of all the all the ngrams of size n from the directory
# def ngram_from_directory(directory, n):
#     file_list = os.listdir(directory)
#     ngram_set = set()
#     for filename in file_list:
#         filepath = directory + filename
#         # Get clean words
#         clean_words = get_cleaned_words(filepath)
#         # Get set of ngram with max length 3
#         ngram = get_ngram_from_list(clean_words, n)
#         # Update ngram_set with potential new ngrams
#         ngram_set.update(ngram)
#     return ngram_set


# Returns a dict with all the n-grams if size 1 and their occurence fro mthe directory
def get_ngram_dict_from_directory(directoryname, n):
    # Dict to hold words and statistics
    statistic_dict = {}
    # Get all file names in directory
    file_list = os.listdir(directoryname)
    total_files = len(file_list)
    i = 0
    for filename in file_list:
        file_to_process = directoryname + filename
        clean_words = get_cleaned_words(file_to_process)
        ngrams_for_file = get_ngram_from_list(clean_words, n)

        # Add occurence of ngram to statistic_dict
        for ngram in ngrams_for_file:
            if ngram in statistic_dict:
                statistic_dict[ngram] += 1  # Incrementation of occurences
            else:
                statistic_dict[ngram] = 1  # Initialization of occurences
        i += 1
        if i % 1000 == 0:
            print("get_ngram_from_directory_progess: " + str(i) + " : " + str(total_files))
    return statistic_dict


# Returns a dict of the union of the keys from the two input dicts, and their values summed
def get_joined_dict(dict1, dict2):
    # Create a dict with all words and their total occurence
    total_ngram_dict = {}
    # Create a set with all words in both pos and neg dict
    total_word_set = set(dict1.keys())
    total_word_set.update(dict2.keys())
    for word in total_word_set:
        word_in_set1 = word in dict1
        word_in_set2 = word in dict2
        occurence = 0
        # Find total number occurences of word in pos and neg dict
        if word_in_set1:
            occurence += dict1[word]
        if word_in_set2:
            occurence += dict2[word]
        total_ngram_dict[word] = occurence
    return total_ngram_dict


# Returns the infromation value dict of subset_dict based on dict
def get_information_value_dict(subset_dict, total_dict):
    information_value_dict = {}
    for key in subset_dict:
        information_value = subset_dict[key] / total_dict[key]
        information_value_dict[key] = information_value
    return information_value_dict


def get_stop_words():
    #Get stop-words to filter out from most popular words
    stop_word_object = open("./data/stop_words.txt")
    stop_words = stop_word_object.read()
    stop_word_object.close()
    stop_words = stop_words.split()
    return stop_words

