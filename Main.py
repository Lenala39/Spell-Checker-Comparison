import DB_access
import Preprocessing
import Apply_Hunspell
import Reduce
import Evaluation
import pandas as pd
import MatchType

if __name__ == '__main__':
    # get data from database

    '''

    data = DB_access.access_corpus(5)

    # process data and remove special chars
    processed_data = Preprocessing.remove_special_chars(data)
    #processed_data2 = Preprocessing.remove_but_keep_meta(data)

    # apply spellchecking
    Apply_Hunspell.apply_hunspell_on_dir("Files")

    for i in range(len(processed_data2)):
        print("Original: ", processed_data2[i][7])
        print("Corrected: ", applied_data2[i][7])
        print("Other corrected version", applied_data[i])

    
    original_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files"
    hunspell_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files\\Hunspell"
    word_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files\\Word"
    
    # delete the files that are unchanged or have the same change
    unchanged, sameChange = Evaluation.get_unchanged_and_sameChange(original_folder, hunspell_folder, word_folder)
    num_unchanged = len(unchanged)/3
    num_sameChange = len(sameChange)/3
    print(num_unchanged)
    print(num_sameChange)

    Evaluation.delete_files(sameChange, "same Change")
    Evaluation.delete_files(unchanged, "unchanged")
    
    
    #data = pd.DataFrame(np.random.randint(low=0, high=1, size=(1,9)),
                        columns=["ID", "Match-Type", "Original", "Gold", "Hunspell", "Word", "L1", "L2", "L3"])
    #data.set_index("ID", inplace=True)
    #print(data)
    #test = pd.Series(np.ndarray(shape=(9,)))
    #data = data.append(test, ignore_index=True)

    test_dict = {"ID": "id",
                 "Match-Type": "test",
                 "Original": "o_words[j]",
                 "Gold": "g_words[j]",
                 "Hunspell": "h_words[j]",
                 "Word": "w_words[j]",
                 "Lev1": 0,
                 "Lev2": 0,
                 "Lev3": 0}
    test = pd.Series(test_dict)
    data.loc[1] = test
    '''

    original_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files"
    hunspell_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files\\Hunspell"
    word_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files\\Word"
    gold_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Files\\Word"
    pd.set_option('display.max_columns', 9)

    # evaluate and compare the files
    data = Evaluation.compare_files(original_folder, hunspell_folder, word_folder, gold_folder)

    # reduce data size
    data = Reduce.reduce(data)
