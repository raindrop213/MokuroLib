import os
import zipfile
import rarfile
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

# 提取ZIP或CBZ文件中的图片
def extract_images_from_zip(zip_path, output_dir):
    zip_name = os.path.splitext(os.path.basename(zip_path))[0]
    zip_output_dir = os.path.join(output_dir, zip_name)
    
    if not os.path.exists(zip_output_dir):
        os.makedirs(zip_output_dir)

    image_count = 0
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_name = os.path.basename(file)
                output_image_path = os.path.join(zip_output_dir, image_name)
                with zip_ref.open(file) as image_file:
                    with open(output_image_path, 'wb') as f:
                        f.write(image_file.read())
                image_count += 1

    return zip_name, image_count

# 提取RAR文件中的图片
def extract_images_from_rar(rar_path, output_dir):
    rar_name = os.path.splitext(os.path.basename(rar_path))[0]
    rar_output_dir = os.path.join(output_dir, rar_name)

    if not os.path.exists(rar_output_dir):
        os.makedirs(rar_output_dir)

    image_count = 0
    with rarfile.RarFile(rar_path, 'r') as rar_ref:
        for file in rar_ref.namelist():
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_name = os.path.basename(file)
                output_image_path = os.path.join(rar_output_dir, image_name)
                with rar_ref.open(file) as image_file:
                    with open(output_image_path, 'wb') as f:
                        f.write(image_file.read())
                image_count += 1

    return rar_name, image_count

# 提取EPUB或CBZ文件中的图片
def extract_images_from_epub(epub_path, output_dir):
    epub_name = os.path.splitext(os.path.basename(epub_path))[0]
    epub_output_dir = os.path.join(output_dir, epub_name)
    
    if not os.path.exists(epub_output_dir):
        os.makedirs(epub_output_dir)

    image_count = 0
    with zipfile.ZipFile(epub_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_name = os.path.basename(file)
                output_image_path = os.path.join(epub_output_dir, image_name)
                with zip_ref.open(file) as image_file:
                    with open(output_image_path, 'wb') as f:
                        f.write(image_file.read())
                image_count += 1

    return epub_name, image_count

# 提取不同格式文件中的图片
def extract_images_from_files(file_paths, output_dir):
    extraction_results = []

    for file_path in file_paths:
        if file_path.endswith(('.epub', '.cbz')):
            epub_name, image_count = extract_images_from_epub(file_path, output_dir)
            extraction_results.append(f"提取了【{image_count}】张图片 ← {epub_name}")
        elif file_path.endswith('.zip'):
            zip_name, image_count = extract_images_from_zip(file_path, output_dir)
            extraction_results.append(f"提取了【{image_count}】张图片 ← {zip_name}")
        elif file_path.endswith('.rar'):
            rar_name, image_count = extract_images_from_rar(file_path, output_dir)
            extraction_results.append(f"提取了【{image_count}】张图片 ← {rar_name}")
    
    return extraction_results

# 拖放文件并提取图片
def on_drop(event):
    file_paths = root.tk.splitlist(event.data)
    output_dir = os.path.join(os.path.dirname(file_paths[0]))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    extraction_results = extract_images_from_files(file_paths, output_dir)
    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, "\n".join(extraction_results))

# 创建主窗口
root = TkinterDnD.Tk()
root.title("图片提取（ZIP, RAR, EPUB, CBZ）")
root.geometry("600x500")

# 提示文本
label = tk.Label(root, text="拖放ZIP、RAR、EPUB或CBZ文件到这里", pady=20)
label.pack()

# 显示提取结果的文本框
results_text = tk.Text(root, width=70, height=15)
results_text.pack(pady=10)

# 设置拖放区域
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# 运行主循环
root.mainloop()
