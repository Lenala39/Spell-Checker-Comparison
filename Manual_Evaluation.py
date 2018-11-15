import os
import Levenshtein
import csv
import pandas as pd

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
    hunspell_list = os.listdir(hunspell_folder)
    word_list = os.listdir(word_folder)

    # open file to write errors in

    with open("Results/" + filename, "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",") #need csv writer
        # write headers
        writer.writerow(["left context", "original word", "right context", "word correction", "hun correction"])

        for i in range(0, len(word_list)):
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

                        # split the words
                        o_words = o_content.split(" ")
                        h_words = h_content.split(" ")
                        w_words = w_content.split(" ")

                        # for every word in the files/wordlists
                        for j in range(0, len(o_words)):
                            # if either word or hunspell changed the word (lev != 0)
                            if((Levenshtein.distance(o_words[j], h_words[j]) != 0) or (Levenshtein.distance(o_words[j], w_words[j]) != 0)):
                                # try to access word with indices
                                try:
                                    writer.writerow([o_words[j-1], o_words[j], o_words[j+1], w_words[j], h_words[j]])
                                except IndexError as error: #with index out of bounds, use - as spaceholder
                                    if j == 0: # first word of file
                                        writer.writerow(["-", o_words[j], o_words[j + 1], w_words[j],
                                                         h_words[j]])
                                    elif j == len(o_words)-1: # last word of file
                                        writer.writerow([o_words[j-1], o_words[j], "-", w_words[j],
                                                         h_words[j]])
                                    else:
                                        print(error)
    print("Writing all edited words into {} for manual inspection - Done!".format("Results/" + filename))

def drop_duplicate_rows_from_csv(filename):
    '''
    Imports the csv file with the errors into dataframe and removes duplicate rows
    :param filename: csv file with the list of errors
    '''
    # read in the csv file containing the errors
    errorlist = pd.read_csv(filename, delimiter=",", header=0, encoding="utf-8")
    # drop duplicates disregarding left and right context
    errorlist = errorlist.drop_duplicates(subset=["original word","word correction","hun correction"], keep="first")
    # build new filename
    new_filename = filename.split(".")[0] + "_noDuplicates.csv"
    # write to (new) csv file
    errorlist.to_csv(new_filename, sep=",", index=False, encoding="utf-8", header=True)

    print("Dropping all duplicate lines in {} and storing result in {} - Done!".format(filename, new_filename))