from factor_analyzer import FactorAnalyzer, Rotator, calculate_bartlett_sphericity, calculate_kmo
from sklearn.utils import check_array
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

def score(database, semester, year, season, answer_key, savedname):
    '''
    Modified so that it uses numerical values of question/answer rather than string values.
    By:
        Ilija Nikolov, 5 March 2018
    '''

    '''
        The score function reads in a QuaRCS dataset and answer key file to create a series of columns
        to add to the dataset. The function creates columns for:
        - score on a binary scale (1 for correct, 0 for incorrect)
        - total score
        - totals and means by category
        - number of questions answered
        - total and mean confidence
        Args:
            database: pre or post QuaRCS dataset for a semester
            answer_key: QuaRCS Assessment Answer Key
            semester: 'PRE' or 'PST'
        Output:
            name of file + '_scored' as .csv file
        Example:
            score('QuaRCS_Summer_2017_Pre.csv', 'PRE', QuaRCS Assessment Answer Key.csv', QuaRCS_Summer_2017_Pre )
            New File saved under QuaRCS_Summer_2017_Pre_scored.csv
            Check folder for files
        By:
            Abdoulaye Sanogo, 08/11/2017
        Future Improvements:
            add columns for confidence means and totals by category
            add extra colums after insert so the deletion of columns will not be necessary
    '''

    question = semester + "_Q" # question = 'PRE_Q' or 'PST_Q'

    data = pd.read_csv(database, encoding = 'utf-8', skiprows = [1,2], header = 0)
    df = pd.read_csv(answer_key, encoding = 'utf-8')


    cols = list(data.columns.values)
    c = len(cols)
    e = 0
    h = len(data)

    # Adds the Q#_SCORE column right next to each question
    questions = np.unique(df['Question #'])

    for item in questions:
        if(question+str(item) in data.columns):
            data.insert(data.columns.get_loc(question+str(item))+1,question+str(item)+'_SCORE', 0)

    # e >= 50 --> Full, e < 50 --> Lite
    for d in range(c):
        column = cols[d]
        column = column[0:5]

        if question == column:
            e = e + 1

    data.insert(6 , 'VERSION', " ")

    if e == 50:
        if(year == "16" and season == "Fa"):
            data['VERSION'] = "Fl_2.0"
            # If the value "progress bar" is in comments, change the version to 2.1
            for v in range(h):
                if 'COMMENTS' in data.columns:
                    if (data.loc[v, 'COMMENTS'] == "progress bar"):
                        data.loc[v, 'VERSION'] = "Fl_2.1"
        else:
            data['VERSION'] = "Fl_1.1"
    elif e == 54:
        data['VERSION'] = "Fl_1.0"
        data = data.drop([semester + '_Q18'], axis=1)
        data = data.drop([semester + '_Q18CF'], axis=1)
        data = data.drop([semester + '_Q25'], axis=1)
        data = data.drop([semester + '_Q25CF'], axis=1)
        e = 50
    elif e == 22:
        data['VERSION'] = "Lt_1.0"
    elif e == 30:
        intyr = int(year)
        if (intyr >= 19 or (year == "18" and season == "Fa")):
            data['VERSION'] = "Lt_2.1"
        else:
            data['VERSION'] = "Lt_2.0"
    elif e == 28:
        data['VERSION'] = "SM_1.0"

    # New columns for the totals
    data[semester + '_TOTAL'] = np.nan
    data[semester + '_PCT_TOTAL'] = np.nan
    data[semester + '_GR_TOTAL'] = np.nan
    data[semester + '_GR_MEAN'] = np.nan
    data[semester + '_AR_TOTAL'] = np.nan
    data[semester + '_AR_MEAN'] = np.nan
    data[semester + '_PR_TOTAL'] = np.nan
    data[semester + '_PR_MEAN'] = np.nan
    data[semester + '_PC_TOTAL'] = np.nan
    data[semester + '_PC_MEAN'] = np.nan
    data[semester + '_SP_TOTAL'] = np.nan
    data[semester + '_SP_MEAN'] = np.nan
    data[semester + '_TR_TOTAL'] = np.nan
    data[semester + '_TR_MEAN'] = np.nan
    data[semester + '_AV_TOTAL'] = np.nan
    data[semester + '_AV_MEAN'] = np.nan
    #data[semester + '_ER_MEAN'] = np.nan
    data[semester + '_UD_TOTAL'] = np.nan
    data[semester + '_UD_MEAN'] = np.nan
    data[semester + '_ES_TOTAL'] = np.nan
    data[semester + '_ES_MEAN'] = np.nan

    # Composite Variables
    data[semester + '_SELFEFF'] = np.nan
    data[semester + '_MATHANX'] = np.nan
    data[semester + '_MATHREL'] = np.nan
    data[semester + '_ACADMAT'] = np.nan
    data[semester + '_SCHMATH'] = np.nan

    corr_ans = {15: 0, 12:0, 14:0, 26:0, 27:0, 23:0, 28:0, 19:0, 3:0, 16:0, 13:0, 31:0,
                          32:0, 29:0, 30:0, 5:0, 6:0, 7:0, 10:0, 11:0, 20:0, 21:0, 33:0, 34:0, 35:0}
    for item in corr_ans:
        corr_ans[item] = int(list(df.loc[df['Question #']==item]['Correct Answer'])[0])

    # Adds totals and means to total and means columns
    for nn in range(h):
        qn = {15: 0, 12:0, 14:0, 26:0, 27:0, 23:0, 28:0, 19:0, 3:0, 16:0, 13:0, 31:0, 32:0, 29:0, 30:0, 5:0, 6:0, 7:0, 10:0, 11:0, 20:0, 21:0, 33:0, 34:0, 35:0}

        for q_num in qn:
            try:

                if(int(data.loc[nn, question + str(q_num)]) == corr_ans[q_num]):

                    qn[q_num] = 1
                    data.loc[nn, question+str(q_num)+'_SCORE'] = 1
            except:
                pass


        GR = int(np.nansum([qn[15], qn[14], qn[12], qn[29], qn[30], qn[13]]))
        AR = int(np.nansum([qn[15], qn[14], qn[26], qn[27], qn[23], qn[28], qn[19], qn[3], qn[16], qn[31], qn[32], qn[5], qn[6], qn[7], qn[29], qn[30], qn[10], qn[11], qn[20], qn[21], qn[33], qn[34], qn[35]]))
        PR = int(np.nansum([qn[15], qn[12], qn[14], qn[23], qn[28], qn[3], qn[16], qn[7], qn[10], qn[11], qn[20], qn[21], qn[33], qn[35], qn[13]]))
        PC = int(np.nansum([qn[27], qn[3], qn[32], qn[20], qn[21]]))
        SP = int(np.nansum([qn[27], qn[23], qn[28], qn[29], qn[30], qn[20], qn[21]]))
        TR = int(np.nansum([qn[26], qn[27], qn[23]]))
        AV = int(np.nansum([qn[31], qn[10], qn[11], qn[33], qn[34]]))
        UD = int(np.nansum([qn[31], qn[6], qn[7], qn[35], qn[16]]))
        ES = int(np.nansum([qn[15], qn[12], qn[14], qn[16], qn[13]]))
        data.loc[nn, semester + '_GR_TOTAL'] = GR
        data.loc[nn, semester + '_AR_TOTAL'] = AR
        data.loc[nn, semester + '_PR_TOTAL'] = PR
        data.loc[nn, semester + '_PC_TOTAL'] = PC
        data.loc[nn, semester + '_SP_TOTAL'] = SP
        data.loc[nn, semester + '_TR_TOTAL'] = TR
        data.loc[nn, semester + '_AV_TOTAL'] = AV
        data.loc[nn, semester + '_UD_TOTAL'] = UD
        data.loc[nn, semester + '_ES_TOTAL'] = ES
        total_full = 0

        for q_num in qn:
                total_full += qn[q_num]
        if e == 50:
            data.loc[nn, semester + '_TOTAL'] = total_full
            data.loc[nn, semester + '_PCT_TOTAL'] = total_full/(25)
            data.loc[nn, semester + '_GR_MEAN'] = GR/6
            data.loc[nn, semester + '_AR_MEAN'] = AR/23
            data.loc[nn, semester + '_PR_MEAN'] = PR/15
            data.loc[nn, semester + '_PC_MEAN'] = PC/5
            data.loc[nn, semester + '_SP_MEAN'] = SP/7
            data.loc[nn, semester + '_TR_MEAN'] = TR/3
            data.loc[nn, semester + '_AV_MEAN'] = AV/5
            data.loc[nn, semester + '_UD_MEAN'] = UD/5
            data.loc[nn, semester + '_ES_MEAN'] = ES/5

        elif e == 22:
            data.loc[nn, semester + '_TOTAL'] = total_full
            data.loc[nn, semester + '_PCT_TOTAL'] = total_full/(11)
            data.loc[nn, semester + '_GR_MEAN'] = GR/4
            data.loc[nn, semester + '_AR_MEAN'] = AR/9
            data.loc[nn, semester + '_PR_MEAN'] = PR/8
            data.loc[nn, semester + '_SP_MEAN'] = SP/3
            data.loc[nn, semester + '_TR_MEAN'] = TR/3
            data.loc[nn, semester + '_ES_MEAN'] = ES/5

        #lacks number of questions for meaningful subscore
            #1 q
            data.loc[nn, semester + '_UD_MEAN'] = np.nan
            data.loc[nn, semester + '_UD_TOTAL'] = np.nan
            #2 qs
            data.loc[nn, semester + '_PC_MEAN'] = np.nan
            data.loc[nn, semester + '_PC_TOTAL'] = np.nan
            #1 q
            data.loc[nn, semester + '_AV_MEAN'] = np.nan
            data.loc[nn, semester + '_AV_TOTAL'] = np.nan

        elif e == 30:
            data.loc[nn, semester + '_TOTAL'] = total_full
            data.loc[nn, semester + '_PCT_TOTAL'] = total_full/(15)
            data.loc[nn, semester + '_GR_MEAN'] = GR/4
            data.loc[nn, semester + '_AR_MEAN'] = AR/13
            data.loc[nn, semester + '_PR_MEAN'] = PR/11
            data.loc[nn, semester + '_SP_MEAN'] = SP/3
            data.loc[nn, semester + '_TR_MEAN'] = TR/3
            data.loc[nn, semester + '_AV_MEAN'] = AV/4
            data.loc[nn, semester + '_ES_MEAN'] = ES/5
        #lacks number of questions for meaningful subscore
            #1 q
            data.loc[nn, semester + '_UD_MEAN'] = np.nan
            data.loc[nn, semester + '_UD_TOTAL'] = np.nan
            #2 qs
            data.loc[nn, semester + '_PC_MEAN'] = np.nan
            data.loc[nn, semester + '_PC_TOTAL'] = np.nan

        elif e == 28:
            data.loc[nn, semester + '_TOTAL'] = total_full
            data.loc[nn, semester + '_PCT_TOTAL'] = total_full/(14)
            data.loc[nn, semester + '_GR_MEAN'] = GR/4
            data.loc[nn, semester + '_AR_MEAN'] = AR/13
            data.loc[nn, semester + '_PR_MEAN'] = PR/9
            data.loc[nn, semester + '_PC_MEAN'] = PC/3
            data.loc[nn, semester + '_SP_MEAN'] = SP/7
            data.loc[nn, semester + '_UD_MEAN'] = UD/5
            data.loc[nn, semester + '_ES_MEAN'] = ES/3

        #lacks number of questions for meaningful subscore
            #2 q
            data.loc[nn, semester + '_TR_MEAN'] = np.nan
            data.loc[nn, semester + '_TR_TOTAL'] = np.nan
            #1 q
            data.loc[nn, semester + '_AV_MEAN'] = np.nan
            data.loc[nn, semester + '_AV_TOTAL'] = np.nan



    data[semester  + '_CF_TOTAL'] = np.nan
    data[semester  + '_CF_TOTAL_CORR'] = np.nan
    data[semester  + '_CF_TOTAL_INCORR'] = np.nan
    data[semester + '_CF_MEAN'] = np.nan
    data[semester + '_CF_MEAN_CORR'] = np.nan
    data[semester + '_CF_MEAN_INCORR'] = np.nan


    # Calculates confidence totals and means; adds to respective columns
    for u in range(h):
        qcf = {'15': 0, '12':0, '14':0, '26':0, '27':0, '23':0, '28':0, '19':0, '3':0, '16':0, '13':0, '31':0, '32':0, '29':0, '30':0, '5':0, '6':0, '7':0, '10':0, '11':0,'20':0, '21':0, '33':0, '34':0, '35':0}
        qc = {'15': 0, '12':0, '14':0, '26':0, '27':0, '23':0, '28':0, '19':0, '3':0, '16':0, '13':0, '31':0, '32':0, '29':0, '30':0, '5':0, '6':0, '7':0, '10':0, '11':0,'20':0, '21':0, '33':0, '34':0, '35':0}

        for q_num in qcf:
            try:
                qcf[q_num] = int(data.loc[u, question + str(q_num) + "CF"])

                qc[q_num] = int(data.loc[u, question + str(q_num) + '_SCORE'])
            except:
                pass

        medscore = 0
        corrscore = 0
        incorrscore = 0
        confcount = 0
        for item in qcf:
            medscore += qcf[item]

            if qcf[item] > 0:
                confcount +=1

                if qc[item] == 1:
                    corrscore += qcf[item]
                else:
                    incorrscore += qcf[item]
        #print(confcount)
        if (confcount == 0):
            confcount = 1
        # Student's score
        numcorr = data.loc[u, semester + '_TOTAL']

        # Calculate confidence scores
        if e == 30:
            data.loc[u, semester + '_CF_TOTAL'] = medscore
            data.loc[u, semester + '_CF_TOTAL_CORR'] = corrscore
            data.loc[u, semester + '_CF_TOTAL_INCORR'] = incorrscore
            data.loc[u, semester + '_CF_MEAN'] = medscore/confcount

            if numcorr != 0:
                data.loc[u, semester + '_CF_MEAN_CORR'] = corrscore/numcorr
            else:
                data.loc[u, semester + '_CF_MEAN_CORR'] = 0
            if numcorr != confcount:
                data.loc[u, semester + '_CF_MEAN_INCORR'] = incorrscore/(confcount-numcorr)
            else:
                data.loc[u, semester + '_CF_MEAN_INCORR'] = 0

        elif e == 22:
            data.loc[u, semester + '_CF_TOTAL'] = medscore
            data.loc[u, semester + '_CF_TOTAL_CORR'] = np.nan
            data.loc[u, semester + '_CF_TOTAL_INCORR'] = incorrscore
            data.loc[u, semester + '_CF_MEAN'] = medscore/confcount
            if numcorr != 0:
                data.loc[u, semester + '_CF_MEAN_CORR'] = corrscore/numcorr
            else:
                data.loc[u, semester + '_CF_MEAN_CORR'] = 0
            if numcorr != confcount:
                data.loc[u, semester + '_CF_MEAN_INCORR'] = incorrscore/(confcount-numcorr)
            else:
                data.loc[u, semester + '_CF_MEAN_INCORR'] = 0
        elif e == 28:
            data.loc[u, semester + '_CF_TOTAL'] = medscore
            data.loc[u, semester + '_CF_TOTAL_CORR'] = np.nan
            data.loc[u, semester + '_CF_TOTAL_INCORR'] = incorrscore
            data.loc[u, semester + '_CF_MEAN'] = medscore/confcount
            if numcorr != 0:
                data.loc[u, semester + '_CF_MEAN_CORR'] = corrscore/numcorr
            else:
                data.loc[u, semester + '_CF_MEAN_CORR'] = 0
            if numcorr != confcount:
                data.loc[u, semester + '_CF_MEAN_INCORR'] = incorrscore/(confcount-numcorr)
            else:
                data.loc[u, semester + '_CF_MEAN_INCORR'] = 0

        elif e == 50:
            data.loc[u, semester + '_CF_TOTAL'] = medscore
            data.loc[u, semester + '_CF_TOTAL_CORR'] = corrscore
            data.loc[u, semester + '_CF_TOTAL_INCORR'] = incorrscore
            data.loc[u, semester + '_CF_MEAN'] = medscore/confcount

            if numcorr != 0:
                data.loc[u, semester + '_CF_MEAN_CORR'] = corrscore/numcorr
            else:
                data.loc[u, semester + '_CF_MEAN_CORR'] = 0
            if numcorr != confcount:
                data.loc[u, semester + '_CF_MEAN_INCORR'] = incorrscore/(confcount-numcorr)
            else:
                data.loc[u, semester + '_CF_MEAN_INCORR'] = 0

    data[semester + '_QCOMPLETE'] = 0
    data[semester + '_COMPFLAG'] = 0
    data[semester +'_EFFFLAG'] = 0

    # Counts number of completed columns
    try:
        if e == 50:
            q = [15, 12, 14, 26, 27, 23, 28, 19, 3, 16, 13, 31, 32, 29, 30, 5, 6, 7, 10, 11, 20, 21, 33, 34, 35]
        elif e == 22:
            q = [15, 12, 13, 14, 26, 27, 23, 28, 19, 3, 16]
        elif e == 30:
            q = [15, 12, 13, 14, 26, 27, 23, 28, 19, 3, 16, 10, 11, 33, 34]
        elif e == 28:
            q = [6, 7, 13, 14, 16, 20, 21, 23, 27, 28, 29, 30, 31, 35]

        for v in range(h):
            # Count up totals
            total = 0
            for w in q:
                count = question + str(w)

                answered = data.loc[v, count]
                if (str(answered) == 'nan' or str(answered) == ' '):
                    continue
                else:
                    total = int(np.nansum([total, 1]))

            data.loc[v, semester + '_QCOMPLETE'] = total

            # Add completed flag
            if total == len(q):
                data.loc[v, semester + '_COMPFLAG'] = 1
            else:
                data.loc[v, semester + '_COMPFLAG'] = 0
    except:
        KeyError

    # Calculating effort column

    for v in range(h):
        # If there is no response for effort, mark completion as 0 for that student!
        if (pd.isnull(data.loc[v, semester + '_EFFORT'])):
            data.loc[v, semester + '_COMPFLAG'] = 0

        # If there is high effort, give full marks in flag
        if data.loc[v, semester + '_EFFORT'] == 4 or data.loc[v, semester + '_EFFORT'] == 5:
            data.loc[v, semester +'_EFFFLAG'] = 1

        # Some effort gives you only so many marks...
        elif data.loc[v, semester + '_EFFORT'] == 3:
            data.loc[v, semester +'_EFFFLAG'] = 0.5

        # NO EFFORT!! :-(
        elif data.loc[v, semester + '_EFFORT'] == 2 or data.loc[v, semester + '_EFFORT'] == 1:
            data.loc[v, semester +'_EFFFLAG'] = 0



    #data.to_csv(semester+"_scored.csv", encoding='utf-8',index=False)

    #print("Results saved to " + savedname + "_scored.csv")

    return data

def swapOrdering(db, index, colname):
    '''
    Swaps ordering of columns so that they're ordered negative -> positive
    Used in Factor Analysis
    '''
    check = int(db.at[index, colname])
    if check == 4:
        db.at[index, colname] = 1
    elif check == 3:
        db.at[index, colname] = 2
    elif check == 2:
        db.at[index, colname] = 3
    elif check == 1:
        db.at[index, colname] = 4
