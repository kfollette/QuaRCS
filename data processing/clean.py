import pandas as pd
import numpy as np
import copy
import pickle

def clean(database, semester):

    # data = pd.read_csv(database, encoding = 'utf-8', header = 0)
    # savedname = database[:-4]
    data = database
    #if semester == "PRE":
    #    with open ('pre_list', 'rb') as fp:
    #        col_list = pickle.load(fp)
    #else:
    #    with open ('pst_list', 'rb') as fp:
    #        col_list = pickle.load(fp)
    if semester == "PRE":
        with open ('prelist.pkl', 'rb') as fp:
            col_list = pickle.load(fp)
    else:
        with open ('pstlist.pkl', 'rb') as fp:
            col_list = pickle.load(fp)

    data["INST_CHANGE"] = np.nan
    data["WHICHADMIN"] = np.nan
    data["NUM_REPEATS"] = 1

    data_old = copy.deepcopy(data)

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
    data_trans = data_old[data_old[semester + '_COMPFLAG'] == 1]

    #filtering out sessions with no name provided
    data_provis = data_old[pd.notnull(data_old['Firstname']) & pd.notnull(data_old['Lastname'])]

    #filtering out sessions with one character names
    data_interim = data_provis[(data_provis['Firstname'].str.len() > 1) & (data_provis['Lastname'].str.len() > 1)]

    data_new = copy.deepcopy(data_interim)

    index_old = data[data.columns[0]].index.tolist()
    index_new = data_new[data_new.columns[0]].index.tolist()

    indeces_dropped = []
    for i in index_old:
        if(i not in index_new):
            indeces_dropped.append(i)
    #indeces_dropped = indeces_dropped[2:]

    df_1 = pd.DataFrame()
    for i in indeces_dropped:
        df_1 = df_1.append(data.loc[i,:], ignore_index=True)
    data_dropped = pd.DataFrame(data=df_1, columns = data.columns.tolist())


    #Write no name sessions for export
    #data_no_name = data_old[pd.isnull(data_old['Firstname']) & pd.isnull(data_old['Lastname'])]

    # Uncomment to save to file:
    # data_no_name.to_csv(savedname+"_no_name.csv", encoding='utf-8',index=False)
    # print("No name results saved to " + savedname + "_no_name.csv")


    #Write incomplete sessions for export
    #data_incomplete = data_old[data_old[semester + '_COMPFLAG'] == 0]

    # Uncomment to save to file:
    #data_incomplete.to_csv(savedname+"_incomplete.csv", encoding='utf-8',index=False)
    #print("Incomplete results saved to " + savedname + "_incomplete.csv")

    h = len(data_new)
    data_new = data_new.reset_index(drop=True)
    #fix usedu column. 2 = No, 1 = Yes, so will change to 2 = 0 = No
    for i in range(h):
        if (semester == "PRE"):
            if(data_new.loc[i, 'PRE_USEDU'] == 2):
                data_new.loc[i, 'PRE_USEDU'] = 0
    #Drop columns
    data_new = data_new.drop(['Status'], axis=1)
    data_new = data_new.drop(['UserLanguage'], axis=1)
    data_new = data_new.drop(['IPAddress'], axis=1)
    data_new = data_new.drop(['EndDate'], axis=1)
    data_new = data_new.drop(['DistributionChannel'], axis=1)
    data_new = data_new.drop(['Finished'], axis=1)
    data_new = data_new.drop(['RecordedDate'], axis=1)
    data_new = data_new.drop(['RecipientLastName'], axis=1)
    data_new = data_new.drop(['RecipientFirstName'], axis=1)
    data_new = data_new.drop(['RecipientEmail'], axis=1)
    data_new = data_new.drop(['ExternalReference'], axis=1)

        #data_new = data_new.drop(['META_INFO_Browser'], axis=1)
        #data_new = data_new.drop(['META_INFO_Resolution'], axis=1)
        #data_new = data_new.drop(['META_INFO_Version'], axis=1)


    if("LocationLatitude" in data_new.columns):
        data_new = data_new.drop(['LocationLatitude'], axis=1)
    if("LocationLongitude" in data_new.columns):
        data_new = data_new.drop(['LocationLongitude'], axis=1)
    if("PRE_YEAR_5_TEXT - Topics" in data_new.columns):
        data_new = data_new.drop(['PRE_YEAR_5_TEXT - Topics'], axis=1)
    if("Firstname - Topics " in data_new.columns):
        data_new = data_new.drop(['Firstname - Topics'], axis=1)

    #Add comment's/flags if they aren't already there
    if ('COMMENTS' not in data_new.columns):
        data_new['COMMENTS'] = ""

    #for v in range(h):
        #if(data_new.loc[v, 'DistributionChannel'] == "preview"):
            #data_new = data_new.drop([v])


    #Add PRE/PST to unlabeled columns
    lst = data_new.columns
    for v in range(len(lst)):
        check = lst[v].split("_")
        if(check[0] != semester):
            data_new.rename(columns={data_new.columns[v]: (semester + "_" + data_new.columns[v])}, inplace=True)


    cols = data_new.columns
    for i in range(len(cols)):
        check = cols[i].split("_")
        if ('INSTR' in check):
            break


    inst_col = i

    data_new.insert(inst_col, semester+'_COURSE', np.nan)
    data_new.insert(inst_col, semester+'_INSTR', np.nan)


    #for-loop to go through the instructors
    j = inst_col + 2
    cols = data_new.columns
    check = cols[j].split("_")
    while((check[1]) == "INSTR" or (check[1]) == "PCCINS" or (check[1]) == "SFSU" or (check[1]) == "PCCCRS"):
        for i in range(len(data_new.iloc[:,inst_col])):
            if(pd.notnull(data_new.iloc[i,j])):
                if(pd.notnull(data_new.iloc[i,inst_col])):
                    data_new.iloc[i,(inst_col + 1)] = data_new.iloc[i,j]
                else:
                    data_new.iloc[i,(inst_col)] = data_new.iloc[i,j]
        j = j + 1
        check = cols[j].split("_")
    for i in range((inst_col + 2), j):
        #print(cols[i])
        data_new = data_new.drop(cols[i], axis=1)

    #standardizing columns
    for i in col_list:
        data_list = data_new.columns
        if (i not in data_list):
            #print(i)
            data_new.insert(0, i, np.nan)

    data_new = data_new.reindex(sorted(data_new.columns), axis=1)


    # Uncomment to save to file
    #data_new.to_csv(savedname+"_cleaned.csv", encoding='utf-8',index=False)
    #data_new.to_csv(semester + "_thing.csv", encoding='utf-8',index=False)
    # print("Results saved to " + savedname + "_cleaned.csv")
    return data_new

    #Legacy Cleaning
    '''
    Returns an automatically polished DataFrame, where any rows containing no names,
    or one-character names are dropped and returned in SEMESTER_no_name.csv.
    It also checks if the name is provided in one cell and makes sure that it is split
    into the two cells - Firstname and Lastname.
    It adds logistical columns at the end of the DataFrame.
    Drops incomplete data and returns those rows in SEMESTER_incomplete.csv.

    Args:
        database: The Pandas DataFrame in question.
        semester: PRE/PST

    Returns:
        data_new: Pandas DataFrame that is automatically cleaned
        SEMESTER_incomplete.csv: File containing the incomplete rows
        SEMESTER_no_name.csv:	File containing rows with no name

    Future improvements:

    Required modules:
        import pandas as pd
        import numpy as np
        import copy

    Originally By:
        Ilija Nikolov, 30.07.17

    '''

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
