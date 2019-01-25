import re #regex used for substituting double space with single one
import os #used for getting list of files in dir
import filecmp #used to compare files

# ---------------------- general preprocessing -----------------------------
def remove_special_chars(data, folder):
    '''
    removes special chars from comment and returns list of only comments
    :param data: list of data tuples with comments
    :return: list of comments (no metadata)
    '''
    # iterate over data
    for i in range(len(data)):
        text = data[i][7] #for each comment in data, only 7 contains text body
        if text is not None: #text non-empty
            text = replace_chars(text) #function to replace special characters
            text = add_crlf(text) #get format of one word per line
            write_file(text, data[i][0], folder) # write each file
    print("Removing special characters - Done!")


def replace_chars(text):
    '''
    replaces all special characters not suitable when spell checking from string
    param: text string
    returns: text string with removed chars
    '''
    text = text.replace("=\r\n", "")
    text = text.replace("\r", " ")
    text = text.replace("\n", " ")
    text = text.replace("(", " ").replace(")", " ")
    text = text.replace(",", " ")
    text = text.replace("!", " ")
    text = text.replace("?", " ")
    text = text.replace(".", " ")
    text = text.replace(";", " ")
    text = text.replace(":", " ")
    text = text.replace("€", " ")
    text = text.replace("\"", " ")
    text = text.replace('"', " ")

    text = text.replace(u'\u201e', "") #double low quotation marks
    text = text.replace(u"\u201C", "") #left double quotation marks
    text = text.replace(u"\u2013", "") #dash
    text = text.replace(u"\u2026", "") #... (horizontal ellipsis)
    text = text.replace(u"\u2019", "") # right single quotation mark

    text = re.sub(r" {2,}", " ", text) #replace more than one whitespace with a single one
    text = text.strip() # remove whitespaces from the beginning of the comment

    return text

def add_crlf(text):
    '''
    takes text-string and substitutes each space with a CRLF
    :param text: string
    :return: string with space substituted by \n
    '''
    single_words = text.split(" ") # split string into words at space
    new_text = '\n'.join(single_words) #re-join using \n
    return new_text

def write_file(comment, id, folder):
    '''
    writes a file with the name id to the folder
    :param comment: content to write in the file
    :param id: comment-id and file name
    :param folder: folder to write the file into
    '''
    # format the filename to write with the dir and the id
    filename = folder + "/{}_original.txt".format(id)
    # open the file and write it
    with open(filename, "w", encoding="utf-8") as file:
        file.write(comment)


#-------------------------- pandas preprocessing------------------------

def get_unchanged_sameChange(original_folder, hunspell_folder, word_folder, gold_folder):
    '''
    gets all files that are unchanged by the checkers or contain the same change
    :param original_folder: folder of original files
    :param hunspell_folder: folder of hunspell files
    :param word_folder: folder of word files
    :param gold_folder: folder of gold files
    :return: two lists: one with file-index and one with file names to be deleted
    '''
    # create lists of all files in the folders (for original need to filter out subdirs
    original_list = [f for f in os.listdir(original_folder) if os.path.isfile(os.path.join(original_folder, f))]
    hunspell_list = os.listdir(hunspell_folder)
    word_list = os.listdir(word_folder)
    gold_list = os.listdir(gold_folder)

    # create lists to store the files to be deleted in/the deleted indices
    to_delete_unchanged = [] # files
    to_delete_sameChange = []
    deleted_indices_unchanged = [] # index numbers of files
    deleted_indices_sameChange = []

    # iterate over all files in the respective lists
    for i in range(len(hunspell_list)):
        # create a path for all of the files
        o_path = os.path.join(original_folder, original_list[i])
        h_path = os.path.join(hunspell_folder, hunspell_list[i])
        w_path = os.path.join(word_folder, word_list[i])
        g_path = os.path.join(gold_folder, gold_list[i])

        # compare the files using filecmp module
        # if original, hunspell, word and gold are identical (no change at all)
        if ((filecmp.cmp(o_path, h_path, shallow=False) == True)
                and (filecmp.cmp(o_path, w_path, shallow=False) == True)
                and filecmp.cmp(o_path, g_path, shallow=False) == True):
            to_delete_unchanged.append(o_path)
            to_delete_unchanged.append(h_path)
            to_delete_unchanged.append(w_path)
            to_delete_unchanged.append(g_path)
            file_index = original_list[i].split(".")[0]
            deleted_indices_sameChange.append(file_index)
            print("Found unchanged file: ", file_index)

        # if files are both changed but exactly the same way also delete them (!= original but word == hun)
        elif ((filecmp.cmp(o_path, h_path, shallow=False) == False)
              and (filecmp.cmp(h_path, w_path, shallow=False) == True)):
            to_delete_sameChange.append(o_path)
            to_delete_sameChange.append(h_path)
            to_delete_sameChange.append(w_path)
            to_delete_sameChange.append(g_path)
            file_index = original_list[i].split(".")[0]
            deleted_indices_sameChange.append(file_index)
            print("Found file w/ same change: ", file_index)

        # write a file with the indices of the files that were deleted
        # a) because they were unchanged
        with open("Results/unchanged.txt", "a", encoding="utf-8") as unchanged_indices:
            for elem in deleted_indices_unchanged:
                unchanged_indices.write("\n")
                unchanged_indices.write(elem)

        # b) because they contained the same change
        with open("Results/sameChange.txt", "a", encoding="utf-8") as sameChange_indices:
            for elem in deleted_indices_sameChange:
                sameChange_indices.write("\n")
                sameChange_indices.write(str(elem))


        return to_delete_unchanged, to_delete_sameChange
