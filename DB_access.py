import sqlite3


def access_corpus(num_posts):
    '''
    accesses the sqlite database of the million-post-corpus
    :param num_posts: number of posts to be retrieved
    :return: posts as list (list of tuples)
    '''
    conn = sqlite3.connect("corpus.sqlite3") # connect to database
    c = conn.cursor() # create cursor
    # select everything from Table Posts that has an ID smaller than num_posts
    c.execute("SELECT * FROM Posts WHERE ID_Post <= ?", (num_posts,))
    data = c.fetchall() # return ALL posts that fulfill condition

    # CHECK FOR EMPTY COMMENTS AND SUBSTITUTE THEM
    empty_comments, to_be_deleted = check_for_empty_comments(data)
    # while some comments are empty
    while empty_comments is not 0:
            data = delete_empty_comments(data, to_be_deleted) #delete comments
            next_upperbound = num_posts + empty_comments #make next upper boundary
            # select comments that have a higher ID than num_posts, but smaller than upper bound
            c.execute("SELECT * FROM Posts WHERE ID_POST > ? AND ID_POST <=?", (num_posts, next_upperbound,))
            new_data = c.fetchall()
            data.extend(new_data) # extend data with next comments
            empty_comments, to_be_deleted = check_for_empty_comments(data) # check for empty comments

    return data

def check_for_empty_comments(data):
    '''
    checks if any comment in the dataset is empty (text body)
    :param data: list of all comments
    :return: number of empty comments, list of comments to be deleted
    '''

    #init variables
    empty_comments = 0
    to_be_deleted = []
    # iterate over data
    for i in range(len(data)):
        if not data[i][7]: #if the text body is empty string
            empty_comments = empty_comments + 1 # increase empty comments by 1
            to_be_deleted.append(data[i]) # append comment to list
    return empty_comments, to_be_deleted

def delete_empty_comments(data, to_be_deleted):
    '''
    deletes all comments that are in to_be_deleted list
    :param data: list of all comments
    :param to_be_deleted: list of comments to be deleted (as tuples)
    :return: data2 containing only comments with text body
    '''
    data2 = [elem for elem in data if elem not in to_be_deleted]
    return data2
