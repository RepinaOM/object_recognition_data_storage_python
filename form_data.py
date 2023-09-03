#Формирование данных
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
import os
import pymysql

#Создание окна и указание его параметров
WIDTH, HEIGHT = 600, 200
window = tk.Tk()
window.title("Формирование данных")
window.geometry('%sx%s' % (WIDTH, HEIGHT))

#Подключение к базе данных
connection = pymysql.connect(
    host='localhost', #Локальный хост
    user='root', #Имя пользователя
    db='potato_learning')#Название базы данных

#Функция для подготовки "плохих" файлов для обучения
def form_dir_dat_bad():
    global connection
    global i
    with connection.cursor() as cursor:
        # Создание запроса для выбора всех "плохих" файлов из базы данных
        sql_bads_files = "SELECT * FROM bads"
        cursor.execute(sql_bads_files)
        bads_files = cursor.fetchall()
        #Создание папки с "плохими" файлами
        os.system('mkdir Bad') 
        #Создание файла с названиями "плохих" файлов
        bad_file = open("Bad.dat", "w")
        bad_file.close()
        i=0
        for bad_file in bads_files:
            #Добавление "плохого" файла в соответствующую папку
            os.system('copy '+bad_file[2]+'\\'+bad_file[1]+' Bad\\image'+str(i)+'.jpg')
            #Запись названия файла в список "плохих" файлов
            bad_file = open("Bad.dat", "a+")
            bad_file.write("Bad\\image"+str(i)+".jpg\n")
            bad_file.close()
            i=i+1

#Функция для подготовки "хороших" файлов для обучения
def form_dir_dat_good():
    global connection
    global j
    with connection.cursor() as cursor:
        # Создание запроса для выбора всех "хороших" файлов из базы данных
        sql_goods_files = "SELECT * FROM goods"
        cursor.execute(sql_goods_files)
        goods_files = cursor.fetchall()
        #Создание папки с "хорошими" файлами
        os.system('mkdir Good') 
        #Создание файла с названиями "хороших" файлов
        good_file = open("Good.dat", "w")
        good_file.close()
        j=0
        for good_file in goods_files:
            #Добавление "хорошего" файла в соответствующую папку
            os.system('copy '+good_file[2]+'\\'+good_file[1]+' Good\\image'+str(j)+'.jpg')
            # Создание запроса для выбора всех координат элементов для "хороших" файлов из базы данных
            sql_goods_files_cor = "SELECT * FROM goods_cor WHERE id_good_file="+str(good_file[0])
            cursor.execute(sql_goods_files_cor)
            good_file_cors = cursor.fetchall()
            str_good_cor = ""
            count_cor=0
            #Сбор строки с координатами элементов и подсчёт количества этих элементов
            for good_file_cor in good_file_cors:                
                str_good_cor = str_good_cor + str(good_file_cor[2])+" "+str(good_file_cor[3])+" "+str(good_file_cor[4])+" "+str(good_file_cor[5])+" "
                count_cor=count_cor+1
            #Добавление названия "хорошего" файла с координатами элементов (клубней)
            good_file = open("Good.dat", "a+")
            good_file.write("Good\\image"+str(j)+".jpg "+str(count_cor)+" "+str_good_cor+"\n")
            good_file.close()
            j=j+1

#Функция для подготовки запуска функций подготовки "хороших" и "плохих" файлов
#и вывода информации о сформированных данных
def form_data():
    form_dir_dat_good()        
    form_dir_dat_bad()
    msg_add = "Сформирован датасет из \n"+str(j)+" 'хороших' файлов. \n и "+str(i)+" 'плохих' файлов."
    mb.showinfo("Информация", msg_add)

#Добавление кнопки запуска формирования данных
btn_form=Button(window,text='Запустить формирование данных \n для обучения', command=form_data)
btn_form.pack(pady=70)

window.mainloop()