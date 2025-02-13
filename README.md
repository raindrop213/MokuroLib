基于 [mokuro](https://github.com/kha-white/mokuro) v0.2.2
的建议漫画书架 + mokuro整合包

## 说明
- 本整合包经过了优化键位；增加点击文字复制到剪切板；因为js和css文件所有漫画共用方便修改，所以现在 "--as_one_file False" 既不嵌入html也不生成独立文件。
- 仅改了页面交互， .mokuro文件与原版相同
- 想用原版的话将"mokuro（原版）"的内容替换进"mokuro-py310\Lib\site-packages\mokuro"。当然用原版的mokuro生成的也可以显示到页面上，只要有html文件，以及漫画文件格式正确。

![image](https://github.com/user-attachments/assets/8e53d9ee-2dee-4562-85a7-e981f72f61c2)

![image](https://github.com/user-attachments/assets/e1d83b10-289e-48d8-84c0-39fc12d8136b)

## 多卷命令
```
mokuro --disable_confirmation --parent_dir "?" --as_one_file False
```
```
mokuro-py310\python.exe -m mokuro --disable_confirmation --parent_dir "manga\[武田日向] やえかのカルテ" --as_one_file False
```

## 单卷命令
```
mokuro --disable_confirmation "?" --as_one_file False
```
```
mokuro-py310\python.exe -m mokuro --disable_confirmation "manga\[西尾維新×大暮維人] 化物語\[西尾維新] 化物語 第01巻" --as_one_file False
```

## 其他命令
```
--pretrained_model_name_or_path: Name or path of the manga-ocr model.
--force_cpu: Force the use of CPU even if CUDA is available.
--disable_confirmation: Disable confirmation prompt. If False, the user will be prompted to confirm the list of volumes to be processed.
--disable_ocr: Disable OCR processing. Generate mokuro/HTML files without OCR results.
--ignore_errors: Continue processing volumes even if an error occurs.
--no_cache: Do not use cached OCR results from previous runs (_ocr directories).
--unzip: Extract volumes in zip/cbz format in their original location.
--disable_html: Disable legacy HTML output. If True, acts as if --unzip is True.
--as_one_file: Applies only to legacy HTML. If False, generate separate CSS and JS files instead of embedding them in the HTML file.
--version: Print the version of mokuro and exit.
```
```
--pretrained_model_name_or_path: 漫画OCR模型的名称或路径。
--force_cpu: 即使CUDA可用，也强制使用CPU。
--disable_confirmation: 禁用确认提示。若为False，用户将被提示确认待处理的卷列表。
--disable_ocr: 禁用OCR处理。生成不含OCR结果的mokuro/HTML文件。
--ignore_errors: 即使发生错误，也继续处理卷。
--no_cache: 不使用之前运行的缓存OCR结果（_ocr目录）。
--unzip: 在原始位置解压zip/cbz格式的卷。
--disable_html: 禁用旧版HTML输出。若为True，则等同于启用--unzip。
--as_one_file: 仅适用于旧版HTML。若为False，生成独立的CSS和JS文件，而非嵌入HTML文件中。
--version: 打印mokuro版本并退出。
```


## 生成过程
_ocr → xxx.mokuro → xxx.html


## 文件结构
```
manga
│  panzoom.min.js
│  script.js
│  styles.css（mokuro的.css和.js可以共用，也方便统一修改，只能放在这位置）
│
└─[武田日向] やえかのカルテ
   │  [武田日向] やえかのカルテ 第01巻.html（mokuro生成的网页）
   │  [武田日向] やえかのカルテ 第02巻.html
   │  [武田日向] やえかのカルテ 第03巻.html
   │
   ├─[武田日向] やえかのカルテ 第01巻
   │      0000.jpg
   │      ...
   │      0016.jpg
   │
   ├─[武田日向] やえかのカルテ 第02巻
   │      0000.jpg
   │      ...
   │      0006.jpg
   │
   ├─[武田日向] やえかのカルテ 第03巻
   │      0000.jpg
   │      ...
   │      0034.jpg
   │
   └─_ocr（mokuro生成的ocr结果）
       ├─[武田日向] やえかのカルテ 第01巻
       │      0000.json
       │      ...
       │      0016.json
       │
       ├─[武田日向] やえかのカルテ 第02巻
       │      0000.json
       │      ...
       │      0006.json
       │
       └─[武田日向] やえかのカルテ 第03巻
               0000.json
               ...
               0034.json 
```

## 其他工具
自己用来处理漫画的修改工具，因为embed版python很难打包tkinter，如果你需要的话自行安装标准pyhton来使用
```
pip install tkinterdnd2 rarfile natsort
```
```
python extract-epub.py
python rename-file.py
python rename-pic.py
python sep-all.py
python sep-select.py
python sep-select2.py
python swap-pic.py
python white-pic.py
```