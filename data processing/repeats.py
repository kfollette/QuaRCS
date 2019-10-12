import pandas as pd
import numpy as np


def repeats(database, semester):
    '''
    Identifies all repeat administrations of the exam to an individual student.
    Their first complete assessment is retained and passed on, while a file containing
    all exams taken by students who took repeat administrations is also produced.

    Returns a dataframe without repeat administrations and a .csv of all repeat administrations.


    *Names must be approximately similar (e.g. no spelling mistakes, no extra names).

    Required functions:
        str_simplify
        col_index

    Args:
        database: The Pandas DataFrame in question.
        semester: PRE/PST

    Returns:
        database

        Repeats.csv
        Example: PRE_S18_Repeats.csv


    Future improvements:
        Better name-matching mechanism.

    Originally By:
        Ilija Nikolov, 20.07.17

    '''
    data = database
    #data = pd.read_csv(database, encoding = 'utf-8', header = 0)
    #savedname = database[:-4]

    data = data.reset_index(drop=True)

    repeats = {}
    bol = True

    #slicing out the dataframe for speed
    df = data[semester + '_STUDENT_ID']

    #Create template datafrane for repeats
    toExport = pd.DataFrame(data)
    toExport = toExport.iloc[0:0]

    i = 0

    #for loop to go through all student IDs
    while (i < len(df)):
        #Check if index exists
        if (i in df.index):

            ID = df[i]


            #for k in range(len(repeats)):
                #Check if index exists
                #if (k in df.index):
                    #if(i in repeats[k]):
                        #bol = False

            if(bol):
                list = []

                #while loop to check IDs starting under specified position
                j = i + 1
                list.append(i)

                while (j < len(df)):
                    #Check if index exists
                    if(j in df.index):

                        #Check for duplicate student IDs
                        if(df[j] == ID):
                            #print('j: ' + df[j] + ' ID: ' + ID)
                            list.append(j)

                    j = j + 1

                if(len(list)>1):
                    #updates the dictionary
                    repeats.update({ID:(list)})

            bol = True

        i = i + 1

    for x in repeats:
        instances = repeats.get(x)
        #print(instances)
        length = len(instances)
        q = 1
        for y in instances:
            data.loc[y, semester+'_NUM_REPEATS'] = length
            toExport = toExport.append(data.loc[y], ignore_index = True)
            if(q > 1):
                data = data.drop([y], axis = 0)
            q = q+1


    #Uncomment to write repeats for export
    #toExport.to_csv(semester+"_repeats.csv", encoding='utf-8',index=False)

    #print("Saved repeat entries to " + semester+"_repeats.csv")


    #returns data without repeat administrations
    #data.to_csv(semester+"_test.csv", encoding='utf-8',index=False)

    return data


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
