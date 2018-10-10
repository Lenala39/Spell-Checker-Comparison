import DB_access
import Preprocessing
import Apply_Hunspell


if __name__ == '__main__':
    # get data from database
    data = DB_access.access_corpus(5)

    # process data and remove special chars
    processed_data = Preprocessing.remove_special_chars(data)
    #processed_data2 = Preprocessing.remove_but_keep_meta(data)

    # apply spellchecking
    Apply_Hunspell.apply_hunspell_on_dir("Files")

    '''
    for i in range(len(processed_data2)):
        print("Original: ", processed_data2[i][7])
        print("Corrected: ", applied_data2[i][7])
        print("Other corrected version", applied_data[i])
    '''
