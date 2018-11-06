import pandas as pd

def mem_usage(pandas_obj):
    '''
    prints mem usage nicely
    :param pandas_obj:
    :return:
    '''
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:  # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    return "{} B".format(usage_b)

def reduce_int(data):
    '''
    reduces the storage for all int64 columns to about a third
    :param data: dataframe
    :return: DataFrame that was reduced
    '''
    data_int = data.select_dtypes(include=['int64']) # select all int64 cols
    converted_int = data_int.apply(pd.to_numeric, downcast='unsigned') #convert to numeric
    # unsigned’: smallest unsigned int dtype (min.: np.uint8)
    data[converted_int.columns] = converted_int #re-assign the down-sized cols to data

    return data

def reduce_matchType(data):
    '''
    reduces size by making Match-Type column a category
    :param data:
    :return:
    '''
    data["Match-Type"] = data["Match-Type"].astype("category")
    return data

def reduce(data):
    '''
    reduces the size of the DataFrame by using uints and category-types
    :param data: big DataFrame
    :return: reduced DataFrame
    '''
    #data = reduce_matchType(data)
    data = reduce_int(data)
    return data


def custom_csv(csv_file):
    '''
    imports a csv file and already assigns correct dtypes for reduced size
    :param csv_file: path to csv
    :return: DataFrame
    '''
    column_names = ['Comment-ID', 'Word-ID', 'Match-Type', 'Original', 'Gold', 'Hunspell', 'Word', 'lev_hg', 'lev_wg', 'lev_hw', 'lev_og']
    dtypes = ['uint8', 'uint8', 'uint8', 'object', 'object', 'object', 'object', 'uint8', 'uint8', 'uint8', 'uint8']
    column_types = dict(zip(column_names, dtypes))
    data = pd.read_csv(csv_file, dtype=column_types)
    return data

