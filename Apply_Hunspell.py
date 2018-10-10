from hunspell import Hunspell
from copy import deepcopy
import platform
import os
import re

def make_checker():
    '''
    creates a checker depending on the system running
    :return: Hunspell object h
    '''
    if platform.system() == 'Windows':
        h = Hunspell('de-DE', hunspell_data_dir="C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\dictionaries")
    else:
        h = Hunspell('de-DE', hunspell_data_dir="/home/lena/Desktop/million_post_corpus/dictionaries")
    return h

def correct_word(word, h):
    '''
    corrects a word using hunspell
    :param word: word to be checked
    :param h: spell checker
    :return: corrected word (if false/suggestions available
    '''

    corrected = ""
    if not h.spell(word): #if spell check returns False
        suggestions = h.suggest(word) # suggest correct words

        if suggestions: # if there are suggestions
            best = suggestions[0]
            corrected = best # make word to be the first suggestion
        else:
            corrected = word # if no suggestions, keep wrong word
    else:
        corrected = word # if word is correct, simply return that

    return corrected


def write_file(comment, id):
    '''
    Writes a string into a file that uses id for its name
    :param comment: string to write
    :param id: file name
    '''
    # @Todo: write metadata?
    filename = "Files/{}_hunspell.txt".format(id)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(comment)

def apply_hunspell_on_dir(directory):
    '''
    Applies hunspell on all files in a directory that are named like XX.txt
    :param directory: directory of the files
    '''

    file_list = os.listdir(directory) #make list of all files in the directory
    h = make_checker() # make checker

    # iterate over all files
    for i in range(len(file_list)):
        file_pattern = re.compile("[0-9]+.txt") # make pattern to match XX.txt files
        if re.match(file_pattern, file_list[i]): # if match
            filename = "{}/{}".format(directory, file_list[i])

            with open(filename, "r", encoding="utf-8") as file: #open the file to read
                comment = file.read() # read the content
                single_words = comment.split(" ") #split the string from the file
                for j in range(len(single_words)): # apply spell check on every word
                    single_words[j] = correct_word(single_words[j], h)

                corrected_comment = " ".join(single_words) # re-join the corrected comments
                corrected_filename = "{}/Hunspell/{}_hunspell.txt".format(directory, i+1) # make new filename
                with open(corrected_filename, "w", encoding="utf-8") as new_file: # open new file
                    new_file.write(corrected_comment) #write correction into new file

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
        single_words = data[i].split(" ") #split the text into single words
        for j in range(len(single_words)): #iterate over single words
            single_words[j] = correct_word(single_words[j], h) # correct each word
        complete_comment = " ".join(single_words)
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
        single_words = corrected_data[i][7].split(" ") # access only the comment and split at " "
        for j in range(len(single_words)):
            single_words[j] = correct_word(single_words[j], h) # correct each single word
        complete_comment = " ".join(single_words)
        corrected_data[i][7] = complete_comment # assign new corrected words to list
        write_file(complete_comment, i+1)
    return corrected_data
