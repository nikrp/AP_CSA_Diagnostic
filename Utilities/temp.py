import pandas as pd
import basic_programming_concepts as bpc
import re

questions = []
op1 = []
op2 = []
op3 = []
op4 = []
ans = []

def convertBasic(questions, op1, op2, op3, op4, ans):
    for (key, value) in bpc.easy.items():
        questions.append(key)
        op1.append(value[0])
        op2.append(value[1])
        op3.append(value[2])
        op4.append(value[3])
        ans.append(value[4])

    bc_df = pd.DataFrame({
        "questions":questions,
        "op1":op1,
        "op2":op2,
        "op3":op3,
        "op4":op4,
        "answer":ans
    })

    bc_df.to_csv("basic_easy.csv")

def convertOOP(questions, op1:list, op2:list, op3:list, op4:list, ans:list):

    file = open("temp_ques.txt", 'r')
    
    file_list = file.readlines()
    file_list = [i for i in file_list if i != "\n"]
    file_list = [i.strip() for i in file_list]
    #print(file_list)
    
    questions = [i for i in file_list if "?" in i]
    questions = [re.sub(r'\d+\. ', "", i) for i in questions]
    
    op1 = [i for i in file_list if i.startswith("a)")]

    
    op2 = [i for i in file_list if i.startswith("b)")]

    
    op3 = [i for i in file_list if i.startswith("c)")]

    
    op4 = [i for i in file_list if i.startswith("d)")]

    
    ans = [i for i in file_list if i.startswith("ans: ")]
    ans = [re.sub(r'ans: ', "", i) for i in ans]
    
    df = pd.DataFrame({
        "questions":questions,
        "op1":op1,
        "op2":op2,
        "op3":op3,
        "op4":op4,
        "answer":ans
    })
    
    df.to_csv("oop.csv")
    
if __name__ == "__main__":
    convertOOP(questions, op1, op2, op3, op4, ans)