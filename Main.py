import DB_access
import Preprocessing
import Apply_Hunspell
import Reduce
import Gold_Evaluation
import MatchType
import Manual_Evaluation

import pandas as pd
import hunspell
import datetime
import time

if __name__ == '__main__':
    # folder names
    original_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files"
    hunspell_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files\\Hunspell"
    word_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files\\Word"
    gold_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files\\Gold"
    file_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files"

    # --------- DATABASE ACCESS + PROCESSING-----------------------
    data = DB_access.access_corpus(6)

    # process data and remove special chars + writes comments into individual files
    Preprocessing.remove_special_chars(data, folder=file_folder)

    # ------------APPLY SPELLCHECKING---------------------------------
    Apply_Hunspell.apply_hunspell_on_dir(file_folder)
    pd.set_option('display.max_columns', 12) # set display options to show all columns

    
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
    
    
    # ------------------------EVAL WITHOUT GOLD - ONLY CSV OUTPUT FOR MANUAL PROCESSING--------------------
    Manual_Evaluation.corrections_toCSV(original_folder=original_folder, hunspell_folder=hunspell_folder,
                                        word_folder=word_folder, filename="errors_test.csv")
    
    '''
    true_pos = Gold_Evaluation.get_truePos(data, "hun")
    true_neg = Gold_Evaluation.get_trueNeg(data, "hun")
    false_pos = Gold_Evaluation.get_falsePos(data, "hun")
    false_neg = Gold_Evaluation.get_falseNeg(data, "hun")


    recall = Gold_Evaluation.calculate_recall(data, "hun")
    precision = Gold_Evaluation.calculate_precision(data, "hun")

    word_percent_correct = Gold_Evaluation.get_percentCorrect(data, "word")
    hun_percent_correct = Gold_Evaluation.get_percentCorrect(data, "hun")

    word_percent_false = Gold_Evaluation.get_percentFalse(data, "word")
    hun_percent_false = Gold_Evaluation.get_percentFalse(data, "hun")
    '''
