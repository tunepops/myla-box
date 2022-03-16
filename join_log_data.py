pip install dropbox

import dropbox
import pandas as pd
import io 

from pathlib import Path

import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Time Series analysis
# https://www.machinelearningplus.com/time-series/time-series-analysis-python/
from dateutil.parser import parse
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import json
plt.rcParams.update({'figure.figsize': (10, 7), 'figure.dpi': 120})


# Important:
# 1. Save a copy of this script to your own Google Drive
# 2. Genereate your own DROPBOX_TOKEN,
#    NEVER share it with others or check into version control systems like GitHub
dbx = dropbox.Dropbox('') ## REPLACE TOKEN HERE
dbx.users_get_current_account()
data_blank = [[]]
df_main = pd.DataFrame(data_blank)
df_logs = pd.DataFrame(data_blank)



for entry in dbx.files_list_folder('/MyLA Data Project').entries:
    file_path = entry.path_lower
    # print(file_path)
    # TODO: use regex for mapping the file names
    # if file_path =='/myla data project/myla_student_data_fall2019_withcanvascourses-anonymized.csv' :
    # TODO Plot the timeseries
    
    
    
    # check for course id map file name to save dataframe for later joining
    if 'course_map' in file_path :
        _, res = dbx.files_download(file_path)
        with io.BytesIO(res.content) as stream:
            df = pd.read_csv(stream, header=None)
#         pd.set_option('display.max_columns', None)
        df_cmap = df
        print(' - - - course map file')
        df_cmap.columns = ['Temp CID','Canvas CID']
        df_cmap['Canvas CID'] = df_cmap['Canvas CID']%1000000
        df_cmap['Canvas CID'] = df_cmap['Canvas CID'].astype(str)
#         print(df_cmap.head(5))
#         print(df_cmap.columns)



    # check for student course roster data file name to compile course headcount main dataframe
    elif 'myla_student_data' in file_path :
    # download and read file
        _, res = dbx.files_download(file_path)
        with io.BytesIO(res.content) as stream:
            df = pd.read_csv(stream)
        pd.set_option('display.max_columns', None)
        # create term code parameter to keep track of each file source
        df_term = file_path[int(file_path.find('student_data_'))+13:int(file_path.find('_withcanvas'))]
        print(' - - - student course file')
        print(file_path)
        if 'fall' in df_term :
            df_term = df_term[-4:] + '10'
            df_term = int(df_term) + 100
        elif 'winter' in df_term :
            df_term = df_term[-4:] + '20'
        df_term = str(df_term)
        df['Term Code'] = df_term
        if df_term == '202110' :
            df = df[['username', 'Sex', 'International or Domestic', 'Acad Level BOT',
                   'Cum GPA', 'Math Plcmt', 'CanvasCourseID_short', 'Term Code']]
            df = df.rename({'username': 'Campus ID','CanvasCourseID_short': 'CanvasCourseID_long'}, axis='columns')
        if df_term == '201920' :
            df = df.rename({'Inferred Canvas LONG ID': 'CanvasCourseID_long'}, axis='columns')
        df_main = pd.concat([df_main,df])

        
        
        
    # check for myla log data file name to analyze tool usage data, later linked to student course data
    elif 'myla_event_log' in file_path and 'grade' not in file_path :
        _, res = dbx.files_download(file_path)
        with io.BytesIO(res.content) as stream:
#             df = json.dumps(stream)
#             df = json.loads(df)
            df = pd.read_csv(stream)
        pd.set_option('display.max_columns', None)
        # create term code parameter to keep track of each file source
        df_term = file_path[int(file_path.find('event_log_'))+10:int(file_path.find('anon'))-1]
        print(' - - - event log file')
        print(file_path)
        if 'fall' in df_term :
            df_term = df_term[-4:] + '10'
            df_term = int(df_term) + 100
        elif 'winter' in df_term :
            df_term = df_term[-4:] + '20'
        df_term = str(df_term)
        df['Term Code'] = df_term
        
        
        
        df = df.rename({'id':'Click ID','timestamp':'Click Timestamp','action':'Module'}, axis='columns')
        
        if df_term == '202110' :
            print(' - - fall 2020 columns: ')
            df = df.rename({'anon-username': 'Temp SID'}, axis='columns')
            df = df[['Click ID', 'Click Timestamp', 'Module', 'Temp SID', 'Term Code']]
#             df['extra'] = df['extra'].astype(str)
#             df_splt = pd.read_json(df['extra'])


#             objs = [df, pd.DataFrame(df['extra'].tolist()).iloc[:, :10]]
#             print('objects are: ')
#             print(objs)
#             df2 = pd.concat(objs, axis=1).drop('extra', axis=1)
#             print('new df is: ')
#             print(df2.head(6))
            
            
#             df_nested_list = pd.json_normalize(df, record_path =['extra'])
#             df['extra'] = df['extra'].map(eval)
#             df_splt = pd.DataFrame(df['extra'].tolist())
#             df_splt = pd.json_normalize(df['extra'])
#             df['extra2'] = df['extra'].apply(pd.Series)
#             print(df['extra2'].head(5))
#             print(df_nested_list.head(6))
#             print(df_splt.head(6))
#             print(course_srch)
#             df['Canvas CID'] = df['Canvas CID'].astype(int)
#             df['Canvas CIDT'] = df['Canvas CID']%1000000
#             df['Canvas CIDT'] = df['Canvas CIDT'].astype(str)
#             print(df.head(5))





        else :
            df = df.rename({'course_id': 'Temp CID','username':'Temp SID'}, axis='columns')
            df = df[['Click ID', 'Click Timestamp', 'Module', 'Temp SID', 'Temp CID', 'Term Code']]
        df_logs = pd.concat([df_logs,df])
#         print(df.head(5))
#         print(df_logs.columns)
#         print(df_logs.head(5))
    else:
        print(' - - - other file')
        print(file_path)
print('\nBREAK')


df_main = df_main.rename({'CanvasCourseID_long': 'Temp CID','International or Domestic': 'Intl Ind',
                        'Acad Level BOT': 'Level'}, axis='columns')
# df_main = df_main['Campus ID', 'Sex', 'International or Domestic', 'Acad Level BOT',
#        'Cum GPA', 'Math Plcmt', 'CanvasCourseID_long', 'Term Code']
df_main = df_main[['Campus ID','Temp CID', 'Term Code']]
# df_main = df_main[['Temp CID', 'Term Code']]
df_main = df_main.dropna()
df_main = df_main.drop_duplicates()



# this command joins the main df with the course map df, so course ID may be consistent
df_combo = df_main.join(df_cmap.set_index('Temp CID'), on='Temp CID', how='left', lsuffix='', rsuffix=' map')

# reduce to 3 columns, sort, and remove canvas course id 322656
df_logs = df_logs[['Term Code','Temp SID','Click Timestamp', 'Temp CID','Module','Click ID']]
df_logs = df_logs.sort_values(by=['Term Code','Temp SID','Click Timestamp'])

df_logs_combo = df_logs.join(df_cmap.set_index('Temp CID'),on='Temp CID', how='left', lsuffix='', rsuffix=' map')
df_logs_combo = df_logs_combo[df_logs_combo['Canvas CID'] != '322656']

# df_logs_combo = df_logs_combo[['Term Code','Temp CID','Canvas CIDF','Campus ID']]
# print(df_log_combo.head(5))

# creates new column, showing Canvas ID when available, and showing Course ID when not (for Fall 2020 file)
df_combo['Canvas CIDF'] = np.where(
    df_combo['Canvas CID'].isna(), df_combo['Temp CID'], 
     np.where(df_combo['Canvas CID'].notna(),  df_combo['Canvas CID'], 'Unknown')
)

# reduce to 3 columns, sort, and remove canvas course id 322656
df_combo = df_combo[['Term Code','Temp CID','Canvas CIDF','Campus ID']]
df_combo = df_combo.sort_values(by=['Term Code','Canvas CIDF','Campus ID'])
df_combo = df_combo[df_combo['Canvas CIDF'] != '322656']

# count students per course per term
enrollments = df_combo.groupby(['Term Code','Canvas CIDF','Temp CID']).count()['Campus ID']

myla_users = df_logs_combo.groupby(['Term Code','Canvas CID']).nunique()['Temp SID']
# myla_users = df_logs.groupby(['Term Code','Temp CID']).nunique()['Temp SID']

# print(enrollments.head(5))
# print(df_combo.columns)
# print(df_combo.head(5))


# print(df_logs.head(5))
print(myla_users.head(5))



# to print dataframe as csv out to file on desktop, use following code
out_file_path = Path('/Users/sticker/Desktop/myla_outputs/out.csv')
out_file_path.parent.mkdir(parents=True, exist_ok=True)

# course_counts.to_csv(out_file_path)
# df_main.to_csv(out_file_path)
# df_combo.to_csv(out_file_path)
# df_cmap.to_csv(out_file_path)
# enrollments.to_csv(out_file_path)
myla_users.to_csv(out_file_path)



#optional code bits

# this lists every unique value for the indicated column
# course_list = df_main.CanvasCourseID_long.unique()
# this counts every row for each value in the indicated column
# course_counts = df_main[['Term Code','Course ID']].value_counts()

# this lists every unique value for the indicated column
# course_term_list = df_main.CanvasCourseID_long.unique()
# this counts every row for each value in the indicated column
# course_term_counts = df_main[['Term Code']].value_counts()



# for col in df_main :
#     na_counts = df_main[col].isnull().sum()
#     print(col, " ",na_counts)

# print(df_main.nunique())
# print(course_list)
# print(course_counts)
