pip install dropbox

import dropbox
import pandas as pd
import io

import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Time Series analysis
# https://www.machinelearningplus.com/time-series/time-series-analysis-python/
from dateutil.parser import parse
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
import pandas as pd
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

# define function to parse term code from file path string
def set_term_code(file_path,year) :
    term_code = ''
    if 'fall' in file_path :
        term_code = year + '10'
        term_code = int(term_code) + 100
        term_code = str(term_code)
    elif 'winter' in file_path :
        term_code = year + '20'
    else :
        print('Error reading term description from file path')
    return term_code

# def get_term_desc(term_code) :
#     int(term_code)

for entry in dbx.files_list_folder('/MyLA Data Identified Subset').entries:
    file_path = entry.path_lower
    
    
    
    # check for course id map file name to save dataframe for later joining
    if 'course_map' in file_path :
        _, res = dbx.files_download(file_path)
        with io.BytesIO(res.content) as stream:
            df = pd.read_csv(stream, header=None)
        df_cmap = df
        print(' - - - course map file')
#         print(file_path)
        df_cmap.columns = ['Temp CID','Canvas CID']
        df_cmap['Canvas CID'] = df_cmap['Canvas CID']%1000000
        df_cmap['Canvas CID'] = df_cmap['Canvas CID'].astype(str)



    # check for student course roster data file name to compile course headcount main dataframe
    elif 'myla_student_data' in file_path :
        _, res = dbx.files_download(file_path)
        with io.BytesIO(res.content) as stream:
            df = pd.read_csv(stream)
        pd.set_option('display.max_columns', None)
        year_code = file_path[int(file_path.find('_withcanvas'))-4:int(file_path.find('_withcanvas'))]
        print(' - - - student course file')
        print(file_path)
        df_term = set_term_code(file_path,year_code)
        print('Term is: ', df_term)
        df['Term Code'] = df_term
        if 'anon' not in file_path :
            if df_term == '202020' :
                df = df.rename({'CanvasCousreName': 'CanvasCourseName'}, axis='columns')
            df = df[['Campus ID', 'Sex', 'International or Domestic','Acad Level BOT', 'Cum GPA', 
                       'CanvasCourseName', 'CanvasCourseID_short', 'Term Code']]
            df = df.rename({'CanvasCourseName': 'Canvas CName','International or Domestic':'Intl/Dom',
                               'Acad Level BOT':'Class Level','CanvasCourseID_short':'Canvas CID',
                               'Campus ID':'Uniqname'}, axis='columns')
            df['Canvas CID'] = df['Canvas CID'].astype(str)
            df['Uniqname'] = df['Uniqname'].str.lower()
#             print(df.head(5))
#             df = df.rename({'Inferred Canvas LONG ID': 'CanvasCourseID_long'}, axis='columns')
            df_main = pd.concat([df_main,df])
#         print(df.head(5))
#         print(df.columns)

        
        
        
    # check for myla log data file name to analyze tool usage data, later linked to student course data
    elif 'myla_event_log' in file_path and 'grade' not in file_path :
        _, res = dbx.files_download(file_path)
        with io.BytesIO(res.content) as stream:
            df = pd.read_csv(stream)
        pd.set_option('display.max_columns', None)
        year_code = file_path[int(file_path.find('.csv'))-4:int(file_path.find('.csv'))]
        print(' - - - event log file')
        df_term = set_term_code(file_path,year_code)
#         print('Term is: ', df_term)
        df['Term Code'] = df_term
        df = df.rename({'id':'Click ID','timestamp':'Click Timestamp','action':'Module',
                       'username':'Uniqname','course_id':'Canvas CID'}, axis='columns')
        df['Canvas CID'] = df['Canvas CID']%1000000
        df['Canvas CID'] = df['Canvas CID'].astype(str)
        df['Click ID'] = df['Click ID'].astype(str)
        df = df[['Click ID', 'Click Timestamp', 'Module', 'Uniqname', 'Canvas CID', 'Term Code']]
        df_logs = pd.concat([df_logs,df])
#         print(df.head(5))
#         print(df_logs.columns)
#         print(df_logs.head(5))




    else:
        print(' - - - other file')
        print(file_path)
print('\nBREAK')


def get_term_desc(term_code) :
    term_type = int(term_code)%100
    year = math.trunc(int(term_code)/100)
    if term_type == 10 :
        year -= 1
        term_typ_desc = 'Fall'
    else :
        term_typ_desc = 'Winter'
    term_desc = term_typ_desc + ' ' + str(year)
    return(term_desc)

# df_main = df_main['Campus ID', 'Sex', 'International or Domestic', 'Acad Level BOT',
#        'Cum GPA', 'Math Plcmt', 'CanvasCourseID_long', 'Term Code']
# df_main = df_main[['Uniqname','Canvas CID', 'Term Code']]
# df_main = df_main[['Temp CID', 'Term Code']]
df_main = df_main.dropna()
df_main = df_main.drop_duplicates()


df_logs = df_logs.dropna()
df_logs = df_logs.drop_duplicates()


print(df_main.columns)
print(df_main.head(6))

# this command joins the main df with the course map df, so course ID may be consistent
# df_combo = df_main.join(df_cmap.set_index('Temp CID'), on='Temp CID', how='left', lsuffix='', rsuffix=' map')

# print(df_logs.head(6))
# reduce to 6 columns, sort, and remove canvas course id 322656
df_logs = df_logs[['Term Code','Uniqname','Click Timestamp', 'Canvas CID','Module','Click ID']]
df_logs = df_logs.sort_values(by=['Term Code','Uniqname','Click Timestamp'])
df_logs['Module'] = df_logs['Module'].replace({'VIEW_FILE_ACCESS': 'VFA',
                                                'VIEW_GRADE_DISTRIBUTION': 'VGD',
                                                'VIEW_ASSIGNMENT_PLANNING':'VAP',
                                                'VIEW_SET_DEFAULT':'VSD',
                                                'VIEW_RESOURCE_ACCESS':'VRA',
                                                'VIEW_ASSIGNMENT_PLANNING_WITH_GOAL_SETTING':'VAP-GS'
                                              })
print(df_logs['Module'].unique())
df_logs['Click Date'] = pd.to_datetime(df_logs['Click Timestamp']).dt.date



# print(df_logs.columns)
# print(df_logs.head(6))

df_click_times = df_logs[['Term Code','Click Date','Click ID']]
df_click_times['Click Week'] = pd.to_datetime(df_click_times['Click Date']).dt.isocalendar().week
# print(df_click_times.columns)
# print(df_click_times.head(6))


print(df_click_times['Term Code'].unique())
for each_term in df_click_times['Term Code'].unique() :
#     print(each_term)
#     print(get_term_desc(each_term))
    
    
    fig, axs = plt.subplots(figsize=(8, 1))
    df_click_times_subset = df_click_times[df_click_times['Term Code'] == each_term]
    day_clicks = df_click_times_subset.groupby(['Click Week']).nunique()['Click ID'].plot(
        kind='bar', rot=0, ax=axs
    )
    
    plt.xlabel(get_term_desc(each_term));
