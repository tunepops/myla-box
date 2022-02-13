# myla-box
Project Repository for work pertaining to MyLA usage research

## Intro
This is my first git repository, so I hope I use these features appropriately.

The first thing I intend to add is the code shared by Zhen, which connects to dropbox via python to access the shared data files in that folder.
It is already set up to connect to, access, and import the files into a dataframe.

Some important upcoming tasks would be to:
- [ ] parse the 'extra' column in the 'event_log' dataset into multiple columns
  - this could be split into multiple cases depending on the 'action' value
- [ ] join the 'event_log' datasets and the 'student_course' datasets into one dataframe
  - [ ] this could be a simple union for the multiple terms of data for 'event_log' and for 'student_course' datasets separately
    - this would be a good one to try first
    - will likely add a column identifying the term code for each of the 4 sets
      - currently only 3 sets until we receive access to Fall 2020 as well
  - [ ] it will likely require a left outer join to combine the 'event_log' data with the 'student_course' data
    - the student id and course id ought to be the key for this join, perhaps the term code as well
    - it will be important that the 'student_course' dataset is the outer in this join
      - this is because not every student appears in the 'event_log' dataset and we want to consider these "non-myla-users" as well in our analysis
