import DB_access
import Preprocessing
import Apply_Hunspell
import Reduce
import Gold_Evaluation
import MatchType
import Manual_Evaluation
import itertools
import pandas as pd
if __name__ == '__main__':
    # folder names
    original_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Many_Files"
    hunspell_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Many_Files\\Hunspell"
    word_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Many_Files\\Word"
    gold_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Many_Files\\Gold"
    file_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Many_Files"


    # --------- DATABASE ACCESS + PROCESSING-----------------------
    data = DB_access.access_corpus(2000)

    # process data and remove special chars + writes comments into individual files
    Preprocessing.remove_special_chars(data, folder=file_folder)
 
    
    # ------------APPLY SPELLCHECKING---------------------------------
    Apply_Hunspell.apply_hunspell_on_dir(file_folder)
    pd.set_option('display.max_columns', 12) # set display options to show all columns
    '''
    
    #---------------------DELETE UNCHANGED------------------------------
    # delete the files that are unchanged or have the same change
    to_delete_un, to_delete_same = Preprocessing.get_unchanged_sameChange(original_folder=original_folder,
                                                                          hunspell_folder=hunspell_folder,
                                                                          word_folder=word_folder,
                                                                          gold_folder=gold_folder)
    Preprocessing.delete_files(to_delete_un)
    Preprocessing.delete_files(to_delete_same)

    # -------------------EVAL WITH GOLD (AUTOMATIC)-------------------------------
    # evaluate and compare the files
    data = Gold_Evaluation.compare_files(original_folder=original_folder, hunspell_folder=hunspell_folder,
                                         word_folder=word_folder, gold_folder=gold_folder)

    #------------------REDUCE DATAFRAME-------------------------------------------
    # drop duplicate rows (want unique items)
    data = data.drop_duplicates(subset=["Match-Type", "Error", "Original", "Gold", "Hunspell", "Word", "lev_hg",
                                        "lev_wg", "lev_hw", "lev_og"], keep="first", inplace=False)
    # reduce data size
    data = Reduce.reduce(data)

    # ----------------WRITE EVALUATION FILES-----------------------------------------
    #write file containing fscore, precision, recall etc
    Gold_Evaluation.write_evalFile(data)
    Gold_Evaluation.gold_eval(data)
    
    '''
    # ------------------------EVAL WITHOUT GOLD - ONLY CSV OUTPUT FOR MANUAL PROCESSING--------------------
    Manual_Evaluation.corrections_toCSV(original_folder=original_folder, hunspell_folder=hunspell_folder,
                                        word_folder=word_folder, filename="many_errors_new.csv")

    # dropping duplicate lines in csv file
    #Manual_Evaluation.drop_duplicate_rows_from_csv("Results/many_errors.csv")

