# Web Project

It is recommended to view the web application in a Chrome or Edge browser in full screen for the best experience.


## Database
The main databases are *School.db* and *Account.db* and may be edited. The *School_copy.db*, *School_backup.db*, and *Account_backup.db* databases are used to revert changes made to *School.db* and *Account.db* and should not be edited.

Within *School.db*, *CCASession* and *TeacherCourse* records as well as Student and Teacher IDs are randomly generated.


## Availability Tab
There are two columns of input boxes. The first column filters for students which will appear in the table below when the *Add Students* button is pressed. Students can be filtered by their name, the name of their PM class, the name of a course they attend, the name of a teacher that teaches any of the courses they attend, and the name of a CCA they attend. 

The second column filters for teachers which will appear in the table below when the *Add Teachers* button is pressed. Teachers can be filtered by their name, the name of their PM class, the name of a course they teach, the name of a student that they teach in any of their courses, and the name of a CCA they attend.

If multiple filters are applied, only students/teachers that pass all filters will be added to the student/teacher table. Filtered students/teachers will be appended to the table and existing elements in the table will not be removed.

The *Clear Students* button removes all elements from the table of filtered students while the *Clear Teachers* button removes all elements from the table of filtered teachers. Individual students/teachers can also be removed from the tables by clicking on the respective delete icon.

The *Search Availability* button will redirect to a new page where the shared availability timings of all the students and teachers in the filtered tables are displayed. Times can be removed from the table in the new page by clicking on the respective delete icon.


## Login
Upon first viewing the landing page, a button to login will be present. A table of usernames and passwords with the respective authorisation levels is shown below.

Username | Password | Authorisation
---------|----------|--------------
Admin | I[Ca@s&MR9 | 1
Username | Password | 2


## Add Tab
Available after logging in, the first select box indicates the table in which a record should be added. The other inputs will change depending on its value.

The *Add Record* button will only become enabled when all fields are properly filled in. If a dropdown is present on a field, one of its items must be selected.

Verification is present for StudentID and TeacherID when adding new students and teachers. The *gen_ic()* function in the *project.py* file may be used to generate legitimate NRIC/FIN numbers for StudentID and TeacherID.

StartTime and EndTime inputs for the Session tables must be valid 24-hour times between 0800 and 1900.

Records may not be added if uniqueness of primary keys or foreign relations are not maintained or if clashes in schedule arise.


## Search Tab
Available after logging in, the first select box indicates the table from which a record should be searched. The other inputs and the table will change depending on its value.

Records are dynamically filtered based on the filters. If multiple filters are applied, only records that pass all filters will be displayed in the table. Filtered records will replace any existing elements in the table. The records can be edited by clicking the edit icon. Any edits must ensure that uniqueness of primary keys and foreign relations are maintained. Edits that result in scheduling clashes will not be registered.

Records can be deleted by selecting the checkboxes for each record and pressing the *Delete* button that appears or the delete key. Shift click can be used to select multiple records.

All changes are automatically saved.


## Account Tab
Available after logging in with an account with level 2 authorisation, a table with all the account data is present. The username and password of each account can be edited by clicking the edit icon. Any edits must ensure that all usernames remain unique.

Accounts can be deleted by selecting the checkboxes for each account and pressing the *Delete* button that appears or the delete key. Shift click can be used to select multiple accounts. Accounts with level 2 authorisation cannot be deleted in this way.

Accounts can be added to the database by pressing the *Add Account* button. The username must be unique. Accounts with level 2 authorisation cannot be added in this way.

All changes are not automatically saved. Refreshing the page will revert all changes that are not saved. The *Save Changes* button must be pressed to save any changes made to the Account database. 

Accounts with level 2 authorisation can be created or deleted by passing a command directly into the /postdata URL while logged in with level 2 authorisation although it is not recommended or by editing *Account.db*.


## Restore Tab
Available after logging in, the *Restore School* button restores the School database to a backup, reverting all changes.

Available after logging in with an account with level 2 authorisation, the *Restore Account* button restores the Account database to a backup, reverting all changes.
