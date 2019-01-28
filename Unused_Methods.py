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

