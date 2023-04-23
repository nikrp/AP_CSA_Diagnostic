########### IMPORTS ###########
from tkinter import *
from pandas import *
import random
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from PIL import ImageTk

########### QUIZ CLASS ###########
class ComputerScienceA():
    
    # Initialize ComputerScienceA()
    def __init__(self, window):
        """Initialize important variables."""
        self.window = window
        self.font = "Comic Sans MS"
        self.correct_answers = 0
        self.question_num = 1
        self.ques_num_index = 0
        self.correct_answers_dict = {}
        self.total_questions = 10
        self.current_index = 0

    
    def start_screen(self):
        """The starting screen for the diagnostic. This screen shows a dropdown where you can select your subject."""
        
        # Welcome - Label()
        self.welcome_title = Label(self.window, text="WELCOME!", font=(self.font, 24, "bold"), justify="center")
        self.welcome_title.grid(column=0, row=0, padx=400, columnspan=2)
        
        # Select Subjects - Label()
        self.select_subjects_txt = Label(self.window, text="Select a Subject to Continue: ", font=(self.font, 18, "bold"))
        self.select_subjects_txt.grid(column=0, row=3, pady=50, padx=(50, 0))
        
        # List of all the Subjects from CSV File - read_csv()
        self.subjects = list(read_csv("subjects.csv")["subjects"])
        
        # Dropdown - OptionMenu()
        self.clicked = StringVar()
        self.clicked.set("Click to Choose a Subject")
        self.drop_font = tkFont.Font(family="Comic Sans MS", size=18, weight="bold")
        self.menu_font = tkFont.Font(family="Comic Sans MS", size=15, weight="bold")
        self.dropdown = OptionMenu(self.window, self.clicked, *self.subjects, command=self.select_subject)
        self.dropdown.config(font=self.drop_font)
        self.menu = self.window.nametowidget(self.dropdown.menuname)
        self.menu.config(font=self.menu_font)
        self.dropdown.grid(column=1, row=3)
            
    def select_subject(self, event):
        """Save which option the user picked into a variable and start the showQuestion() method."""
        
        # List of all the File Names - read_csv()
        self.file_names = list(read_csv("subjects.csv")["file"])

        # Match self.clicked (the selected subject) with a File Name from subjects.csv - .index()
        self.file_name = self.file_names[self.subjects.index(self.clicked.get())]
        
        self.completed_subjects.append(self.subjects.index(self.clicked.get()))
        self.current_index = self.subjects.index(self.clicked.get())
        
        # Show the Questions
        self.showQuestion()
        
    def showQuestion(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.file_df = read_csv(self.file_name)
        self.questions = self.file_df["questions"][self.ques_num_index]
        self.op1 = self.file_df["op1"][self.ques_num_index]
        self.op2 = self.file_df["op2"][self.ques_num_index]
        self.op3 = self.file_df["op3"][self.ques_num_index]
        self.op4 = self.file_df["op4"][self.ques_num_index]
        self.ans = self.file_df["answer"][self.ques_num_index]
        
        self.v = StringVar(self.window, "0")
        
        self.values = {
            self.op1:"1",
            self.op2:"2",
            self.op3:"3",
            self.op4:"4",
        }
        
        r_btns = []
        btn_row = 2
        
        
        self.question_lbl = Label(self.window, text=f"{self.question_num}. {self.questions}", justify="center", font=(self.font, 18, "bold"))
        self.question_lbl.grid(column=0, row=0, padx=150)
        
        for (text, value) in self.values.items():
            r_btns.append(Radiobutton(self.window, text=text, variable=self.v, value=value, justify="left", font=(self.font, 15, "bold")))
        
        for btn in r_btns:
            btn.grid(column=0, row=btn_row, padx=30, pady=20, sticky="W")
            btn_row += 1
        
        self.submit_ans = Button(self.window, text="Submit", font=(self.font, 15, "bold"), command=self.check_answer)
        self.submit_ans.grid(column=0, row=6)
        
    def check_answer(self):
        """Check the answer and see if the user has finished all the questions or needs to move to the next one."""
        
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.chosen_ans = ""
        
        # Save the Chosen Answer into a Variable - (key, value)
        for (key, value) in self.values.items():
            if value == self.v.get():
                self.chosen_ans = key
                break
        
        # Compare the Chosen Answer and Correct Answer
        if self.chosen_ans == self.ans:
            Label(self.window, text="✔️ That was the correct answer!", font=(self.font, 24, "bold")).grid(column=0, row=0, padx=200)
            self.correct_answers += 1
        else:
            Label(self.window, text="❌ Sorry, that was incorrect.", font=(self.font, 24, "bold")).grid(column=0, row=0, padx=200)
            Label(self.window, text=f"The correct answer was: {self.ans}\nYou selected: {self.chosen_ans}", font=(self.font, 15, "bold")).grid(column=0, row=2, pady=10, padx=50)
        
        self.question_num += 1
        # "Next Question Button for the User"
        self.next_btn = Button(self.window, text="Next Question", font=(self.font, 18, "bold"), command=self.showQuestion)
        self.end_test = Button(self.window, text="End Test", font=(self.font, 18, "bold"), command=self.show_results)
        
        # Decide Which Button to Grid
        if self.question_num >= self.total_questions + 1:
            self.end_test.grid(column=0, row=3, pady=30)
        else:
            self.ques_num_index += 1
            self.next_btn.grid(column=0, row=3, pady=30)
    
    def show_results(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.subjects_csv = read_csv("subjects.csv")
        self.subjects_csv.loc[self.current_index, "correct"] = int(self.correct_answers)
        self.subjects_csv.to_csv("subjects.csv", index=False)
        
        self.correct_total = Label(self.window, text=f"{self.correct_answers}/{self.question_num - 1} Questions Answered Correctly", font=(self.font, 24, "bold"))
        self.correct_total.grid(column=0, row=0, padx=250)
        
        # Create the Bar Graph
        plt.figure(figsize=[11, 4])
        
        # Get the Total Questions for Each Subject
        self.total_qs = [self.total_questions for i in self.subjects]
            
        # Graph the Colored Bars to their Respective Area
        for i in range(len(self.subjects)):
            plt.bar(self.subjects[self.current_index], self.total_qs[i] - list(self.subjects_csv["correct"])[self.current_index], bottom=list(self.subjects_csv["correct"])[self.current_index], color="red")
            plt.bar(self.subjects[self.current_index], list(self.subjects_csv["correct"])[self.current_index], color="green")
        
        # Place the Legend onto the Screen
        plt.legend(labels=["Wrong Answers", "Correct Answers"])
        
        # Change the Title of the Graph
        plt.title("Results of your Diagnostic(s)")
        
        # Create the Axis Labels
        plt.xlabel("Subjects")
        plt.ylabel("Results")
        
        # Save the Graph as a PNG Image
        plt.savefig("BarPlot.png")