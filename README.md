# email_validator_GUI
This is a tkinter project, that takes excel or csv files, takes the emails row, divides the file, and validates them,  them separating the valid and invalid ones.


#email_validator_GUIV1.py
This is the main code. It uses tkinter as the GUI, and pyAutoGUI as support, concurrent.futures to make the functions work cuncurrently, pandas to read csv and excel, as well as write csv's.

It can take both csv or excel files, it turns the excel file to a csv for speedier access, with it the file is divided into the number of logical processors avalible in your machine, and starts the search cuncurrently. A flaw in this program is that tkinter can't run it's pages while the python script is making the search, two solutions is to reserve one logical processor for maintainig the GUI and showing progress of the search (but it is not very efective thinking purelly from time lost from not using te processor) Or using another GUI like PyQT5 which has a thread safe function that avoids the freezing of the pages.
***The only way to see the progress of the search in this version is the command line***

#You can donwload this build as an easy to install EXE file in the *** directory
