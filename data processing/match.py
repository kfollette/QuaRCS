
def match(PREdata, PSTdata):
    '''
    A O(n^2) (lol) matching algorithm that matches on _STUDENT_ID column

    Args:
        PREdata: The Pandas DataFrame of the pre-semester dataset.
        PSTdata: The Pandas DataFrame of the post-semester dataset.

    Returns:
        PRE_not_matched: a Python list of int row-indeces for names that did not match in the pre data

        PST_not_matched: a Python list of int row-indeces for names that did not match in the post data

        pairs: a Python dictionary with int keys of int row-indeces for names that matched. First of the two elements
        in the list of each dictionary key is the pre_data row index and the second is the post_data row index.

        instructor_change: a Python dictionary with int keys of int row-indeces for students that changed instructors. First of the two elements
        in the list of each dictionary key is the pre_data row index and the second is the post_data row index.

    By:
        Ilija Nikolov, 17.07.17

    Heavily edited by:
        Your friendly neighborhood Camilo Ortiz (August 5th, 2019)
    '''
    # Variables to return
    pairs = {}
    PRE_not_matched = []
    PST_not_matched = []
    instructor_change = {}

    # Meta variables
    PRE_h = len(PREdata)
    PST_h = len(PSTdata)

    # Matching
    for i in PREdata.index:
        PRE_student_id = PREdata.loc[i, "PRE_STUDENT_ID"]
        match = False
        # Look for a match
        for j in PSTdata.index:

            PST_student_id = PSTdata.loc[j, 'PST_STUDENT_ID']

            if PRE_student_id == PST_student_id:

                # Update data variables
                pairs.update({len(pairs):(i,j)})

                # Record changes in instructor
                if(PREdata.loc[i, "PRE_INSTR_ID"] != PSTdata.loc[j, "PST_INSTR_ID"]):
                    instructor_change.update({len(instructor_change): (i, j)})
                match = True
                break

        if not match:
            # Add index to PRE_not_matched
            PRE_not_matched.append(i)


    # Find all indeces of non-matching data in PST dataset
    for i in PSTdata.index:
        match = False
        # Check if there is a match in the pairs dictionary
        for key in pairs:
            if(i == pairs[key][1]):
                match = True
                break

        if not match:
            # Add index to the PST_not_matched
            PST_not_matched.append(i)

    return (PRE_not_matched, PST_not_matched, pairs, instructor_change)
