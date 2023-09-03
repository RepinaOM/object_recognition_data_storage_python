from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
from PIL import Image, ImageTk
import os
import pymysql

#Подключение к базе данных
connection = pymysql.connect(
    host='localhost', #Подклюение к локальному хостингу
    user='root',#Имя пользователя
    db='potato_learning')#Название базы данных


#Добавление "плохих" файлов, когда все файлы папки "плохие"
def add_bads_files():
    global connection
    #Объект в памяти компьютера с методами для проведения SQL команд
    with connection.cursor() as cursor:
        path = str(folder_tf.get())
        files = os.listdir(path)
        row=0
        for file in files:
            # Создание нового запроса к таблице bads ("плохих" файлов)
            sql_add_bad = "INSERT INTO `bads` (`bad_file`, `dir_bad_file`) VALUES (%s, %s)"
            cursor.execute(sql_add_bad, (file, path))
            row=row+1
        #Сохранение изменений в базе данных
        connection.commit()
        #Подсчёт всех "плохих" файлов в базе данных и вывод этой информации на экран
        sql_count_bad = "SELECT COUNT(id_bad_file) from bads"
        cursor.execute(sql_count_bad)
        count_bads = cursor.fetchone()
        msg_add_bads = "Добавлено "+str(row)+" 'плохих' файлов. \n Общее количество 'плохих' файлов: "+str(count_bads[0])+"."
        mb.showinfo("Информация", msg_add_bads)
    connection.cursor.close()

#Добавление всех хороших файлов, где все изображения в папке содержат только один клубень
def add_goods_files():
    global connection
    with connection.cursor() as cursor:
        path = str(folder_tf.get())
        files = os.listdir(path)
        row=0
        for file in files:
            # Создание запроса к таблице goods ("хороших" файлов)
            sql_add_good = "INSERT INTO `goods` (`good_file`, `dir_good_file`) VALUES (%s, %s)"
            cursor.execute(sql_add_good, (file, path))
            # Определение размера изображения
            im = Image.open(path +"/"+ file)
            width, height = im.size
            # Получение id крайнего добавленного элемента к таблице goods
            sql_good_id = "SELECT * FROM goods WHERE id_good_file=LAST_INSERT_ID()"
            cursor.execute(sql_good_id)
            id_good = cursor.fetchone()  
            # Создание запроса к таблице goods_cor (координат "хороших" элементов изображения)
            # Хранение координат необходимо для формирования данных, с которыми будет работать библиотека распознавания
            sql_add_good_cor = "INSERT INTO `goods_cor` (`id_good_file`, `x0`, `y0`, `x1`, `y1`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_add_good_cor, (int(id_good[0]), 0, 0, width, height))
            connection.commit()
            row=row+1
        #Подсчёт всех "хороших" файлов в базе данных и вывод этой информации на экран
        sql_count_good = "SELECT COUNT(id_good_file) from goods"
        cursor.execute(sql_count_good)
        count_goods = cursor.fetchone()
        msg_add_goods = "Добавлено "+str(row)+" 'хороших' файлов. \n Общее количество 'хорошх' файлов: "+str(count_goods[0])+"."
        mb.showinfo("Информация", msg_add_goods)
    connection.cursor.close()

#Создание окна и установка его параметров
WIDTH, HEIGHT = 600, 600
topx, topy, botx, boty = 0, 0, 0, 0
rect_id = None

window = tk.Tk()
window.title("Подготовка данных")
window.geometry('%sx%s' % (WIDTH, HEIGHT))

#Чтение изображений из папки
def read_images():
    global path
    global files
    global count_img
    global count_images
    global new_image
    count_img = 0
    path = str(folder_tf.get())#папка
    files = os.listdir(path)#список файлов
    count_images = len(files)#количествво файлов в папке
    #Создание объекта озображения
    new_image=ImageTk.PhotoImage(file = path +"/"+ files[count_img])
    canvas.itemconfig(image_id, image=new_image)
    canvas.config(width=new_image.width(), height=new_image.height())

#Блок окна, где осуществляется работа с папками
#Для экономии времени на отборе файлов можно нажать на 
#кнопки добавления всех файлов папки в таблицу "хороших" или "плохих"
group_folder = tk.LabelFrame(window, padx=15, pady=10,
                                text="Работа с папками")
group_folder.pack(padx=10, pady=5)
folder_lb = Label(
   group_folder,
   text="Введите назание папки"
)
folder_lb.grid(row=0, column=0)
 
folder_tf = Entry(
   group_folder,
)
folder_tf.grid(row=0, column=1)

bad_btn = Button(
   group_folder,
   text='Все файлы в этой папке "плохие"',
   command=add_bads_files
)
bad_btn.grid(row=1, column=0, pady=7, padx=5)

good_btn = Button(
   group_folder,
   text='На этих файлах изображены только клубни, \n и только по одному',
   command=add_goods_files
)
good_btn.grid(row=2, columnspan=2, pady=7)

good_many_btn = Button(
   group_folder,
   text='Файлы этой папки нуждаются в проверке',
   command=read_images
)
good_many_btn.grid(row=1, column=1, pady=7, padx=5)

#Если нажата кнопка 'Файлы этой папки нуждаются в проверке',
#начинается работа вне блока "Работа с папками"

#Вывод стартового изображения, пока не выбрана папка для проверки изображений
img = ImageTk.PhotoImage(file = "start.jpg")
canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                borderwidth=0, highlightthickness=0)
canvas.pack()
image_id = canvas.create_image(0, 0, image=img, anchor=tk.NW)

#Создание прямоугольника для выделения области изображения
rect_id = canvas.create_rectangle(topx, topy, topx, topy,
                                dash=(2,2), fill='', outline='white')
#Функция для получения координат положения мыши
def get_mouse_posn(event):
    global topy, topx
    topx, topy = event.x, event.y

#Функция для изменения прямоугольника 
#в соответствии с движением мыши
def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty
    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)# Изменение прямоугольника
canvas.bind('<Button-1>', get_mouse_posn)
canvas.bind('<B1-Motion>', update_sel_rect)
#new_image=ImageTk.PhotoImage(file = "new/images6.jpg")

#Вывод следующей картинки
def show_new_img():
    global count_img
    global count_images
    global new_image
    #Если картинка в папке последняя, то выводится стартовое изображение
    if count_img >= count_images-1:
        new_image=ImageTk.PhotoImage(file = "start.jpg")
        canvas.itemconfig(image_id, image=new_image)
        canvas.config(width=new_image.width(), height=new_image.height())
    #Иначе выводится следующая по алфовиту картинка в папке
    else:
        count_img = count_img + 1
        new_image=ImageTk.PhotoImage(file = path + "/" +files[count_img])
        canvas.itemconfig(image_id, image=new_image)
        canvas.config(width=new_image.width(), height=new_image.height())
        
#Добавление хорошего файла, на котром изображён только один клубень
def add_good_file():
    global connection
    with connection.cursor() as cursor:
            # Создание запроса к таблице goods для добавления записи
            sql_add_good = "INSERT INTO `goods` (`good_file`, `dir_good_file`) VALUES (%s, %s)"
            cursor.execute(sql_add_good, (files[count_img], path))
            im = Image.open(path +"/"+ files[count_img])
            width, height = im.size
            # Полуение id крайнего добавленного элемента
            sql_good_id = "SELECT * FROM goods WHERE id_good_file=LAST_INSERT_ID()"
            cursor.execute(sql_good_id)
            id_good = cursor.fetchone()  
            # Добавление записи с координатами размера файла, так как на картинке только один клубень
            sql_add_good_cor = "INSERT INTO `goods_cor` (`id_good_file`, `x0`, `y0`, `x1`, `y1`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_add_good_cor, (int(id_good[0]), 0, 0, width, height))
            connection.commit()
            #Подсчёт количества "хороших" изображений и вывод этой информации на экран
            sql_count_good = "SELECT COUNT(id_good_file) from goods"
            cursor.execute(sql_count_good)
            count_goods = cursor.fetchone()
            msg_add_goods = "'Хороший' файл добавлен. \n Общее количество 'хорошх' файлов: "+str(count_goods[0])+"."
            mb.showinfo("Информация", msg_add_goods)
    connection.cursor.close()

#Добавление просматриваемого изображения в список "плохих" файлов
def add_bad_file():
    global connection
    with connection.cursor() as cursor:
            # Создание запроса к таблице bads для добавления записи
            sql_add_bad = "INSERT INTO `bads` (`bad_file`, `dir_bad_file`) VALUES (%s, %s)"
            cursor.execute(sql_add_bad, (files[count_img], path))
            connection.commit()
            # Подсчёт "плохих" файлов и вывод этой информации на экран
            sql_count_bad = "SELECT COUNT(id_bad_file) from bads"
            cursor.execute(sql_count_bad)
            count_bads = cursor.fetchone()
            msg_add_goods = "'Плохой' файл добавлен. \n Общее количество 'плохих' файлов: "+str(count_bads[0])+"."
            mb.showinfo("Информация", msg_add_goods)
    connection.cursor.close()

#Добавление "хорошего" изображения с несколькими клубнями на нём
def add_good_file_many():
    global connection
    with connection.cursor() as cursor:
            global id_good
            # Запрос на добавление "хорошего" файла в базу данных
            sql_add_good = "INSERT INTO `goods` (`good_file`, `dir_good_file`) VALUES (%s, %s)"
            cursor.execute(sql_add_good, (files[count_img], path))
            # Получение id добавленного элемента
            sql_good_id = "SELECT * FROM goods WHERE id_good_file=LAST_INSERT_ID()"
            cursor.execute(sql_good_id)
            id_good = cursor.fetchone()
            # Присвоение глобальной переменной id_good значения id добавленноо элемента 
            id_good = int(id_good[0])
    connection.cursor.close()

def add_good_file_many_cor():
    global connection
    global id_good
    with connection.cursor() as cursor:
            # Добавление записи в таблицу координат "хороших" файлов, где id файла — крайний добавленный элемент,
            # а координаты взяты из выделенного прямоугольника
            sql_add_good_cor = "INSERT INTO `goods_cor` (`id_good_file`, `x0`, `y0`, `x1`, `y1`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_add_good_cor, (id_good, topx, topy, botx, boty))
            connection.commit()
            #Подсчёт количества "хороших" файлов и вывод этой информации на экран
            sql_count_good = "SELECT COUNT(id_good_file) from goods"
            cursor.execute(sql_count_good)
            count_goods = cursor.fetchone()
            msg_add_goods = "Координаты добавлены. \n Общее количество 'хорошх' файлов: "+str(count_goods[0])+"."
            mb.showinfo("Информация", msg_add_goods)
    connection.cursor.close()

#Отрисовка кнопок для функций
btn_obj_good=Button(window,text='На этой картинке несколько клубней', command=add_good_file_many)
btn_obj_good.pack(pady=10)

btn_obj_cor=Button(window,text='Запомнить координаты объекта', command=add_good_file_many_cor)
btn_obj_cor.pack(pady=10)

btn_img_next=Button(window,text='След. картитнка', command=show_new_img)
btn_img_next.pack(pady=10)


btn_img_bad=Button(window,text='Это изображение "плохое"', command=add_bad_file)
btn_img_bad.pack(pady=10)

btn_img_bad=Button(window,text='Картинка содержит только один клубень', command=add_good_file)
btn_img_bad.pack(pady=10)

window.mainloop()