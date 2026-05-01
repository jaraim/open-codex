# desktop_launcher.py
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext

# 从 open_codex 包导入需要的函数（不修改 main.py）
from open_codex.main import get_agent, run_one_shot


def run_gui():
    """简单的 tkinter 桌面窗口"""
    def on_submit():
        prompt = entry.get().strip()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt.")
            return
        btn.config(state="disabled", text="Processing...")
        root.update()
        try:
            # 构造一个默认参数对象，模拟命令行参数
            class Args:
                model = "phi4-mini:latest"
                ollama = False
                ollama_host = "http://localhost:11434"
            agent = get_agent(Args())
            response = run_one_shot(agent, prompt)
            output_area.insert(tk.END, f"> {prompt}\n{response}\n\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            btn.config(state="normal", text="Submit")

    root = tk.Tk()
    root.title("Open Codex - Desktop")
    root.geometry("650x500")

    tk.Label(root, text="Enter your prompt:").pack(pady=(10, 0))
    entry = tk.Entry(root, width=80)
    entry.pack(pady=5)
    entry.focus()

    btn = tk.Button(root, text="Submit", command=on_submit)
    btn.pack(pady=5)

    output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    output_area.pack(padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    # PyInstaller 打包的 Windows GUI 程序必须调用 freeze_support
    from multiprocessing import freeze_support
    freeze_support()

    # 只有 exe 本身且无命令行参数时才启动 GUI
    if len(sys.argv) == 1:
        run_gui()
    else:
        # 如果通过命令行传了参数（例如调试），则按原 CLI 流程执行
        from open_codex.main import main
        main()
