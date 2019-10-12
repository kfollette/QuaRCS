from repeats import repeats
import pandas as pd
import numpy as np
import pickle
import copy

def merge(nomatch_pre, nomatch_post, df_pre, df_post, pairs):
    '''
    Retruns a single Pandas DataFrame from Pre and Post DataFrames

    Required functions:
        repeats
        col_index

    Args:
        nomatch_pre: Python list of int row indeces of inputs in the pre-semester dataset.
        nomatch_post: Python list of int row indeces of inputs in the post-semester dataset.
        df_pre: The Pandas DataFrame of the pre-semester dataset.
        df_post: The Pandas DataFrame of the post-semester dataset.
        pairs: Python int key dictionary of int row indeces of matching pairs


    Returns:
        df_1: Pandas DataFrame

    Required modules:
        pandas as pd
        numpy as np

    By:
        Ilija Nikolov, 31.07.17

    '''

    df = pd.DataFrame()
    columns = []

    # Indeces of the pre dataframe columns
    columns_pre = df_pre.columns.tolist()

    # Get the list of the names of the columns, for PRE and PST DF
    for i in range(len(df_pre.columns)):
        columns.append(df_pre.columns[i])
    for i in range(len(df_post.columns)):
        columns.append(df_post.columns[i])


    # Get the indeces of the post dataframe columns, in order
    columns_post = []
    j = len(df_pre.columns)
    while(j < (len(df_pre.columns) + len(df_post.columns))):
        columns_post.append(j)
        j = j + 1


    pre_pairs = []
    for i in range(len(pairs)):
        pre_pairs.append(pairs[i][0])

    # Add by row for the pairs section of the dataframes
    for i in range(len(pairs)):
        df_pre.loc[pairs[i][0], "PRE_WHICHADMIN"] = 2
        df_post.loc[pairs[i][1], "PST_WHICHADMIN"] = 2
        left = df_pre.loc[pairs[i][0],:]
        right = df_post.loc[pairs[i][1],:]
        concat = pd.concat([left,right], ignore_index=True)
        df = df.append(concat, ignore_index=True)

    # Add by row for the pre-nomatches
    for i in range(len(nomatch_pre)):
        df_pre.loc[nomatch_pre[i], "PRE_WHICHADMIN"] = 0
        left = df_pre.loc[nomatch_pre[i],:]
        right = pd.Series(np.nan, columns_post)
        concat = pd.concat([left,right], ignore_index=True)
        df = df.append(concat, ignore_index=True)


    post_pairs = []
    for i in range(len(pairs)):
        post_pairs.append(pairs[i][1])

    # Add by row for the post-nomatches
    for i in range(len(nomatch_post)):
        df_post.loc[nomatch_post[i], "PST_WHICHADMIN"] = 1
        left = pd.Series(np.nan, columns_pre)
        right = df_post.loc[nomatch_post[i],:]
        concat = pd.concat([left,right], ignore_index=True)
        df = df.append(concat, ignore_index=True)

    # Create one big dataframe with the right column names
    #df_1 = pd.DataFrame(data = pd.DataFrame.as_matrix(df), columns = columns)
    df_1 = pd.DataFrame(data = pd.DataFrame.to_numpy(df), columns = columns)

    #For now, make empty columns for the info that will be imported from the instructor db
    df_1['MRG_CRS_TYP'] = np.nan
    df_1['MRG_CRS_SUBJ'] = np.nan
    df_1['MRG_SCHL_TYPE'] = np.nan
    df_1['MRG_CRS_CRED'] = np.nan

    #Make the merged effort flag
    df_1['MRG_EFFBOTH'] = np.nan
    for i in range(len(df_1)):
        if(df_1.loc[i, 'PRE_EFFFLAG'] == 1 and df_1.loc[i, 'PST_EFFFLAG'] == 1):
            df_1.loc[i,'MRG_EFFBOTH'] = 1
    #Collapse student ID into one column
    df_1['STUDENT_ID'] = df_1['PRE_STUDENT_ID']
    for i in range(len(df_1)):
        if(pd.isnull(df_1.loc[i, 'STUDENT_ID'])):
            df_1.loc[i,'STUDENT_ID'] = df_1.loc[i,'PST_STUDENT_ID']

    #Collapse Response ID into one column
    df_1['RESPONSE_ID'] = df_1['PRE_ResponseId']
    for i in range(len(df_1)):
        if(pd.isnull(df_1.loc[i, 'RESPONSE_ID'])):
            df_1.loc[i,'RESPONSE_ID'] = df_1.loc[i,'PST_ResponseId']
    # Order the column names
    with open('nameorder.pkl', 'rb') as f:
        nameorder = pickle.load(f)
    df_pub_cut = df_1[nameorder]
    #df_pub_cut["STUDENT_ID"] = df_pub_cut["PRE_STUDENT_ID"]
    #df_pub_cut = df_pub_cut.drop(['PRE_STUDENT_ID'], axis=1)
    #df_pub_cut = df_pub_cut.drop(['PST_STUDENT_ID'], axis=1)
    df_pub = copy.deepcopy(df_pub_cut)

    #df_1 = df_1.reindex(columns=nameorder)
    #for i in df_1.columns:
        #if i not in nameorder:
            #print(i)

    return df_pub
