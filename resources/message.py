import tkinter as tk
from tkinter import messagebox
from .os.op import Operations_Os
import subprocess


class Message:
    def __init__(self) -> None:
        self.op = Operations_Os()
        pass
    def show_message_info(self,message):
        messagebox.showinfo('Informacion',message)
    def show_message_error(self,message):
        messagebox.showerror('Error',message)
    def show_asokandnot(self,message,header):
        mesg = "Si tiene dudas consulte a Nicolás: 3103391854 \n{}".format(message)
        respuesta = messagebox.askokcancel(title=header, message=mesg)
        return respuesta
    def show_message_op(self,title,message,time=4):
            
            image_url = self.op.get_resource_path(relative_path="assets/back_message.png")
            #descomentarear cuando se use en entorno de desarrollo
            
            #image_url = "C:\\Users\\Nicolas Torres\\OneDrive\\Escritorio\\Nueva carpeta\\Lector_Biblioteca\\assets\\back_message.png"
              
            app_id = "Concurrent Udec"
            powershell_command = f"""
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;
            $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastImageAndText02);
            $textNodes = $template.GetElementsByTagName("text");
            $textNodes.Item(0).AppendChild($template.CreateTextNode("{title}")) > $null;
            $textNodes.Item(1).AppendChild($template.CreateTextNode("{message}")) > $null;
            """

            powershell_command += f"""
            $imagePath = "{image_url}"
            $imageNodes = $template.GetElementsByTagName("image");
            $imageNodes.Item(0).Attributes.GetNamedItem("src").NodeValue = $imagePath;
            """
            
            powershell_command += f"""
            $toast = [Windows.UI.Notifications.ToastNotification]::new($template);
            $toast.ExpirationTime = [System.DateTimeOffset]::Now.AddSeconds({time});
            $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("{app_id}");
            $notifier.Show($toast);
            """
            #print(powershell_command)
            subprocess.run(["powershell", "-Command", powershell_command])

       
        
        
        
        