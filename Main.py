import DB_access
import Preprocessing
import Apply_Hunspell
import Reduce
import Evaluation
import pandas as pd
import MatchType

if __name__ == '__main__':
    original_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files"
    hunspell_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files\\Hunspell"
    word_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files\\Word"
    gold_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files\\Word"

    # get data from database
    data = DB_access.access_corpus(50)

    # process data and remove special chars
    processed_data = Preprocessing.remove_special_chars(data)

    # apply spellchecking
    #Apply_Hunspell.apply_hunspell_on_dir("Files")
    pd.set_option('display.max_columns', 10)

    '''
    
    # delete the files that are unchanged or have the same change
    unchanged, sameChange = Evaluation.get_unchanged_and_sameChange(original_folder, hunspell_folder, word_folder)
    num_unchanged = len(unchanged)/3
    num_sameChange = len(sameChange)/3
    print(num_unchanged)
    print(num_sameChange)

    Evaluation.delete_files(sameChange, "same Change")
    Evaluation.delete_files(unchanged, "unchanged")
 
    # evaluate and compare the files
    data = Evaluation.compare_files(original_folder, hunspell_folder, word_folder, gold_folder)

    # reduce data size
    data = Reduce.reduce(data)

    #write data to csv
    #data.to_csv("data.csv", sep=",", index=False)

    # read from csv but using types and cols we want
    data2 = Reduce.custom_csv("data.csv")
    #print(data2[data2["lev_hg"] != 0])
    #print(data2[data2["Match-Type"] != 0])
    
    true_pos = Evaluation.get_truePos(data, "hun")
    true_neg = Evaluation.get_trueNeg(data, "hun")
    false_pos = Evaluation.get_falsePos(data, "hun")
    false_neg = Evaluation.get_falseNeg(data, "hun")


    recall = Evaluation.calculate_recall(data, "hun")
    print("recall", recall)
    precision = Evaluation.calculate_precision(data, "hun")
    print("precision", precision)

    word_percent_correct = Evaluation.get_percentCorrect(data, "word")
    hun_percent_correct = Evaluation.get_percentCorrect(data, "hun")
    print(word_percent_correct)
    print(hun_percent_correct)

    word_percent_false = Evaluation.get_percentFalse(data, "word")
    hun_percent_false = Evaluation.get_percentFalse(data, "hun")
    print(word_percent_false)
    print(hun_percent_false)
    
    Evaluation.write_evalFile(data2)
    '''