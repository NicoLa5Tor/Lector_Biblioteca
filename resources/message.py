import tkinter as tk
from tkinter import messagebox
class Message:
    def __init__(self) -> None:
        pass
    def show_message_info(self,message):
        messagebox.showinfo('Informacion',message)
    def show_message_error(self,message):
        messagebox.showerror('Error',message)