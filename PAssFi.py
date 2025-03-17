import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# Function to show the password for the selected network
def show_password():
    selected_network = network_list.get() # Get the selected network from the dropdown menu
    if selected_network:
        try:
            # Retrieve the password for the selected network
            password_output = subprocess.check_output(["netsh", "wlan", "show", "profile", selected_network, "key=clear"]).decode("utf-8")
            password_lines = [l.strip() for l in password_output.split("\n")]
            password_line = [l for l in password_lines if "Key Content" in l][0]
            password = password_line.split(":")[1].strip()
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to retrieve password. Make sure you are connected to the selected network.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Get the list of Wi-Fi networks
networks = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8").split("\n")
network_names = [n.split(":")[1].strip() for n in networks if "All User Profile" in n]

# Create a Tkinter window and a dropdown menu
window = tk.Tk()
window.title("Wi-Fi Password Viewer")
window.configure(background="#222222")

network_frame = ttk.Frame(window)
network_frame.pack(padx=10, pady=(20, 10))

network_label = ttk.Label(network_frame, text="Select a network:", font=("Arial", 12, "bold"), foreground="#00ff00", background="#222222")
network_label.pack(side=tk.LEFT)

network_list = ttk.Combobox(network_frame, values=network_names, font=("Arial", 12), state="readonly")
network_list.pack(side=tk.LEFT, padx=5)

password_frame = ttk.Frame(window)
password_frame.pack(padx=10, pady=10)

password_label = ttk.Label(password_frame, text="Password:", font=("Arial", 12, "bold"), foreground="#00ff00", background="#222222")
password_label.pack(side=tk.LEFT)

password_entry = ttk.Entry(password_frame, show="", font=("Arial", 12), width=25)
password_entry.pack(side=tk.LEFT, padx=5)

button_frame = ttk.Frame(window)
button_frame.pack(padx=10, pady=(10, 20))

password_button = ttk.Button(button_frame, text="Show Password", command=show_password, style="my.TButton")
password_button.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(button_frame, mode="indeterminate")
progress_bar.pack(side=tk.LEFT, padx=5)

# Define custom styles for the widgets
style = ttk.Style(window)
style.configure("TFrame", background="#222222")
style.configure("TLabel", foreground="#00ff00", background="#222222")
style.configure("TButton", foreground="#00ff00", background="#333333", font=("Arial", 12, "bold"), width=15)

# Start the Tkinter event loop
window.mainloop()
