########### IMPORTS ###########
from quiz_ui import ComputerScienceA
from tkinter import *

########### TKINTER WINDOW ###########
tkinter_win = Tk(screenName="AP CSA Diagnostic")
tkinter_win.title("AP CSA Diagnostic")
tkinter_win.geometry("1200x450")

quiz = ComputerScienceA(tkinter_win)
quiz.start_screen()

tkinter_win.mainloop()