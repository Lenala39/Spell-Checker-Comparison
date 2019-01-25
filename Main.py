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
    pd.set_option('display.max_columns', 12)  # set display options to show all columns

    # folder names
    original_folder = "C:\\Users\\Lena Langholf\\Dropbox\\Spell_Checking\\Files"
    hunspell_folder = "C:\\Users\\Lena Langholf\\Dropbox\\Spell_Checking\\Files\\Hunspell"
    word_folder = "C:\\Users\\Lena Langholf\\Dropbox\\Spell_Checking\\Files\\Word"
    gold_folder = "C:\\Users\\Lena Langholf\\Dropbox\\Spell_Checking\\Files\\Gold"
    file_folder = "C:\\Users\\Lena Langholf\\Dropbox\\Spell_Checking\\Files"


    # --------- DATABASE ACCESS + PROCESSING-----------------------
    data = DB_access.access_corpus(5) #number specifies returned comments

    '''   
    # process data and remove special chars + writes comments into individual files
    Preprocessing.remove_special_chars(data, folder=file_folder)
 
    
    # ------------APPLY SPELLCHECKING---------------------------------
    Apply_Hunspell.apply_hunspell_on_dir(file_folder)
    
    
    #---------------------DELETE UNCHANGED------------------------------
    # delete the files that are unchanged or have the same change
    to_delete_un, to_delete_same = Preprocessing.get_unchanged_sameChange(original_folder=original_folder,
                                                                          hunspell_folder=hunspell_folder,
                                                                          word_folder=word_folder,
                                                                          gold_folder=gold_folder)

    
    Preprocessing.delete_files(to_delete_un, "unchanged")
    Preprocessing.delete_files(to_delete_same, "same change")
    
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
    data.to_csv("Results/200_Errors.csv", index=False, encoding="utf-8", header=True)

    
    # ----------------WRITE EVALUATION FILES-----------------------------------------
    # write file containing fscore, precision, recall etc
    data = pd.read_csv("Results/200_Errors.csv", delimiter=",",
                       header=0, encoding="utf-8")
    Gold_Evaluation.write_evalFile(data) # recall etc

    # ------------------ PROCESS EVALUATION FILE--------------------------------------

    results = pd.read_csv("Results/results200.csv", delimiter=",", header=None, encoding="utf-8")  # import from csv
    results = results.drop_duplicates(keep="first")  # drop duplicate rows
    # write back to csv
    results.to_csv("Results/results200_noDuplicates.csv", index=False, encoding="utf-8")
      
    # ------------------------EVAL WITHOUT GOLD - ONLY CSV OUTPUT FOR MANUAL PROCESSING--------------------
    Manual_Evaluation.corrections_toCSV(original_folder=original_folder, hunspell_folder=hunspell_folder,
                                        word_folder=word_folder, filename="Many_Errors.csv")

    # dropping duplicate lines in csv file
    Manual_Evaluation.drop_duplicate_rows_from_csv("Results/Many_Errors.csv")
    

    # ------------------------ READ IN THE MANUALLY EDITED FILE ---------------------------------------------
    manual_data = pd.read_csv("Results/Many_Errors_noDuplicates_Lena.csv", delimiter=",", header=0, encoding="utf-8")
    Manual_Evaluation.manual_evaluation_results(manual_data)
    '''
