# myla-box
Project Repository for work pertaining to MyLA usage research

## Intro
This is my first git repository, so I hope I use these features appropriately.

The first thing I intend to add is the code shared by Zhen, which connects to dropbox via python to access the shared data files in that folder.
It is already set up to do so and import the files into a dataframe.

Some important upcoming tasks would be to:
- parse the 'extra' column in the 'event_log' dataset into multiple columns
  - this could be split into multiple cases depending on the 'action' value
- join the 'event_log' datasets and the 'student_course' datasets into one dataframe
  - this could be a simple union for the multiple terms of data for 'event_log' and for 'student_course'
