<<<<<<< HEAD
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
from datetime import datetime
from tkinter import filedialog
class SecurityProjectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Security System")
        self.root.geometry("800x700")
        self.root.configure(bg="#e8f5e9")
        
        # Data storage
        self.car_data = {}
        self.current_range = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        title_label = tk.Label(self.root, text="Car Security System", 
        font=("Helvetica", 24, "bold"), bg="#e8f5e9", fg="#2e7d32")
        title_label.pack(pady=20)
        
        description = ("This project is designed to enhance the attendance of cars coming into the church and out. "
        "It includes features such as car detection, license plate recognition, and logging of entry and exit times.")
        desc_label = tk.Label(self.root, text=description, font=("Helvetica", 14), 
                    bg="#e8f5e9", fg="#388e3c", wraplength=700, justify="center")
        desc_label.pack(pady=10)

        button_style = {
            "font": ("Helvetica", 16),
            "bg": "#4caf50",  # Green background
            "fg": "white",    # White text
            "activebackground": "#388e3c",  # Darker green when clicked
            "activeforeground": "white",
            "relief": "raised",
            "border": 5,
            "padx": 10,
            "pady": 5
        } 
        
        start_button = tk.Button(self.root, text="Start Security System", 
                                font=("Helvetica", 16), command=self.start_security_system)
        start_button.pack(pady=20)
        
        settings_button = tk.Button(self.root, text="Settings", 
                        font=("Helvetica", 16), command=self.open_settings)
        settings_button.pack(pady=10)
        
        view_data_button = tk.Button(self.root, text="View Car Data", 
                                    font=("Helvetica", 16), command=self.view_car_data)
        view_data_button.pack(pady=10)
        
        exit_car_button = tk.Button(self.root, text="Exit Car", 
                                    font=("Helvetica", 16),bg="#ff9800", fg="white", activebackground="#f57c00", activeforeground="white", relief="raised", border=5, padx=10, pady=5, command=self.exit_car)
        exit_car_button.pack(pady=10)
        save_button = tk.Button(self.root, text="Save Data to File",
                                    font= ("Helvetica", 16), command=self.save_to_file)
        save_button.pack(pady=10)
        
        exit_button = tk.Button(self.root, text="Exit", 
                    font=("Helvetica", 16), command=self.root.quit)
        exit_button.pack(pady=10)
        
    def select_date(self):
        date_str = simpledialog.askstring("Input", "Enter the date (YYYY-MM-DD):", parent=self.root)
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return selected_date
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid date format. Please enter in YYYY-MM-DD format.")
            return None
    
    def start_security_system(self):
        messagebox.showinfo("Start", "Security system starting...")
        self.select_car_range()
    
    def select_car_range(self):
        self.select_date()
        ranges = ["1-40", "1-50", "1-60", "1-70", "1-80", "1-90", 
                "1-100", "1-110", "1-120", "1-130", "1-140", 
                "1-150", "1-160", "1-170", "1-180", "1-190", "1-200"]
        
        range_window = tk.Toplevel(self.root)
        range_window.title("Select Car Range")
        range_window.geometry("300x400")
        
        tk.Label(range_window, text="Select expected number of cars:", 
                font=("Helvetica", 12)).pack(pady=10)
        
        for range_str in ranges:
            tk.Button(range_window, text=range_str, font=("Helvetica", 11),
            command=lambda r=range_str: self.input_license_plates(r, range_window)).pack(pady=2)
    
    def input_license_plates(self, car_range, parent_window):
        parent_window.destroy()
        self.current_range = car_range
        self.car_data[car_range] = {}
        
        # Get the range boundaries
        min_cars, max_cars = map(int, car_range.split('-'))
        
        # Create input window
        input_window = tk.Toplevel(self.root)
        input_window.title(f"Input License Plates - {car_range} cars for {datetime.now().date()}")
        input_window.geometry("600x500")
        
        # Create scrollable frame
        frame = tk.Frame(input_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create input fields
        entries = []
        for i in range(min_cars, max_cars + 1):
            row_frame = tk.Frame(scrollable_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(row_frame, text=f"Car {i}:", width=10).pack(side=tk.LEFT)
            entry = tk.Entry(row_frame, width=20)
            entry.pack(side=tk.LEFT, padx=5)
            entries.append(entry)
        
        def save_data():
            for i, entry in enumerate(entries):
                car_num = min_cars + i
                plate = entry.get().strip()
                if plate:
                    self.car_data[self.current_range][f"car_{car_num}"] = {
                        "plate": plate,
                        "entry_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "exit_time": None
                    }
            
            messagebox.showinfo("Success", f"License plates for {car_range} cars on {datetime.now().date()} saved!")
            input_window.destroy()
            self.show_summary()
        
        tk.Button(scrollable_frame, text="Save All", command=save_data, 
            font=("Helvetica", 12), bg="green", fg="white").pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_summary(self):
        summary_window = tk.Toplevel(self.root)
        summary_window.title(f"Data Summary for {datetime.now().date()}. ")
        summary_window.geometry("500x400")
        
        tk.Label(summary_window, text=f"Data for {self.current_range} cars on {datetime.now().date()}. ", 
                font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Display saved data
        text_widget = tk.Text(summary_window, height=15, width=60)
        text_widget.pack(padx=10, pady=10)
        
        data = self.car_data.get(self.current_range, {})
        for car_id, info in data.items():
            text_widget.insert(tk.END, f"{car_id}: {info['plate']} - Entry: {info['entry_time']}\n")
    
    def view_car_data(self):
        if not self.car_data:
            messagebox.showinfo("Info", "No car data available yet.")
            return
        
        data_window = tk.Toplevel(self.root)
        data_window.title("All Car Data")
        data_window.geometry("600x500")
        
        notebook = ttk.Notebook(data_window)
        
        for range_str, cars in self.car_data.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=range_str)
            
            text_widget = tk.Text(frame, height=20, width=70)
            scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            for car_id, info in cars.items():
                text_widget.insert(tk.END, 
                                f"{car_id}: {info['plate']}\n"
                                f"   Entry: {info['entry_time']}\n"
                                f"   Exit: {info.get('exit_time', 'Not recorded')}\n\n")
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        notebook.pack(expand=1, fill="both", padx=10, pady=10)
    
    def open_settings(self):
        messagebox.showinfo("Settings", "Settings feature would go here")
    
    def save_to_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.car_data, f, indent=2)
            messagebox.showinfo("Success", f"Data saved to {filename}")
    
    def exit_car(self):
        if not self.car_data:
            messagebox.showinfo("Info", "No car data available yet.")
            return
        
        # Create window for exiting cars
        exit_window = tk.Toplevel(self.root)
        exit_window.title("Exit Car")
        exit_window.geometry("500x400")
        
        tk.Label(exit_window, text="Select a car to exit:", 
                font=("Helvetica", 14, "bold")).pack(pady=10)
        
        # Create frame for car selection
        selection_frame = tk.Frame(exit_window)
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Get all available cars that haven't exited yet
        available_cars = []
        for range_str, cars in self.car_data.items():
            for car_id, car_info in cars.items():
                if car_info.get('exit_time') is None:  # Only show cars that haven't exited
                    available_cars.append((range_str, car_id, car_info))
        
        if not available_cars:
            tk.Label(selection_frame, text="No cars currently in the system.", 
                    font=("Helvetica", 12)).pack(pady=20)
            return
        
        # Create listbox to display available cars
        listbox = tk.Listbox(selection_frame, height=15, font=("Helvetica", 11))
        listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = tk.Scrollbar(selection_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        # Populate listbox with available cars
        for range_str, car_id, car_info in available_cars:
            display_text = f"{range_str} - {car_id}: {car_info['plate']} (Entered: {car_info['entry_time']})"
            listbox.insert(tk.END, display_text)
        
        def process_exit():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a car to exit.")
                return
            
            selected_index = selection[0]
            range_str, car_id, car_info = available_cars[selected_index]
            
            # Record exit time
            self.car_data[range_str][car_id]['exit_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Option to completely remove from system
            result = messagebox.askyesno("Exit Car", 
                    f"Car {car_id} ({car_info['plate']}) has been marked as exited.\n\n"
                    "Do you want to completely remove this car from the system?")
            
            if result:
                del self.car_data[range_str][car_id]
                messagebox.showinfo("Success", f"Car {car_id} has been completely removed from the system.")
            else:
                messagebox.showinfo("Success", f"Car {car_id} has been marked as exited.")
            
            exit_window.destroy()
        
        # Exit button
        exit_button = tk.Button(exit_window, text="Mark as Exited", 
                        font=("Helvetica", 12), command=process_exit,
                        bg="orange", fg="white")
        exit_button.pack(pady=10)        
    
    
# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityProjectApp(root)
=======
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
from datetime import datetime
from tkinter import filedialog
class SecurityProjectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Security System")
        self.root.geometry("800x700")
        self.root.configure(bg="#e8f5e9")
        
        # Data storage
        self.car_data = {}
        self.current_range = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        title_label = tk.Label(self.root, text="Car Security System", 
        font=("Helvetica", 24, "bold"), bg="#e8f5e9", fg="#2e7d32")
        title_label.pack(pady=20)
        
        description = ("This project is designed to enhance the attendance of cars coming into the church and out. "
        "It includes features such as car detection, license plate recognition, and logging of entry and exit times.")
        desc_label = tk.Label(self.root, text=description, font=("Helvetica", 14), 
                    bg="#e8f5e9", fg="#388e3c", wraplength=700, justify="center")
        desc_label.pack(pady=10)

        button_style = {
            "font": ("Helvetica", 16),
            "bg": "#4caf50",  # Green background
            "fg": "white",    # White text
            "activebackground": "#388e3c",  # Darker green when clicked
            "activeforeground": "white",
            "relief": "raised",
            "border": 5,
            "padx": 10,
            "pady": 5
        } 
        
        start_button = tk.Button(self.root, text="Start Security System", 
                                font=("Helvetica", 16), command=self.start_security_system)
        start_button.pack(pady=20)
        
        settings_button = tk.Button(self.root, text="Settings", 
                        font=("Helvetica", 16), command=self.open_settings)
        settings_button.pack(pady=10)
        
        view_data_button = tk.Button(self.root, text="View Car Data", 
                                    font=("Helvetica", 16), command=self.view_car_data)
        view_data_button.pack(pady=10)
        
        exit_car_button = tk.Button(self.root, text="Exit Car", 
                                    font=("Helvetica", 16),bg="#ff9800", fg="white", activebackground="#f57c00", activeforeground="white", relief="raised", border=5, padx=10, pady=5, command=self.exit_car)
        exit_car_button.pack(pady=10)
        save_button = tk.Button(self.root, text="Save Data to File",
                                    font= ("Helvetica", 16), command=self.save_to_file)
        save_button.pack(pady=10)
        
        exit_button = tk.Button(self.root, text="Exit", 
                    font=("Helvetica", 16), command=self.root.quit)
        exit_button.pack(pady=10)
        
    def select_date(self):
        date_str = simpledialog.askstring("Input", "Enter the date (YYYY-MM-DD):", parent=self.root)
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return selected_date
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid date format. Please enter in YYYY-MM-DD format.")
            return None
    
    def start_security_system(self):
        messagebox.showinfo("Start", "Security system starting...")
        self.select_car_range()
    
    def select_car_range(self):
        self.select_date()
        ranges = ["1-40", "1-50", "1-60", "1-70", "1-80", "1-90", 
                "1-100", "1-110", "1-120", "1-130", "1-140", 
                "1-150", "1-160", "1-170", "1-180", "1-190", "1-200"]
        
        range_window = tk.Toplevel(self.root)
        range_window.title("Select Car Range")
        range_window.geometry("300x400")
        
        tk.Label(range_window, text="Select expected number of cars:", 
                font=("Helvetica", 12)).pack(pady=10)
        
        for range_str in ranges:
            tk.Button(range_window, text=range_str, font=("Helvetica", 11),
            command=lambda r=range_str: self.input_license_plates(r, range_window)).pack(pady=2)
    
    def input_license_plates(self, car_range, parent_window):
        parent_window.destroy()
        self.current_range = car_range
        self.car_data[car_range] = {}
        
        # Get the range boundaries
        min_cars, max_cars = map(int, car_range.split('-'))
        
        # Create input window
        input_window = tk.Toplevel(self.root)
        input_window.title(f"Input License Plates - {car_range} cars for {datetime.now().date()}")
        input_window.geometry("600x500")
        
        # Create scrollable frame
        frame = tk.Frame(input_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create input fields
        entries = []
        for i in range(min_cars, max_cars + 1):
            row_frame = tk.Frame(scrollable_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(row_frame, text=f"Car {i}:", width=10).pack(side=tk.LEFT)
            entry = tk.Entry(row_frame, width=20)
            entry.pack(side=tk.LEFT, padx=5)
            entries.append(entry)
        
        def save_data():
            for i, entry in enumerate(entries):
                car_num = min_cars + i
                plate = entry.get().strip()
                if plate:
                    self.car_data[self.current_range][f"car_{car_num}"] = {
                        "plate": plate,
                        "entry_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "exit_time": None
                    }
            
            messagebox.showinfo("Success", f"License plates for {car_range} cars on {datetime.now().date()} saved!")
            input_window.destroy()
            self.show_summary()
        
        tk.Button(scrollable_frame, text="Save All", command=save_data, 
            font=("Helvetica", 12), bg="green", fg="white").pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_summary(self):
        summary_window = tk.Toplevel(self.root)
        summary_window.title(f"Data Summary for {datetime.now().date()}. ")
        summary_window.geometry("500x400")
        
        tk.Label(summary_window, text=f"Data for {self.current_range} cars on {datetime.now().date()}. ", 
                font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Display saved data
        text_widget = tk.Text(summary_window, height=15, width=60)
        text_widget.pack(padx=10, pady=10)
        
        data = self.car_data.get(self.current_range, {})
        for car_id, info in data.items():
            text_widget.insert(tk.END, f"{car_id}: {info['plate']} - Entry: {info['entry_time']}\n")
    
    def view_car_data(self):
        if not self.car_data:
            messagebox.showinfo("Info", "No car data available yet.")
            return
        
        data_window = tk.Toplevel(self.root)
        data_window.title("All Car Data")
        data_window.geometry("600x500")
        
        notebook = ttk.Notebook(data_window)
        
        for range_str, cars in self.car_data.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=range_str)
            
            text_widget = tk.Text(frame, height=20, width=70)
            scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            for car_id, info in cars.items():
                text_widget.insert(tk.END, 
                                f"{car_id}: {info['plate']}\n"
                                f"   Entry: {info['entry_time']}\n"
                                f"   Exit: {info.get('exit_time', 'Not recorded')}\n\n")
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        notebook.pack(expand=1, fill="both", padx=10, pady=10)
    
    def open_settings(self):
        messagebox.showinfo("Settings", "Settings feature would go here")
    
    def save_to_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.car_data, f, indent=2)
            messagebox.showinfo("Success", f"Data saved to {filename}")
    
    def exit_car(self):
        if not self.car_data:
            messagebox.showinfo("Info", "No car data available yet.")
            return
        
        # Create window for exiting cars
        exit_window = tk.Toplevel(self.root)
        exit_window.title("Exit Car")
        exit_window.geometry("500x400")
        
        tk.Label(exit_window, text="Select a car to exit:", 
                font=("Helvetica", 14, "bold")).pack(pady=10)
        
        # Create frame for car selection
        selection_frame = tk.Frame(exit_window)
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Get all available cars that haven't exited yet
        available_cars = []
        for range_str, cars in self.car_data.items():
            for car_id, car_info in cars.items():
                if car_info.get('exit_time') is None:  # Only show cars that haven't exited
                    available_cars.append((range_str, car_id, car_info))
        
        if not available_cars:
            tk.Label(selection_frame, text="No cars currently in the system.", 
                    font=("Helvetica", 12)).pack(pady=20)
            return
        
        # Create listbox to display available cars
        listbox = tk.Listbox(selection_frame, height=15, font=("Helvetica", 11))
        listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = tk.Scrollbar(selection_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        # Populate listbox with available cars
        for range_str, car_id, car_info in available_cars:
            display_text = f"{range_str} - {car_id}: {car_info['plate']} (Entered: {car_info['entry_time']})"
            listbox.insert(tk.END, display_text)
        
        def process_exit():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a car to exit.")
                return
            
            selected_index = selection[0]
            range_str, car_id, car_info = available_cars[selected_index]
            
            # Record exit time
            self.car_data[range_str][car_id]['exit_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Option to completely remove from system
            result = messagebox.askyesno("Exit Car", 
                    f"Car {car_id} ({car_info['plate']}) has been marked as exited.\n\n"
                    "Do you want to completely remove this car from the system?")
            
            if result:
                del self.car_data[range_str][car_id]
                messagebox.showinfo("Success", f"Car {car_id} has been completely removed from the system.")
            else:
                messagebox.showinfo("Success", f"Car {car_id} has been marked as exited.")
            
            exit_window.destroy()
        
        # Exit button
        exit_button = tk.Button(exit_window, text="Mark as Exited", 
                        font=("Helvetica", 12), command=process_exit,
                        bg="orange", fg="white")
        exit_button.pack(pady=10)        
    
    
# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityProjectApp(root)
>>>>>>> 1dae6cd9d3586bf883c1d53ee9504f430cb8eb67
    root.mainloop()