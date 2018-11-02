import os
from enum import Enum
import pandas as pd
import numpy as np
import MatchType
import Levenshtein
import json
def get_unchanged_and_sameChange(original_folder, hunspell_folder, word_folder):
    '''
    removes the files that have the same content (are unchanged) in all three folders
    :param original_folder: folder with the extracted comments from db
    :param hunspell_folder: files processed by hunspell
    :param word_folder: files processed by word
    :return: lists of files that are unchanged or word and hunspell made the same change
    '''

    #create lists of all files in the folders (for original need to filter out subdirs
    original_list = [f for f in os.listdir(original_folder) if os.path.isfile(os.path.join(original_folder, f))]
    hunspell_list = os.listdir(hunspell_folder)
    word_list = os.listdir(word_folder)

    # create lists to store the files to be deleted in/the deleted indices
    to_delete_unchanged = []
    to_delete_sameChange = []
    deleted_indices_unchanged = []
    deleted_indices_sameChange = []

    # iterate over all files in the respective lists
    for i in range(len(hunspell_list)):
        #create a path for all of the files
        o_path = os.path.join(original_folder, original_list[i])
        h_path = os.path.join(hunspell_folder, hunspell_list[i])
        w_path = os.path.join(word_folder, word_list[i])

        # open the files
        with open(o_path, "r") as original_file:
            with open(h_path, "r") as hunspell_file:
                with open(w_path, "r") as word_file:

                    # read the content of the files
                    o_content = original_file.read()
                    h_content = hunspell_file.read()
                    w_content = word_file.read()

                    # if the content matches for all three files
                    if o_content == h_content and h_content == w_content:
                        # append all file(paths) to the to_delete list and the current index to deleted_indeces
                        to_delete_unchanged.append(o_path)
                        to_delete_unchanged.append(h_path)
                        to_delete_unchanged.append(w_path)
                        deleted_indices_unchanged.append(i)
                    elif h_content == w_content and o_content != h_content:
                        to_delete_sameChange.append(o_path)
                        to_delete_sameChange.append(h_path)
                        to_delete_sameChange.append(w_path)
                        deleted_indices_sameChange.append(i)

    # write a file with the indices of the files that were deleted
    # a) because they were unchanged
    with open("Results/unchanged.txt", "a", encoding="utf-8") as unchanged_indices:
        for elem in deleted_indices_unchanged:
            unchanged_indices.write(elem)

    # b) because they contained the same change
    with open("Results/sameChange.txt", "a", encoding="utf-8") as sameChange_indices:
        for elem in deleted_indices_sameChange:
            sameChange_indices.write(elem)

    return to_delete_unchanged, to_delete_sameChange


def delete_files(path_list, status="none"):
    # iterate over all file(paths) in to_delete and delete the files
    if len(path_list) is 0:
        print("no files to delete because of: ", status)
    else:
        print("deleted because: ", status)
        for path in path_list:
            print("deleting: ", path)
            os.unlink(path)


def compare_files(original_folder, hunspell_folder, word_folder, gold_folder):
    # create lists of all files in the folders (for original need to filter out subdirs
    original_list = [f for f in os.listdir(original_folder) if os.path.isfile(os.path.join(original_folder, f))]
    hunspell_list = os.listdir(hunspell_folder)
    word_list = os.listdir(word_folder)
    gold_list = os.listdir(gold_folder)

    for i in range(0, 1):
    #for i in range(len(hunspell_list)):
        #create a path for all of the files
        o_path = os.path.join(original_folder, original_list[i])
        h_path = os.path.join(hunspell_folder, hunspell_list[i])
        w_path = os.path.join(word_folder, word_list[i])
        g_path = os.path.join(gold_folder, gold_list[i])

        data = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, 11)),
                            columns=["Comment-ID", "Word-ID", "Match-Type", "Original", "Gold", "Hunspell", "Word", "lev_hg", "lev_wg", "lev_hw", "lev_og"])

        # open the files
        with open(o_path, "r") as original_file:
            with open(h_path, "r") as hunspell_file:
                with open(w_path, "r") as word_file:
                    with open(g_path, "r") as gold_file:

                        # read the content of the files
                        o_content = original_file.read()
                        h_content = hunspell_file.read()
                        w_content = word_file.read()
                        g_content = gold_file.read()

                        o_words = o_content.split(" ")
                        h_words = h_content.split(" ")
                        w_words = w_content.split(" ")
                        g_words = g_content.split(" ")

                        type = ""
                        lev_hg = 0
                        lev_wg = 0
                        lev_hw = 0
                        for j in range(len(h_words)):
                            #id = str(i+1) + "." + str(j)
                            if g_words[j] == h_words[j]:
                                if g_words[j] == w_words[j]:
                                    # both correct
                                    type = MatchType.MatchType(0)
                                    # all Levenshteins are 0
                                    lev_hg = 0
                                    lev_wg = 0
                                    lev_hw = 0
                                    lev_og = Levenshtein.distance(g_words[j], o_words[j])
                                elif g_words[j] != w_words[j]:
                                    # only hun correct
                                    type = MatchType.MatchType(1)
                                    lev_hg = Levenshtein.distance(g_words[j], h_words[j])
                                    lev_wg = Levenshtein.distance(g_words[j], w_words[j])
                                    lev_hw = Levenshtein.distance(g_words[j], h_words[j])
                                    lev_og = Levenshtein.distance(g_words[j], o_words[j])
                            elif g_words[j] == w_words[j]:
                                # only word correct
                                type = MatchType.MatchType(2)
                                lev_hg = Levenshtein.distance(g_words[j], h_words[j])
                                lev_wg = Levenshtein.distance(g_words[j], w_words[j])
                                lev_hw = Levenshtein.distance(g_words[j], h_words[j])
                                lev_og = Levenshtein.distance(g_words[i], o_words[i])
                            else:
                                if w_words[j] == h_words[j]:
                                    # both false, but same
                                    type = MatchType.MatchType(3)
                                    lev_hg = Levenshtein.distance(g_words[j], h_words[j])
                                    lev_wg = Levenshtein.distance(g_words[j], w_words[j])
                                    lev_hw = Levenshtein.distance(g_words[j], h_words[j])
                                    lev_og = Levenshtein.distance(g_words[i], o_words[i])
                                else:
                                    # both false but different
                                    type = MatchType.MatchType(4)
                                    lev_hg = Levenshtein.distance(g_words[j], h_words[j])
                                    lev_wg = Levenshtein.distance(g_words[j], w_words[j])
                                    lev_hw = Levenshtein.distance(g_words[j], h_words[j])
                                    lev_og = Levenshtein.distance(g_words[i], o_words[i])

                            test_dict = {"Comment-ID": i+1,
                                         "Word-ID": j,
                                         "Match-Type": type.value,
                                         "Original": o_words[j],
                                         "Gold": g_words[j],
                                         "Hunspell": h_words[j],
                                         "Word": w_words[j],
                                         "lev_hg": lev_hg,
                                         "lev_wg": lev_wg,
                                         "lev_hw": lev_hw,
                                         "lev_og": lev_og}

                            one_word = pd.Series(test_dict)
                            data.loc[j] = one_word

    return data

def get_truePos(data, checker):
    '''
    returns a dataframe containing all true positive corrections
    -> correct
    -> + correct of checker to evaluate
    -> + original != gold (a change has been done)
    :param data: dataframe containing the evaluation of the checkers
    :param checker: which checker to get true positives for
    :return: dataframe with the true positives
    '''

    #get all correctly checked words
    true_pos = get_correctWords(data, checker)

    # filter out unchanged words (those would be true negatives)
    true_pos = true_pos[true_pos["lev_og"] != 0]
    return true_pos

def get_trueNeg(data, checker):
    '''
    returns a dataframe containing all true negative corrections
    -> correct
    -> + correct of checker to evaluate
    -> + original = gold (no change has been done)
    :param data: dataframe containing the evaluation of the checkers
    :param checker: which checker to get true negatives for
    :return: dataframe with the true negatives
    '''

    #get all correctly checked words
    true_neg = get_correctWords(data, checker)
    # filter out changed words (those would be true positives)
    true_neg = true_neg[true_neg["lev_og"] == 0]
    return true_neg


def get_falsePos(data, checker):
    '''
    returns false positives for the specified checker
    -> False
    -> + the other checker correct (implies not both false/true but the checker has to be false)
    -> + orginal = gold (should not have been changed)
    :param data: whole dataframe with evaluation data
    :param checker: checker to evaluate
    :return: dataframe of false Positives
    '''
    false_pos = get_falseWords(data, checker)
    false_pos = false_pos[false_pos["lev_og"] == 0]
    return false_pos

def get_falseNeg(data, checker):
    '''
    returns false negatives for the specified checker
    -> False
    -> + the other checker correct (implies not both false/true but the checker has to be false)
    -> + orginal != gold (should have been changed, but wasn't)
    :param data: whole dataframe with evaluation data
    :param checker: checker to evaluate
    :return: dataframe of false Positives
    '''
    false_neg = get_falseWords(data, checker)
    false_neg = false_neg[false_neg["lev_og"] != 0]
    return false_neg

def get_falseWords(data, checker):
    # get all words that are false
    false_data = data[data["Match-Type"] == 3]     # false but the same
    false_data.append(data[data["Match-Type"] == 4])    # false but different

    #false words
    if checker == "hun":
        false_data.append(data[data["Match-Type"] == 2]) # append only word correct (implies hun is false)
    elif checker == "word":
        false_data.append(data[data["Match-Type"] == 1]) # append only hun correct (implies word is false)
    else:
        print("Please enter a valid checker option to receive true positives")
        return
    return false_data


def get_correctWords(data, checker):
    '''
    return all words that are correct(ly edited) from the checker
    :param data: whole set of words
    :param checker: checker that should be evaluated
    :return: data with all correct(ly changed) words
    '''

    # correct data
    correctData = data[data["Match-Type"] == 0]
    # append either the only hun/word correct to all correct ones
    if checker == "hun":
        correctData.append(data[data["Match-Type"] == 1])
    elif checker == "word":
        correctData.append(data[data["Match-Type"] == 2])
    else:
        print("Please enter a valid checker option to receive true positives")
        return
    return correctData

def calculate_recall(data, checker):
    true_pos = get_truePos(data, checker)
    false_pos = get_falsePos(data, checker)
    try:
        recall = len(true_pos.index) / (len(true_pos.index) + len(false_pos.index))
    except ZeroDivisionError:
        recall = 0
    return recall

def calculate_precision(data, checker):
    true_pos = get_truePos(data, checker)
    false_neg = get_falseNeg(data, checker)

    try:
        precision = len(true_pos.index) / (len(true_pos.index) + len(false_neg.index))
    except ZeroDivisionError:
        precision = 0
    return precision

def get_percentCorrect(data, checker):
    correct_entries = data[data["Match-Type"] == 0]
    all_data_size = len(data.index)
    if checker == "word":
        only_word = data[data["Match-Type"] == 2]
        correct_entries = correct_entries.append(only_word)
    elif checker == "hun":
        correct_entries = correct_entries.append(data[data["Match-Type"] == 1])
    else:
        print("please enter a valid checker name to get percent correct")

    correct_entries_size = len(correct_entries.index)
    percent_correct = (correct_entries_size / all_data_size) * 100
    return round(percent_correct,2)

def get_percentFalse(data, checker):
    false_entries = data[data["Match-Type"] == 3]
    false_entries.append(data[data["Match-Type"] == 4])
    all_data_size = len(data.index)
    if checker == "word":
        false_entries = false_entries.append(data[data["Match-Type"] == 1])
    elif checker == "hun":
        false_entries = false_entries.append(data[data["Match-Type"] == 2])
    else:
        print("please enter a valid checker name to get percent false")

    false_entries_size = len(false_entries.index)
    percent_false = (false_entries_size / all_data_size) * 100
    return round(percent_false, 2)

def calculate_FScore(data, checker):
    # https://en.wikipedia.org/wiki/Precision_and_recall
    recall = calculate_recall(data, checker)
    precision = calculate_precision(data, checker)
    try:
        f_score = 2 * ((precision * recall) / (precision + recall))
    except ZeroDivisionError:
        f_score = 0
    return round(f_score,2)

def calculate_Accuracy(data, checker):
    true_pos = get_truePos(data, checker)
    true_neg = get_trueNeg(data, checker)

    all_size = len(data.index)
    true_pos_size = len(true_pos.index)
    true_neg_size = len(true_neg.index)

    accuracy = (true_pos_size + true_neg_size) / all_size
    return round(accuracy,2)


def calculate_Specificity(data, checker):
    # https://en.wikipedia.org/wiki/Sensitivity_and_specificity#Specificity
    # Specificity relates to the test's ability to correctly reject healthy patients without a condition
    # -> correctly reject words that are spelled right
    # true_neg / true_neg + false_pos

    true_neg = get_trueNeg(data, checker)
    false_pos = get_falsePos(data, checker)
    try:
        specificity = len(true_neg.index) / (len(true_neg.index) + len(false_pos.index))
    except ZeroDivisionError:
        specificity = 0
    return round(specificity,2)

def write_evalFile(data):
    word_percentCorrect = get_percentCorrect(data, "word")
    hun_percentCorrect = get_percentCorrect(data, "hun")

    word_percentFalse = get_percentFalse(data, "word")
    hun_percentFalse = get_percentFalse(data, "hun")

    word_precision = calculate_precision(data, "word")
    hun_precision = calculate_precision(data, "hun")

    word_recall = calculate_recall(data, "word")
    hun_recall = calculate_recall(data, "hun")

    word_fscore = calculate_FScore(data, "word")
    hun_fscore = calculate_FScore(data, "hun")

    word_accuracy = calculate_Accuracy(data, "word")
    hun_accuracy = calculate_Accuracy(data, "hun")

    word_specificity = calculate_Specificity(data, "word")
    hun_specificity = calculate_Specificity(data, "hun")

    output_dict = {"Word_Percent_correct" : word_percentCorrect,
                   "Hun_Percent_correct": hun_percentCorrect,
                   "Word_Percent_false": word_percentFalse,
                   "Hun_Percent_false": hun_percentFalse,
                   "Word_Precision": word_precision,
                   "Hun_Precision": hun_precision,
                   "Word_Recall": word_recall,
                   "Hun_Recall": hun_recall,
                   "Word_Fscore": word_fscore,
                   "Hun_Fscore": hun_fscore,
                   "Word_accuracy": word_accuracy,
                   "Hun_accuracy": hun_accuracy,
                   "Word_specificity": word_specificity,
                   "Hun_specificity": hun_specificity,
                   }
    with open("results.txt", "w") as file:
        file.write(json.dumps(output_dict,  indent=4))
