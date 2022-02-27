pip install dropbox

import dropbox
import pandas as pd
import io

# from Chandan code :
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# from Zhen code :
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
print(df_main)

for entry in dbx.files_list_folder('/MyLA Data Project').entries:
    file_path = entry.path_lower
    # print(file_path)
    # TODO: use regex for mapping the file names
    # if file_path =='/myla data project/myla_student_data_fall2019_withcanvascourses-anonymized.csv' :
    if 'myla_student_data' in file_path :

    # download and read file
        _, res = dbx.files_download(file_path)
        with io.BytesIO(res.content) as stream:
            df = pd.read_csv(stream)
        pd.set_option('display.max_columns', None)
        df_term = file_path[int(file_path.find('student_data_'))+13:int(file_path.find('_withcanvas'))]
        df['Term Code'] = df_term
        if df_term == 'fall2020' :
            print('Fall 2020 dataset')
            print(df.columns)
            df = df[['username', 'Sex', 'International or Domestic', 'Acad Level BOT',
                   'Cum GPA', 'Math Plcmt', 'CanvasCourseID_long', 'Term Code']]
            print(df.columns)
            df = df.rename({'username': 'Campus ID'}, axis='columns')
            print(df.columns)
        if df_term == 'winter2019' :
            print('Winter 2019 dataset')
            print(df.columns)
            df = df.rename({'Inferred Canvas LONG ID': 'CanvasCourseID_long'}, axis='columns')
            print(df.columns)
        df_main = pd.concat([df_main,df])
        print('- - - - - ',df_term,' df column list - - - - - -')
        print(df.columns)
        i = 0
        for item in df.columns :
            i += 1
            print(i,': ',item)
        print('- - - - - full df column list - - - - - -')
        print(df_main.columns)
        i = 0
        for item in df_main.columns :
            i += 1
            print(i,': ',item)
        # print(df_main.head(5))
        # print(df_main.shape)

    # TODO Plot the timeseries
    else:
        print(' - other file')

print('BREAK')
print(df_main.columns)
print(df_main.head(5))
