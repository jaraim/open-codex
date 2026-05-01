import sys
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog

from open_codex.main import get_agent, run_one_shot

CONFIG_FILE = "desktop_config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "model": "phi4-mini:latest",
            "ollama": False,
            "ollama_host": "http://localhost:11434"
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def open_settings(current_config, callback):
    win = tk.Toplevel()
    win.title("Settings")
    win.geometry("350x250")

    tk.Label(win, text="Model Name:").pack(pady=5)
    model_var = tk.StringVar(value=current_config["model"])
    tk.Entry(win, textvariable=model_var, width=30).pack()

    ollama_var = tk.BooleanVar(value=current_config["ollama"])
    tk.Checkbutton(win, text="Use Ollama", variable=ollama_var).pack(pady=5)

    tk.Label(win, text="Ollama Host:").pack()
    host_var = tk.StringVar(value=current_config["ollama_host"])
    tk.Entry(win, textvariable=host_var, width=30).pack(pady=5)

    def save():
        new_config = {
            "model": model_var.get(),
            "ollama": ollama_var.get(),
            "ollama_host": host_var.get()
        }
        save_config(new_config)
        callback(new_config)
        win.destroy()

    tk.Button(win, text="Save", command=save).pack(pady=20)

def run_gui():
    config = load_config()

    def on_submit():
        prompt = entry.get().strip()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt.")
            return
        btn.config(state="disabled", text="Processing...")
        root.update()
        try:
            class Args:
                model = config["model"]
                ollama = config["ollama"]
                ollama_host = config["ollama_host"]
            agent = get_agent(Args())
            response = run_one_shot(agent, prompt)
            output_area.insert(tk.END, f"> {prompt}\n{response}\n\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            btn.config(state="normal", text="Submit")

    def refresh_config(new_config):
        nonlocal config
        config = new_config
        messagebox.showinfo("Settings", "Settings saved! They will be used from now on.")

    root = tk.Tk()
    root.title("Open Codex - Desktop")
    root.geometry("650x500")

    # 设置按钮
    tk.Button(root, text="⚙ Settings", command=lambda: open_settings(config, refresh_config)).pack(pady=5)

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
    from multiprocessing import freeze_support
    freeze_support()
    if len(sys.argv) == 1:
        run_gui()
    else:
        from open_codex.main import main
        main()
