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
plt.rcParams.update({'figure.figsize': (10, 7), 'figure.dpi': 120})



# Important:
# 1. Save a copy of this script to your own Google Drive
# 2. Genereate your own DROPBOX_TOKEN, and NEVER share it with others or check into version control systems like GitHub
dbx = dropbox.Dropbox('') ## REPLACE TOKEN HERE
dbx.users_get_current_account()
data_blank = [[]]
df_main = pd.DataFrame(data_blank)
# print(df_main)
for entry in dbx.files_list_folder('/MyLA Data Project').entries:
    file_path = entry.path_lower
    # print(file_path)
    # TODO: use regex for mapping the file names
    # if file_path =='/myla data project/myla_student_data_fall2019_withcanvascourses-anonymized.csv' :
    
    # check for course id map file name to save dataframe for later joining
    if 'course_map' in file_path :
        _, res = dbx.files_download(file_path)
        with io.BytesIO(res.content) as stream:
            df = pd.read_csv(stream, header=None)
#         pd.set_option('display.max_columns', None)
        df_cmap = df
        df_cmap.columns = ['Course ID','Canvas ID']
        df_cmap['Canvas ID'] = df_cmap['Canvas ID']%1000000
        print('course map')
        print(df_cmap.head(5))
        print(df_cmap.columns)
    # check for student course roster data file name to compile course headcount main dataframe
    if 'myla_student_data' in file_path :
    # download and read file
        _, res = dbx.files_download(file_path)
        with io.BytesIO(res.content) as stream:
            df = pd.read_csv(stream)
        pd.set_option('display.max_columns', None)
        # create term code parameter to keep track of each file source
        df_term = file_path[int(file_path.find('student_data_'))+13:int(file_path.find('_withcanvas'))]
        if 'fall' in df_term :
            print(df_term)
            df_term = df_term[-4:] + '10'
            df_term = int(df_term) + 100
        elif 'winter' in df_term :
            print(df_term)
            df_term = df_term[-4:] + '20'
            df_term = int(df_term)
        df_term = str(df_term)
        print(df_term)
        df['Term Code'] = df_term
        if df_term == '202110' :
            print('202110')
            df = df[['username', 'Sex', 'International or Domestic', 'Acad Level BOT',
                   'Cum GPA', 'Math Plcmt', 'CanvasCourseID_short', 'Term Code']]
            df = df.rename({'username': 'Campus ID','CanvasCourseID_short': 'CanvasCourseID_long'}, axis='columns')
        if df_term == '201920' :
            print('201920')
            print(df.columns)
            df = df.rename({'Inferred Canvas LONG ID': 'CanvasCourseID_long'}, axis='columns')
        df_main = pd.concat([df_main,df])
        print(df_main.columns)

    # TODO Plot the timeseries
    else:
        print(' - other file')
print('BREAK')
df_main = df_main.rename({'CanvasCourseID_long': 'Course ID','International or Domestic': 'Intl Ind',
                        'Acad Level BOT': 'Level'}, axis='columns')
# df_main = df_main['Campus ID', 'Sex', 'International or Domestic', 'Acad Level BOT',
#        'Cum GPA', 'Math Plcmt', 'CanvasCourseID_long', 'Term Code']
df_main = df_main[['Campus ID','Course ID', 'Term Code']]
# df_main = df_main[['Course ID', 'Term Code']]
df_main = df_main.dropna()
df_main = df_main.drop_duplicates()


# print(df_main.columns)
print(df_main.head(5))
print(df_cmap.head(5))

df_combo = df_main.join(df_cmap.set_index('Course ID'), on='Course ID', how='left', lsuffix='', rsuffix=' map')

# df_combo['Canvas Course'] = 'Unknown'
# df_combo.loc[df_combo['Canvas ID'].isna(), 'Canvas Course'] = df_combo['Course ID']
# df_combo.loc[df_combo['Time'].between(30, 60, inclusive=True), 'difficulty'] = 'Medium'

df_combo['Canvas Course'] = np.where(
    df_combo['Canvas ID'].isna(), 
    df_combo['Course ID'], 
     np.where(
        df_combo['Canvas ID'].notna(),  df_combo['Canvas ID'], 'Unknown'
     )
)

print(df_combo.columns)
print(df_combo.head(5))

# choose filepath for your own machine if desired
filepath = Path('/Users/sticker/Desktop/myla_outputs/out.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)


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

# course_counts.to_csv(filepath)
# df_main.to_csv(filepath)
df_combo.to_csv(filepath)

