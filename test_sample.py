import DB_access
import Preprocessing
import Apply_Hunspell
import Reduce
import Gold_Evaluation

import pandas as pd

data = DB_access.access_corpus(6)
original_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files"
hunspell_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files\\Hunspell"
word_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files\\Word"
gold_folder = "C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files\\Gold"

# get data from database
comments = DB_access.access_corpus(5)

# process data and remove special chars
# writes comments into individual files
processed_data = Preprocessing.remove_special_chars(comments, folder="C:\\Users\\Lena_Langholf\\Dropbox\\Spell_Checking\\Test_Files")
pd.set_option('display.max_columns', 12)

# evaluate and compare the files
data = Gold_Evaluation.compare_files(original_folder, hunspell_folder, word_folder, gold_folder)


def test_DB_Access():
    # check that getting 0 posts returns empty list
    assert DB_access.access_corpus(0) == []
    data = DB_access.access_corpus(10)
    # assert that data access with num_posts does not return empty
    assert data != []
    assert isinstance(data, list) # returned object should be list
    assert len(data) == 10 # should contain 10 elems


def test_reduce():
    # get old memory usage
    mem_usage_old = data.memory_usage(deep=True)
    # reduce data # get new memory usage
    smaller_data = Reduce.reduce(data)
    mem_usage = smaller_data.memory_usage(deep=True)

    #assert that datatypes have been converted
    assert smaller_data.dtypes["Error"] == "category"
    assert smaller_data.dtypes["lev_hg"] == "uint8"

    #assert that some values use less space
    assert mem_usage["Error"] < mem_usage_old["Error"]
    assert mem_usage["lev_hg"] < mem_usage_old["lev_hg"]
    assert mem_usage["Match-Type"] < mem_usage_old["Match-Type"]


def test_preprocessing():
    # create strings containing special characters
    test_string1 = "I put some \u201especial\u201e characters in here ;-)\n"
    test_string2 = "In h€r€ I hid some others as well ..., or did I?"
    test_string3 = "    This should test how the strip()-Method works!!!!!"
    test_string4 = "How about something I didn't test before?  "
    test_string5 = "I hope this last one works \u2026"

    # apply replace method
    string1 = Preprocessing.replace_chars(test_string1)
    string2 = Preprocessing.replace_chars(test_string2)
    string3 = Preprocessing.replace_chars(test_string3)
    string4 = Preprocessing.replace_chars(test_string4)
    string5 = Preprocessing.replace_chars(test_string5)

    # assert that characters were removed according to method
    assert string1 == "I put some special characters in here -"
    assert string2 == "In h r I hid some others as well or did I"
    assert string3 == "This should test how the strip -Method works"
    assert string4 == "How about something I didn't test before"
    assert string5 == "I hope this last one works"

def test_unchanged_files():
    # delete the files that are unchanged or have the same change
    unchanged, sameChange = Preprocessing.get_unchanged_sameChange(original_folder, hunspell_folder,
                                                                   word_folder, gold_folder)

    # assert that return value is list
    assert isinstance(unchanged, list)
    assert isinstance(sameChange, list)

    # assert that len is dividable by 4 since the files have to be deleted from 4 folders
    assert (len(unchanged)/4) % 1 == 0
    assert (len(sameChange)/4) % 1 == 0

    # delete the files that stayed the same
    Preprocessing.delete_files(unchanged)
    Preprocessing.delete_files(sameChange)

    # re-test method again, after deletion the returned lists should be empty
    unchanged2, sameChange2 = Preprocessing.get_unchanged_sameChange(original_folder, hunspell_folder, word_folder, gold_folder)
    assert len(unchanged2) == 0
    assert len(sameChange2) == 0
