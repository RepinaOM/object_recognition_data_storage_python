from tkinter import *
from subprocess import call

#Создание окна приложения
root=Tk()
root.geometry('500x500')
root.title('Главное меню')
frame = Frame(root)
frame.pack(pady=20,padx=20)

#Функция открытия окна для скачивания картинок
def Open_parse_img():
    call(["python", "parse_with_window.py"])

#Функция открытия окна для изменения размера картинок
def Open_resize_img():
    call(["python", "resize_with_window.py"])

#Функция открытия окна для добавления картинок в базу данных
def Open_db_img():
    call(["python", "add_into_db_with_window.py"])

#Функция открытия окна для формирования необходимых для обучения данных
def Open_form_data():
    call(["python", "form_data.py"])

#Функция открытия окна для запуска обучения
def Open_create_cascade():
    call(["python", "create_cascade.py"])

#Функция открытия окна для поиска клубня на картинке
def Open_search():
    call(["python", "search_potato.py"])

#Отрисовка кнопок
btn_img_parse=Button(frame,text='Открыть окно для скачивания картинок',command=Open_parse_img)
btn_img_parse.grid(row=2, column=1)

btn_img_resize=Button(frame,text='Изменить размер картинок в папке',command=Open_resize_img)
btn_img_resize.grid(row=5, column=1, pady=15)

btn_img_db=Button(frame,text='Отфильтровать картинки',command=Open_db_img)
btn_img_db.grid(row=6, column=1)

btn_img_form=Button(frame,text='Сформировать данные',command=Open_form_data)
btn_img_form.grid(row=7, column=1, pady=15)

btn_img_cascade=Button(frame,text='Обучение',command=Open_create_cascade)
btn_img_cascade.grid(row=8, column=1)

btn_img_search=Button(frame,text='Найти клубень на картинке',command=Open_search)
btn_img_search.grid(row=9, column=1, pady=15)

#Запуск окна
root.mainloop()