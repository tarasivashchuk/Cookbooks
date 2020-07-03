import tkinter as tk


class Application(tk.Frame):

    def __init__(self, master: tk.Tk = None, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.button = tk.Button(self)
        self.button["text"] = "Well hello there, ya sexy sexy human ;) (click me)"
        self.button["command"] = self.respond
        self.button.pack(side="top")

        self.quit = tk.Button(self, text="Bye!", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def respond(self):
        print("Well, well.. aren't you naughty?")


window = tk.Tk(screenName="TKinter Hello World", baseName="GUI Cookbook")
app = Application(master=window)
app.mainloop()
