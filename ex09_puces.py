import tkinter
from tkinter import simpledialog

import psutil


def start():
    global n
    n = float(simpledialog.askstring(title="Fréquence de rafraîchissement", prompt="Durée en secondes ? :"))
    b.configure(text="Arrêter", command=stop)
    get_info()


def stop():
    l.after_cancel(repeat)
    b.configure(text="Démarrer", command=start)


def get_info():
    global repeat
    dico = psutil.virtual_memory()
    temp = str(dico.percent) + '°C'
    l.configure(text=temp)
    repeat = l.after(int(n * 1000), get_info)


root = tkinter.Tk()
root.resizable(width=tkinter.FALSE, height=tkinter.FALSE)
root.title("Moniteur")
l = tkinter.Label(text="", width=30)
l.pack()
b = tkinter.Button(text="Démarrer", command=start)
b.pack()
root.mainloop()
