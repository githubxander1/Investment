import tkinter as tk
import openpyxl
class App:
    def __init__(self, master):
        self.master = master
        master.title("Text Demo")

        # 创建Text窗口部件
        self.text = tk.Text(master)
        self.text.pack(fill=tk.BOTH, expand=True)

        # 设置Text窗口部件的初始文本内容
        self.text.insert(tk.END, "用户详细描述：\n\n")
        self.text.insert(tk.END, "产品简介：\n\n")

        # 创建一个按钮，用来保存编辑后的文本内容到Excel
        self.save_button = tk.Button(master, text="保存到Excel",command=self.save_text_to_excel)
        self.save_button.pack()

    def save_text_to_excel(self):
        # 获取Text窗口部件中的文本内容
        text_content = self.text.get(1.0, tk.END)

        # 将文本内容拆分成行
        lines = text_content.split('\n')

        # 创建一个新的Excel工作簿
        wb = openpyxl.Workbook()

        # 选择默认的工作表
        ws = wb.active

        # 逐行将文本内容写入Excel工作表
        for i, line in enumerate(lines):
            ws.cell(row=i + 1, column=1, value=line)

        # 保存Excel文件
        wb.save("text_to_excel.xlsx")

def main():
    # 创建一个Tk对象
    root = tk.Tk()

    # 创建一个App对象
    app = App(root)

    # 运行主循环
    root.mainloop()

if __name__ == '__main__':
    main()