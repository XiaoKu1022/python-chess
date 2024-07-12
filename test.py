import tkinter as tk
import subprocess

def run_command():
    command = entry.get()
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    text_widget.delete("1.0", tk.END)  # 清空文本框
    text_widget.insert(tk.END, output.stdout + output.stderr)  # 显示命令输出

# 创建主窗口
root = tk.Tk()
root.title("Command Interface")

# 创建输入框
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# 创建按钮
button = tk.Button(root, text="Run Command", command=run_command)
button.pack(pady=5)

# 创建文本框来显示输出
text_widget = tk.Text(root, height=20, width=80)
text_widget.pack(pady=10)

# 启动主循环
root.mainloop()
