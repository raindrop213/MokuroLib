import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import messagebox, StringVar
from natsort import natsorted, ns
import os

def rename_images_gui(folder_path, num_digits):
    extensions = ('.png', '.jpg', '.jpeg', '.webp', '.json', '.JPG', '.JPEG')
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(extensions)]
    files = natsorted(files, alg=ns.PATH)

    digit_format = f"{{:0{num_digits}d}}"
    preview_list = []
    if len(files) <= 10:
        for i, filename in enumerate(files):
            preview_list.append(f"{filename} -> {digit_format.format(i)}{os.path.splitext(filename)[1].lower()}")
    else:
        for i, filename in enumerate(files[:5]):
            preview_list.append(f"{filename} -> {digit_format.format(i)}{os.path.splitext(filename)[1].lower()}")
        preview_list.append("...")
        for i, filename in enumerate(files[-5:], start=len(files) - 5):
            preview_list.append(f"{filename} -> {digit_format.format(i)}{os.path.splitext(filename)[1].lower()}")

    preview = "\n".join(preview_list)

    if messagebox.askyesno("重命名预览", f"文件夹: {folder_path}\n预览:\n{preview}\n\n是否继续重命名?"):
        for i, filename in enumerate(files):
            ext = os.path.splitext(filename)[1].lower()
            new_filename = digit_format.format(i) + ext
            try:
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
            except Exception as e:
                messagebox.showerror("错误", f"重命名 {filename} 时出错: {e}")
        messagebox.showinfo("完成", f"文件夹 {folder_path} 的重命名已完成")

def on_drop(event):
    paths = event.data.strip('{}').split('} {')
    num_digits = digits_var.get()
    if num_digits.isdigit():
        num_digits = int(num_digits)
        for path in paths:
            folder_path = path.strip('{}')
            if os.path.isdir(folder_path):
                rename_images_gui(folder_path, num_digits)
            else:
                messagebox.showerror("错误", f"{folder_path} 不是有效的文件夹。")
    else:
        messagebox.showerror("错误", "请输入有效的数字位数。")

root = TkinterDnD.Tk()
root.title("批量图片名重命名")
root.geometry("600x400")

label = tk.Label(root, text="将一个或多个文件夹拖拽到此处", pady=20)
label.pack()

digits_var = StringVar(root, value='4')  # 默认值设置为4
digits_label = tk.Label(root, text="请输入数字位数：")
digits_label.pack()

digits_entry = tk.Entry(root, textvariable=digits_var)
digits_entry.pack()

frame = tk.Frame(root, bg="lightgray", width=500, height=300)
frame.pack(pady=20)
frame.drop_target_register(DND_FILES)
frame.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
