import tkinter as tk
from tkinter import ttk,scrolledtext, messagebox
from tkcalendar import DateEntry
from toolTipGui import CreateToolTip
import sys,os
import botExceptions as be
from SqirtleMusicBot import Run_Bot
from threading import Thread
from Alerts import Alerts
from pathlib import Path
import platform

base_path = getattr(sys, '_MEIPASS', Path.cwd())
base_path = Path(base_path)

class StdoutRedirector():
    def __init__(self, entry_widget):
        self.entry_widget = entry_widget
    
    def write(self, message):
        if(Alerts.WARNING in message):
            self.entry_widget.insert(tk.END, message,'warning')
        elif(Alerts.DOWNLOADED in message):
            self.entry_widget.insert(tk.END, message,'download')
        elif(Alerts.COMPRESSED in message):
            self.entry_widget.insert(tk.END, message,'compressed')
        elif(Alerts.ERROR in message):
            self.entry_widget.insert(tk.END, message,'error')
        elif(Alerts.DONE in message):
            self.entry_widget.insert(tk.END, message,'done')
        else:
            self.entry_widget.insert(tk.END, message)
        self.entry_widget.see(tk.END)  
   
    def flush(self):
        pass
class BotStateHolder():
    def __init__(self):
        self.e = None
        self.doneState = False
    def set(self,e):
        self.e = e
    def done(self):
        self.doneState = True

class App(ttk.Frame):
    help_text = {
        'token': 'The token that is used to control the bot. \nIf you have not created a Discord bot before, \ncheck the Discord Developer Portal',
        'channel': 'Right click a channel in a server and paste \nthe channel id from "Copy Channel ID". \nIf the option does not appear, make sure to \nturn on developer mode in the Discord Settings',
        'server': 'Right click top left of a server and paste \nthe server id from "Copy Server ID". \nIf the option does not appear, make sure to \nturn on developer mode in the Discord Settings',
        'date': 'The date to search for songs from in mm-dd-yyyy format',
        'output': 'Console Log Output',
        'download':'Using a Discord Bot in a server, \ndownloads youtube links to smash audio files',
        'view': 'Open folder where smash audio files are downloaded',
        'renamed': 'Files that got renamed during conversion process'
    }
    invalid_text = {
        'token':'*Invalid Token. Check that the token is copied correctly',
        'token_empty': '*Token field is empty',
        'channel':'*Invalid Channel ID. Check that the ID is copied correctly',
        'channel_empty': '*Channel ID field is empty',
        'server':'*Invalid Server ID. Check that the ID is copied correctly',
        'server_empty': '*Server ID field is empty'
    }

    tagged_console_font = ('sans-serif', '9', 'bold')
    def __init__(self, parent):
        ttk.Frame.__init__(self)
    
        #GUI variables
        self.bot_token = tk.StringVar()
        self.bot_token.set('')

        self.channel_id = tk.StringVar()
        self.channel_id.set('')

        self.server_id = tk.StringVar()
        self.server_id.set('')

        self.valid_token_msg = tk.StringVar()
        self.valid_token_msg.set('')

        self.valid_channel_msg = tk.StringVar()
        self.valid_channel_msg.set('')

        self.valid_server_msg = tk.StringVar()
        self.valid_server_msg.set('')

        self.parent = parent
        self.parent.resizable(False,False)
        self.parent.columnconfigure((1,2,3),weight=1)
        self.parent.columnconfigure((0),weight=0)

        self.row_count = -1

        self.botExcept = BotStateHolder()
        self.has_old_files = False
        self.has_renamed_files = False

        self.setup_widgets()

    def setup_widgets(self):

        #Bot Token Input
        self.inc_row_count()
        self.token_label = ttk.Label(text="Discord Bot Token:")
        self.token_label.grid(row=self.row_count, column=0, sticky='nesw', pady=(10,5), padx=10)
        self.bot_token_entry = ttk.Entry(textvariable=self.bot_token)
        self.bot_token_entry.grid(row=self.row_count, column=1, columnspan=3,sticky="ew", pady=(20,5), padx=10)
        self.token_helpText = CreateToolTip(widget=self.token_label, text=App.help_text['token'])
        #Token Invalid
        self.inc_row_count()
        self.token_invalid = ttk.Label(text=self.valid_token_msg.get(), foreground="red")
        self.token_invalid.grid(row=self.row_count, column = 1, sticky="w", pady=5, padx=10)
        self.valid_token_msg.trace_add('write', self.update_invalid)

        #Server ID Input
        self.inc_row_count()
        self.server_label = ttk.Label(text="Server ID:")
        self.server_label.grid(row=self.row_count, column=0, sticky="nesw", pady=(10,5), padx=10)
        self.server_id_entry = ttk.Entry(width=75, textvariable=self.server_id)
        self.server_id_entry.grid(row=self.row_count, column=1,columnspan=3, sticky="ew", pady=(20,5), padx=10)
        self.server_helpText = CreateToolTip(widget=self.server_label, text=App.help_text['server'])
        #Server ID Invalid
        self.inc_row_count()
        self.server_invalid = ttk.Label(text=self.valid_channel_msg.get(), foreground="red")
        self.server_invalid.grid(row=self.row_count, column = 1, sticky="w", pady=5, padx=10)
        self.valid_server_msg.trace_add('write', self.update_invalid)
        

        #Channel ID Input
        self.inc_row_count()
        self.channel_label = ttk.Label(text="Channel ID:")
        self.channel_label.grid(row=self.row_count, column=0, sticky="nesw", pady=(10,5), padx=10)
        self.channel_id_entry = ttk.Entry(width=75, textvariable=self.channel_id)
        self.channel_id_entry.grid(row=self.row_count, column=1,columnspan=3, sticky="ew", pady=(20,5), padx=10)
        self.channel_helpText = CreateToolTip(widget=self.channel_label, text=App.help_text['channel'])
        #Channel ID Invalid
        self.inc_row_count()
        self.channel_invalid = ttk.Label(text=self.valid_channel_msg.get(), foreground="red")
        self.channel_invalid.grid(row=self.row_count, column = 1, sticky="w", pady=5, padx=10)
        self.valid_channel_msg.trace_add('write', self.update_invalid)


        #Date Picker
        self.inc_row_count()
        self.date_label = ttk.Label(text="Date:")
        self.date_label.grid(row=self.row_count, column=0, sticky="nesw", pady=10, padx=10)
        self.date_entry = DateEntry(date_pattern="mm-dd-yyyy")
        self.date_entry.grid(row=self.row_count, column=1,sticky="w", pady=10, padx=10 )
        self.date_helpText = CreateToolTip(widget=self.date_label, text=App.help_text['date'])

        #Buttons to Interact
        self.inc_row_count()
        self.download = ttk.Button(text="Start Download", command=self.start_download)
        self.download.grid(row=self.row_count,column=0, sticky="w", padx=10)
        self.download_helpText = CreateToolTip(widget=self.download, text=App.help_text['download'])

        #View Smash Files
        self.view_smash = ttk.Button(text="View Smash Audio Files", command=self.open_folder)
        self.view_smash.grid(row=self.row_count,column=3, sticky="e", padx=10)
        self.view_smash_helptext = CreateToolTip(widget=self.view_smash, text=App.help_text['view'])
        self.check_smash_folder()

        self.view_renamed = ttk.Button(text="View Renamed Files", command=self.open_renamed)
        self.view_renamed.grid(row=self.row_count,column=2, sticky="e", padx=10)
        self.view_renamed_helptext = CreateToolTip(widget=self.view_renamed, text=App.help_text['renamed'])
        self.check_renamed_folder()

        #Output Label
        self.inc_row_count()
        self.output_label = ttk.Label(text="Output", justify="left", font=("", 10, "bold underline"))
        self.output_label.grid(row=self.row_count, column=0, sticky="w", pady=5, padx=10)
        self.output_helpText = CreateToolTip(widget=self.output_label, text=App.help_text['output'])

        #Console Log Output
        self.inc_row_count()
        self.output_text = scrolledtext.ScrolledText(wrap=tk.WORD, bg='black', fg='white')
        self.output_text.grid(row=self.row_count, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.output_text.tag_config('warning', foreground="yellow", font=App.tagged_console_font)
        self.output_text.tag_config('download', foreground="green", font=App.tagged_console_font)
        self.output_text.tag_config('compressed', foreground="green", font=App.tagged_console_font)
        self.output_text.tag_config('done', foreground="green", font=App.tagged_console_font)
        self.output_text.tag_config('error', foreground="red", font=App.tagged_console_font)

        output_redirect = StdoutRedirector(self.output_text)
        sys.stdout = output_redirect
        # redirect_stdout(sys.stdout)
        # redirect_stderr
       

        # #TempButton
        # self.inc_row_count()
        # self.print_button = ttk.Button(text="Print to GUI", command=self.print_to_gui)
        # self.print_button.grid(row=self.row_count, column=0, columnspan=2, pady=10)
        # return
    
    def check_smash_folder(self):
        output_dir = Path(os.getcwd()) / "bot_files" / "smash_audio"
        if(not os.path.exists(str(output_dir.resolve()))):
            self.view_smash.config(state='disabled')
            self.has_old_files = False
            return
        if(len(os.listdir(output_dir)) == 0):
            self.view_smash.config(state='disabled')
            self.has_old_files = False
            return
        self.has_old_files = True
    def check_renamed_folder(self):
        need_rename = Path(os.getcwd()) / "bot_files"/ "need_rename"
        rename_file = need_rename / "rename_file.txt"

        if(not os.path.exists(str(rename_file.resolve()))):
            self.view_renamed.config(state='disabled')
            self.has_renamed_files = False
            return
    
        self.has_renamed_files = True
        
    def start_download(self):
        def warn_user():
            if(self.has_old_files):
                res = messagebox.askquestion("Detected Old Files", "Files from a previous download session has been detected!\nContinuing will DELETE all previous files\n Proceed?")
                if(res == 'yes'):
                    return True
                return False
            return True
        def clear_old_files():
            raw_dir = Path(os.getcwd()) / "bot_files"/ "raw_audio"
            smash_dir = Path(os.getcwd()) / "bot_files" / "smash_audio"
            comp_dir = Path(os.getcwd())/ "bot_files" /"compressed_audio"
            rename_dir = Path(os.getcwd()) / "bot_files"/ "need_rename"
            rename_file = rename_dir/ 'rename_file.txt'

            error_dir = Path(os.getcwd()) / "bot_files"/ "error_links"
            error_file = error_dir / 'error.txt'
             
            if(os.path.exists(str(smash_dir.resolve()))):
                for file in os.listdir(smash_dir):
                    if file.endswith(".nus3audio"):
                        os.remove(os.path.join(smash_dir, file))

            if(os.path.exists(str(comp_dir.resolve()))):
                for file in os.listdir(comp_dir):
                    if file.endswith(".mp3"):
                        os.remove(os.path.join(comp_dir, file))

            if(os.path.exists(str(raw_dir.resolve()))):
                for file in os.listdir(raw_dir):
                    if file.endswith(".mp3"):
                        os.remove(os.path.join(raw_dir, file))

            if(os.path.exists(str(rename_file.resolve()))):
                os.remove(rename_file)

            if(os.path.exists(str(error_file.resolve()))):
                os.remove(error_file)

        def start_bot():
            try:
                token = self.bot_token.get().strip()
                channel_id = self.channel_id.get().strip()
                server = self.server_id.get().strip()
                date = self.date_entry.get_date()
                try:
                    channel_id = int(channel_id)
                except Exception:
                    raise be.TypeChannel
                try:
                    server = int(server)
                except Exception:
                    raise be.TypeServer
                self.botExcept.doneState = False
                Run_Bot(token= token,channel_id=channel_id,date=date,server=server, botExcept=self.botExcept)
                self.after_id = self.after(500, self.check_except)
                self.after_done = self.after(500, self.check_done)
            except be.InvalidToken:
                self.valid_token_msg.set(App.invalid_text['token'])
                self.download.config(state="enabled")
                print("Failed to Start Bot")
            except be.InvalidServer:
                self.valid_server_msg.set(App.invalid_text['server'])
                self.download.config(state="enabled")
                print(Alerts.ERROR, "Could not find Server ID associated with Bot")
            except be.InvalidChannel:
                self.valid_channel_msg.set(App.invalid_text['channel'])
                self.download.config(state="enabled")
                print(Alerts.ERROR, "Could not find Channel ID associated with Server ID")
            except be.TypeChannel:
                self.valid_channel_msg.set(App.invalid_text['channel'])
                self.download.config(state="enabled")
                print("Channel ID should be numbers")
            except be.TypeServer:
                self.valid_server_msg.set(App.invalid_text['server'])
                self.download.config(state="enabled")
                print("Server ID should be numbers")

                    
        self.valid_token_msg.set('')
        self.valid_channel_msg.set('')
        self.valid_server_msg.set('')
        valid = True
        if(self.bot_token.get() == ''):
            valid = False
            self.valid_token_msg.set(App.invalid_text['token_empty'])
        if(self.channel_id.get() == ''):
            valid = False
            self.valid_channel_msg.set(App.invalid_text['channel_empty'])
        if(self.server_id.get() == ''):
            valid = False
            self.valid_server_msg.set(App.invalid_text['server_empty'])
        if(not valid):
           return
        user_cont = warn_user()
        if(not user_cont):
            return
        clear_old_files()
        print('Turning on Bot...')
        self.download.config(state='disabled')
        bot_thread = Thread(target=start_bot)
        bot_thread.daemon= True
        bot_thread.start()
        
    def print_to_gui(self):
        print(Alerts.WARNING+ " Hello World")
        print("Bot token", self.bot_token.get())
        print("Channel token", self.channel_id.get())
        print("Date: ", self.date_entry.get())
        # self.valid_channel_msg.set(App.invalid_text['channel'])
        # self.valid_token_msg.set(App.invalid_text['token'])
        # self.valid_server_msg.set(App.invalid_text['server'])


    def update_invalid(self,*args):
        self.channel_invalid.config(text=self.valid_channel_msg.get())
        self.token_invalid.config(text=self.valid_token_msg.get())
        self.server_invalid.config(text=self.valid_server_msg.get())
        return

    def check_except(self):
        if(isinstance(self.botExcept.e, be.InvalidChannel)):
            self.valid_channel_msg.set(App.invalid_text['channel'])
            self.download.config(state="enabled")
            print(Alerts.ERROR, "Could not find Channel ID associated with Server ID")
            self.after_cancel(self.after_id)
            self.botExcept.e = None
            return
        if(isinstance(self.botExcept.e, be.InvalidServer)):
            self.valid_server_msg.set(App.invalid_text['server'])
            self.download.config(state="enabled")
            print(Alerts.ERROR, "Could not find Server ID associated with Bot")
            self.after_cancel(self.after_id)
            self.botExcept.e = None 
            return
    def check_done(self):
        if(self.botExcept.doneState): #bot done
            self.download.config(state="enabled")
            self.after_cancel(self.after_done)
            self.view_smash.config(state="enabled")
            self.view_renamed.config(state="enabled")
            return

    #Open smash audio folder
    def open_folder(self):
        curr_dir = Path(os.getcwd())
        expected_dir = curr_dir / "bot_files" / "smash_audio"
        path_str = str(expected_dir.resolve())
        if(os.path.exists(path_str)):
            if(platform.system() == 'Windows'):
                os.system("explorer " + path_str)
            elif(platform.system() == 'Darwin'):
                os.system("open " + path_str)
            else:
                print("Can not open folder automaitically, check the following path\n" + path_str)
        return

    #open renamed folder
    def open_renamed(self):
        need_rename = Path(os.getcwd()) / "bot_files"/ "need_rename"
        path_str = str(need_rename.resolve())
        if(os.path.exists(path_str)):
            if(platform.system() == 'Windows'):
                os.system("explorer " + path_str)
            elif(platform.system() == 'Darwin'):
                os.system("open " + path_str)
            else:
                print("Can not open folder automaitically, check the following path\n" + path_str)
        return
    #Call before using a row number
    def inc_row_count(self):
        self.row_count = self.row_count + 1

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sqirtle Music Bot")

    theme_dir = base_path / 'Azure-ttk-theme-main' /'azure.tcl'
    root.tk.call("source", str(theme_dir.resolve()))
    root.tk.call("set_theme", "light")

    app = App(root)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-50))
    root.mainloop()
