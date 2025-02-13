import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
from PIL import Image

class ImageSwapApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("成对图片左右对调")
        self.geometry("500x350")

        # 输入输出文件夹路径
        self.input_folder = ""
        self.output_folder = ""

        # 创建控件
        self.input_label = tk.Label(self, text="输入文件夹路径：")
        self.input_label.pack(pady=5)

        # 文本框用于输入文件夹路径
        self.input_text = scrolledtext.ScrolledText(self, width=50, height=5)
        self.input_text.pack(pady=5)
        self.input_text.bind("<KeyRelease>", self.on_input_change)  # 监听输入变化

        # 按钮用于选择文件夹
        self.input_button = tk.Button(self, text="选择输入文件夹", command=self.select_input_folder)
        self.input_button.pack(pady=5)

        # 输出文件夹路径标签
        self.output_label = tk.Label(self, text="输出文件夹路径：")
        self.output_label.pack(pady=5)

        # 文本框用于显示输出路径
        self.output_text = scrolledtext.ScrolledText(self, width=50, height=3)
        self.output_text.pack(pady=5)
        self.output_text.config(state=tk.DISABLED)  # 使其不可编辑

        # 按钮用于开始交换图片
        self.swap_button = tk.Button(self, text="开始交换图片", command=self.swap_images, state=tk.DISABLED)
        self.swap_button.pack(pady=20)

    def select_input_folder(self):
        folder_selected = filedialog.askdirectory(title="选择输入文件夹")
        if folder_selected:
            self.input_folder = folder_selected
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(tk.END, self.input_folder)
            self.update_output_folder()
            self.check_ready_to_swap()

    def update_output_folder(self):
        # 设置输出文件夹为输入文件夹 + '_swap'
        if self.input_folder:
            self.output_folder = self.input_folder + "_swap"
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)  # 清空文本框
            self.output_text.insert(tk.END, self.output_folder)  # 更新路径
            self.output_text.config(state=tk.DISABLED)  # 使其不可编辑

    def on_input_change(self, event=None):
        # 每次输入时自动更新输出路径
        input_folder = self.input_text.get(1.0, tk.END).strip()
        if input_folder:
            self.input_folder = input_folder
            self.update_output_folder()
            self.check_ready_to_swap()

    def check_ready_to_swap(self):
        # 如果输入文件夹已选择，则启用交换按钮
        if self.input_folder:
            self.swap_button.config(state=tk.NORMAL)

    def swap_images(self):
        try:
            # 直接从文本框读取输入文件夹路径
            input_folder = self.input_text.get(1.0, tk.END).strip()
            if not input_folder:
                raise ValueError("请输入有效的文件夹路径")

            # 设定输出文件夹
            output_folder = input_folder + "_swap"

            # 调用交换图片函数
            swap_images_in_pairs(input_folder, output_folder)
            messagebox.showinfo("完成", "图片交换完成！")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

def swap_images_in_pairs(input_folder, output_folder):
    # 创建输出文件夹如果它不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取所有jpg文件并排序
    files = sorted([f for f in os.listdir(input_folder) if f.endswith('.jpg')])

    # 处理成对的图片
    for i in range(0, len(files), 2):
        if i + 1 < len(files):
            # 获取图片路径
            img1_path = os.path.join(input_folder, files[i])
            img2_path = os.path.join(input_folder, files[i + 1])

            # 打开图片
            img1 = Image.open(img1_path)
            img2 = Image.open(img2_path)

            # 保存图片到输出文件夹，交换顺序
            img1.save(os.path.join(output_folder, files[i + 1]))
            img2.save(os.path.join(output_folder, files[i]))
        else:
            # 如果总数是奇数，最后一张图片不交换，直接复制
            img_path = os.path.join(input_folder, files[i])
            img = Image.open(img_path)
            img.save(os.path.join(output_folder, files[i]))


if __name__ == "__main__":
    app = ImageSwapApp()
    app.mainloop()
