from hunspell import Hunspell #spell check wrapper for Hunspell
import platform #check operating system to make checker with different paths
import os # get list of files in directory
import re #regex: process only txt-files

def apply_hunspell_on_dir(directory):
    '''
    Applies hunspell on all files in a directory that are named like $X_original.txt
    :param directory: directory of the files
    '''
    print("Applying hunspell on{}".format(directory))
    file_list = os.listdir(directory) #make list of all files in the directory
    dir_size = len(file_list) #get size of directory
    h = make_checker() # make checker
    
    # iterate over all files
    for i in range(len(file_list)):
        # print occasional status update
        if i % 50 is 0:
            print("Applying Hunspell: {}% done".format(round(i/dir_size * 100, 0)) )

        file_pattern = re.compile("[0-9]+_original.txt") # make pattern to match XX.txt files
        if re.match(file_pattern, file_list[i]): # if match
            filename = "{}/{}".format(directory, file_list[i])

            with open(filename, "r", encoding="utf-8") as file: #open the file to read
                content = file.read() # read the content 
                single_words = content.split("\n") #split the string from the file
                for j in range(len(single_words)): # apply spell check on every word
                    single_words[j] = correct_word(single_words[j], h) #assign correction to word

                corrected_comment = "\n".join(single_words) # re-join the corrected comments
                file_index = file_list[i].split("_")[0] #get the id from $id_original.txt
                corrected_filename = "{}/Hunspell/{}_hunspell.txt".format(directory, file_index) # make new filename
                with open(corrected_filename, "w", encoding="utf-8") as new_file: # open new file
                    new_file.write(corrected_comment) #write correction into new file

    print("Applying Hunspell - Done!")

def make_checker():
    '''
    creates a checker depending on the system running
    :return: Hunspell object h
    '''
    if platform.system() == 'Windows':
        h = Hunspell('de_DE_frami', hunspell_data_dir="C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\dictionaries")
    else:
        h = Hunspell('de_DE_frami', hunspell_data_dir="/home/lena/Desktop/million_post_corpus/dictionaries")
    return h

def correct_word(word, h):
    '''
    corrects a single word using hunspell
    :param word: word to be checked
    :param h: spell checker
    :return: corrected word (if false/suggestions available otherwise original word)
    '''

    corrected = ""
    try:
        if not h.spell(word): #if spell check returns False
            suggestions = h.suggest(word) # suggest correct words
            if suggestions: # if there are suggestions (list is non-empty)
                best = suggestions[0]
                corrected = best # make word to be the first suggestion
            else:
                corrected = word # if no suggestions, keep wrong word
        else:
            corrected = word # if word is correct, simply return that
    except UnicodeEncodeError as Error:
        # in case of Unicode error, simply take original word
        # should not happen
        print(Error)
        corrected = word
    return corrected

