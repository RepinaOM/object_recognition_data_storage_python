from tkinter import *
from bs4 import *
import requests
import os
from PIL import Image

# Создание папки с изображениями
def folder_create(images):
    try:
        folder_name = str(folder_tf.get())
        # создание пустой папки
        os.mkdir(folder_name)
 
    # вывести сообщение, если папка с таким именем уже существует
    except:
        exist_lb = Label(
        frame,
        text="Папка с таким именем уже существует!"
        )
        exist_lb.grid(row=6, column=1)
        folder_create()
 
    # скачииваем иизображения в папку
    download_images(images, folder_name)
 
 
# Скачивание всех изображений с веб-страницы
def download_images(images, folder_name):
   
    # задаём начальное значение кол-ва картинок
    count = 0
 
    # вывод кол-ва найденных на веб-странице картинок
    img_found_lb = Label(
        frame,
        text=f"     Найдено {len(images)} картинок!     "
        )
    img_found_lb.grid(row=6, column=1)
 
    # проверяем, что кол-во найденных изображений НЕ равно 0
    if len(images) != 0:
        for i, image in enumerate(images):
            # Извлечём URL-адрес источника изображения из тега изображения
            # будем искать "data-srcset" в теге img
            try:
                # В теге изображения выполним поиск "data-srcset"
                image_link = image["data-srcset"]
                 
            # затем мы будем искать "data-src" в img
            except:
                try:
                    # В теге изображения выполним поиск "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # В теге изображения выполним поиск "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # В теге изображения выполним поиск "src"
                            image_link = image["src"]
 
                        # если исходный URL не найден
                        except:
                            pass
 
            # После получения URL-адреса источника изображения
            # Попытаемся получить содержимое изображения
            try:
                r = requests.get(image_link).content
                try:
 
                    # возможность декодирования
                    r = str(r, 'utf-8')
 
                except UnicodeDecodeError:
 
                    # Начинаем скачивание изображений
                    with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                        f.write(r)
                    # Уменьшим изображение до 100px в ширину с сохранением пропорций
                    fixed_width = 100
                    img = Image.open(f"{folder_name}/images{i+1}.jpg")
                    # получаем процентное соотношение
                    # старой и новой ширины
                    if img.size[0]>100:
                        width_percent = (fixed_width / float(img.size[0]))
                        # на основе предыдущего значения
                        # вычисляем новую высоту
                        height_size = int((float(img.size[1]) * float(width_percent)))
                        # меняем размер на полученные значения
                        new_image = img.resize((fixed_width, height_size))
                        new_image.save(f"{folder_name}/images{i+1}.jpg")
                        
                        
                    # засчитываем загруженное изображение
                    count += 1
            except:
                pass
 
        # если все изображения скачаны
        if count == len(images):
            img_down_lb = Label(
            frame,
            text="Все картинки скачаны!"
            )
            img_down_lb.grid(row=7, column=1)
             
        # если не все изображения скачаны
        else:
            img_down_lb = Label(
            frame,
            text=f"Скачано {count} картинок {len(images)}"
            )
            img_down_lb.grid(row=7, column=1)
 
# Главная функция
def main():

    # получаем URL страницы
    url = str(url_tf.get())
    # запрос страницы
    r = requests.get(url)
 
    # Анализ HTML кода
    soup = BeautifulSoup(r.text, 'html.parser')
 
    # находим все изображения по данному URL
    images = soup.findAll('img')
 
    # Вызываем ункцию созданя папки и скачивания в неё картинок
    folder_create(images)
 
#Код интерфейса
window = Tk()
window.title('Скачать картинки со страницы')
window.geometry('400x300')
 
frame = Frame(
   window,
   padx=10,
   pady=10
)
frame.pack(expand=True)
 
url_lb = Label(
   frame,
   text="Введите url"
)
url_lb.grid(row=3, column=1)
 
folder_lb = Label(
   frame,
   text="Введите назввание папки для сохранения  ",
)
folder_lb.grid(row=4, column=1)
 
url_tf = Entry(
   frame,
)
url_tf.grid(row=3, column=2, pady=5)
 
folder_tf = Entry(
   frame,
)
folder_tf.grid(row=4, column=2, pady=5)
 
cal_btn = Button(
   frame,
   text='Скачать изображения',
   command=main
)
cal_btn.grid(row=5, column=2)
 
window.mainloop()