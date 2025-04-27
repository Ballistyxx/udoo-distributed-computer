import tkinter as tk
from tkinter import Menu, Toplevel, Frame, BOTH, YES, filedialog, messagebox
import os
import subprocess
import threading

def openssh(worker_ip):
    termf = Toplevel(root)
    termf.geometry("800x600")
    termf.title(f"SSH - {worker_ip}")
    termf_frame = Frame(termf, height=800, width=600)
    termf_frame.pack(fill=BOTH, expand=YES)
    wid = termf_frame.winfo_id()
    os.system(f'xterm -into {wid} -geometry 90x48 +si -sl 1000 -sb -e "ssh {worker_ip}" &')

def fetch_temp_and_cpu(name, ip, results):
    try:
        temp = subprocess.check_output(['ssh', ip, 'cat /sys/class/thermal/thermal_zone0/temp'])
        temp_celsius = int(temp) / 1000
        cpu_usage = subprocess.check_output(['ssh', ip, "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'"])
        result = f"{name} ({ip}): {temp_celsius:.2f}°C, CPU: {cpu_usage.decode('utf-8').strip()}%\n"
    except subprocess.CalledProcessError as e:
        #result = f"Failed to get temp/cpu from {name} ({ip}): {e}\n"
        result = f"{name} ({ip}): Offline\n"

    results.append((name, result))

def update_thermal_info():
    def update_thread():
        threads = []
        results = []
        for name, ip in workers:
            thread = threading.Thread(target=fetch_temp_and_cpu, args=(name, ip, results))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        results.sort(key=lambda x: x[0])  # Sort results by worker name
        thermal_info_text.delete(1.0, tk.END)
        for _, result in results:
            thermal_info_text.insert(tk.END, result)
    
    threading.Thread(target=update_thread).start()

def auto_update():
    if auto_refresh.get():
        update_thermal_info()
        root.after(5000, auto_update)

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        def upload_to_worker(name, ip):
            try:
                subprocess.run(['scp', file_path, f'{ip}:~/'], check=True)
                print("Success", f"File sent to {name} ({ip})")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to send file to {name} ({ip}): {e}")

        def upload_files_thread():
            threads = []
            for name, ip in workers[1:]:
                thread = threading.Thread(target=upload_to_worker, args=(name, ip))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
            
            # Re-enable the UI after upload is complete
            root.config(cursor="")
            upload_button_cmd.config(state=tk.NORMAL)
        
        # Disable the UI during upload
        #root.config(cursor="wait")
        upload_button_cmd.config(state=tk.DISABLED)
        threading.Thread(target=upload_files_thread).start()

def send_command():
    command = command_entry.get()
    if command:
        def execute_on_worker(name, ip):
            try:
                output = subprocess.check_output(['ssh', ip, command], stderr=subprocess.STDOUT)
                print(f"Output from {name} ({ip}): {output.decode('utf-8')}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to run command on {name} ({ip}): {e.output.decode('utf-8')}")

        threads = []
        for name, ip in workers[1:]:
            thread = threading.Thread(target=execute_on_worker, args=(name, ip))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

root = tk.Tk()
root.geometry("800x750")
root.title("Cluster Management")

# Menu bar setup
menubar = Menu(root)
menubar.add_command(label="Exit", command=root.quit)

sshmenu = Menu(menubar, tearoff=0)
workers = [("master", "127.0.0.1"), ("worker01", "169.254.193.49"), ("worker02", "169.254.227.2"), ("worker03", "169.254.31.206"),
           ("worker04", "169.254.65.41"), ("worker05", "169.254.116.252"), ("worker06", "169.254.99.59"),
           ("worker07", "169.254.239.88"), ("worker08", "169.254.133.134"), ("worker09", "169.254.22.237"),
           ("worker10", "169.254.45.241"), ("worker11", "169.254.245.86"), ("worker12", "169.254.210.57")]

for name, ip in workers:
    sshmenu.add_command(label=f"{name} ({ip})", command=lambda ip=ip: openssh(ip))

menubar.add_cascade(label="SSH", menu=sshmenu)
root.config(menu=menubar)

# Thermal information section
thermal_frame = Frame(root)
thermal_frame.place(x=0, y=0, width=400, height=600)

thermal_label = tk.Label(thermal_frame, text="Cluster Information:") #used to be 'Thermal Information'
thermal_label.pack(anchor=tk.NW, padx=5, pady=5)

thermal_info_text = tk.Text(thermal_frame, height=28)
thermal_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Button to update thermal information
update_button = tk.Button(thermal_frame, text="Update", command=update_thermal_info)
update_button.pack(pady=5)

# Checkbox for automatic refreshing
auto_refresh = tk.BooleanVar()
auto_refresh_checkbutton = tk.Checkbutton(thermal_frame, text="Auto Refresh (5s)", variable=auto_refresh, command=auto_update)
auto_refresh_checkbutton.pack(pady=5)

# Embedded terminal
cmd_terminal = Frame(root, height=550, width=400)
cmd_terminal.place(x=400, y=0, width=400, height=550)
root.update_idletasks()  # Ensure the frame is fully created before getting its ID
wid = cmd_terminal.winfo_id()
os.system(f'xterm -into {wid} -geometry 90x48 +si -sl 1000 -sb &')

# File upload and command section for terminal side
cmd_upload_frame = Frame(root)
cmd_upload_frame.place(x=400, y=550, width=400, height=200)

upload_label_cmd = tk.Label(cmd_upload_frame, text="Upload File:")
upload_label_cmd.pack(side=tk.TOP, padx=5, pady=5)

upload_button_cmd = tk.Button(cmd_upload_frame, text="Browse", command=upload_file)
upload_button_cmd.pack(side=tk.TOP, padx=5, pady=5)

# Command entry and button
command_entry = tk.Entry(cmd_upload_frame)
command_entry.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X, expand=False)

command_button = tk.Button(cmd_upload_frame, text="Send Command to All", command=send_command)
command_button.pack(side=tk.TOP, padx=5, pady=5)

root.mainloop()
