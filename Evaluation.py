import os
from enum import Enum
import pandas as pd
import numpy as np
import MatchType
import Levenshtein

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

        data = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, 10)),
                            columns=["Comment-ID", "Word-ID", "Match-Type", "Original", "Gold", "Hunspell", "Word", "lev_hg", "lev_wg", "lev_hw"])

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
                                elif g_words[j] != w_words[j]:
                                    # only hun correct
                                    type = MatchType.MatchType(1)
                                    lev_hg = Levenshtein.distance(g_words[i], h_words[i])
                                    lev_wg = Levenshtein.distance(g_words[i], w_words[i])
                                    lev_hw = Levenshtein.distance(g_words[i], h_words[i])
                            elif g_words[j] == w_words[j]:
                                # only word correct
                                type = MatchType.MatchType(2)
                                lev_hg = Levenshtein.distance(g_words[j], h_words[j])
                                lev_wg = Levenshtein.distance(g_words[j], w_words[j])
                                lev_hw = Levenshtein.distance(g_words[j], h_words[j])
                            else:
                                if w_words[j] == h_words[j]:
                                    # both false, but same
                                    type = MatchType.MatchType(3)
                                    lev_hg = Levenshtein.distance(g_words[j], h_words[j])
                                    lev_wg = Levenshtein.distance(g_words[j], w_words[j])
                                    lev_hw = Levenshtein.distance(g_words[j], h_words[j])
                                else:
                                    # both false but different
                                    type = MatchType.MatchType(4)
                                    lev_hg = Levenshtein.distance(g_words[j], h_words[j])
                                    lev_wg = Levenshtein.distance(g_words[j], w_words[j])
                                    lev_hw = Levenshtein.distance(g_words[j], h_words[j])

                            test_dict = {"Comment-ID": i+1,
                                         "Word-ID": j,
                                         "Match-Type": type,
                                         "Original": o_words[j],
                                         "Gold": g_words[j],
                                         "Hunspell": h_words[j],
                                         "Word": w_words[j],
                                         "lev_hg": lev_hg,
                                         "lev_wg": lev_wg,
                                         "lev_hw": lev_hw }

                            one_word = pd.Series(test_dict)
                            data.loc[j] = one_word

    return data