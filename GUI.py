from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import os
import Main

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("PR++ IDLE")
        master.geometry("1280x720")

        self.menu = Menu()
        master.config(menu=self.menu)

        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=None)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)

        self.edit_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=None)
        self.edit_menu.add_command(label="Redo", command=None)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=None)
        self.edit_menu.add_command(label="Copy", command=None)
        self.edit_menu.add_command(label="Paste", command=None)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=None)
        
        self.run_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run PR++ file", command=self.run_and_save)
        
        self.help_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.about)

        self.help = ttk.Notebook(master)
        self.help.grid(row=0, column=0, sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=4)  # 让editor列占据更多空间
        
        self.tab1 = ttk.Frame(self.help)
        
        self.help_list = Listbox(self.tab1)
        self.scrollbar_x = Scrollbar(self.tab1, orient='horizontal')
        self.scrollbar_y = Scrollbar(self.tab1)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)
        self.scrollbar_y.pack(side=LEFT, fill=Y)
        self.help_list.config(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_x.config(command=self.help_list.xview)
        self.scrollbar_y.config(command=self.help_list.yview)
        
        self.help_list.pack(fill=BOTH, expand=1)
        self.help_list.insert(END, "----帮助----")
        self.help_list.insert(END, "    1.基本命令")
        self.help_list.insert(END, "        1.輸出：prln([打印內容])")
        self.help_list.insert(END, "        2.輸入：a = input([提示詞]) 讀取用戶輸入")
        self.help_list.insert(END, "        3.提示框：messagebox.showinfo([標題],[內容])")
        
        self.help.add(self.tab1, text="帮助")

        self.editor = ttk.Notebook(master)
        self.editor.grid(row=0, column=1, sticky="nsew")
        
        self.tab2 = ttk.Frame(self.editor)
        
        self.welcome_list = Listbox(self.tab2)
        self.welcome_list.pack(fill=BOTH, expand=1)
        self.welcome_list.insert(END, "欢迎使用PR++")
        self.welcome_list.insert(END, "1. 打开文件")
        self.welcome_list.insert(END, "2. 保存文件")
        self.welcome_list.insert(END, "3. 另存为")
        self.welcome_list.insert(END, "4. 退出")

        self.tab3 = ttk.Frame(self.editor)
        
        self.text_input = Text(self.tab3,font=("Ubuntu Mono", 12))
        self.text_input.pack(fill=BOTH, expand=1)
        
        self.scrollbar_input_y = Scrollbar(self.text_input, orient=VERTICAL)
        self.scrollbar_input_x = Scrollbar(self.text_input, orient=HORIZONTAL)
        self.scrollbar_input_y.pack(side=RIGHT, fill=Y)
        self.scrollbar_input_x.pack(side=BOTTOM, fill=X)
        
        self.text_input.config(xscrollcommand=self.scrollbar_input_x.set, yscrollcommand=self.scrollbar_input_y.set)
        self.scrollbar_input_y.config(command=self.text_input.yview) # 绑定滚动条事件
        self.scrollbar_input_x.config(command=self.text_input.xview) # 绑定滚动条事件

        self.keywords = ['return', 'func', 'run', 'loop', 'while', 'loop',
                         'while', 'True', 'False', 'load', 'as', 'from']
        self.modules = ['print', 'prln', 'input']

        for i in self.modules:
            self.text_input.tag_configure(i, foreground='purple')


        # 定义关键词标签和样式
        self.text_input.tag_configure('print', foreground='blue')
        self.text_input.tag_configure('prln', foreground='blue')
        self.text_input.tag_configure("'", foreground='green')
        self.text_input.tag_configure('//', foreground='gray')  # 为注释添加颜色
        self.text_input.tag_configure('return', foreground='blue')
        self.text_input.tag_configure('func', foreground='blue')
        self.text_input.tag_configure('run', foreground='blue')
        self.text_input.tag_configure('loop', foreground='blue')
        self.text_input.tag_configure('while', foreground='blue')
        self.text_input.tag_configure('True', foreground='green')
        self.text_input.tag_configure('False', foreground='red')
        self.text_input.tag_configure('load', foreground='purple')
        self.text_input.tag_configure('as', foreground='purple')
        self.text_input.tag_configure('from', foreground='purple')
        
        self.text_input.bind("<KeyRelease>", self.highlight_keywords)  # 绑定键盘事件，实时高亮关键词

        self.editor.add(self.tab2, text="歡迎")
        self.editor.add(self.tab3, text="未命名1.pr")

    def about(self):
        messagebox.showinfo("關於","作者：取名困難症\n版本：0.1\n日期：2023/3/18")

    def open_file(self):
        file = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("PR++ projects", "*.pr"), ("Text files", "*.txt"), ("All files", "*.*")))
        if file:
            with open(file, "r") as f:
                content = f.read()
                self.text_input.delete("1.0", END)
                self.text_input.insert(END, content)
                self.highlight_keywords()  # 添加此行以高亮关键词

    def save_file(self):
        file = filedialog.asksaveasfilename(initialdir="/", title="Save file", filetypes=(("PR++ projects", "*.pr"), ("Text files", "*.txt"), ("All files", "*.*")))
        if file:
            self.save_content(file)

    def save_file_as(self):
        file = filedialog.asksaveasfilename(initialdir="/", title="Save file as", filetypes=(("PR++ projects", "*.pr"), ("Text files", "*.txt"), ("All files", "*.*")))
        if file:
            self.save_content(file)

    def run_and_save(self):
        os.system("cls")
        Main.start(self.text_input.get("1.0", END))
    
    def save_content(self, file):
        with open(file, "w") as f:
            content = self.text_input.get("1.0", END)
            f.write(content)

    def highlight_keywords(self, event=None):
        # 清除所有标签

        self.text_input.tag_remove("'", '1.0', END)
        self.text_input.tag_remove('//', '1.0', END)  # 清除注释标签
        self.text_input.tag_remove('return', '1.0', END)
        self.text_input.tag_remove('func', '1.0', END)
        self.text_input.tag_remove('loop', '1.0', END)
        self.text_input.tag_remove('while', '1.0', END)
        self.text_input.tag_remove('run', '1.0', END)
        self.text_input.tag_remove('True', '1.0', END)
        self.text_input.tag_remove('False', '1.0', END)
        self.text_input.tag_remove('print', '1.0', END)
        self.text_input.tag_remove('prln', '1.0', END)
        self.text_input.tag_remove('load', '1.0', END)
        self.text_input.tag_remove('as', '1.0', END)
        self.text_input.tag_remove('from', '1.0', END)
        
        # 高亮关键词 prln
        content = self.text_input.get("1.0", END)
        start = "1.0"
        while True:
            start = self.text_input.search("prln", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('prln')}c"
            self.text_input.tag_add('prln', start, end)
            start = end
            
        # 高亮关键词 print
        content = self.text_input.get("1.0", END)
        start = "1.0"
        while True:
            start = self.text_input.search("print", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('print')}c"
            self.text_input.tag_add('print', start, end)
            start = end
            
        # 高亮关键词 load
        content = self.text_input.get("1.0", END)
        start = "1.0"
        while True:
            start = self.text_input.search("load", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('load')}c"
            self.text_input.tag_add('load', start, end)
            start = end
            
        # 高亮关键词 as
        content = self.text_input.get("1.0", END)
        start = "1.0"
        while True:
            start = self.text_input.search("as", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('as')}c"
            self.text_input.tag_add('as', start, end)
            start = end
            
        # 高亮关键词 from
        content = self.text_input.get("1.0", END)
        start = "1.0"
        while True:
            start = self.text_input.search("from", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('from')}c"
            self.text_input.tag_add('from', start, end)
            start = end
                
        # 高亮关键词 ''
        start = "1.0"
        while True:
            start = self.text_input.search("'", start, stopindex=END, regexp=False)  # 使用半角单引号
            if not start:
                break
            # 找到单引号后，找到下一个单引号的位置
            end = self.text_input.search("'", f"{start}+1c", stopindex=END, regexp=False)
            if not end:
                break
            # 高亮从第一个单引号到第二个单引号之间的内容
            self.text_input.tag_add("'", start, f"{end}+1c")  # 使用半角单引号作为标签名称
            start = f"{end}+1c"  # 继续搜索下一个单引号

        # 高亮关键词 return   
        start = "1.0"
        while True:
            start = self.text_input.search("return", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('return')}c"
            self.text_input.tag_add('return', start, end)
            start = end
            
        start = "1.0"
        while True:
            start = self.text_input.search("True", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('True')}c"
            self.text_input.tag_add('True', start, end)
            start = end
            
        start = "1.0"
        while True:
            start = self.text_input.search("False", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('False')}c"
            self.text_input.tag_add('False', start, end)
            start = end
                
        # 高亮关键词 func   
        start = "1.0"
        while True:
            start = self.text_input.search("func", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('func')}c"
            self.text_input.tag_add('func', start, end)
            start = end
            
        # 高亮关键词 return  
        start = "1.0"
        while True:
            start = self.text_input.search("return", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('return')}c"
            self.text_input.tag_add('return', start, end)
            start = end   
        
        # 高亮关键词 while  
        start = "1.0"
        while True:
            start = self.text_input.search("while", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('while')}c"
            self.text_input.tag_add('while', start, end)
            start = end
            
        # 高亮关键词 run   
        start = "1.0"
        while True:
            start = self.text_input.search("run", start, stopindex=END, regexp=False)
            if not start:
                break
            end = f"{start}+{len('run')}c"
            self.text_input.tag_add('run', start, end)
            start = end

        # 高亮注释 //
        start = "1.0"
        while True:
            start = self.text_input.search("//", start, stopindex=END, regexp=False)
            if not start:
                break
            # 找到注释的开始位置后，找到该行的末尾
            line_end = self.text_input.index(f"{start} lineend")
            self.text_input.tag_add('//', start, line_end)
            start = self.text_input.index(f"{start} +1line")
root = Tk()
my_gui = GUI(root)
root.mainloop()
