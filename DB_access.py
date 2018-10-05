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
    return data





