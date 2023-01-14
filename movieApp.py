import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet

#renkleri ayarı
bg_color = "#02B2BF"

#özel yazı tiplerini ekle
pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")
pyglet.font.add_file("fonts/Shanti-Regular.ttf")

#tüm çerçeve widget'larını seçin ve silin
def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetchDb():
    # sqlite veritabanını bağlama
    connection = sqlite3.connect("data/movies.db")
    cursor = connection.cursor()

    # tüm tablo adlarını getir
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()

    #rasgele seçme
    idx = random.randint(0, len(all_tables) - 1)

    # tablodan kayıtları getir
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()
    connection.close()
    return table_name, table_records

def pre_process(table_name, table_records):
    # ön işleme tablosu adı
    title = table_name[:-3]
    title = "".join([char if char.islower() else " " + char for char in title])

    # tablo kayıtlarını ön işleme
    ingredients = []

    for i in table_records:
        movie_name = i[1]
        year = i[2]
        imdb = i[3]
        ingredients.append(str(year) + ".  " + movie_name + "  / " + str(imdb))
    return title, ingredients

def loadFrame1():
    clear_widgets(frame2)
    # çerçeve 1'i çerçeve 2'nin üzerine yık
    frame1.tkraise()
    # pencere öğelerinin çerçeveyi değiştirmesini önleme
    frame1.pack_propagate(False)

    # logo için
    logoImg = ImageTk.PhotoImage(file="assets/logo_olacak.png")
    logoWidget = tk.Label(frame1, image=logoImg, bg=bg_color)
    logoWidget.image = logoImg
    logoWidget.pack()

    # talimatlar için etiket widget'ı oluştur
    tk.Label(
        frame1,
        text="What Should I Watch Today?",
        bg=bg_color,
        fg="white",
        font=("Shanti", 14)
        ).pack()

    # buton için
    tk.Button(
        frame1,
        text="SHUFFLE",
        font=("Ubuntu", 20),
        bg="#28393a",
        fg="#02B2BF",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda:loadFrame2()
        ).pack(pady=20)

def loadFrame2():
    clear_widgets(frame1)
    # çerçeve 2'yi çerçeve 1'in üzerine yık
    frame2.tkraise()

    # veritabanından getir
    table_name, table_records = fetchDb()
    title, ingredients = pre_process(table_name, table_records)

    #  button için resim
    logoImg = ImageTk.PhotoImage(file="assets/logo_button.png")
    logoWidget = tk.Label(frame2, image=logoImg, bg=bg_color)
    logoWidget.image = logoImg
    logoWidget.pack(pady=20)

    # tarif başlığı widget
    tk.Label(
        frame2,
        text=title,
        bg=bg_color,
        fg="white",
        font=("Ubuntu", 20)
        ).pack(pady=25,padx=25)

    # tarif malzemeleri widget'ları
    for i in ingredients:
        tk.Label(
            frame2,
            text=i,
            bg="#28393a",
            fg="#02B2BF",
            font=("Shanti", 12)
            ).pack(fill="both",padx=25)

        # geri buton için
    tk.Button(
        frame2,
        text="BACK",
        font=("Ubuntu", 18),
        bg="#28393a",
        fg="#02B2BF",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda: loadFrame1()
        ).pack(pady=20)

# uygulamayı temel ayarlarla başlat
root = tk.Tk()
root.title("MOVIE BOOKLET")
root.eval("tk::PlaceWindow . center")

#uygulamayı ekranın ortasına yerleştirmek
#x = root.winfo_screenwidth() // 2
#y = int(root.winfo_screenheight() * 0.1)
#root.geometry('500x600+' + str(x) + '+' + str(y))

#widget için çerçeve
frame1 = tk.Frame(root, width=500, height=600, bg=bg_color)
frame2 = tk.Frame(root, bg=bg_color)

# çerçeve widget'larını pencereye yerleştir
for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")

# ilk kareyi yükle
loadFrame1()

#uygulamayı çalıştır
root.mainloop()