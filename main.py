import tkinter as tk
from tkinter import filedialog
import markdown
from tkinterweb import HtmlFrame


class MarkdownPreviewer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # 创建上部样式选择区域
        self.style_label = tk.Label(self, text="样式选择:")
        self.style_label.grid(row=0, column=0, sticky="w")
        self.style_var = tk.StringVar(value="default.css")
        self.style_var.trace('w', self.on_option_changed)
        self.style_options = ["default.css", "dark.css", "github.css"]
        self.style_menu = tk.OptionMenu(self, self.style_var, *self.style_options)
        self.style_menu.grid(row=0, column=1, sticky="w")
        
        
   



        # 创建Markdown编辑框
        self.text_label = tk.Label(self, text="Markdown:")
        self.text_label.grid(row=1, column=0, sticky="w")
        self.text = tk.Text(self)
        self.text.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.text.config(wrap="word", undo=True)
        scrollb = tk.Scrollbar(self, command=self.text.yview)
        scrollb.grid(row=2, column=1, sticky="nsew")
        self.text["yscrollcommand"] = scrollb.set

        # 创建Markdown预览框
        self.preview_label = tk.Label(self, text="预览:")
        self.preview_label.grid(row=1, column=2, sticky="w")
        self.preview_text = HtmlFrame(self)
        self.preview_text.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        # 创建底部按钮
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=3, column=0, columnspan=3, sticky="w")
        self.preview_button = tk.Button(
            self.button_frame, text="预览", command=self.preview
        )
        self.preview_button.pack(side="left", padx=5)
        self.save_button = tk.Button(self.button_frame, text="保存", command=self.save)
        self.save_button.pack(side="left", padx=5)

    # 定义切换事件的处理函数
    def on_option_changed(self,*e):
        self.preview()
    
    def preview(self):
        # 预览Markdown内容
        md_text = self.text.get("1.0", tk.END)
        html = markdown.markdown(md_text)
        style_path = "styles/" + self.style_var.get()
        with open(style_path, "r") as f:
            style = f.read()
        html = f"<!DOCTYPE html><html><head><style>{style}</style></head><body>{html}</body></html>"
        self.preview_text.load_html(html)

    def save(self):
        # 保存Markdown内容
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md", filetypes=[("Markdown Files", "*.md")]
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.text.get("1.0", tk.END))


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownPreviewer(master=root)
    app.mainloop()
