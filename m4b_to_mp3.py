import os
import json
import platform
import tkinter as tk
from tkinter.filedialog import askopenfilename

class GuiWindow(object):
    def __init__(self, master):
        self.master = master
        self.ffmpeg = "ffmpeg.exe"
        if platform.system() == 'Linux':
            self.ffmpeg = "ffmpeg"
        self.ext = ".m4b"
        with open('lang/hr_lang.json') as json_file:
            self.lang = json.load(json_file)
        self.filenames = ()
        self.for_conversion = []

        self.file_label = tk.LabelFrame(self.master, text=self.lang[0])
        self.file_name = tk.Button(self.file_label, font='Helvetica 12', text=self.lang[1],command=self.start)
        self.file_name.pack(fill=tk.X)
        self.file_label.pack(fill=tk.X, padx = 10)
        self.orig_button_color = self.file_name.cget("background")
        print(self.orig_button_color)

        self.file_list = tk.LabelFrame(self.master, text=self.lang[2])
        self.canvas = tk.Canvas(self.file_list, bg="white", height=200, width=200)
        self.scrollbar = tk.Scrollbar(self.file_list, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.file_list.pack(fill=tk.X, padx = 10)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.options_label = tk.LabelFrame(self.master, text=self.lang[3])
        self.CheckVar1 = tk.IntVar()
        self.option_1 = tk.Checkbutton(self.options_label, variable=self.CheckVar1, text=self.lang[4]).pack(anchor=tk.W)
        self.options_label.pack(fill=tk.X, padx = 10)

        self.start_button = tk.Button(self.master, text=self.lang[5], width=15,command=self.convert_file)
        self.start_button.pack(fill=tk.X, padx = 20, pady=10)

    def start(self):
        self.filenames = askopenfilename(title = self.lang[5], multiple=True)
        self.file_name.config(bg="#d9d9d9")
        print(self.filenames)
        for self.widget in self.scrollable_frame.winfo_children():
            self.widget.destroy()
        for self.name in self.filenames:
            if self.name.endswith(self.ext):
                self.for_conversion.append(self.name)
                tk.Label(self.scrollable_frame, bg="white", text=self.name).pack()
                print(self.name)

    def convert_file(self):
        if self.for_conversion:
            for self.file in self.for_conversion:
                print(self.file)
                self.outFile = self.file.replace(self.ext, ".mp3")
                self.filename = os.path.basename(self.file)
                if self.CheckVar1.get() == "0":
                    self.converted = os.path.join(os.path.dirname(self.file), "converted")
                    print(self.converted)
                    if not os.path.isdir(self.converted):
                        os.makedirs(self.converted)
                    self.outFile = os.path.join(self.converted ,self.filename.split(".")[0] + ".mp3")
                print(self.outFile)
                cmd = f'{self.ffmpeg} -i "{self.file}" -codec:a libmp3lame -loglevel warning -vn -ar 22050 "{self.outFile}"'

                try:
                    os.system(cmd)
                except Exception as e:
                    print(e)
                print(f"File '{self.filename}' converted")
            print("All files converted")
        else:
            self.file_name.config(bg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = GuiWindow(root)
    root.title('spear1403\'s m4b to mp3 converter')
    root.minsize(350, 370)
    root.mainloop()
