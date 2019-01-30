# ----------PREPROCESSING-----------------
def remove_but_keep_meta(data):
    '''
    removes the same metacharacters as the other function but keeps metadata like author ...
    :param data: list of tuples with comments
    :return: list of comments with metadata (tuple structure kept)
    '''
    for i in range(len(data)):
        text = data[i][7]
        if text is None:
            pass
        else:
            text = replace_chars(text)

        data[i] = list(data[i])
        data[i][7] = text
        write_file(text, data[i][0])

    print("Removing special characters (keep metadata) - Done!")
    return data

def delete_files(path_list, status="none"):
    '''
    iterate over all file(paths) in to_delete and delete the files
    :param path_list: list of file paths
    :param status: why the file needed to be deleted
    '''
    with open("Deleted_Files.txt", "a") as file:
        try:
            file.write(status)
        except:
            pass
        file.write("\n")
        file.write("\n".join(path_list))
        file.write(str(len(path_list)))

    if len(path_list) is 0:
        print("no files to delete because of: ", status)
    else:
        print("deleted because: ", status)
        for path in path_list:
            print("deleting: ", path)
            os.unlink(path)
    print("Deleting unchanged files - Done!")



# ----------------------APPLY_HUNSPELL-------------------
def write_file(comment, id):
    '''
    Writes a string into a file that uses id for its name
    :param comment: string to write
    :param id: file name
    '''

    filename = "Files/{}_hunspell.txt".format(id)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(comment)

def apply_hunspell_on_list(data):
    '''
    applies hunspell spell checking on a dataset
    :param data: list of comments to be corrected
    :return: list of corrected comments
    '''
    h = make_checker() # create a checker from hunspell

    # if data is just the comments
    if isinstance(data[0], str):
        return normal_correction(data, h)

    # if data is list of lists with comments + metadata
    elif isinstance(data[0], list):
        return metadata_correction(data, h)

    return "unknown data format"


def normal_correction(data, h):
    '''
    corrects a list of comments
    :param data: list of comments
    :param h: spell checker
    :return: corrected comments as list
    '''

    corrected_comments = []
    single_words = []

    # for every comment in list of comments
    for i in range(len(data)):
        single_words = data[i].split("\n") #split the text into single words
        for j in range(len(single_words)): #iterate over single words
            single_words[j] = correct_word(single_words[j], h) # correct each word
        complete_comment = "\n".join(single_words)
        corrected_comments.append(complete_comment) # append to corrected comments
        write_file(complete_comment, i+1)
    return corrected_comments

def metadata_correction(data, h):
    '''
    corrects a list of comments, that are still in a list with their metadata
    :param data: list of lists with metadata + comments
    :param h: spellchecker
    :return: list of lists containing metadata + corrected comments
    '''

    corrected_data = deepcopy(data) # copy data as deepcopy to keep orginal
    for i in range(len(corrected_data)): # for every list in the dataset
        single_words = corrected_data[i][7].split("\n") # access only the comment and split at " "
        for j in range(len(single_words)):
            single_words[j] = correct_word(single_words[j], h) # correct each single word
        complete_comment = "\n".join(single_words)
        corrected_data[i][7] = complete_comment # assign new corrected words to list
        write_file(complete_comment, i+1)
    return corrected_data

#------- GOLD EVAL------------------
def gold_eval(data):
    only_errors = data[data["Error"] == 1]

    data_size = len(only_errors.index)

    hun_unrecognized = only_errors[only_errors["Original"] == only_errors["Hunspell"]]
    word_unrecognized = only_errors[only_errors["Original"] == only_errors["Word"]]

    hun_percent = round(len(hun_unrecognized.index) / data_size * 100,2)
    word_percent = round(len(word_unrecognized.index) / data_size * 100, 2)

    output_dict = {
        "All errors": data_size,
        "Word": {
            "# word unrecognized": len(word_unrecognized.index),
            "% word unrecognized": word_percent,
        },
        "Hunspell": {
            "# hunspell unrecognized": len(hun_unrecognized.index),
            "% hun unrecognized": hun_percent
        }
    }
    filename = 'Results/results200.csv'
    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in output_dict.items():
            # get nested dict output
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    writer.writerow([nested_key, nested_value])
            else:
                writer.writerow([key, value])
    print("Writing statistics about unfound errors into {} - Done!".format(filename))

# -------------- MANUAL EVAL -----------------
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
                        o_words = o_content.split("\n")
                        h_words = h_content.split("\n")
                        w_words = w_content.split("\n")

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


def calculate_accuracy(data, checker):
    true_pos = get_truePos(data, checker)
    true_neg = get_trueNeg(data, checker)

    accuracy = (len(true_pos.index) + len(true_neg.index)) / \
               (len(data.index))

    return round(accuracy, 2)

def calculate_specifictiy(data, checker):
    true_neg = get_trueNeg(data, checker)
    false_pos = get_truePos(data, checker)

    specificity = len(true_neg.index) / (len(true_neg.index) + len(false_pos.index))

    return round(specificity, 2)

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
    _, true_neg = get_CorrectWords(data, checker)
    # filter out changed words (those would be true positives)
    true_neg = true_neg[true_neg["Error"] != 1.0]
    return true_neg

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
    _, false_neg = get_FalseWords(data, checker)
    false_neg = false_neg[false_neg["Error"] == 1.0]
    return false_neg


