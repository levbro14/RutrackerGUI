import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from py_rutracker import RuTrackerClient
from threading import Thread
import os
import sys

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу для работы как в EXE, так и в исходном коде """
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

proxies = {
    'http': 'http://modeler_Dw1W7l:4Cl2yaPqRGDS@45.86.163.132:14798',
    'https': 'http://modeler_Dw1W7l:4Cl2yaPqRGDS@45.86.163.132:14798'
}
try:
    client = RuTrackerClient("levletsplay", "plokmijnuhb12", proxies)
except Exception as ex:
    messagebox.showerror("Ошибка", ex)
def get_info():
    btn.configure(state="disabled")
    try:
        for item in tree.get_children():
            tree.delete(item)
        search = entry.get()
        if search == "":
            messagebox.showerror("Ошибка", "Запрос не должен быть пустым!")
            return
        
        
        results = client.search_all_pages(search)

        for torrent in results:
            if torrent.approved == "проверено":
                tree.insert("", END, values=(torrent.title, torrent.author, torrent.added, f"{torrent.approved}✅", torrent.category, torrent.download_counter, torrent.download_url, torrent.topic_id))
            else:
                tree.insert("", END, values=(torrent.title, torrent.author, torrent.added, f"{torrent.approved}❌", torrent.category, torrent.download_counter, torrent.download_url, torrent.topic_id))
    except Exception as ex:
        messagebox.showerror("Ошибка", ex)

    btn.configure(state="normal")

def on_double_click(event):
    selected_item = tree.focus()
    if not selected_item:
        return
    
    item_data = tree.item(selected_item)["values"]
    if item_data and len(item_data) >= 8:
        topic_id = item_data[7]
        name = item_data[0]
        
        bytes_data = client.download(topic_id)
        with open(f"{name}.torrent", "wb") as file:
            file.write(bytes_data)
        messagebox.showinfo("Инфо", f"Торрент скачан!\nНазвание: {name}.torrent")




root = tkinter.Tk()
root.title("RuTracker")
root.geometry("1000x500")
root.resizable(width=False, height=False)
root.iconbitmap(resource_path("icon.ico"))

entry = ttk.Entry(font=("Arial", 25))
entry.place(x=10, y=10, width=850, height=50)

btn = ttk.Button(text="Найти", command=lambda: Thread(target=get_info).start())
btn.place(x=870, y=10, height=50, width=120)

lbl = ttk.Label(text="Внимание, чтобы скачать торрент нужно нажать на него 2 раза!")
lbl.place(x=10, y=80)

columns = ("name", "author", "added", "approved", "category", "download_counter", "URL", "topic_id")
tree = ttk.Treeview(root, columns=columns, show="headings")

tree.heading("name", text="Название")
tree.heading("author", text="Автор")
tree.heading("added", text="Добавлено")
tree.heading("approved", text="Проверка")
tree.heading("category", text="Категория")
tree.heading("download_counter", text="Кол-во скачиваний")
tree.heading("URL", text="URL")
tree.heading("topic_id", text="id темы")

tree.place(x=10, y=100, width=970, height=350)

# Вертикальный Scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.place(x=980, y=100, height=350)



# Привязываем двойной клик
tree.bind("<Double-1>", on_double_click)

root.mainloop()