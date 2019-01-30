import os
import csv
import pandas as pd
import collections # used to get left and right context (shift by one)
import itertools #used for zipping lists together for output

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

    # assert lists have equal length
    assert len(original_list) == len(word_list)
    assert len(hunspell_list) == len(word_list)

    # open file to write errors in
    with open("Results/" + filename, "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")  # need csv writer
        # write headers
        writer.writerow(["left context", "original word", "right context", "word correction", "hun correction"])

        for i in range(0, len(word_list)):
            if i % 50 == 0:
                print("working on csv file: {}%".format(round(i / len(word_list) * 100)))

            # create a path for all of the files
            o_path = os.path.join(original_folder, original_list[i])
            h_path = os.path.join(hunspell_folder, hunspell_list[i])
            w_path = os.path.join(word_folder, word_list[i])

            # open the files
            with open(o_path, "r", encoding="utf-8") as original_file:
                with open(h_path, "r", encoding="utf-8") as hunspell_file:
                     with open(w_path, "r", encoding="cp1252") as word_file: #old reading with encoding
                        # read the content of the files
                        o_content = original_file.read().strip()
                        h_content = hunspell_file.read().strip()
                        w_content = word_file.read().strip()

                        # split the words
                        o_words = o_content.split("\n")
                        h_words = h_content.split("\n")
                        w_words = w_content.split("\n")
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

def test_inputFromCSV(filename):
    '''
    test encoding when importing from csv
    :param filename: file to import
    '''

    with open("Results/" + filename, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            try:
                print(row[3])
            except IndexError:
                pass

def drop_duplicate_rows_from_csv(filename):
    '''
    Imports the csv file with the errors into dataframe and removes duplicate rows
    :param filename: csv file with the list of errors
    '''
    # read in the csv file containing the errors
    errorlist = pd.read_csv(filename, delimiter=",", header=0, encoding="utf-8")
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

def get_results(data, filename="Results/ResultsMany.csv"):
    '''
    creates a csv file containing the results of the manual evaluation
    :param data: Dataframe containing the manually classified words
    :param filename: file to write results in
    :return:
    '''
    manual_evaluation(data, filename) #manual eval with all words (except Match-Type 0)
    manual_Eval_without_special_cases(data, filename) #no special cases at all
    manual_Eval_onlySingleCategory(data, "Abkuerzung", filename) # only abbreviaions
    manual_Eval_onlySingleCategory(data, "Eigenname", filename) # only proper nouns
    manual_Eval_onlySingleCategory(data, "Englisch", filename) #only English
    manual_Eval_onlySingleCategory(data, "Oesterreichisch", filename) # only Austrian

    # remove duplicate lines (empty ones)
    results_many = pd.read_csv(filename, delimiter=",", header=None,
                               encoding="utf-8")  # import from csv
    results_many = results_many.drop_duplicates(keep="first")  # drop duplicate rows
    # write back to csv
    results_many.to_csv(filename, index=False, encoding="utf-8")
    print("Writing results of Manual Evaluation into {} - Done!".format(filename))


def manual_evaluation(data, filename):
    '''
    gets the precision and % correct values from the data
    writes it into file
    :param data: dataframe with the words
    :return:
    '''
    # remove cols with MatchType 0 and URLs/Email entries
    # classified as n.A. in manual eval
    data = data[data["Match-Type"] != 0]
    data = data[data["URL/Email"] != 1.0]

    hun_P_correct, _ = get_CorrectWords(data, "hunspell")
    word_P_correct, _ = get_CorrectWords(data, "word")
    hun_P_false, _ = get_FalseWords(data, "hunspell")
    word_P_false, _ = get_FalseWords(data, "word")

    hun_precision = calculate_precision(data, "hunspell")
    word_precision = calculate_precision(data, "word")
    # assert that all entries have a MatchType
    # -1 because header is counted in the full index
    assert len(data.index)-1  == (len(data[data["Match-Type"] == 1.0].index)
                               + len(data[data["Match-Type"] == 2.0].index)
                               + len(data[data["Match-Type"] == 3.0].index)
                               + len(data[data["Match-Type"] == 4.0].index)
                               + len(data[data["Match-Type"] == 5.0].index)
                               )


    # make sure that false and correct add up to 100%
    assert (round(word_P_false + word_P_correct, 0)) == 100.0
    assert (round(hun_P_false + hun_P_correct, 0)) == 100.0

    result_dict = {
        "Number of entries": len(data.index),
        "Word": {
            "Word % correct" :word_P_correct,
            "Word % false": word_P_false,
            "Word precision": word_precision,
            },
        "Hunspell": {
            "Hunspell % correct" :hun_P_correct,
            "Hunspell % false": hun_P_false,
            "Hunspell precision": hun_precision,
            }
    }

    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in result_dict.items():
            # get nested dict output
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    writer.writerow([nested_key, nested_value])
            else:
                writer.writerow([key, value])

def manual_Eval_without_special_cases(data, filename):
    '''
    Removes all special categories like abbreviations and proper names from data
    :param data: dataframe with all entries
    '''
    input_data = data

    data = data[data["Match-Type"] != 0]
    data = data[data["URL/Email"] != 1.0]
    data = data[data["Abkuerzung"] != 1.0]
    data = data[data["Eigenname"] != 1.0]
    data = data[data["Englisch"] != 1.0]
    data = data[data["Oesterreichisch"] != 1.0]
    assert len(data.index) < len(input_data.index)

    hun_P_correct, _ = get_CorrectWords(data, "hunspell")
    word_P_correct, _ = get_CorrectWords(data, "word")
    hun_P_false, _ = get_FalseWords(data, "hunspell")
    word_P_false, _ = get_FalseWords(data, "word")

    hun_precision = calculate_precision(data, "hunspell")
    word_precision = calculate_precision(data, "word")

    result_dict = {
        "Number of entries noSpecialCases": len(data.index),
        "Word": {
            "Word % correct noSpecialCases": word_P_correct,
            "Word % false noSpecialCases": word_P_false,
            "Word precision noSpecialCases": word_precision,
        },
        "Hunspell": {
            "Hunspell % correct noSpecialCases": hun_P_correct,
            "Hunspell % false noSpecialCases": hun_P_false,
            "Hunspell precision noSpecialCases": hun_precision,
        }
    }

    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in result_dict.items():
            # get nested dict output
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    writer.writerow([nested_key, nested_value])
            else:
                writer.writerow([key, value])

def manual_Eval_onlySingleCategory(data, category, filename):
    '''
    calculates %correct and precision only for one word-category like abbreviation etc.
    :param data: dataframe containing all rows
    :param category: Column-name for which the metrics should be calculated
    :param filename: output filename
    '''
    # filter ONLY the words belonging to category
    data = data[data[category] == 1.0]

    # calculate metrics
    hun_P_correct, _ = get_CorrectWords(data, "hunspell")
    word_P_correct, _ = get_CorrectWords(data, "word")
    hun_P_false, _ = get_FalseWords(data, "hunspell")
    word_P_false, _ = get_FalseWords(data, "word")

    hun_precision = calculate_precision(data, "hunspell")
    word_precision = calculate_precision(data, "word")

    # make result dict and format only$Category (onlyAbkuerzungen ...)
    result_dict = {
        "Number of entries only{}".format(category): len(data.index),
        "Word": {
            "Word % correct only{}".format(category): word_P_correct,
            "Word % false only{}".format(category): word_P_false,
            "Word precision only{}".format(category): word_precision,
        },
        "Hunspell": {
            "Hunspell % correct only{}".format(category): hun_P_correct,
            "Hunspell % false only{}".format(category): hun_P_false,
            "Hunspell precision only{}".format(category): hun_precision,
        }
    }

    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in result_dict.items():
            # get nested dict output
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    writer.writerow([nested_key, nested_value])
            else:
                writer.writerow([key, value])


def get_CorrectWords(data, checker):
    '''
    Calculate the % of correct edits done by the checker
    :param data: dataset
    :param checker: checker to evaluate
    :return: % correct, rounded to two digits and df of correct entries
    '''

    # get entries that are corrected right by both checker
    correct_entries = data[data['Match-Type'] == 1.0]
    all_data_size = len(data.index)

    if checker.lower() == "word":
        only_word = data[data["Match-Type"] == 2.0]  # append word_correct rows
        correct_entries = correct_entries.append(only_word)
    elif checker.lower() == "hun" or checker.lower() == "hunspell":
        correct_entries = correct_entries.append(data[data["Match-Type"] == 3.0])  # append hun_correct rows
    else:
        print("please enter a valid checker name to get percent correct")

    # calculate %
    correct_entries_size = len(correct_entries.index)
    percent_correct = (correct_entries_size / all_data_size) * 100
    return round(percent_correct, 2), correct_entries

def get_FalseWords(data, checker):
    '''
    Calculate the % of false matches
    :param data: dataset
    :param checker: checker to evaluate
    :return: % false and df of false entries
    '''
    # get all entries that are false (both or different)
    false_entries = data[data["Match-Type"] == 4.0]
    false_entries = false_entries.append(data[data["Match-Type"] == 5.0])

    all_data_size = len(data.index)

    if checker.lower() == "word":
        false_entries = false_entries.append(data[data["Match-Type"] == 3.0]) #append all hun_correct

    elif checker.lower() == "hun" or checker.lower() == "hunspell":
        false_entries = false_entries.append(data[data["Match-Type"] == 2.0]) #append all word_correct
    else:
        print("please enter a valid checker name to get percent false")

    false_entries_size = len(false_entries.index)
    percent_false = (false_entries_size / all_data_size) * 100


    return round(percent_false, 2), false_entries


def calculate_precision(data, checker):
    '''
    calculates the precision of the checker
    :param data: df of words
    :param checker: hun or word
    :return: value, rounded to 2 digits
    '''
    true_Pos = get_truePos(data, checker)
    false_Pos = get_falsePos(data, checker)

    precision = len(true_Pos.index) / (len(true_Pos.index) + len(false_Pos.index))
    return round(precision, 2)


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
    _, true_pos = get_CorrectWords(data, checker)

    # filter out unchanged words (those would be true negatives)
    true_pos = true_pos[true_pos["Error"] == 1.0]
    return true_pos


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
    _, false_pos = get_FalseWords(data, checker)
    false_pos = false_pos[false_pos["Error"] != 1.0]
    return false_pos

