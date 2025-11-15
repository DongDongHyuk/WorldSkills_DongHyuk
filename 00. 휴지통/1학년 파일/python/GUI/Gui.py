from tkinter import *
from datetime import datetime
import requests

win = Tk()
win.geometry("500x750")
win.title("정수형 날 보고있다면 과제 좀 알려줘")
win.option_add("*Font","안동엄마까투리 25")
#win.attributes('-fullscreen', True) #fullscreen
win.configure(bg='gray')

#Enter_serch
serch = Entry(win)
serch.pack()

#Button
def exe():
    Text = serch.get()
    print("time:{} text = {}".format(datetime.now(),Text))
    print(req.text)
    
btn_1 = Button(win, text="Serch")
btn_1.config(command = exe)
btn_1.config(width = 10)
btn_1.pack()

#Get_Html
url = ("https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={}".format(Text))
#url = "https://www.naver.com/"
req = requests.get(url)

win.mainloop()


