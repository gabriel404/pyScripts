import os
import sys

#Variables
gameRunning = True
rletters = []
wletters = []
keyword = []

#Functions
#Func that uses the command 'clear' on the terminal
clear = lambda: os.system("clear")

def playAgain():
    pA = input("Do you want to play again? (Y/n)")
    if (pA == "") or (pA == "y"):
        game()
    else:
        sys.exit()

def chkWin():
    if (rletters == keyword):
        clear()
        print("CONGRATULATIONS")
        print("THE WORD WAS: {}".format(keyword))
        playAgain()

def game():
    global gameRunning
    global rletters
    global wletters
    global keyword

    rletters = []
    wletters = []
    keyword = []

    clear()
    x = input("Type in the Keyword: ")
    x = x.upper()
    clear()
    for c in x:
        keyword.append(c)

    while gameRunning:
        letter = input("Type in a letter: ")
        letter = letter.upper()

        for key in keyword:
            if key == letter:
                rletters.append(letter)
                break
        else:
            wletters.append(letter)

        clear()
        rletters.sort(key=keyword.index)
        print("Wrong Letters: {}".format(wletters))
        print("Right Letters: {}".format(rletters))
        chkWin()

while True:
    game()
    playAgain()
