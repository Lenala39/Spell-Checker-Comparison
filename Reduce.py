import pandas as pd

def mem_usage(pandas_obj):
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
    gl_obj = data.select_dtypes(include=['object']).copy()
    gl_obj.describe()

    dow = gl_obj["Match-Type"]
    print(Reduce.mem_usage(dow))
    dow_cat = dow.astype('category')
    print(Reduce.mem_usage(dow_cat))
    '''
    data["Match-Type"] = data["Match-Type"].astype("category")
    return data

def reduce(data):
    data = reduce_matchType(data)
    data = reduce_int(data)
    return data