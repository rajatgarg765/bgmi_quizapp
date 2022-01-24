

from filecmp import clear_cache
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import certifi
import ssl
import urllib.request as urlrq
#from urllib.request import urlopen
import json
import pandas as pd
import random

webpage= urlrq.urlopen("https://opentdb.com/api.php?amount=50&category=21&difficulty=medium&type=multiple", cafile=certifi.where())
data=json.loads(webpage.read().decode())
#print(data)
df=pd.DataFrame(data['results'])
#print(df.head(5))

def preload_data(idx):
    question=df['question'][idx]
    correct=df['correct_answer'][idx]
    wrong=df['incorrect_answers'][idx]

    #characters with bad formatting and their correction
    formatting=[
        ("#039;",""),
        ("&'","'"),
        ("&quot;",'"'),
        ("&lt;","<"),
        ("#gt;",">")
    ]

    #replace  bad characters in string
    for tuple in formatting:
        question=question.replace(tuple[0],tuple[1])
        correct=correct.replace(tuple[0],tuple[1])

    #replace bad characters in lists
    for tuple in formatting:
        wrong=[char.replace(tuple[0],tuple[1]) for char in wrong]
    print(wrong)
    parameters["question"].append(question)
    parameters["correct"].append(correct)

    all_answer=wrong+[correct]
    random.shuffle(all_answer)
    #print(all_answer)

    parameters["answer1"].append(all_answer[0])
    parameters["answer2"].append(all_answer[1])
    parameters["answer3"].append(all_answer[2])
    parameters["answer4"].append(all_answer[3])

parameters={
    "question":[],
    'answer1':[],
    'answer2':[],
    'answer3':[],
    'answer4':[],
    "correct":[],
    "score":[],
    "index":[]
}
#global dictionary of dynamically changing widgets
widgets={ 
    "logo": [],
    "button": [],
    "question":[],
    'score':[],
    'answer1':[],
    'answer2':[],
    'answer3':[],
    'answer4':[],
    "message": [],
    "message2": []
}

app=QApplication(sys.argv)

#for just making the starter file
window=QWidget()
window.setWindowTitle("Lets play a quiz on BGIS!!!!")
window.setFixedWidth(1000)
#window.setFixedHeight(2000)
window.move(100,100)
window.setStyleSheet("background: #161219;")
#for grid layout by adding widget
grid =QGridLayout()

def clear_widgets():
        #''' hide all existing widgets and erasethem from the global dictionary'''
    for widget in widgets:
        if widgets[widget]!=[]:
            widgets[widget][-1].hide()
        for i in range(0,len(widgets[widget])):
            widgets[widget].pop()

def clear_parameters():
    for parm in parameters:
        if parameters[parm]!=[]:
            for i in range(0,len(parameters[parm])):
                parameters[parm].pop()
    
    parameters["index"].append(random.randint(0,49))
    parameters["score"].append(0)

def show_frame1():
    clear_widgets()
    clear_parameters()
    frame1()

def start_game():
    #start the game, reset all widgets
    clear_widgets()
    clear_parameters()
    preload_data(parameters["index"][-1])
    frame2()

def create_buttons(answer,l_margin,r_margin):
    button=QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet("*{border:4px solid '#BC006C';"+
                         "margin-left:"+str(l_margin)+"px;"+
                         "margin-right:"+str(r_margin)+"px;"+
                         "color:white;"+
                         "font-family:'shanti';"+
                         "font-size:16px;"+
                         "border-radius:25px;"+
                         "padding:15px 0;"+
                         "margin-top:5px}"+
                         "*:hover{background: '#BC006C'}" )
    
    #button.clicked.connect(show_frame1)
    button.clicked.connect(lambda x: is_correct(button))
    return button

def is_correct(btn):
    #print(answer)
    if btn.text()==parameters['correct'][-1]:
        print(btn.text()+" is correct.")
    
        temp_score=parameters["score"][-1]
        parameters["score"].pop()
        parameters['score'].append(temp_score+10)

        parameters["index"].pop()
        parameters['index'].append(random.randint(0,49))
        preload_data(parameters["index"][-1])

        widgets['score'][-1].setText(str(parameters["score"][-1]))
        widgets['question'][0].setText(parameters["question"][-1])
        widgets['answer1'][0].setText(parameters["answer1"][-1])
        widgets['answer2'][0].setText(parameters["answer2"][-1])
        widgets['answer3'][0].setText(parameters["answer3"][-1])
        widgets['answer4'][0].setText(parameters["answer4"][-1])

        if parameters['score'][-1]==100:
            clear_widgets()
            frame3()

    else:
        clear_widgets()
        frame4()

def frame1():
    clear_widgets()
    #display logo
    image=QPixmap('logo.png')
    logo=QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 20px;")
    widgets['logo'].append(logo)

    #button widget
    button=QPushButton("Start")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    #button.setStyleSheet("margin-top: 100px;")
    button.setStyleSheet("*{border:3px solid '#BC006C';"+
                        "border-radius: 25px;" +
                        "font-size:25px;"+
                        "color:'white';"+
                        "padding: 25px 0px;"+
                        "margin:40px 150px;}"+
                        "*:hover{background:'#BC006C';}")
    button.clicked.connect(start_game)

    widgets['button'].append(button)

    grid.addWidget(widgets['logo'][-1],0,0,1,2)
    grid.addWidget(widgets['button'][-1],1,0,1,2)
#frame1()

def frame2():
    score=QLabel(str(parameters["score"][-1]))
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet("border:1px solid '#64A314';"+
                        "border-radius: 40px;" +
                        "font-size:25px;"+
                        "color:'white';"+
                        "padding:25px 20px 0px 20px;"+
                        "margin:10px 140px;"+
                        "background:'#64A314';")
    
    widgets['score'].append(score)
    
    #question=QLabel("Lets start the  quiz. Are You Ready???")
    question=QLabel(parameters["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet("font-family: 'shanti';"+
                           "font-size: 25px;"+
                           "color:'white';"+
                           "padding:35px")
    
    widgets['question'].append(question)

    button1=create_buttons(parameters["answer1"][-1],85,5)
    button2=create_buttons(parameters["answer2"][-1],5,85)
    button3=create_buttons(parameters["answer3"][-1],85,5)
    button4=create_buttons(parameters["answer4"][-1],5,85)
    
    widgets['answer1'].append(button1)
    widgets['answer2'].append(button2)
    widgets['answer3'].append(button3)
    widgets['answer4'].append(button4)

    #display logo
    image=QPixmap('logo_bot.png')
    logo=QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:10px; margin-bottom:30px;")
    widgets['logo'].append(logo)


    grid.addWidget(widgets["score"][-1],0,1)
    grid.addWidget(widgets["question"][-1],1,0,1,2)
    grid.addWidget(widgets["answer1"][-1],2,0)
    grid.addWidget(widgets["answer2"][-1],2,1)
    grid.addWidget(widgets["answer3"][-1],3,0)
    grid.addWidget(widgets["answer4"][-1],3,1)
    grid.addWidget(widgets["logo"][-1],4,0,1,2)


def frame3():
    #congradulations widget
    message = QLabel("Congratulations! You\n have WON!\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 25px; color: 'white'; margin: 100px 0px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel(str(parameters['score'][-1]))
    score.setStyleSheet("font-size: 100px; color: #8FC740; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #go back to work widget
    message2 = QLabel("OK. Now go back to WORK.")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
        )
    widgets["message2"].append(message2)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{background:'#BC006C'; padding:25px 0px; border: 1px solid '#BC006C'; color: 'white'; font-family: 'Arial'; font-size: 25px; border-radius: 40px; margin: 10px 300px;} *:hover{background:'#ff1b9e';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)
    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bot.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)

#*********************************************
#                  FRAME 4 - FAIL
#*********************************************
def frame4():
    #sorry widget
    message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel(str(parameters['score'][-1]))
    score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        '''*{
            padding: 25px 0px;
            background: '#BC006C';
            color: 'white';
            font-family: 'Arial';
            font-size: 35px;
            border-radius: 40px;
            margin: 10px 200px;
        }
        *:hover{
            background: '#ff1b9e';
        }'''
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)
    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bot.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)


frame1()

window.setLayout(grid)

window.show()
sys.exit(app.exec())
