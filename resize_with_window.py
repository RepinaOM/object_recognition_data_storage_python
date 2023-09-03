from tkinter import *
import os
from PIL import Image

def main():
    count = 0 
    folder_name = str(folder_tf.get())#Получение названия папки
    for address, dirs, files in os.walk(folder_name):
        for name in files:
            image_file = os.path.join(address, name)
            #Фиксированная ширина для изменения размера всех картинок под этот параметр
            fixed_width = 100 
            img = Image.open(image_file)
            # Получение процентного соотношения
            # старой и новой ширины
            if img.size[0]>100:
                width_percent = (fixed_width / float(img.size[0]))
                # на основе предыдущего значения
                # вычисляется новая высота
                height_size = int((float(img.size[1]) * float(width_percent)))
                # изменение размера на полученные значения
                new_image = img.resize((fixed_width, height_size))
                new_image.save(image_file)
            # Подсчёт изменённых изображений
            count += 1
            img_resize_lb = Label(
            frame,
            text=f"Изменён размер {count} картинок!"
            )
            img_resize_lb.grid(row=6, column=1)
#Интерфейс окна  
window = Tk()
window.title('Изменить размер картинок в папке')
window.geometry('500x300')
 
 
frame = Frame(
   window,
   padx=10,
   pady=10
)
frame.pack(expand=True)
 
 
folder_lb = Label(
   frame,
   text="Введите назание папки"
)
folder_lb.grid(row=3, column=1)
 
folder_tf = Entry(
   frame,
)
folder_tf.grid(row=3, column=2, pady=5)
 
cal_btn = Button(
   frame,
   text='Изменить размер изображений',
   command=main
)
cal_btn.grid(row=5, column=2)
 
window.mainloop()


