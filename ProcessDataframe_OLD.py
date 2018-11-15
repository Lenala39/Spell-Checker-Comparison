import os

# ---------------------------- UNUSED METHODS -----------------------------

def get_unchanged_and_sameChange(original_folder, hunspell_folder, word_folder):
    '''
    OLD!!!
    removes the files that have the same content (are unchanged) in all three folders
    :param original_folder: folder with the extracted comments from db
    :param hunspell_folder: files processed by hunspell
    :param word_folder: files processed by word
    :return: lists of files that are unchanged or word and hunspell made the same change
    '''

    #create lists of all files in the folders (for original need to filter out subdirs
    original_list = [f for f in os.listdir(original_folder) if os.path.isfile(os.path.join(original_folder, f))]
    hunspell_list = os.listdir(hunspell_folder)
    word_list = os.listdir(word_folder)

    # create lists to store the files to be deleted in/the deleted indices
    to_delete_unchanged = []
    to_delete_sameChange = []
    deleted_indices_unchanged = []
    deleted_indices_sameChange = []

    # iterate over all files in the respective lists
    for i in range(len(hunspell_list)):
        #create a path for all of the files
        o_path = os.path.join(original_folder, original_list[i])
        h_path = os.path.join(hunspell_folder, hunspell_list[i])
        w_path = os.path.join(word_folder, word_list[i])

        # open the files
        with open(o_path, "r") as original_file:
            with open(h_path, "r") as hunspell_file:
                with open(w_path, "r") as word_file:

                    # read the content of the files
                    o_content = original_file.read()
                    h_content = hunspell_file.read()
                    w_content = word_file.read()

                    # if the content matches for all three files
                    if o_content == h_content and h_content == w_content:
                        # append all file(paths) to the to_delete list and the current index to deleted_indeces
                        to_delete_unchanged.append(o_path)
                        to_delete_unchanged.append(h_path)
                        to_delete_unchanged.append(w_path)
                        deleted_indices_unchanged.append(i)
                    elif h_content == w_content and o_content != h_content:
                        to_delete_sameChange.append(o_path)
                        to_delete_sameChange.append(h_path)
                        to_delete_sameChange.append(w_path)
                        deleted_indices_sameChange.append(i)

    # write a file with the indices of the files that were deleted
    # a) because they were unchanged
    with open("Results/unchanged.txt", "a", encoding="utf-8") as unchanged_indices:
        for elem in deleted_indices_unchanged:
            unchanged_indices.write(elem)

    # b) because they contained the same change
    with open("Results/sameChange.txt", "a", encoding="utf-8") as sameChange_indices:
        for elem in deleted_indices_sameChange:
            sameChange_indices.write(str(elem))

    return to_delete_unchanged, to_delete_sameChange

