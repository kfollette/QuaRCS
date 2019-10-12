def empty_stu_DB():
  import pandas as pd
  #This creates an new empty student ID database and saves it with the name: 
  # "Student_ID_Database" + ".csv"

  student_ID = pd.DataFrame(columns=['Firstname', 'Lastname', 'EMAIL', 'SCHOOL', 'STUDENT_ID'])
  name = "Student_ID_Database" + ".csv"
  student_ID.to_csv(name, encoding='utf-8', index = False)

  return

def empty_instr_DB():
  import pandas as pd
  #This creates an new empty instructor ID database and saves it with the name: 
  # "Instr_ID_Database" + ".csv"

  instr_ID = pd.DataFrame(columns=['Name', 'Firstname', 'Lastname', 'INSTR_ID'])
  name = "Instr_ID_Database" + ".csv"
  instr_ID.to_csv(name, encoding='utf-8', index = False)

  return

    


