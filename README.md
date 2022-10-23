# Email validator GUI *Project Overview*
This is a easy to use email validator user interface, that takes excel or csv files, selects the row that has emails, divides the file into various files to make it easier to search, and validates them, separating the valid and invalid ones, then gives you the option to exctract a csv of the valid or invalid ones.
I plan on adding a function that analizes and gives potential reasons that the invalid emails does't exist.


# email_validator_GUIV1.py
This is the main code. It uses tkinter as the GUI, and pyAutoGUI as support, concurrent.futures to make the functions work cuncurrently, pandas to read csv and excel, as well as write csv's.

It can take both csv or excel files, it turns the excel file to a csv for speedier access, with the CSV ready the file is divided into the number of logical processors avalible in your machine, and starts the search cuncurrently. A flaw in this program is that tkinter can't run it's pages while the python script is making the search, two solutions is to reserve one logical processor for maintainig the GUI and showing progress of the search (but it is not very efective thinking purelly from time lost from not using te processor) Or using another GUI like PyQT5 which has a thread safe function that avoids the freezing of the pages.
***The only way to see the progress of the search in this version is the command line***

# You can donwload this build as an easy to install EXE file in the email_valV1 directory
made using auto-py-to-exe.
