import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

import ffmpeg
import os
import random


def modify_mp4(input_file, output_file, progress_var, progress_label, step_text, chunk_size):
    try:
        # 获取输入文件大小
        input_file_size = os.path.getsize(input_file)

        # 用于存储修改后的数据
        modified_data = bytearray()

        # 读取原始 MP4 文件的内容
        with open(input_file, 'rb') as f:
            original_data = f.read()

        # 将原始数据拷贝到修改后的数据中
        modified_data += original_data

        # 每隔 chunk_size 修改一个字节
        for i in range(0, input_file_size, chunk_size):
            start_index = i
            end_index = min(i + chunk_size, input_file_size)

            # 在当前块中随机选择一个字节并修改
            random_index = random.randint(start_index, end_index - 1)
            modified_data[random_index] = random.randint(0, 255)

            # 计算进度百分比并更新进度条和标签
            progress = (end_index / input_file_size) * 100
            progress_var.set(progress)
            progress_label.config(text=f"Progress: {int(progress)}%")

            # 在文本框中显示当前处理的步骤
            step_text.insert(tk.END, f"Processed chunk from {start_index} to {end_index}\n")
            step_text.see(tk.END)  # 滚动文本框以便显示最新的内容

        # 将修改后的数据写入新的 MP4 文件
        with open(output_file, 'wb') as f:
            f.write(modified_data)

        messagebox.showinfo("Success", "MP4 文件修改完成！")

        # 安排在1秒后执行清空文本框和将进度条归零的操作
        step_text.after(1000, lambda: clear_text_and_progress(step_text, progress_var, progress_label))
    except Exception as e:
        print("Error:", e)


def clear_text_and_progress(step_text, progress_var, progress_label):
    step_text.delete("1.0", tk.END)
    progress_var.set(0)
    progress_label.config(text="Progress: 0%")


def browse_input_file(label):
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    label.config(text=file_path)


def browse_output_file(label):
    file_path = filedialog.asksaveasfilename(filetypes=[("MP4 files", "*.mp4")], defaultextension=".mp4")
    label.config(text=file_path)


def start_modification(input_label, output_label, progress_var, progress_label, step_text, chunk_size_entry):
    input_file = input_label.cget("text")
    output_file = output_label.cget("text")

    # 获取用户输入的修改间隔，默认为2048字节
    chunk_size = int(chunk_size_entry.get()) if chunk_size_entry.get() else 2048

    # 清空文本框
    step_text.delete("1.0", tk.END)

    # 在每次开始新的工程时将进度条归零
    progress_var.set(0)

    modify_mp4(input_file, output_file, progress_var, progress_label, step_text, chunk_size)


def create_ui():
    root = tk.Tk()
    root.title("MP4 Modification Tool")

    input_label = tk.Label(root, text="Select input MP4 file:")
    input_label.pack()

    input_button = tk.Button(root, text="Browse", command=lambda: browse_input_file(input_label))
    input_button.pack()

    output_label = tk.Label(root, text="Select output MP4 file:")
    output_label.pack()

    output_button = tk.Button(root, text="Browse", command=lambda: browse_output_file(output_label))
    output_button.pack()

    chunk_size_label = tk.Label(root, text="Chunk Size (bytes):")
    chunk_size_label.pack()

    chunk_size_entry = tk.Entry(root)
    chunk_size_entry.pack()
    chunk_size_entry.insert(0, "10240")  # 设置默认值为10240字节

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(fill=tk.X, padx=10, pady=5)

    progress_label = tk.Label(root, text="Progress: 0%")
    progress_label.pack()

    step_label = tk.Label(root, text="Current Step:")
    step_label.pack()

    step_text = tk.Text(root, height=5, width=50)
    step_text.pack()

    start_button = tk.Button(root, text="Start Modification",
                             command=lambda: start_modification(input_label, output_label, progress_var, progress_label,
                                                                step_text, chunk_size_entry))
    start_button.pack()

    root.mainloop()


if __name__ == "__main__":
    create_ui()
