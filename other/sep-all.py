import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# 裁剪图片函数
def crop_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size

        # 只处理宽度大于高度的图片
        if width > height:
            # 计算新的宽度，使其等于高度
            new_width = width // 2

            # 裁剪图片的左半部分
            left_image = img.crop((0, 0, new_width, height))
            left_path = f"{os.path.splitext(image_path)[0]}_b{os.path.splitext(image_path)[1]}"
            left_image.save(left_path, quality=95)

            # 裁剪图片的右半部分
            right_image = img.crop((new_width, 0, width, height))
            right_path = f"{os.path.splitext(image_path)[0]}_a{os.path.splitext(image_path)[1]}"

            right_image.save(right_path, quality=95)
            os.remove(image_path)

            print(f"图片已裁剪：{image_path}")
        else:
            print(f"跳过宽度小于高度的图片：{image_path}")

# 处理文件夹内所有图片的函数
def process_images_in_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', 'webp'))]
    crop_files = []

    if not image_files:
        messagebox.showinfo("无图片", "文件夹内没有支持的图片文件！")
        return []

    # 筛选需要裁剪的图片
    for file in image_files:
        image_path = os.path.join(folder_path, file)
        with Image.open(image_path) as img:
            width, height = img.size
            if width > height:
                crop_files.append(file)

    # 如果没有符合裁剪条件的图片
    if not crop_files:
        crop_files.append("没有图片被裁剪")

    # 更新UI显示
    image_listbox.delete(0, tk.END)
    for file in crop_files:
        image_listbox.insert(tk.END, file)

    return crop_files

# 执行裁剪
def start_cropping():
    folder_path = folder_path_var.get()
    if not folder_path:
        messagebox.showerror("错误", "请先选择一个文件夹！")
        return
    
    crop_files = process_images_in_folder(folder_path)
    if "没有图片被裁剪" in crop_files:
        return  # 如果没有图片被裁剪，停止执行

    # 开始裁剪
    for filename in crop_files:
        if filename != "没有图片被裁剪":  # 忽略“没有图片被裁剪”项
            image_path = os.path.join(folder_path, filename)
            crop_image(image_path)

    messagebox.showinfo("完成", "所有图片裁剪完成！")

# 选择文件夹
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)
        # 选择文件夹后立即检查并显示符合条件的图片
        process_images_in_folder(folder_path)

# 创建主窗口
root = tk.Tk()
root.title("图片裁剪")
root.geometry("600x500")

# 文件夹路径变量
folder_path_var = tk.StringVar()

# UI组件
label = tk.Label(root, text="请选择包含图片的文件夹", pady=10)
label.pack()

folder_button = tk.Button(root, text="选择文件夹", command=select_folder)
folder_button.pack()

folder_path_label = tk.Label(root, textvariable=folder_path_var, wraplength=500)
folder_path_label.pack(pady=10)

# 图片文件列表
image_listbox_label = tk.Label(root, text="将会被裁剪的图片", pady=10)
image_listbox_label.pack()

image_listbox = tk.Listbox(root, width=50, height=10)
image_listbox.pack()

# 开始裁剪按钮
crop_button = tk.Button(root, text="开始裁剪", command=start_cropping)
crop_button.pack(pady=20)

# 运行主循环
root.mainloop()
