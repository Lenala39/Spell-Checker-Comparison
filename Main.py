import DB_access
import Preprocessing
import Apply_Hunspell
import Reduce
import NumberCrunching
import Evaluation
import pandas as pd
import MatchType
import hunspell
import datetime
import time

if __name__ == '__main__':
    original_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files"
    hunspell_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files\\Hunspell"
    word_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files\\Word"
    gold_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files\\Gold"

    # get data from database
    #data = DB_access.access_corpus(2000)

    # process data and remove special chars
    # writes comments into individual files
    #processed_data = Preprocessing.remove_special_chars(data)

    # apply spellchecking
    #Apply_Hunspell.apply_hunspell_on_dir("C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files")
    pd.set_option('display.max_columns', 12)

    ''' 
    # delete the files that are unchanged or have the same change
    unchanged, sameChange = NumberCrunching.get_unchanged_and_sameChange(original_folder, hunspell_folder, word_folder)
    num_unchanged = len(unchanged)/3
    num_sameChange = len(sameChange)/3
    print(num_unchanged)
    print(num_sameChange)

    NumberCrunching.delete_files(sameChange, "same Change")
    NumberCrunching.delete_files(unchanged, "unchanged")
    '''
    
    # evaluate and compare the files
    data = NumberCrunching.compare_files(original_folder, hunspell_folder, word_folder, gold_folder)
    # drop duplicate rows (want unique items)
    data_unique = data.drop_duplicates(subset=["Match-Type", "Error", "Original", "Gold", "Hunspell", "Word", "lev_hg", "lev_wg", "lev_hw", "lev_og"], keep="first", inplace=False)

    # reduce data size
    data_unique = Reduce.reduce(data)
    #write data to csv
    #data_unique.to_csv("data.csv", sep=",", index=False)
    NumberCrunching.write_evalFile(data_unique)

    Evaluation.gold_eval(data_unique)


    '''
    true_pos = NumberCrunching.get_truePos(data_unique, "hun")
    true_neg = NumberCrunching.get_trueNeg(data_unique, "hun")
    false_pos = NumberCrunching.get_falsePos(data_unique, "hun")
    false_neg = NumberCrunching.get_falseNeg(data_unique, "hun")


    recall = NumberCrunching.calculate_recall(data_unique, "hun")
    print("recall", recall)
    precision = NumberCrunching.calculate_precision(data_unique, "hun")
    print("precision", precision)

    word_percent_correct = NumberCrunching.get_percentCorrect(data_unique, "word")
    hun_percent_correct = NumberCrunching.get_percentCorrect(data_unique, "hun")
    print(word_percent_correct)
    print(hun_percent_correct)

    word_percent_false = NumberCrunching.get_percentFalse(data_unique, "word")
    hun_percent_false = NumberCrunching.get_percentFalse(data_unique, "hun")
    print(word_percent_false)
    print(hun_percent_false)
    '''
