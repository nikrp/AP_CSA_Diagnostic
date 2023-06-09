########### IMPORTS ###########
from tkinter import *
from pandas import *
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from smtplib import SMTP
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox

########### QUIZ CLASS ###########
class ComputerScienceA():
    
    # Initialize ComputerScienceA()
    def __init__(self, window):
        """Initialize important variables."""
        self.window = window
        self.font = "Comic Sans MS"
        self.correct_answers = 0
        self.ques_num_index = 0
        self.correct_answers_dict = {}
        self.total_questions = 10
        self.current_index = 0

    # Start Screen
    def start_screen(self):
        """The starting screen for the diagnostic. This screen shows a dropdown where you can select your subject."""
        
        # Destroy all Widgets on Screen
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Question Num Reset
        self.question_num = 1
        
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
    
    # Select Which Subject They Picked
    def select_subject(self, event):
        """Save which option the user picked into a variable and start the showQuestion() method."""
        
        # List of all the File Names - read_csv()
        self.file_names = list(read_csv("subjects.csv")["file"])

        # Match self.clicked (the selected subject) with a File Name from subjects.csv - .index()
        self.file_name = self.file_names[self.subjects.index(self.clicked.get())]
        
        # Get the Current Index of the Chosen Subject
        self.current_index = self.subjects.index(self.clicked.get())
        
        # Show the Questions
        self.show_question()
    
    # Start Showing Questions
    def show_question(self):
        """This method starts showing questions for the user to answer."""
        
        # Destroy all Widgets on Screen
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Get the Questions and Answers and the Correct Answer
        self.file_df = read_csv(self.file_name)
        self.questions = self.file_df["questions"][self.ques_num_index]
        self.op1 = self.file_df["op1"][self.ques_num_index]
        self.op2 = self.file_df["op2"][self.ques_num_index]
        self.op3 = self.file_df["op3"][self.ques_num_index]
        self.op4 = self.file_df["op4"][self.ques_num_index]
        self.ans = self.file_df["answer"][self.ques_num_index]
        
        # Radio Buttons StringVar()
        self.v = StringVar(self.window, "0")
        
        # Radio Button Values
        self.values = {
            self.op1:"1",
            self.op2:"2",
            self.op3:"3",
            self.op4:"4",
        }
        
        # Radio Button Variables
        r_btns = []
        btn_row = 2
        
        # Show the Question with the Number
        self.question_lbl = Label(self.window, text=f"{self.question_num}. {self.questions}", justify="center", font=(self.font, 18, "bold"))
        self.question_lbl.grid(column=0, row=0, padx=150)
        
        # Create the Radio Button Objects
        for (text, value) in self.values.items():
            r_btns.append(Radiobutton(self.window, text=text, variable=self.v, value=value, justify="left", font=(self.font, 15, "bold")))
        
        # Grid the Radio Buttons
        for btn in r_btns:
            btn.grid(column=0, row=btn_row, padx=30, pady=20, sticky="W")
            btn_row += 1
        
        # Submit Answer Button
        self.submit_ans = Button(self.window, text="Submit", font=(self.font, 15, "bold"), command=self.check_answer)
        self.submit_ans.grid(column=0, row=6)
        
    # Check the Answer    
    def check_answer(self):
        """Check the answer and see if the user has finished all the questions or needs to move to the next one."""
        
        # Destroy all Widgets on Screen
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Get the Users Chosen Answer
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
        
        # Add to the Question Number
        self.question_num += 1
        
        # Next Question Button for the User
        self.next_btn = Button(self.window, text="Next Question", font=(self.font, 18, "bold"), command=self.show_question)
        self.end_test = Button(self.window, text="End Test", font=(self.font, 18, "bold"), command=self.show_results)
        
        # Decide Which Button to Grid
        if self.question_num >= self.total_questions + 1:
            self.end_test.grid(column=0, row=3, pady=30)
        else:
            self.ques_num_index += 1
            self.next_btn.grid(column=0, row=3, pady=30)
    
    def show_results(self):
        """Show how the user did on their test and give some extra options."""
        
        # Destroy all Widgets on Screen
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Save the amt of Correct and Total Answers
        self.subjects_csv = read_csv("subjects.csv")
        self.subjects_csv.loc[self.current_index, "correct"] = int(self.correct_answers)
        self.subjects_csv.loc[self.current_index, "total"] = int(self.question_num - 1)
        self.subjects_csv.to_csv("subjects.csv", index=False)
        
        # Show the Total Score of the User
        self.correct_total = Label(self.window, text=f"{self.correct_answers}/{self.question_num - 1} Questions Answered Correctly", font=(self.font, 24, "bold"))
        self.correct_total.grid(column=0, row=0, padx=250, columnspan=2)
        
        # Create the Bar Graph
        plt.figure(figsize=[11, 4])
                    
        # Graph the Colored Bars to their Respective Area
        for i in range(len(self.subjects)):
            plt.bar(self.subjects[i], self.subjects_csv["total"][i] - self.subjects_csv["correct"][i], bottom=self.subjects_csv["correct"][i], color="red")
            plt.bar(self.subjects[i], self.subjects_csv["correct"][i], color="green")
        
        # Place the Legend onto the Screen
        plt.legend(labels=["Wrong Answers", "Correct Answers"])
        
        # Change the Title of the Graph
        plt.title("Results of your Diagnostic(s)")
        
        # Create the Axis Labels
        plt.xlabel("Subjects")
        plt.ylabel("Results")
        
        # Save the Graph
        plt.savefig("BarPlot.png")
        
        # Create the Show Graph Button
        self.show_graph = Button(self.window, text="Show Graph", font=(self.font, 15, "bold"), command=self.show_graph_command)
        
        # Graph the Button
        self.show_graph.grid(column=0, row=3)
        
        # Entry Object to send User their Results
        self.email_input = Entry(self.window, width=20, font=("self.font", 15))
        self.email_input.grid(column=1, row=1)
        
        # Entry Decription Label
        self.email_description = Label(self.window, text="Please enter your email and press send to be sent your results.\nOr press exit or another test to leave this screen: ", font=(self.font, 15, "bold"))
        self.email_description.grid(column=0, row=1, rowspan=2)
        
        # Create the Send Button
        self.send_btn = Button(self.window, text="Send", font=(self.font, 15, "bold"), command=self.send)
        self.send_btn.grid(column=1, row=5)
        
        # Create Another Test Button
        self.another_test = Button(self.window, text="Take Another Test", font=(self.font, 15, "bold"), command=self.start_screen)
        self.another_test.grid(column=0, row=5)
        
        # Create Clear Graph Button
        self.clear = Button(self.window, text="Clear History", font=(self.font, 15, "bold"), command=self.clear_graph)
        self.clear.grid(column=0, row=6, columnspan=2, pady=50)
    
    def show_graph_command(self):
        """Show the graph after a button is clicked."""
        plt.show()
    
    def send(self):
        """Send the email to the user's entered email address."""
        
        # Save the Reciever's Email Address
        self.sender = "<youremailid-here>@gmail.com"
        self.reciever = self.email_input.get()
        
        # Read the Image
        with open("BarPlot.png", 'rb') as f:
            self.img_data = f.read()
        
        # Set the Labels in the Msg
        self.msg = MIMEMultipart()
        self.msg["Subject"] = "AP CSA Diagnostic Results"
        self.msg["From"] = self.sender
        self.msg["To"] = self.reciever
        
        # Attach the Text and Image to the Msg
        self.text = MIMEText("test")
        self.msg.attach(self.text)
        self.image = MIMEImage(self.img_data, name = os.path.basename("BarPlot.png"))
        self.msg.attach(self.image)
        
        # Login to the Host Server
        s = SMTP("smtp.gmail.com", port=587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user=self.sender, password="<your app password>")
        
        # Try Sending the Email
        try:
            s.sendmail(self.sender, self.reciever, self.msg.as_string())
        except:
            messagebox.showerror("Error Sending Email", "There was an error trying to send an email, sorry.")
        else:
            messagebox.showinfo("Completed", "The plot was sent to your email. Please check it and your results will appear shortly.")
        finally:
            s.quit()
        
    def clear_graph(self):
        """Clear the Graph's History"""
        
        # Change all Scores and Totals Back to 0
        self.subjects_csv["correct"] = 0
        self.subjects_csv["total"] = 0
        self.subjects_csv.to_csv("subjects.csv", index=False)
        
        # Show Completion
        messagebox.showinfo("Graph History", "Your Graph History is cleared. Next time you take a diagnostic, it's a fresh start.")
        
        # Loop Back
        self.start_screen()