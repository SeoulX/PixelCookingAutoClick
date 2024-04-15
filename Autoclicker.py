import importlib
import subprocess

def check_dependencies(dependencies):
    missing_dependencies = []
    for module in dependencies:
        try:
            importlib.import_module(module)
        except ImportError:
            missing_dependencies.append(module)
    return missing_dependencies

def install_dependencies(dependencies):
    for module in dependencies:
        subprocess.run(["pip", "install", module])

def main():
    required_dependencies = ["pyautogui", "keyboard", "tkinter"]

    missing_dependencies = check_dependencies(required_dependencies)

    if missing_dependencies:
        print("Installing missing dependencies...")
        install_dependencies(missing_dependencies)
        print("Dependencies installed successfully!")

    import pyautogui
    from datetime import datetime, timedelta
    import time
    import keyboard
    import tkinter as tk
    import threading
    
    stop_flag = False

    def get_location():
        keyboard.wait("enter")
        click_location = pyautogui.position()
        instructions_label.config(text=click_location)
        return click_location

    def perform_steps(interval, point, amount):
        global stop_flag
        x = point[0]
        y = point[1]

        for i in range(amount):
            loop_label.config(text=f"Loop {i+1}/{amount}")
            if stop_flag:
                break

            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()

            end_time = datetime.now() + timedelta(seconds=interval)
            while datetime.now() < end_time:
                if stop_flag:
                    break
                time.sleep(0.1)

            if stop_flag:
                loop_label.config(text="Auto-clicking completed.")
                break

            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            time.sleep(1)

        if not stop_flag:
            instructions_label.config(text="Click START then place cursor to desire \n" +
                                  'location to perform clicking and hit ENTER')

    def start_clicker():
        if not amount_entry.get() or not item_time_entry.get():
            error_label.config(text="Error: Please fill in all fields.")
        else:
            error_label.config(text="")
            global stop_flag
            stop_flag = False
            
            point = get_location()
            
            num_loops = int(amount_entry.get())
            interval = int(item_time_entry.get()) + 3

        threading.Thread(target=perform_clicks, args=(num_loops, interval, point)).start()

    def perform_clicks(num_loops, interval, point):
        global stop_flag
        perform_steps(interval, point, num_loops)
        if stop_flag:
            loop_label.config(text="Auto-clicking completed.")

        if not stop_flag:
            loop_label.config(text="Auto-clicking completed.")

    def stop_clicker():
        global stop_flag
        stop_flag = True
        instructions_label.config(text="Click START then place cursor to desire \n" +
                                  'location to perform clicking and hit ENTER')

    # GUI setup
    root = tk.Tk()
    root.title("Auto Clicker")
    root.geometry("400x350")
    root.resizable(False, False)  # Setting fixed size and making the window non-resizable

    amount_label = tk.Label(root, text="Amount:")
    amount_label.pack()
    amount_entry = tk.Entry(root)
    amount_entry.pack()

    item_time_label = tk.Label(root, text="Item Time (seconds):")
    item_time_label.pack()
    item_time_entry = tk.Entry(root)
    item_time_entry.pack()

    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    instructions_label = tk.Label(root, text="Click START then place cursor to desire \n" +
                                  'location to perform clicking and hit ENTER')
    instructions_label.pack()

    loop_label = tk.Label(root, text="")
    loop_label.pack()

    button_frame = tk.Frame(root)
    button_frame.pack()

    start_button = tk.Button(button_frame, text="Start", command=start_clicker)
    start_button.pack(side="left", padx=5)

    stop_button = tk.Button(button_frame, text="Stop", command=stop_clicker)
    stop_button.pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()


