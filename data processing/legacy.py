import pandas as pd
import numpy as np


def str_simplify(some_string):
    '''
    Simplifies a string (str) to an alphabet-only and lowercase-only (a-z) str.

    Args:
        some_string: The string in question.

    Returns:
        A super-simplified str.

    Examples:
        >>> str_simplify('A1m0H()** % 55Er+"s"+t'' @')
        'amherst'

    Future improvements:
        Fix possible problems with multiple apostrophes mid string.

    By:
        Ilija Nikolov, 20.07.17
    '''
    some_string = str(some_string)
    some_string = some_string.lower()

    #removes any special characters, whitespaces and capitalizations
    some_string = ''.join(e for e in some_string if e.isalnum())

    #removes any digit in a string
    some_string = ''.join(i for i in some_string if not i.isdigit())

    return some_string


def col_index(df, col_name):
    '''
    Returns the index for the specified column from a given DataFrame. If the column appears more than once,
    it returns the index of lower indexed column.

    Args:
        df: The Pandas DataFrame containing the column.
        col_name: The str name of the column, must be exact as it appears in the df.

    Returns:
        An int column index.

    Examples:
        >>> col_index(data_pre, 'Firstname')
        31

    Future improvements:
        Column name error tolerance.

    By:
        Ilija Nikolov, 30.07.17

    '''
    #If the column appears only once, pandas.get_loc returns the desired int
    if (type(df.columns.get_loc(col_name)) == int):
        i = df.columns.get_loc(col_name)

    #Otherwise, pd.get_loc returns a boolean mask
    else:
        for i in range(len(df.columns)):
            #First time a column is seen, the for cycle stops
            if (df.columns.get_loc(col_name)[i] == True):
                break

    #returns the column index
    return i


def col_index_second(df, col_name):
    '''
    Returns the index for the specified column, the second time it apperas in the given Pandas DataFrame.

    Args:
        df: The Pandas DataFrame containing the column.
        col_name: The str name of the column, must be exact as it appears in the df.

    Returns:
        An int column index.

    Examples:
        >>> col_index(data_pre, 'Firstname')
        131

    Future improvements:
        If more columns of the same name, ability to choose which one to select, in order of appearance.
        Column name error tolerance.

    By:
        Ilija Nikolov, 30.07.17

    '''
    #boolean for skipping the first introduction to the column
    count = True

    for i in range(len(df.columns)):
        #pd.get_loc returns a boolean mask
        if (df.columns.get_loc(col_name)[i] == True):
            if(count):
                count = False
            else:
                break
    #returns the column index
    return i

def inst_col_indx(df):
    '''
    Returns the column index for the first time it sees an instructor column in the given Pandas DataFrame.
    The column name must include the str: 'instr'.

    Required functions:
        str_simplify

    Args:
        df: The Pandas DataFrame in question.

    Returns:
        An int column index.

    Examples:
        >>> inst_col_index(data_pre)
        21

    Future improvements:
        Better capability to recognize the instructor column.

    By:
        Ilija Nikolov, 30.07.17

    '''
    cols = df.columns
    for i in range(len(cols)):
        if ('instr' in str_simplify(cols[i])):
            break
    return i


def only_complete(data_old_keep, semester):
    '''
    Returns an automatically polished DataFrame, where any rows containing no names,
    or one-character names are dropped and stored in another DataFrame.
    It also checks if the name is provided in one cell and makes sure that it is split
    into the two cells - Firstname and Lastname.
    It adds logistical columns at the end of the DataFrame.

    Args:
        data_old_keep: The Pandas DataFrame in question.

    Returns:
        data_new: Pandas DataFrame that is automatically cleaned
        data_dropped: Pandas DataFrame containing the dropped rows

    Future improvements:

    Required modules:
        import pandas as pd
        import numpy as np
        import copy

    By:
        Ilija Nikolov, 30.07.17

    '''
    import pandas as pd
    import numpy as np
    import copy

    data_old_keep.loc[:,"INST_CHANGE"] = np.nan
    data_old_keep.loc[:,"WHICHADMIN"] = "BOTH"
    data_old_keep.loc[:, "NUMREPS"] = "1 of 1"
    data_old_keep.loc[:,"RETAKE_TRACKER"] = np.nan

    data_old = copy.deepcopy(data_old_keep)

    #replaces all the whitespace (of any length) cells with an np.nan
    data_old = data_old.applymap(lambda x: np.nan if isinstance(x, str) and x.isspace() else x)

    #accounting for old data with full-name provided in "NAME" column
    if 'NAME' in data_old.columns:

        #Create first name and last name columns
        data_old['Firstname'] = " "
        data_old['Lastname'] = " "

        #split using the whitespaces provided in name
        for i in range(len(data_old.iloc[:,col_index(data_old,'NAME')])):
            name = str(data_old.iloc[i,col_index(data_old,'NAME')]).strip()
            names = name.split(" ")

            #firstname cell gets the first element
            data_old.iloc[i,col_index(data_old,'Firstname')] = names[0]

            #the rest go to lastname cell
            m = 1
            nm =''
            while(m<len(names)):
                nm = nm + ' ' + names[m]
                m = m + 1
            data_old.iloc[i, col_index(data_old,'Lastname')] = nm

        # makes list of column titles
        cols = list(data_old.columns.values)
        findex = cols.index('NAME')
        lindex = findex + 1

        # rearranges placement of columns
        cols.insert(findex, "Firstname")
        cols.insert(lindex, "Lastname")

        #deletes duplicates of column names
        del cols[-2] #deletes second to last object in list which is "First Name"
        del cols[-1] #deletes last object which is "Last Name"
        del cols[cols.index('NAME')]

        #Applies new column order
        data_old = data_old[cols]

    #accounting for full-name provided in one cell
    for i in range(len(data_old.iloc[:,col_index(data_old,'Firstname')])):

        #check if Firstname cell is empty
        if(pd.isnull(data_old.iloc[i,col_index(data_old,'Firstname')])):

            #skip if no name provided at all
            if(pd.isnull(data_old.iloc[i,col_index(data_old,'Lastname')])):
                continue

            #full-name is in the lastname cell
            else:
                #split using the whitespaces provided in the one cell
                name = str(data_old.iloc[i,col_index(data_old,'Lastname')]).strip()
                names = name.split(" ")

                #firstname cell gets the first element
                data_old.iloc[i,col_index(data_old,'Firstname')] = names[0]

                #the rest go to lastname cell
                m = 1
                nm =''
                while(m<len(names)):
                    nm = nm + ' ' + names[m]
                    m = m + 1
                data_old.iloc[i, col_index(data_old,'Lastname')] = nm

        #firstname cell contains data
        else:
            #skip if lastname cell also contains data
            if(pd.notnull(data_old.iloc[i,col_index(data_old,'Lastname')])):
                continue

            #full-name name is in the firstname cell
            else:
                #split using the whitespaces provided in the one cell
                name = str(data_old.iloc[i,col_index(data_old,'Firstname')]).strip()
                names = name.split(" ")

                #firstname cell gets the first element
                data_old.iloc[i,col_index(data_old,'Firstname')] = names[0]

                #the rest go to lastname cell
                m = 1
                nm =''
                while(m<len(names)):
                    nm = nm + ' ' + names[m]
                    m = m + 1
                data_old.iloc[i, col_index(data_old,'Lastname')] = nm

    #filtering out unfinished sessions
    data_trans = data_old[data_old[semester + '_COMPFLAG'] == '1']

    #filtering out sessions with no name provided
    data_provis = data_old[pd.notnull(data_old['Firstname']) & pd.notnull(data_old['Lastname'])]

    #filtering out sessions with one character names
    data_interim = data_provis[(data_provis['Firstname'].str.len() > 1) & (data_provis['Lastname'].str.len() > 1)]

    #adding a comments columns
    data_new = copy.deepcopy(data_interim)

    index_old = data_old_keep[data_old_keep.columns[0]].index.tolist()
    index_new = data_new[data_new.columns[0]].index.tolist()

    indeces_dropped = []
    for i in index_old:
        if(i not in index_new):
            indeces_dropped.append(i)
    #indeces_dropped = indeces_dropped[2:]

    df_1 = pd.DataFrame()
    for i in indeces_dropped:
        df_1 = df_1.append(data_old_keep.loc[i,:], ignore_index=True)
    data_dropped = pd.DataFrame(data=df_1, columns = data_old_keep.columns.tolist())

    return data_new, data_dropped


def repeating_names(df_prov):
    '''
    Returns a Python dictionary of int indeces of the any retakes in this format:
    {count1: [first time seen, second time seen, etc...], count2: [first time seen, second time seen, etc...], etc...}.

    *Names must be approximately similar (e.g. no spelling mistakes, no extra names).

    Required functions:
        str_simplify
        col_index

    Args:
        df_prov: The Pandas DataFrame in question.

    Returns:
        A Python dictionary.

    Examples:
        >>> inst_col_index(data_pre)
        {0: [2, 68, 77],
        1: [12, 271],
        2: [14, 667],
        ...
        80: [999, 1076],
        81: [1010, 1081, 1084]}

    Future improvements:
        Better name-matching mechanism.

    By:
        Ilija Nikolov, 20.07.17

    '''
    repeats = {}
    count = 0
    bol = True

    #slicing out the dataframe for speed
    the_list = ['Firstname', 'Lastname']
    df = df_prov[the_list]

    #using column indexces
    first_inx = col_index(df, 'Firstname')
    lst_inx = col_index(df, 'Lastname')

    #for loop to go through all first names
    for i in range(len(df['Firstname'])):

        for k in range(len(repeats)):
            if(i in repeats[k]):
                bol = False

        if(bol):
            list = []

            #simplified first and last name
            nm = str_simplify(df.iloc[i, first_inx])
            lst = str_simplify(df.iloc[i, lst_inx])

            #while loop to check named starting under specified position
            j = i + 1
            list.append(i)

            while (j < (len(df['Firstname']))):

                #only when first and last name equal //this part can be improved
                if((nm == str_simplify(df.iloc[j,first_inx])) and (lst == str_simplify(df.iloc[j, lst_inx]))):
                    list.append(j)

                j = j + 1

            if(len(list)>1):
                #updates the dictionary
                repeats.update({count:(list)})
                count = count + 1

        bol = True

    return repeats


def instructors_list(data_old, kind):
    '''
    Returns the same Pandas DataFrame, but all instructor names will be in an "PRE"/"PST" + "_INSTR" columns.

    Required functions:
        str_simplify
        inst_col_indx

    Args:
        data_old: The Pandas DataFrame in question.
        kind: str, should only take values of "PRE" and "PST"

    Returns:
        A Pandas DataFrame

    Required modules:
        math
        numpy as np

    By:
        Ilija Nikolov, 18.07.17

    '''
    import math
    import numpy as np

    inst_col = inst_col_indx(data_old)

    data_old.insert(inst_col, kind+'_INSTR', np.nan)

    #get a list of all columns
    columns = data_old.columns

    #for-loop to go throgh the instructors
    j = inst_col
    check = columns[j].split("_")
    while((check[1]) == "INSTR" or (check[1]) == "PCCINS"):
        for i in range(len(data_old.iloc[:,inst_col])):
            if(pd.notnull(data_old.iloc[i,j])):
                data_old.iloc[i,inst_col] = data_old.iloc[i,j]
        j = j + 1
        check = columns[j].split("_")
    return data_old


def comments_fill(kind, nomatch, df, df_drop, repeat, instructor_change):
    '''
    Fils out columns about which kinds of exams were taken, a number of admins and an instructor change

    Required functions:
        col_index

    Args:
        kind: str, "PRE" or "POST"
        nomatch: Python int key dictionary of int row indeces of studentes with nomathces
        df: Pandas DataFrame of the dataset in question
        repeat: Python int key dictionary of int row indeces of students whose number of administration is greater than 1
        instructor_change: Python int key dictionary of int row indeces of students with instructor change

    By:
        Ilija Nikolov, 03.08.17

    '''
    comments_indx = col_index(df, "NUMREPS")

    #there is a problem with this piece of coding specifically
    #when the len(repeat[i]) == 3, it execudes twice the code? :/
    for i in range(len(repeat)):
        for j in range(len(repeat[i])):
            df.iloc[repeat[i][j], comments_indx] = str(j+1)+" of "+str(len(repeat[i]))

    comments_indx = col_index(df_drop, "WHICHADMIN")
    for i in range(len(df_drop)):
        if(kind == "PRE"):
            df_drop.iloc[i, comments_indx] = "PARTIAL SESSION"
        elif(kind == "PST"):
            df_drop.iloc[i, comments_indx] = "PARTIAL SESSION"

    comments_indx = col_index(df, "INST_CHANGE")

    # Indicate instructor change
    for i in range(len(instructor_change)):
        if(kind == "PRE"):
            df.iloc[instructor_change[i][0], comments_indx] = "YES"

        elif(kind == "PST"):
            df.iloc[instructor_change[i][1], comments_indx] = "YES"


def standardize(df, typ):
    lst = df.columns

    for i in range(len(lst)):
        check = lst[i].split("_")

        if(check[0] != typ):
            df.rename(columns={df.columns[i]: (typ + "_" + df.columns[i])}, inplace=True)

    return df

def merger(nomatch_pre, nomatch_post, df_pre, df_post, df_pre_drop, df_post_drop, pairs, repeat_pre, repeat_post):
    '''
    Retruns a single Pandas DataFrame from Pre and Post DataFrames

    Required functions:
        str_simplify
        inst_col_indx
        col_index
        repeating_names
        match
        match_refine

    Args:
        nomatch_pre: Python list of int row indeces of inputs in the pre-semester dataset.
        nomatch_post: Python list of int row indeces of inputs in the post-semester dataset.
        df_pre: The Pandas DataFrame of the pre-semester dataset.
        df_post: The Pandas DataFrame of the post-semester dataset.
        pairs: Python int key dictionary of int row indeces of matching pairs
        repeat_pre:Python int key dictionary of int row indeces of any retakes in the pre-semester dataset
        repeat_pos: Python int key dictionary of int row indeces of any retakes in the post-semester dataset


    Returns:
        df_1: Pandas DataFrame

    Required modules:
        pandas as pd
        numpy as np

    By:
        Ilija Nikolov, 31.07.17

    '''
    import pandas as pd
    import numpy as np

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

    # Adds the RETAKES_TRACKER
    for i in range(len(repeat_pre)):
        for j in range(len(repeat_pre[i])):
            df_pre.iloc[repeat_pre[i][j], col_index(df_pre,"PRE_RETAKE_TRACKER")] = str(repeat_pre[i][j])

    for i in range(len(repeat_post)):
        for j in range(len(repeat_post[i])):
            df_post.iloc[repeat_post[i][j],col_index(df_post, "PST_RETAKE_TRACKER")] = str(repeat_post[i][j])
    pre_pairs = []
    for i in range(len(pairs)):
        pre_pairs.append(pairs[i][0])

    comments_indx_pre = col_index(df_pre, "PRE_WHICHADMIN")
    comments_indx_post = col_index(df_post, "PST_WHICHADMIN")

    # Add by row for the pairs section of the dataframes
    for i in range(len(pairs)):
        df_pre.iloc[pairs[i][0], comments_indx_pre] = "BOTH"
        df_post.iloc[pairs[i][1], comments_indx_post] = "BOTH"
        left = df_pre.iloc[pairs[i][0],:]
        right = df_post.iloc[pairs[i][1],:]
        concat = pd.concat([left,right], ignore_index=True)
        df = df.append(concat, ignore_index=True)

    # Add by row for the pre-repeats
    for i in range(len(repeat_pre)):
        for j in range(len(repeat_pre[i])):
            if(not(repeat_pre[i][j] in nomatch_pre) and not(repeat_pre[i][j] in pre_pairs)):
                df_pre.iloc[repeat_pre[i][j], comments_indx_pre] = "PRE_ONLY"
                left = df_pre.iloc[repeat_pre[i][j],:]
                right = pd.Series(np.nan, columns_post)
                concat = pd.concat([left,right], ignore_index=True)
                df = df.append(concat, ignore_index=True)
    # Add by row for the pre-nomatches
    for i in range(len(nomatch_pre)):
        df_pre.iloc[nomatch_pre[i], comments_indx_pre] = "PRE_ONLY"
        left = df_pre.iloc[nomatch_pre[i],:]
        right = pd.Series(np.nan, columns_post)
        concat = pd.concat([left,right], ignore_index=True)
        df = df.append(concat, ignore_index=True)

    # Add by row inclomplete data for pre
    for i in range(len(df_pre_drop)):
        left = df_pre_drop.iloc[i,:]
        right = pd.Series(np.nan, columns_post)
        concat = pd.concat([left,right], ignore_index=True)
        df = df.append(concat, ignore_index=True)

    post_pairs = []
    for i in range(len(pairs)):
        post_pairs.append(pairs[i][1])

    # Add by row for the post-repeats
    for i in range(len(repeat_post)):
        for j in range(len(repeat_post[i])):
            if(not(repeat_post[i][j] in nomatch_post) and not (repeat_post[i][j] in post_pairs)):
                df_post.iloc[repeat_post[i][j], comments_indx_post] = "POST_ONLY"
                left = pd.Series(np.nan, columns_pre)
                right = df_post.iloc[repeat_post[i][j],:]
                concat = pd.concat([left,right], ignore_index=True)
                df = df.append(concat, ignore_index=True)

    # Add by row for the post-nomatches
    for i in range(len(nomatch_post)):
        df_post.iloc[nomatch_post[i], comments_indx_post] = "POST_ONLY"
        left = pd.Series(np.nan, columns_pre)
        right = df_post.iloc[nomatch_post[i],:]
        concat = pd.concat([left,right], ignore_index=True)
        df = df.append(concat, ignore_index=True)

    # Add incomplete data by row for the PST
    for i in range(len(df_post_drop)):
        left = pd.Series(np.nan, columns_pre)
        right = df_post_drop.iloc[i,:]
        concat = pd.concat([left,right], ignore_index=True)
        df = df.append(concat, ignore_index=True)


    # Create one big dataframe with the right column names
    df_1 = pd.DataFrame(data = pd.DataFrame.as_matrix(df), columns = columns)
    df_1['MRG_EFFBOTH'] = np.nan
    for i in range(len(df_1)):
        if(df_1.loc[i, 'PRE_EFFFLAG'] == 1 and df_1.loc[i, 'PST_EFFFLAG'] == 1):
            df_1.loc[i,'MRG_EFFBOTH'] = 1

    return df_1


#return an anonymized public merged file
def public_merged(mrgd_data_1, data_pre):
    '''
    Drop and renames certain columns for the public dataset

    Required functions:
        str_simplify
        inst_col_indx
        col_index
        repeating_names
        match
        match_refine
        merger

    Args:
        mrgd_data_1: The Pandas DataFrame of the merged dataset
        data_pre: The Pandas DataFrame of the pre-semester dataset.

    Returns:
        mrgd_data: Pandas DataFrame

    Required modules:
        copy

    By:
        Ilija Nikolov, 01.08.17

    '''
    import copy
    mrgd_data = copy.deepcopy(mrgd_data_1)

    # All the columns that need to be dropped for the public DF
    dropping_columns = ['PRE_RESPID','PRE_RESPSET','PRE_NAME','PRE_EXT_DATA', 'PRE_EMAIL', 'PRE_IPAddress', 'PRE_STATUS']
    dropping_columns.extend(['PST_RESPID', 'PST_RESPSET', 'PST_NAME', 'PST_EXT_DATA', 'PST_EMAIL', 'PST_IPAddress', 'PST_INTRO'])
    dropping_columns.extend(['PST_Unnamed: 0','PST_Unnamed: 0.1', 'PST_Unnamed: 0.2'])
    dropping_columns.extend(['PRE_Unnamed: 0','PRE_Unnamed: 0.1', 'PRE_Unnamed: 0.2'])
    dropping_columns.extend(['PRE_FINISHED', 'PRE_INTRO', 'PRE_META_INFO_2_TEXT', 'PRE_META_INFO_5_TEXT', 'PRE_META_INFO_6_TEXT'])
    dropping_columns.extend(['PRE_META_INFO_7_TEXT', 'PRE_Name_warning', 'PRE_Name_warning.1', 'PRE_Name_warning.2'])
    dropping_columns.extend(['PST_Name_warning', 'PST_Name_warning.1', 'PST_Name_warning.2'])
    dropping_columns.extend(['PRE_PRIMER', 'PST_STATUS', 'PST_FINISHED', 'PST_META_INFO_2_TEXT', 'PST_META_INFO_5_TEXT', 'PRE_META_INFO_6_TEXT', 'PRE_META_INFO_7_TEXT'])
    dropping_columns.extend(['PST_PRIMER', 'PRE_LocationLatitude', 'PRE_LocationLatitude.1', 'PRE_LocationLatitude.2','PRE_LocationLongitude','PRE_LocationLongitude.1','PRE_LocationLongitude.2'])
    dropping_columns.extend(['PST_LocationLatitude', 'PST_LocationLatitude.1', 'PST_LocationLatitude.2','PST_LocationLongitude','PST_LocationLongitude.1','PST_LocationLongitude.2'])
    dropping_columns.extend(['PRE_LocationAccuracy', 'PRE_LocationAccuracy.1', 'PRE_LocationAccuracy.2'])
    dropping_columns.extend(['PST_LocationAccuracy', 'PST_LocationAccuracy.1', 'PST_LocationAccuracy.2'])


    # Delete extra instructor columns from predata set
    stop = col_index(mrgd_data, 'PRE_Firstname')
    i = inst_col_indx(mrgd_data) + 1

    while (i < stop):
        dropping_columns.append(mrgd_data.columns[i])
        i = i + 1

    # Delete extra instructor columns from postdata set
    j = inst_col_indx(mrgd_data) + 1 + len(data_pre.columns)
    stop = col_index(mrgd_data, 'PST_Firstname')

    while (j < stop):
        dropping_columns.append(mrgd_data.columns[j])
        j = j + 1

    # Remove instroctor instituition from column name
    inst_colname_pre = mrgd_data.columns[inst_col_indx(mrgd_data)]
    inst_colname_post = mrgd_data.columns[inst_col_indx(mrgd_data) + len(data_pre.columns)]

    # Drop 'em
    for to_drop in dropping_columns:
        try:
            mrgd_data.drop(to_drop, axis=1, inplace=True)
        except:
            pass

    #mrgd_data.rename(columns={inst_colname_pre: 'PRE_INSTR', inst_colname_post: 'PST_INSTR'}, inplace=True)

    return mrgd_data


def match(data_pre_prov, data_post_prov):
    '''
    A preliminary matching algorithm that uses first two letters of the simplified firstname,
    simplified full lastname and instituition, provided that the student has completed the session.

    *Names must be approximately similar (e.g. no spelling mistakes, no extra names).

    Required functions:
        str_simplify
        inst_col_indx
        col_index

    Args:
        data_pre_prov: The Pandas DataFrame of the pre-semester dataset.
        data_post_prov: The Pandas DataFrame of the post-semester dataset.

    Returns:
        no_match_pre: a Python list of int row-indeces for names that did not match in the pre data,
        no_match_post: a Python list of int row-indeces for names that did not match in the post data and
        pairs: a Python dictionary with int keys of int row-indeces for names that matched. First of the two elements
        in the list of each dictionary key is the pre_data row index and the second is the post_data row index.
        instructor_change: a Python dictionary with int keys of int row-indeces for students that changed instructors. First of the two elements
        in the list of each dictionary key is the pre_data row index and the second is the post_data row index.

    Examples:
        >>> print(prelim_no_matches_pre, prelim_no_matches_post, prelim_pairs = match(data_PRE, data_POST))
        '[5, 10, 15, 16, 34, ... etc]',

        '[0, 11, 12, 24, 34, ... etc]',

        '{0: [17, 22],
        1: [11, 271],
        2: [55, 667],
        ...
        880: [999, 1076],
        881: [1010, 1081]}'

        '{0: [5, 67],
        1: [7, 8],
        ...
        4: [25, 576]}'

    Future improvements:
        Better automated name-matching mechanism attempted.

    By:
        Ilija Nikolov, 17.07.17

    '''
    # Data variables
    pairs = {}
    no_match_pre = []
    no_match_post = []
    count = 0
    instructor_change = {}

    # Get Meta and INSTR columns from PRE and PST datasets
    the_list = ['Firstname', 'Lastname', 'PRE_COMPFLAG', 'SCHOOL', data_pre_prov.columns[inst_col_indx(data_pre_prov)]]
    data_pre = data_pre_prov[the_list]

    the_list = ['Firstname', 'Lastname', 'PST_COMPFLAG', 'SCHOOL', data_post_prov.columns[inst_col_indx(data_post_prov)]]
    data_post = data_post_prov[the_list]

    # Get INSTR column indexes from PRE and PST
    inst_col_pre = inst_col_indx(data_pre)
    inst_col_post = inst_col_indx(data_post)

    # Get index of SCHOOL column in PRE and PST
    schl_col_pre = col_index(data_pre, 'SCHOOL')
    schl_col_post = col_index(data_post, 'SCHOOL')

    # Index of Firstname and Lastname in PRE
    Fist_pre_inx = col_index(data_pre, 'Firstname')
    Last_pre_inx = col_index(data_pre, 'Lastname')

    # Index of Firstname and Lastname in PST
    Fist_post_inx = col_index(data_post, 'Firstname')
    Last_post_inx = col_index(data_post, 'Lastname')

    # For each name in PRE dataset
    for i in range(len(data_pre['Firstname'])):
        # If they completed everything
        if(data_pre.iloc[i, col_index(data_pre, 'PRE_COMPFLAG')] == 1):

            # First 2 letters of first name, full last name, and instructor
            PREnm = str_simplify(data_pre.iloc[i,Fist_pre_inx])[:2]
            PRElst = str_simplify(data_pre.iloc[i, Last_pre_inx])
            PREschl = data_pre.iloc[i,schl_col_pre]

            # For each name in PST dataset
            for j in range(len(data_post['Firstname'])):
                # If they completed everything
                if(data_post.iloc[j, col_index(data_post, 'PST_COMPFLAG')] == 1):

                    PSTnm = str_simplify(data_post.iloc[j,Fist_post_inx])[:2]
                    PSTlst = str_simplify(data_post.iloc[j, Last_post_inx])
                    PSTschl = data_post.iloc[j,schl_col_post]

                    if PREnm == PSTnm and PRElst == PSTlst and PREschl == PSTschl:
                        # Update data variables
                        pairs.update({count:(i,j)})

                        count += 1

                        # Record changes in instructor
                        if(data_pre.iloc[i,inst_col_pre] != data_post.iloc[j,inst_col_post]):
                            instructor_change.update({len(instructor_change): (i, j)})
                        break

                # No match --> add data to no_match_pre
                if(j == (len(data_post['Firstname']))-1):
                    no_match_pre.append(i)
        else:
            no_match_pre.append(i)


    # Find all indeces of non-matching data in PST dataset
    for name in range(len(data_post)):

        # Check if there is a match in the pairs dictionary
        for i in range((len(pairs)-1)):
            if(name == pairs[i][1]):
                break

            # No match --> add that row index to the no_match_post list
            if(i == ((len(pairs))-2)):
                no_match_post.append(name)

    return(no_match_pre, no_match_post, pairs, instructor_change)

def non_match(nomatches, df_prov):
    '''
    Takes a list of nomatches, uses the row indeces to get the names from the DataFrame
    in question and alphabetizes them according to the last name.
    It also adds a whitespace element each time the first letter changes.

    Required functions:
        str_simplify
        col_index

    Args:
        nomatches: Python list of int row indeces
        df_prov: The Pandas DataFrame in question

    Returns:
        List of str.

    Required modules:
        re

    Examples:
        >>> non_match(no_matches_pre, data_POST)
        ['Avarez, Fall', 'Automn, Spring', ' ','Boston, City','Beautiful, Person',' ',
        ...
        'Ze, Who']

    By:
        Ilija Nikolov, 24.07.17

    '''
    import re

    # Filter by name
    the_list = ['Firstname', 'Lastname']
    df = df_prov[the_list]

    names = []
    for i in range(len(nomatches)):
        Full_name = str( df.iloc[nomatches[i], col_index(df, 'Lastname')] ).strip() + ', ' +str(df.iloc[nomatches[i], col_index(df, 'Firstname')]).strip()
        names.append(Full_name)

    names_sorted = sorted(names, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())

    # Add " " to the list to separate groups of different starting letters of the string
    names = []
    for i in range(len(names_sorted)):
        first_letter = str_simplify(names_sorted[i])[:1]

        if(i < (len(names_sorted)-1)):
            if(first_letter != str_simplify(names_sorted[i+1])[:1]):
                names.append(names_sorted[i])
                names.append(" ")
            else:
                names.append(names_sorted[i])
        else:
            names.append(names_sorted[i])

    return names


def matches(pairs, df_pre_prov, df_post_prov):
    '''
    Takes a Python dictionary of pairs, uses the row indeces to get the names from the DataFrame
    in question and alphabetizes them according to the last name. First of the two is from the pre-dataset
    and the second should be similar and from the post-dataset. **If otherwise, error occured.**

    Required functions:
        col_index

    Args:
        pairs: Python list of int row indeces
        df_pre_prov: The Pandas DataFrame of the pre-semester dataset.
        df_post_prov: The Pandas DataFrame of the post-semester dataset.

    Returns:
        List of str.

    Required modules:
        re

    Examples:
        >>> non_match(no_matches_pre, data_POST)
        ['AUtoMN, Fall',
        'Automn, Fall',
        'Boston, City',
        'BOSTON, city,' ',
        ...
        'ze, WHO'
        'Ze, Who']

    Future improvements:
        Catch a potential error as described above.

    By:
        Ilija Nikolov, 24.07.17

    '''
    import re

    # Filter datasets by First and last names
    the_list = ['Firstname', 'Lastname']
    df_pre = df_pre_prov[the_list]
    df_post = df_post_prov[the_list]

    names = []
    for i in range(len(pairs)):
        Full_name_pre = str(df_pre.iloc[pairs[i][0],col_index(df_pre, 'Lastname')]).strip()+ ', '+str(df_pre.iloc[pairs[i][0],col_index(df_pre, 'Firstname')]).strip()
        names.append(Full_name_pre)

        Full_name_post = str(df_post.iloc[pairs[i][1],col_index(df_pre, 'Lastname')]).strip()+', '+str(df_post.iloc[pairs[i][1],col_index(df_pre, 'Firstname')]).strip()
        names.append(Full_name_post)

    return sorted(names, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())

def list_to_txtfile(kind, theList):
    '''
    Writes a list to a text file.

    Args:
        kind: str, "PRE" or "POST".
        theList: Python list of str.

    By:
        Ilija Nikolov, 30.07.17

    '''
    thefile = open(str(kind) +'_list.txt', 'w')
    for item in theList:
        thefile.write("%s\n" % item)


def match_refine(pre_nomatch, post_nomatch, pairs_transitional, df_pre_prov, df_post_prov, repeat_names_pre, repeat_names_post, instructor_change_1):
    '''
    A more advanced matching algorithm that accounts for a spelling error in the firstname or lastname.
    It takes into account the inclusion of nicknames, middlenames, as well as suffixes and prefixes.
    It will also mark a change in the instructor.
    Gets rid of the doubles in the nomatches list.
    In the pairs, it gets rid of for the repeating matches, keeping the one the first time it was taken it.

    Required functions:
        str_simplify
        inst_col_indx
        col_index
        repeating_names
        match

    Args:
        pre_nomatch: Python list of int row indeces of inputs in the pre-semester dataset
        post_nomatch: Python list of int row indeces of inputs in the post-semester dataset
        pairs_transitional: Python int key dictionary of int row indeces of matching pairs
        df_pre_prov: The Pandas DataFrame of the pre-semester dataset.
        df_post_prov: The Pandas DataFrame of the post-semester dataset.
        repeat_names_pre: Python int key dictionary of int row indeces of any retakes in the pre-semester dataset
        repeat_names_post: Python int key dictionary of int row indeces of any retakes in the post-semester dataset
        instructor_change_1:  Python int key dictionary of int row indeces/students that have an instructor change

    Returns:
        nomatch_pre: a Python list of int row-indeces for names that did not match in the pre data,
        nomatch_post: a Python list of int row-indeces for names that did not match in the post data and
        pairs_refined_2: a Python dictionary with int keys of int row-indeces for names that matched. First of the two elements
        in the list of each dictionary key is the pre_data row index and the second is the post_data row index.
        instructor_change: a Python int key dictionary of int row indeces where the a pair of an instructor change is indicated

    Required modules:
        re
        copy

    Examples:
        >>> print(no_matches_pre, no_matches_post, pairs, instructor_change = match_refine(prelim_no_matches_pre, prelim_no_matches_post, prelim_pairs, data_PRE, data_POST, retakes_pre, retakes_post))
        ''[5, 10, 15, 16, 34, ... etc]',

        '[0, 11, 12, 24, 34, ... etc]',

        '{0: [17, 22],
        1: [11, 271],
        2: [55, 667],
        ...
        880: [999, 1076],
        881: [1010, 1081]}'

        '{0: [7, 895],
        1: [1, 71],
        2: [69, 67],
        ...
        5: [14, 85]''

    Future improvements:
        Better matching mechanism that would for example catch nicknames like Liz. A dictionary of nicknames could be used.
        There is also a similartiy code that will give a score of how similar two strings are.

    By:
        Ilija Nikolov, 28.07.17

    '''
    import re
    import copy

    #slicing out the dataframes for speed
    the_list = ['Firstname', 'Lastname', 'PRE_COMPFLAG','SCHOOL', df_pre_prov.columns[inst_col_indx(df_pre_prov)]]
    df_pre = df_pre_prov[the_list]

    the_list = ['Firstname', 'Lastname', 'PST_COMPFLAG','SCHOOL', df_post_prov.columns[inst_col_indx(df_post_prov)]]
    df_post = df_post_prov[the_list]


    #makeing a copy of the list due to links created
    nomatch_pre = copy.deepcopy(pre_nomatch)
    nomatch_post = copy.deepcopy(post_nomatch)
    pairs = copy.deepcopy(pairs_transitional)
    instructor_change = copy.deepcopy(instructor_change_1)

    inst_col_pre = inst_col_indx(df_pre)
    inst_col_post = inst_col_indx(df_post)

    #column indeces initialization
    Fist_pre_inx = col_index(df_pre, 'Firstname')
    Last_pre_inx = col_index(df_pre, 'Lastname')

    Fist_post_inx = col_index(df_post, 'Firstname')
    Last_post_inx = col_index(df_post, 'Lastname')

    #accounting for potential spelling mistakes
    #compare the lenth of the string (first and last name) and tollerate only one string(+/-) difference
    #first and last simplified string character of the first and last name must be the same
    for i in range(len(pre_nomatch)):

        if(df_pre.iloc[pre_nomatch[i], col_index(df_pre, 'PRE_COMPFLAG')] == 1):

            nm_char_pre = str_simplify(df_pre.iloc[pre_nomatch[i],Fist_pre_inx])[:1] + str_simplify(df_pre.iloc[pre_nomatch[i],Fist_pre_inx])[-1:]
            nm_len_pre = len(str_simplify(df_pre.iloc[pre_nomatch[i],Fist_pre_inx]))

            lst_char_pre = str_simplify(df_pre.iloc[pre_nomatch[i], Last_pre_inx])[:1] + str_simplify(df_pre.iloc[pre_nomatch[i],Last_pre_inx])[-1:]
            lst_len_pre = len(str_simplify(df_pre.iloc[pre_nomatch[i], Last_pre_inx]))

            inst = df_pre.iloc[pre_nomatch[i],inst_col_pre]

            for j in range(len(post_nomatch)):

                if(inst == df_post.iloc[post_nomatch[j],inst_col_post] and df_post.iloc[post_nomatch[j], col_index(df_post, 'PST_COMPFLAG')] == 1):

                    nm_char_post = str_simplify(df_post.iloc[post_nomatch[j],Fist_post_inx])[:1] + str_simplify(df_post.iloc[post_nomatch[j],Fist_post_inx])[-1:]
                    nm_len_post = len(str_simplify(df_post.iloc[post_nomatch[j],Fist_post_inx]))

                    if ((nm_char_pre == nm_char_post) and (nm_len_pre - 1 <= nm_len_post <= nm_len_pre + 1)):

                        lst_char_post = str_simplify(df_post.iloc[post_nomatch[j], Last_post_inx])[:1] + str_simplify(df_post.iloc[post_nomatch[j], Last_post_inx])[-1:]
                        lst_len_post = len(str_simplify(df_post.iloc[post_nomatch[j], Last_post_inx]))

                        if((lst_char_pre == lst_char_post) and (lst_len_pre - 1 <= lst_len_post <= lst_len_pre + 1)):

                            pairs.update({len(pairs): (pre_nomatch[i], post_nomatch[j])})
                            try:
                                nomatch_post.remove(post_nomatch[j])
                            except ValueError:
                                continue
                            try:
                                nomatch_pre.remove(pre_nomatch[i])
                            except ValueError:
                                continue

                            break

    #makeing a copy of the list due to, again, links created
    pre_nomatch_trans = copy.deepcopy(nomatch_pre)
    post_nomatch_trans = copy.deepcopy(nomatch_post)

    #accounting for firstnames or lastnames which consist of two parts, once spaces used and once capital letters with no spaces
    #accounting for instructor change as well, provided the instituition is the same
    for i in range(len(pre_nomatch_trans)):

        if(df_pre.iloc[pre_nomatch_trans[i], col_index(df_pre, 'PRE_COMPFLAG')] == 1):

            #tries to separate by using capital letters
            lst_pre = df_pre.iloc[pre_nomatch_trans[i], Last_pre_inx].strip()
            lasts_pre =  re.findall('[A-Z][^A-Z]*', lst_pre)

            #check of the length of the list created by this separation

            #no separation created, means it is all small caps
            if(len(lasts_pre) == 0):
                lasts_pre.append(str_simplify(lst_pre))

            elif(len(lasts_pre)>2 and len(lasts_pre)<=4):
                for n in range(len(lasts_pre)):
                    lasts_pre[n] = str_simplify(lasts_pre[n])

            elif(len(lasts_pre)>4):
                        name_ex = []
                        name_ex.append('')
                        for n in range(len(lasts_pre)):
                            name_ex[0] = name_ex[0]+str_simplify(lasts_pre[n])
                        lasts_pre = copy.deepcopy(name_ex)

            elif(len(lst_pre.split(' '))>1):
                lasts_pre = lst_pre.split(' ')
                for n in range(len(lasts_pre)):
                    lasts_pre[n] = str_simplify(lasts_pre[n])
            else:
                lasts_pre[0] = str_simplify(lasts_pre[0])

            #repeats this method four times for the first and last names of the pre and post

            nm_pre = df_pre.iloc[pre_nomatch_trans[i],Fist_pre_inx].strip()
            names_pre = re.findall('[A-Z][^A-Z]*', nm_pre)

            if(len(names_pre) == 0):
                names_pre.append(str_simplify(nm_pre))

            elif(len(names_pre)>2 and len(names_pre) <=4):
                for n in range(len(names_pre)):
                    names_pre[n] = str_simplify(names_pre[n])

            elif(len(names_pre)>4):
                        name_ex = []
                        name_ex.append('')
                        for n in range(len(names_pre)):
                            name_ex[0] = name_ex[0]+str_simplify(names_pre[n])
                        names_pre = copy.deepcopy(name_ex)

            elif(len(nm_pre.split(' '))>1):
                names_pre = nm_pre.split(' ')
                for n in range(len(names_pre)):
                    names_pre[n] = str_simplify(names_pre[n])
            else:
                names_pre[0] = str_simplify(names_pre[0])

            for j in range(len(post_nomatch_trans)):

                if((df_pre.iloc[pre_nomatch_trans[i],col_index(df_pre,'SCHOOL')] == df_post.iloc[post_nomatch_trans[j],col_index(df_post,'SCHOOL')]) and (df_post.iloc[post_nomatch_trans[j], col_index(df_post, 'PST_COMPFLAG')] == 1)):

                    lst_post = df_post.iloc[post_nomatch_trans[j], Last_post_inx].strip()
                    lasts_post =  re.findall('[A-Z][^A-Z]*', lst_post)

                    if(len(lasts_post) == 0):
                       lasts_post.append(str_simplify(lst_post))

                    elif(len(lasts_post)>2 and len(lasts_post)<=4):
                        for n in range(len(lasts_post)):
                            lasts_post[n] = str_simplify(lasts_post[n])

                    elif(len(lasts_post)>4):
                        name_ex = []
                        name_ex.append('')
                        for n in range(len(lasts_post)):
                            name_ex[0] = name_ex[0]+str_simplify(lasts_post[n])
                        lasts_post = copy.deepcopy(name_ex)

                    elif(len(lst_post.split(' '))>1):
                        lasts_post = lst_post.split(' ')
                        for n in range(len(lasts_post)):
                            lasts_post[n] = str_simplify(lasts_post[n])
                    else:
                        lasts_post[0] = str_simplify(lasts_post[0])


                    nm_post = df_post.iloc[post_nomatch_trans[j],Fist_post_inx].strip()
                    names_post = re.findall('[A-Z][^A-Z]*', nm_post)

                    if(len(names_post) == 0):
                       names_post.append(str_simplify(nm_post))

                    elif(len(names_post)>2 and len(names_post)<=4):
                        for n in range(len(names_post)):
                            names_post[n] = str_simplify(names_post[n])

                    elif(len(names_post)>4):
                        name_ex = []
                        name_ex.append('')
                        for n in range(len(names_post)):
                            name_ex[0] = name_ex[0]+str_simplify(names_post[n])
                        names_post = copy.deepcopy(name_ex)

                    elif(len(nm_post.split(' '))>1):
                        names_post = nm_post.split(' ')
                        for n in range(len(names_post)):
                            names_post[n] = str_simplify(names_post[n])
                    else:
                        names_post[0] = str_simplify(names_post[0])

                    #actually checking if any of the elements in the firstnames or lastnames arrays match
                    bool_first, bool_last = False, False

                    for u in range(len(names_pre)):
                        if((names_pre[u] in names_post) or (names_pre[u] in lasts_post)):
                            bool_first = True

                    for u in range(len(lasts_pre)):
                        if(lasts_pre[u] in lasts_post):
                            bool_last = True

                    if(bool_last and bool_first):
                        pairs.update({len(pairs): (pre_nomatch_trans[i], post_nomatch_trans[j])})
                        try:
                            nomatch_post.remove(post_nomatch_trans[j])
                            nomatch_pre.remove(pre_nomatch_trans[i])
                        except ValueError:
                            continue
                        #indicate an instructor change
                        if(df_pre.iloc[pre_nomatch_trans[i],inst_col_pre] != df_post.iloc[post_nomatch_trans[j],inst_col_post]):
                            instructor_change.update({len(instructor_change): (pre_nomatch_trans[i], post_nomatch_trans[j])})

                        break

    #only keep first of the pairs (aplies to the repeating names)
    #meaning that the first time takes will be saved
    pairs_refined_1 = {}
    remove = []
    for i in range(len(repeat_names_pre)):
        check = False
        for j in range(len(repeat_names_pre[i])):
            if(not check):
                for k in range(len(pairs)):
                    if(repeat_names_pre[i][j] == pairs[k][0]):
                        check = True
                        jth = j
                        break
            if(check):
                for u in range(len(repeat_names_pre[i])):
                    if(u != jth):
                        for k in range(len(pairs)):
                            if(repeat_names_pre[i][u] == pairs[k][0]):
                                remove.append(k)


    for i in range(len(repeat_names_post)):
        check = False
        for j in range(len(repeat_names_post[i])):
            if(not check):
                for k in range(len(pairs)):
                    if(repeat_names_post[i][j] == pairs[k][1]):
                        check = True
                        jth = j
                        break
            if(check):
                for u in range(len(repeat_names_post[i])):
                    if(u != jth):
                        for k in range(len(pairs)):
                            if(repeat_names_post[i][u] == pairs[k][1]):
                                remove.append(k)
    for i in range(len(pairs)):
        if(not (i in remove)):
            pairs_refined_1.update({len(pairs_refined_1): (pairs[i][0], pairs[i][1])})


    #getting rid of the retakes in the nomatch-lists


    for i in range(len(repeat_names_pre)):
        for j in range(len(repeat_names_pre[i])):
                try:
                    nomatch_pre.remove(repeat_names_pre[i][j])
                except ValueError:
                    continue

    for i in range(len(repeat_names_post)):
        for j in range(len(repeat_names_post[i])):
                try:
                    nomatch_post.remove(repeat_names_post[i][j])
                except ValueError:
                    continue

    return nomatch_pre, nomatch_post, pairs_refined_1, instructor_change


def comments_fill(kind, nomatch, df, df_drop, repeat, instructor_change):
    '''
    Fils out columns about which kinds of exams were taken, a number of admins and an instructor change

    Required functions:
        col_index

    Args:
        kind: str, "PRE" or "POST"
        nomatch: Python int key dictionary of int row indeces of studentes with nomathces
        df: Pandas DataFrame of the dataset in question
        repeat: Python int key dictionary of int row indeces of students whose number of administration is greater than 1
        instructor_change: Python int key dictionary of int row indeces of students with instructor change

    By:
        Ilija Nikolov, 03.08.17

    '''
    comments_indx = col_index(df, "NUMREPS")

    #there is a problem with this piece of coding specifically
    #when the len(repeat[i]) == 3, it execudes twice the code? :/
    for i in range(len(repeat)):
        for j in range(len(repeat[i])):
            df.iloc[repeat[i][j], comments_indx] = str(j+1)+" of "+str(len(repeat[i]))

    comments_indx = col_index(df_drop, "WHICHADMIN")
    for i in range(len(df_drop)):
        if(kind == "PRE"):
            df_drop.iloc[i, comments_indx] = "PARTIAL SESSION"
        elif(kind == "PST"):
            df_drop.iloc[i, comments_indx] = "PARTIAL SESSION"

    comments_indx = col_index(df, "INST_CHANGE")

    # Indicate instructor change
    for i in range(len(instructor_change)):
        if(kind == "PRE"):
            df.iloc[instructor_change[i][0], comments_indx] = "YES"

        elif(kind == "PST"):
            df.iloc[instructor_change[i][1], comments_indx] = "YES"


def standardize(df, typ):
    lst = df.columns

    for i in range(len(lst)):
        check = lst[i].split("_")

        if(check[0] != typ):
            df.rename(columns={df.columns[i]: (typ + "_" + df.columns[i])}, inplace=True)

    return df


def public_data_anonym(pub_data_1, repeat_pre, repeat_post, both_len, onlyPre_len, onlyPost_len, kind):
    '''
    Retruns an anonymized public dataset, where students' names are changed with anonymous identifiers,
    instructors with instructor identifiers, and institutions with institutional type.
    It also adds a general course descriptor column.

    Required functions:
        str_simplify
        inst_col_indx
        col_index
        repeating_names
        match
        match_refine
        merger
        public_merged

    Args:
        pub_data_1: The Pandas DataFrame of the public merged dataset.
        repeat_pre: Python int key dictionary of int row indeces of any retakes in the pre-semester dataset
        repeat_post: Python int key dictionary of int row indeces of any retakes in the post-semester dataset
        both_len: int of the length of the pairs
        onlyPre_len: int of the length of the nomatches in the pre-semester dataset
        onlyPost_len: int of the length of the nomatches in the post-semester dataset
        kind: str of the semester and the year, examples: "F16", "S15", etc.

    Returns:
        pub_data: Pandas DataFrame

    Required modules:
        random
        pandas as pd
        numpy as np
        copy
        math


    By:
        Ilija Nikolov, 02.07.17

    '''
    import random
    import pandas as pd
    import numpy as np
    import copy

    pub_data = copy.deepcopy(pub_data_1)
    random_nums = []

    pub_data.insert(0, "ADMINISTRATION", kind)

    col_track = col_index(pub_data,'PRE_RETAKE_TRACKER')
    Fst_col_pre = col_index(pub_data,'PRE_Firstname')
    total_students = len(pub_data)

    #just for the pairs
    for i in range(both_len):
        while True:
            num_stu = random.randint(1,total_students + 1)
            if(not (num_stu in random_nums)):
                random_nums.append(num_stu)
                break

        #code to add zeroes as a prefix
        while(len(str(num_stu)) < 4):
            num_stu='0' + str(num_stu)

        code_stu = kind + "S" + str(num_stu)
        pub_data.iloc[i, Fst_col_pre] = code_stu
    #rest of the pre
    j = both_len

    while(type(pub_data.iloc[j, Fst_col_pre]) == str):
        track = pub_data.iloc[j, col_track]
        if(type(track) != str):

            while True:
                num_stu = random.randint(1,total_students + 1)
                if(not (num_stu in random_nums)):
                    random_nums.append(num_stu)
                    break

            #code to add zeroes as a prefix
            while(len(str(num_stu)) < 4):
                num_stu='0' + str(num_stu)

            code_stu = kind + "S" + str(num_stu)
            pub_data.iloc[j, Fst_col_pre] = code_stu

        else:

            for i in range(len(repeat_pre)):
                for k in range(len(repeat_pre[i])):
                    if(track == str(repeat_pre[i][k])):
                        break
                if(track == str(repeat_pre[i][k])):
                    break
            ith = i

            while True:
                num_stu = random.randint(1,total_students + 1)
                if(not (num_stu in random_nums)):
                    random_nums.append(num_stu)
                    break

            #code to add zeroes as a prefix
            while(len(str(num_stu)) < 4):
                num_stu='0' + str(num_stu)

            code_stu = kind + "S" + str(num_stu)
            pub_data.iloc[j, Fst_col_pre] = code_stu

            k = 0
            while(k < len(repeat_pre[ith])):
                i = 0
                while (type(pub_data.iloc[i, 3]) == str):
                    if(str(repeat_pre[ith][k]) == str(pub_data.iloc[i, col_track])):
                        pub_data.iloc[i, Fst_col_pre] = code_stu
                        if(i < both_len):
                            pub_data.iloc[i, col_index(pub_data, 'PRE_WHICHADMIN')] = 'BOTH'
                            pub_data.iloc[j, col_index(pub_data, 'PST_WHICHADMIN')] = 'BOTH'
                        break
                    i = i + 1
                k = k + 1

        j = j + 1
    #post-only, no matches in the pre, but possible retakes

    col_track_post = col_index(pub_data, 'PST_RETAKE_TRACKER')
    Fst_col_post = col_index(pub_data, 'PST_Firstname')

    cnt = j
    strt = j
    while (cnt < len(pub_data)):
        track = pub_data.iloc[cnt, col_track_post]
        if(type(track) != str):
            while True:
                num_stu = random.randint(1,total_students + 1)
                if(not (num_stu in random_nums)):
                    random_nums.append(num_stu)
                    break


            #code to add zeroes as a prefix
            while(len(str(num_stu)) < 4):
                num_stu='0' + str(num_stu)

            code_stu = kind + "S" + str(num_stu)
            pub_data.iloc[cnt, Fst_col_post] = code_stu

        else:
            for i in range(len(repeat_post)):
                for k in range(len(repeat_post[i])):
                    if(track == str(repeat_post[i][k])):
                        break
                if(track == str(repeat_post[i][k])):
                    break
            ith = i

            while True:
                num_stu = random.randint(1,total_students + 1)
                if(not (num_stu in random_nums)):
                    random_nums.append(num_stu)
                    break

            #code to add zeroes as a prefix
            while(len(str(num_stu)) < 4):
                num_stu='0' + str(num_stu)

            code_stu = kind + "S" + str(num_stu)
            pub_data.iloc[cnt, Fst_col_post] = code_stu

            k = 0
            while(k < len(repeat_post[ith])):
                i = strt
                while (i < len(pub_data)):
                    if(str(repeat_post[ith][k]) == str(pub_data.iloc[i, col_track_post])):
                        pub_data.iloc[i, Fst_col_post] = code_stu
                        break
                    i = i + 1
                k = k + 1

        cnt = cnt + 1

    #copying for the pairs in the post from the pre
    for i in range(both_len):
        pub_data.iloc[i, Fst_col_post] = pub_data.iloc[i, Fst_col_pre]

    #accounting for any retakes in the post_only data and the pairs
    for i in range(both_len):
        track = pub_data.iloc[i,col_track_post]
        if(type(track) == str):

            for u in range(len(repeat_post)):
                for q in range(len(repeat_post[u])):
                    if(track == str(repeat_post[u][q])):
                        break
                if(track == str(repeat_post[u][q])):
                    break

            ith = u

            j = strt
            while(j < len(pub_data)):
                if( type(pub_data.iloc[j,col_track_post]) == str):
                    k=0
                    while(k < len(repeat_post[ith])):
                        if(str(pub_data.iloc[j,col_index(pub_data, 'PST_RETAKE_TRACKER')]) == str(repeat_post[ith][k])):
                            pub_data.iloc[j, Fst_col_post] = pub_data.iloc[i, Fst_col_post]
                            pub_data.iloc[j, col_index(pub_data, 'PST_WHICHADMIN')] = 'BOTH'
                        k = k + 1
                j = j + 1

    #dropping unnecessary columns
    to_drop = ['PRE_Lastname', 'PRE_RETAKE_TRACKER', 'PST_Lastname', 'PST_RETAKE_TRACKER']
    pub_data.drop(to_drop, axis=1, inplace=True)

    #renaming columns
    pub_data.rename(columns={'PRE_Firstname': 'STUDENT_CODE'}, inplace=True)

    #Getting rid of extra student code column

    #pub_data.insert(col_index(pub_data, 'STUDENT_CODE'), "STUDENT_CODE_PRE", pub_data.iloc[:,col_index(pub_data,'STUDENT_CODE')])

    #pub_data.insert(col_index_second(pub_data, 'STUDENT_CODE'), "STUDENT_CODE_PST", pub_data.iloc[:,col_index_second(pub_data,'STUDENT_CODE')])

    id1 = col_index(pub_data, 'STUDENT_CODE')
    #print(id1)
    id2 = col_index(pub_data, 'PST_Firstname')
    #print(id2)

    for i in range(len(pub_data.iloc[:, id2])):
        if(pd.isnull(pub_data.iloc[i, col_index(pub_data, 'STUDENT_CODE')])):
            pub_data.iloc[i, col_index(pub_data, 'STUDENT_CODE')] = pub_data.iloc[i, id2]
    pub_data.drop(pub_data.columns[id2], axis=1, inplace = True)
    #pub_data.drop(pub_data.columns[col_index(pub_data, 'STUDENT_CODE_PST')], axis=1, inplace = True)
    #pub_data.rename(columns={'STUDENT_CODE_PRE': 'STUDENT_CODE'}, inplace=True)
    #print(pub_data.columns[id1])
    #print(pub_data.columns[id2])
    #print(col_index(pub_data, 'STUDENT_CODE_'))
    return pub_data



#returns the private data with the anonymized columns
def anonym_adder(columns_pre_len, data_priv_1, data_pub):
    '''
    Adds the annonymized columns in the private data_set.

    Required functions:
        inst_col_indx
        col_index
        repeating_names
        match
        match_refine
        merger
        public_merged
        public_data_anonym

    Args:
        mrgd_data_1: The Pandas DataFrame of the merged dataset
        data_pre: The Pandas DataFrame of the pre-semester dataset.

    Returns:
        mrgd_data: Pandas DataFrame

    Required modules:
        copy

    By:
        Ilija Nikolov, 01.08.17

    '''
    import copy
    data_priv = copy.deepcopy(data_priv_1)

    data_priv.insert(col_index(data_priv, 'PRE_Firstname'), "STUDENT_CODE", data_pub.iloc[:,col_index(data_pub,'STUDENT_CODE')])

    #data_priv.insert(col_index_second(data_priv, 'Firstname'), "STUDENT_CODE_PST", data_pub.iloc[:,col_index_second(data_pub,'STUDENT_CODE')])

    #data_priv.drop('WHICHADMIN', axis=1, inplace=True)

    #data_priv.insert(col_index(data_priv, 'INST_CHANGE')+1, 'WHICHADMIN_PRE', data_pub.iloc[:,col_index(data_pub,'WHICHADMIN')])
    #data_priv.insert(col_index_second(data_priv, 'INST_CHANGE')+1, 'WHICHADMIN_PST', data_pub.iloc[:,col_index_second(data_pub,'WHICHADMIN')])

    data_priv.insert(0, 'ADMINISTRATION', data_pub['ADMINISTRATION'])

    data_priv.drop('PST_RETAKE_TRACKER', axis=1, inplace=True)
    data_priv.rename(columns={'PRE_RETAKE_TRACKER': 'RETAKE_TRACKER'}, inplace=True)

    dropping_columns = []
    dropping_columns.extend(['Unnamed: 0','Unnamed: 0.1', 'Unnamed: 0.2'])
    for to_drop in dropping_columns:
        try:
            data_priv.drop(to_drop, axis=1, inplace=True)
        except:
            pass

    return data_priv
