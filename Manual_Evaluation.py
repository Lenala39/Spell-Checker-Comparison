import os
import Levenshtein
import csv
import pandas as pd
import collections
import itertools
import io

def corrections_toCSV(original_folder, hunspell_folder, word_folder, filename):
    '''
    writes every word that was corrected by at least one of the checkers into csv
    left context, original word, right context, word correction, hun correction
    :param original_folder: folder with the original files
    :param hunspell_folder: folder with the files processed by hunspell
    :param word_folder: folder with the files processed by word
    '''


    # make lists for directory contents
    original_list = [f for f in os.listdir(original_folder) if os.path.isfile(os.path.join(original_folder, f))]
    hunspell_list = [f for f in os.listdir(hunspell_folder) if os.path.isfile(os.path.join(hunspell_folder, f))]
    word_list = [f for f in os.listdir(word_folder) if os.path.isfile(os.path.join(word_folder, f))]
    # sort so the files with the same index will be compared
    original_list.sort()
    hunspell_list.sort()
    word_list.sort()

    # open file to write errors in
    with open("Results/" + filename, "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")  # need csv writer
        # write headers
        writer.writerow(["left context", "original word", "right context", "word correction", "hun correction"])

        for i in range(0, len(word_list)):
            # create a path for all of the files
            o_path = os.path.join(original_folder, original_list[i])
            h_path = os.path.join(hunspell_folder, hunspell_list[i])
            w_path = os.path.join(word_folder, word_list[i])

            # open the files
            with open(o_path, "r", encoding="utf-8") as original_file:
                with open(h_path, "r", encoding="utf-8") as hunspell_file:
                    with io.open(w_path, "r", encoding="utf-8") as word_file:
                        # read the content of the files
                        o_content = original_file.read().strip()
                        h_content = hunspell_file.read().strip()
                        w_content = word_file.read().strip()

                        # split the words
                        o_words = o_content.split(" ")
                        h_words = h_content.split(" ")
                        w_words = w_content.split(" ")

                        # rotate the original words list by 1/-1 to get the word before/after the original
                        left_context = collections.deque(o_words)
                        left_context.rotate(-1)
                        left_context = list(left_context)
                        left_context[len(o_words)-1] = "-" # would otherwise be first

                        right_context = collections.deque(o_words)
                        right_context.rotate(1)
                        right_context = list(right_context)
                        right_context[0] = "-" # would otherwise be the last word

                        # make list of lists: each row in csv is a list
                        # take each element from the lists left_context, o_words, right_context, w_words, h_words:
                        # zip them (take longest and fill other fields with ~)
                        # make output list if o != w OR o != h (have been edited)
                        output_list = [[l, o, r, w, h] for l, o, r, w, h in
                                        itertools.zip_longest(left_context, o_words, right_context, w_words, h_words,
                                                              fillvalue="~") if (o != w or o != h)]
                        # csv writer makes each list in the list a row
                        writer.writerows(output_list)
    print("Writing all edited words into {} for manual inspection - Done!".format("Results/" + filename))


def drop_duplicate_rows_from_csv(filename):
    '''
    Imports the csv file with the errors into dataframe and removes duplicate rows
    :param filename: csv file with the list of errors
    '''
    # read in the csv file containing the errors
    errorlist = pd.read_csv(filename, delimiter=",", header=0, encoding="cp1252")
    old_length = len(errorlist.index)
    # drop duplicates disregarding left and right context
    errorlist = errorlist.drop_duplicates(subset=["original word","word correction","hun correction"], keep="first")
    new_length = len(errorlist.index)
    # build new filename
    new_filename = filename.split(".")[0] + "_noDuplicates.csv"
    # write to (new) csv file
    errorlist.to_csv(new_filename, sep=",", index=False, encoding="utf-8", header=True)
    print("Removed {} duplicate lines - Done.".format(old_length - new_length))
    #print("Dropping all duplicate lines in {} and storing result in {} - Done!".format(filename, new_filename))

# -------------------------OLD and UNUSED--------------------------------------

def corrections_toCSV_OLD(original_folder, hunspell_folder, word_folder, filename):
    '''
    writes every word that was corrected by at least one of the checkers into csv
    left context, original word, right context, word correction, hun correction
    :param original_folder: folder with the original files
    :param hunspell_folder: folder with the files processed by hunspell
    :param word_folder: folder with the files processed by word
    '''

    # make lists for directory contents
    original_list = [f for f in os.listdir(original_folder) if os.path.isfile(os.path.join(original_folder, f))]
    hunspell_list = [f for f in os.listdir(hunspell_folder) if os.path.isfile(os.path.join(hunspell_folder, f))]
    word_list = [f for f in os.listdir(word_folder) if os.path.isfile(os.path.join(word_folder, f))]
    original_list.sort()
    hunspell_list.sort()
    word_list.sort()

    # open file to write errors in

    with open("Results/" + filename, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")  # need csv writer
        # write headers
        writer.writerow(["left context", "original word", "right context", "word correction", "hun correction"])

        for i in range(0, len(word_list)):
            if i%50 == 0:
                print("Processing: {}%".format(i / len(word_list) * 100))
            # create a path for all of the files
            o_path = os.path.join(original_folder, original_list[i])
            h_path = os.path.join(hunspell_folder, hunspell_list[i])
            w_path = os.path.join(word_folder, word_list[i])

            # open the files
            with open(o_path, "r", encoding="utf-8") as original_file:
                with open(h_path, "r", encoding="utf-8") as hunspell_file:
                    with open(w_path, "r", encoding="latin-1") as word_file:
                        # read the content of the files
                        o_content = original_file.read().strip()
                        h_content = hunspell_file.read().strip()
                        w_content = word_file.read().strip()

                        # split the words
                        o_words = o_content.split(" ")
                        h_words = h_content.split(" ")
                        w_words = w_content.split(" ")

                        parser_list = [o_words, w_words, h_words]
                        index = min([len(f) for f in parser_list])
                        # for every word in the files/wordlists
                        for j in range(0, index):
                            # if either word or hunspell changed the word (lev != 0)
                            if ((Levenshtein.distance(o_words[j], h_words[j]) != 0) or (
                                    Levenshtein.distance(o_words[j], w_words[j]) != 0)):
                                # try to access word with indices
                                try:
                                    writer.writerow(
                                        [o_words[j - 1], o_words[j], o_words[j + 1], w_words[j], h_words[j]])
                                except IndexError as error:  # with index out of bounds, use - as spaceholder
                                    if j == 0 and index == 1:  # first word of file == last word of file
                                        writer.writerow(["-", o_words[j], "-", w_words[j],
                                                         h_words[j]])
                                    elif j == index - 1:  # last word of file
                                        writer.writerow([o_words[j - 1], o_words[j], "-", w_words[j],
                                                         h_words[j]])
                                    elif (j == 0):  # first word of file
                                        writer.writerow(["-", o_words[j], o_words[j + 1], w_words[j],
                                                         h_words[j]])

                                    else:
                                        print(error)

    print("Writing all edited words into {} for manual inspection - Done!".format("Results/" + filename))
