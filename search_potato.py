import cv2 
from matplotlib import pyplot as pltd 
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb

#Создание окна
WIDTH, HEIGHT = 600, 200

window = tk.Tk()
window.title("Поиск клубня")
window.geometry('%sx%s' % (WIDTH, HEIGHT))

#Функция для поиска клубня на изображении
def search():
    path = str(image_file.get())#Получения названия файла изображения
    # Открытие изображения из файла 
    imaging = cv2.imread(path) 
    # Изменение свойств изображения с помощью cv2
    imaging_gray = cv2.cvtColor(imaging, cv2.COLOR_BGR2GRAY) 
    imaging_rgb = cv2.cvtColor(imaging, cv2.COLOR_BGR2RGB) 
    # Импорт xml-данных каскадного классификатора Хаара, созданного ранее
    xml_data = cv2.CascadeClassifier('haarcascade/cascade.xml') 
    # Обнаружение объекта на изображении с помощью каскадного классификатора Хаара  
    detecting = xml_data.detectMultiScale(imaging_gray,  
                                    minSize =(50, 50)) 
    # Количество обнаруженных объектов
    amountDetecting = len(detecting) 
    # Использование условия if для выделения обнаруженного объекта 
    if amountDetecting != 0: 
        for(a, b, width, height) in detecting: 
            cv2.rectangle(imaging_rgb,(a, b), # Выделение обнаруженного объекта прямоугольником
                        (a + height, b + width),  
                        (42, 250, 0), 5) 
    else:
        msg_no_find = "Клубни не найдены."
        mb.showinfo("Информация", msg_no_find)
    # Построение изображения
    pltd.subplot(1, 1, 1) 
    # Отображение изображения
    pltd.imshow(imaging_rgb) 
    pltd.show() 

#Отрисовка элементов окна
img_lb = Label(
   text="Введите название файла с картинкой"
)
img_lb.grid(row=1, column=4, padx=200, pady=10)
image_file = tk.Entry()
image_file.grid(row=2, column=4, pady=5)

btn_form=Button(window,text='Найти клубень/клубни', command=search)
btn_form.grid(row=3, column=4,pady=15)

window.mainloop()