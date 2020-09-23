from tkinter import *
from PIL import ImageTk, Image

bg = "LightCyan3"
guia = "LightCyan2"
act = "black"


def attack():
    return 0


def defence():
    rootdefence = Toplevel(root)
    rootdefence.geometry("500x700")
    img = ImageTk.PhotoImage(Image.open('map.jpg'))
    view = Label(rootdefence, image=img)
    Button(rootdefence, text="Выйти", font="TimesNewRoman 15",
           command=exit, background=guia, fg=act,
           relief="raised", activebackground=guia,
           activeforeground=act, bd=7, width=10, ).pack(side=BOTTOM)
    view.pack(side="bottom", fill="both", expand="yes")
    rootdefence.mainloop()


def adm():
    rootadm = Toplevel(root)
    rootadm.geometry("500x700")
    img = ImageTk.PhotoImage(Image.open('map.jpg'))
    view = Label(rootadm, image=img)
    view.pack(side="bottom", fill="both", expand="yes")
    Button(rootadm, text="Выйти", font="TimesNewRoman 15",
           command=exit, background=guia, fg=act,
           relief="raised", activebackground=guia,
           activeforeground=act, bd=7, width=10, ).pack(side=BOTTOM)
    rootadm.mainloop()


def menu():
    global root, rootattack, rootdefence, rootadm
    root = Tk()
    root.focus_set()
    root.title("Project")
    root.geometry("500x500")
    root.configure(background='cornsilk3')
    Label(bg='cornsilk3', fg=act, font="Times 22",
          text="Выберите роль:").place(x=150, y=20)
    Button(root, text="Выйти", font="TimesNewRoman 15",
           command=exit, background=guia, fg=act,
           relief="raised", activebackground=guia,
           activeforeground=act, bd=7, width=10,).pack(side=BOTTOM)
    Button(root, text="Защита", font="TimesNewRoman 15",
           command=defence,
           background=guia, fg=act, relief="raised",
           activebackground=guia, bd=7,
           activeforeground=act).place(x=205, y=200)
    Button(root, text="Нападение", font="TimesNewRoman 15",
           command=attack,
           background=guia, activebackground=guia, fg=act,
           relief="raised", bd=7, activeforeground=act, ).place(x=190, y=130)

    Button(root, text="Администратор", font="TimesNewRoman 15",
           command=adm, bd=7,
           background=guia, fg=act,
           relief="raised", activebackground=guia,
           activeforeground=act).place(x=170, y=275)
    root.mainloop()


menu()
