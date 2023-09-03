from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
import os
import time

#Создание окна
WIDTH, HEIGHT = 600, 200

window = tk.Tk()
window.title("Обучение")
window.geometry('%sx%s' % (WIDTH, HEIGHT))

#Функция для приведения положительных изображений к общему формату,
#т.е. создание файла samples.vec на основе данных из good.dat
def plus_imges():
    os.system(r"c:\Users\olesi\desktop\opencv\build\x64\vc10\bin\opencv_createsamples.exe -info c:\Users\olesi\desktop\potato\good.dat -vec c:\users\olesi\desktop\potato\samples.vec -w 20 -h 30")
    msg_add = "Положительные изображения приведены к общему формату."
    mb.showinfo("Информация", msg_add)

#Функция создания итогового каскада,
#на основе которого будет производиться распознавание клубней
def create_cascade():
    os.system('mkdir haarcascade')
    start = time.time()
    os.system(r"c:\Users\olesi\desktop\opencv\build\x64\vc10\bin\opencv_traincascade.exe -data haarcascade -vec c:\users\olesi\desktop\potato\samples.vec -bg C:\Users\olesi\Desktop\potato\bad.dat -numStages 16 -minhitrate 0.8 -maxFalseAlarmRate 0.4 -numPos 17 -numNeg 330 -w 20 -h 30 -mode ALL -precalcValBufSize 1024 -precalcIdxBufSize 1024")
    end = (time.time()-start)/60
    msg_add = "Итоговый каскад создан за "+str(end)+" минут."
    mb.showinfo("Информация", msg_add)

#Добавление кнопок для запуска функций
btn_one_format=Button(window,text='Привести положительные изображения \n к общему формату', command=plus_imges)
btn_one_format.pack(pady=15)

btn_one_format=Button(window,text='Создать итоговый каскад', command=create_cascade)
btn_one_format.pack(pady=15)

window.mainloop()