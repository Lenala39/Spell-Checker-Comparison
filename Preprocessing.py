import re
def remove_special_chars(data):
    '''
    removes special chars from comment and returns list of only comments
    :param data: list of data tuples with comments
    :return: list of comments (no metadata)
    '''
    new_data = []
    for i in range(len(data)):
        text = data[i][7]
        if text is not None:
            text = replace_chars(text)
            new_data.append(text)
            write_file(text, data[i][0])
    return new_data

def remove_but_keep_meta(data):
    '''
    removes the same metacharacters as the other function but keeps metadata like author ...
    :param data: list of tuples with comments
    :return: list of comments with metadata (tuple structure kept)
    '''
    for i in range(len(data)):
        text = data[i][7]
        if text is None:
            pass
        else:
            text = replace_chars(text)

        data[i] = list(data[i])
        data[i][7] = text
        write_file(text, data[i][0])


    return data

def replace_chars(text):
    '''
    replaces all special characters not suitable when spell checking from string
    param: text string
    returns: text string with removed chars
    '''
    text = text.replace("=\r\n", "")
    text = text.replace("\r", "")
    text = text.replace("\n", " ")
    text = text.replace("(", "").replace(")", "")
    text = text.replace(",", "")
    text = text.replace("!", "")
    text = text.replace("?", "")
    text = text.replace(".", "")
    text = text.replace(";", "")
    text = text.replace(":", "")
    text = re.sub(r" {2,}", " ", text) #replace more than one whitespace with a single one
    return text

def write_file(comment, id):
    filename = "Files/{}.txt".format(id)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(comment)


