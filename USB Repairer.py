import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import getpass
import subprocess

class App:
    def __init__(self):
        self.x_pos = 500
        self.main = tk.Tk()
        self.main.title("USB Repairer")
        self.main.geometry("500x400")

        self.open_img = Image.open("C:/Users/Joseph/Pictures/usb_.jpg")
        self.open_win2img = Image.open("C:/Users/Joseph/Pictures/usb_.jpg")

        self.resize_img = self.open_img.resize((355,175))
        self.resize_win2img = self.open_win2img.resize((355,175))

        self.convert_img = ImageTk.PhotoImage(self.resize_img)
        self.convert_win2img = ImageTk.PhotoImage(self.resize_win2img)

        self.var = tk.IntVar()
        self.progress_value = 0

        self.repair_steps = [
            "Accessing drive...",
            "Scanning drive for suspicious files...",
            "Deleting suspicious files...",
            "Running filesystem check (fsck)...",
            "Finalizing repair...",
            "Done: USB successfully repaired!"
        ]

        self.frame1 = tk.Frame(self.main)
        self.frame2 = tk.Frame(self.main)

        for frame in (self.frame1, self.frame2):
            frame.place(relwidth=1, relheight=1)

        self.window_1()
        self.window2()
        self.switch_win(self.frame1)

        self.main.mainloop()

    def window_1(self):
        image = tk.Label(self.frame1, image=self.convert_img)
        image.place(x=120, y=205)

        welcome_txt = tk.Label(self.frame1, text = "WELCOME TO JAYTEC'S UNIVERSIAL SERIAL BUS \n "
                                                   "DRIVE REPAIRING(USB Stick) SERVICES", font=("Comic Sans", 14, "bold"),
                               fg="dark green")
        welcome_txt.pack(pady=3)

        term_heading = tk.Label(self.frame1, text = "      Terms And Conditions", font=("Arial", 12, "bold"))
        term_heading.pack()

        terms_condition = tk.Label(self.frame1, text = "This application is intended for lawful and ethical use only.\n"
        "JayTec is not responsible for any damage, data loss, or misuse of this software.\n"
        "The user assumes full responsibility for any action taken using this app.\n"
        "This tool is provided 'as-is' without warranties or guarantees.\n"
        "It is strongly recommended to back up your USB data before repair.\n"
    )
        terms_condition.pack()

        agree_or_disagree = tk.Checkbutton(self.frame1, text = "I agreed to the Terms And Conditions",
                                           font=("Arial", 10, "bold"), variable=self.var)
        agree_or_disagree.place(x=110, y=160)

        next_button = tk.Button(self.frame1, text = "Next", command = self.validate_next)
        next_button.pack(pady=5)

        exit_App = tk.Button(self.frame1, text = "Exit App", command = self.close_App)
        exit_App.place(x=30, y=350)

    def validate_next(self):
        if self.var.get() == 1:
            self.switch_win(self.frame2)
            self.move_text()
        else:
            messagebox.showerror("Error", "Please Validate the Terms And Condition")

    def window2(self):
        wel_txt = tk.Label(self.frame2, text = "WELCOME AGAIN USER!", font=("Comic Sans", 14, "bold"), fg = "dark green")
        wel_txt.pack(pady = 10)

        back_button = tk.Button(self.frame2, text= " Back", command= lambda: self.switch_win(self.frame1))
        back_button.place(x=20, y=20)

        self.scrolling_txt = tk.Label(self.frame2, text = "For one in one Developer discussion, Please contact the following number: "
                                                     "+23279174763", fg = "dark green", font=("Arial", 10, "bold"))
        self.scrolling_txt.place(x=500, y=50)

        self.drive_name = ttk.Combobox(self.frame2, values=self.detect_usb_drives(), state="readonly")
        self.drive_name.pack(pady=10)
        self.drive_name.set("Select USB Drive")

        refresh_button = tk.Button(self.frame2, text="Refresh Drives", command=lambda: self.drive_name.config(values=self.detect_usb_drives()))
        refresh_button.pack(pady=5)

        self.progreaa_bar = ttk.Progressbar(self.frame2, length=200, mode="determinate", maximum=100)
        self.progreaa_bar.pack(pady=10)

        self.progress_label = tk.Label(self.frame2, text="Progress: 0%", font=("Arial", 10))
        self.progress_label.pack()

        self.progress_detail_label = tk.Label(self.frame2, text="", font=("Arial", 10, "italic"), fg="darkblue")
        self.progress_detail_label.pack()

        self.start_button = tk.Button(self.frame2, text = "Start Repairing", command=self.start_repair)
        self.start_button.pack(pady=5)

        image = tk.Label(self.frame2, image=self.convert_win2img)
        image.pack(pady=5)

    def detect_usb_drives(self):
        username = getpass.getuser()
        usb_root = f"/media/{username}/"
        if os.path.exists(usb_root):
            # Return only mounted directories
            return [os.path.join(usb_root, d) for d in os.listdir(usb_root) if os.path.ismount(os.path.join(usb_root, d))]
        return []

    def get_device_from_mount(self, mount_point):
        # Uses 'df' command to get device path from mount point
        try:
            output = subprocess.check_output(['df', mount_point]).decode()
            lines = output.strip().split('\n')
            if len(lines) > 1:
                device = lines[1].split()[0]
                return device
        except Exception as e:
            print("Error getting device from mount:", e)
        return None

    def start_repair(self):
        selected_path = self.drive_name.get()
        if not os.path.ismount(selected_path):
            messagebox.showerror("Invalid Path", "The selected path is not a valid mounted USB drive.")
            return

        self.usb_path = selected_path
        self.device_path = self.get_device_from_mount(selected_path)
        if not self.device_path:
            messagebox.showerror("Error", "Could not find device for the selected mount point.")
            return

        self.progress_value = 0
        self.progreaa_bar["value"] = 0
        self.progress_label.config(text="Progress: 0%")
        self.progress_detail_label.config(text="")
        self.suspicious_files = []
        self.step_index = 0
        self.start_button.config(state="disabled")

        self.increment_progress()

    def increment_progress(self):
        if self.progress_value == 0:
            self.progress_detail_label.config(text=self.repair_steps[0])
            self.progress_value += 10
            self.progreaa_bar["value"] = self.progress_value
            self.progress_label.config(text=f"Progress: {self.progress_value}%")
            # Delay next step a bit
            self.main.after(800, self.increment_progress)

        elif self.progress_value == 10:
            self.progress_detail_label.config(text=self.repair_steps[1])
            # Scan drive for suspicious files
            self.scan_for_suspicious_files()
            self.progress_value += 20
            self.progreaa_bar["value"] = self.progress_value
            self.progress_label.config(text=f"Progress: {self.progress_value}%")
            self.main.after(800, self.increment_progress)

        elif self.progress_value == 30:
            self.progress_detail_label.config(text=self.repair_steps[2])
            # Delete suspicious files found
            self.delete_suspicious_files()
            self.progress_value += 20
            self.progreaa_bar["value"] = self.progress_value
            self.progress_label.config(text=f"Progress: {self.progress_value}%")
            self.main.after(800, self.increment_progress)

        elif self.progress_value == 50:
            self.progress_detail_label.config(text=self.repair_steps[3])
            # Run filesystem check (fsck)
            self.run_fsck()
            self.progress_value += 30
            self.progreaa_bar["value"] = self.progress_value
            self.progress_label.config(text=f"Progress: {self.progress_value}%")
            self.main.after(1500, self.increment_progress)

        elif self.progress_value == 80:
            self.progress_detail_label.config(text=self.repair_steps[4])
            self.progress_value += 20
            self.progreaa_bar["value"] = self.progress_value
            self.progress_label.config(text=f"Progress: {self.progress_value}%")
            self.main.after(800, self.increment_progress)

        elif self.progress_value >= 100:
            self.progress_detail_label.config(text=self.repair_steps[-1])
            messagebox.showinfo("Repair Complete", "USB Repair/Scan Completed Successfully!")
            self.start_button.config(state="normal")

    def scan_for_suspicious_files(self):
        self.suspicious_files = []
        suspicious_patterns = ['autorun.inf', '.lnk', '.exe', '.vbs', '.bat']
        for root, dirs, files in os.walk(self.usb_path):
            for file in files:
                for pattern in suspicious_patterns:
                    if file.lower().endswith(pattern) or file.lower() == pattern:
                        full_path = os.path.join(root, file)
                        self.suspicious_files.append(full_path)

    def delete_suspicious_files(self):
        for file_path in self.suspicious_files:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

    def run_fsck(self):
        if not self.device_path:
            return
        # Run fsck non-interactive (-y) on the device
        try:
            # Note: This requires sudo privileges!
            result = subprocess.run(['sudo', 'fsck', '-y', self.device_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("fsck output:", result.stdout)
            if result.returncode == 0:
                print("Filesystem check and repair completed successfully.")
            else:
                print("Filesystem check completed with errors or warnings.")
        except Exception as e:
            print("Error running fsck:", e)

    def move_text(self):
        self.x_pos -= 1
        self.scrolling_txt.place(x=self.x_pos, y=50)

        if self.x_pos + self.scrolling_txt.winfo_width() < 0:
            self.x_pos = 500
        self.main.after(20, self.move_text)

    def switch_win(self, frame):
        frame.tkraise()

    def close_App(self):
        confirm_exit = messagebox.askyesno("Confirm Exiting", "Are you sure to Exit Application?")
        if confirm_exit:
            self.main.destroy()

App()
