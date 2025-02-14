# import tkinter as tk
# from tkinter import messagebox
# import threading
# import time
# import random

# class BatteryExperimentApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Battery Additives Experiment UI") #Title of window
#         self.root.geometry("500x400") # size of window
#         self.root.config(bg="#f0f0f0")  # Light gray background

#         # Global Variables
#         self.iterations = 10
#         self.compounds = []  # List to store compounds
#         self.conductivity_value = tk.StringVar()
#         self.conductivity_value.set("0.00")
#         self.experiment_parameters = {"iterations": 10, "compounds": []}  # Global storage

#         # Title Label
#         self.title_label = tk.Label(root, text="Battery Additives Experiment UI",
#                                     font=("Helvetica", 18, "bold"),
#                                     bg="#f0f0f0", fg="#2C3E50")
#         self.title_label.pack(pady=20)

#         # Number of Iterations
#         self.iterations_frame = tk.Frame(root, bg="#f0f0f0")
#         self.iterations_frame.pack(pady=10)
#         self.iterations_label = tk.Label(self.iterations_frame, text="Number of Iterations:",
#                                          font=("Helvetica", 12), bg="#f0f0f0")
#         self.iterations_label.pack(side="left")
#         self.iterations_entry = tk.Entry(self.iterations_frame, font=("Helvetica", 12), width=10)
#         self.iterations_entry.insert(0, str(self.iterations))
#         self.iterations_entry.pack(side="left", padx=5)

#         # Compound Input Frame
#         self.compound_input_frame = tk.Frame(root, bg="#f0f0f0")
#         self.compound_input_frame.pack(pady=10)

#         self.compound_name_label = tk.Label(self.compound_input_frame, text="Compound Name:",
#                                             font=("Helvetica", 12), bg="#f0f0f0")
#         self.compound_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
#         self.compound_name_entry = tk.Entry(self.compound_input_frame, font=("Helvetica", 12), width=20)
#         self.compound_name_entry.grid(row=0, column=1, padx=5, pady=5)

#         self.compound_conc_label = tk.Label(self.compound_input_frame, text="Concentration (%):",
#                                             font=("Helvetica", 12), bg="#f0f0f0")
#         self.compound_conc_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
#         self.compound_conc_entry = tk.Entry(self.compound_input_frame, font=("Helvetica", 12), width=10)
#         self.compound_conc_entry.grid(row=1, column=1, padx=5, pady=5)

#         self.add_compound_button = tk.Button(self.compound_input_frame, text="Add Compound",
#                                              command=self.add_compound, font=("Helvetica", 12),
#                                              bg="#2ECC71", fg="white")
#         self.add_compound_button.grid(row=2, column=0, columnspan=2, pady=10)

#         # Compounds List
#         self.compounds_list_label = tk.Label(root, text="Compounds List:",
#                                              font=("Helvetica", 12, "bold"), bg="#f0f0f0")
#         self.compounds_list_label.pack(pady=5)
#         self.compounds_listbox = tk.Listbox(root, font=("Helvetica", 12), width=40)
#         self.compounds_listbox.pack(pady=5)

#         # Increase Concentrations by 10%
#         self.increase_button = tk.Button(root, text="Increase Concentrations by 10%",
#                                          command=self.increase_concentrations, font=("Helvetica", 12),
#                                          bg="#3498DB", fg="white")
#         self.increase_button.pack(pady=10)

#         # Conductivity Monitor (Placeholder)
#         self.conductivity_label = tk.Label(root, text="Conductivity: (Placeholder)",
#                                            font=("Helvetica", 14), bg="#f0f0f0")
#         self.conductivity_label.pack(pady=5)
#         self.conductivity_value_label = tk.Label(root, textvariable=self.conductivity_value,
#                                                  font=("Helvetica", 14), bg="#f0f0f0", fg="#E74C3C")
#         self.conductivity_value_label.pack(pady=5)

#         # Run Experiment Button
#         self.run_button = tk.Button(root, text="Run Experiment", command=self.run_experiment,
#                                     font=("Helvetica", 12), bg="#2ECC71", fg="white")
#         self.run_button.pack(pady=10)

#         # Print Parameters Button
#         self.print_button = tk.Button(root, text="Print Parameters", command=self.print_parameters,
#                                        font=("Helvetica", 12), bg="#F39C12", fg="white")
#         self.print_button.pack(pady=10)

#         # Start Real-Time Conductivity Updates
#         self.running = True
#         threading.Thread(target=self.update_conductivity, daemon=True).start()

#         # Handle window close
#         self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def add_compound(self):
#         name = self.compound_name_entry.get().strip()
#         conc = self.compound_conc_entry.get().strip()
#         if not name or not conc:
#             messagebox.showerror("Invalid Input", "Please enter both compound name and concentration.")
#             return
#         try:
#             conc = float(conc)
#             if conc < 0:
#                 raise ValueError
#             # Add to compounds list
#             compound = {'name': name, 'concentration': conc}
#             self.compounds.append(compound)
#             self.experiment_parameters["compounds"].append(compound)
#             # Update the listbox
#             self.update_compounds_listbox()
#             # Clear input fields
#             self.compound_name_entry.delete(0, tk.END)
#             self.compound_conc_entry.delete(0, tk.END)
#         except ValueError:
#             messagebox.showerror("Invalid Input", "Please enter a valid concentration (non-negative number).")

#     def update_compounds_listbox(self):
#         self.compounds_listbox.delete(0, tk.END)
#         for compound in self.compounds:
#             self.compounds_listbox.insert(tk.END, f"{compound['name']}: {compound['concentration']:.2f}%")

#     def increase_concentrations(self):
#         if not self.compounds:
#             messagebox.showinfo("No Compounds", "Please add compounds before increasing concentrations.")
#             return
#         for compound in self.compounds:
#             compound['concentration'] *= 1.10  # Increase by 10%
#         self.update_compounds_listbox()

#     def update_conductivity(self):
#         while self.running:
#             # Placeholder for conductivity simulation
#             conductivity = random.uniform(0, 100)
#             self.conductivity_value.set(f"{conductivity:.2f}")
#             time.sleep(1)  # Update every second

#     def run_experiment(self):
#         try:
#             self.iterations = int(self.iterations_entry.get())
#             if self.iterations < 1:
#                 raise ValueError
#             self.experiment_parameters["iterations"] = self.iterations
#             if not self.compounds:
#                 messagebox.showerror("No Compounds", "Please add at least one compound before running the experiment.")
#                 return
#             # Print to terminal
#             print(f"Running {self.iterations} iterations with the following compounds:")
#             for compound in self.compounds:
#                 print(f"{compound['name']}: {compound['concentration']:.2f}%")
#             messagebox.showinfo("Experiment Started", "Experiment parameters have been printed to the terminal.")
#         except ValueError:
#             messagebox.showerror("Invalid Input", "Please ensure iterations is a valid positive integer.")

#     def print_parameters(self):
#         print("Experiment Parameters:")
#         print(self.experiment_parameters)

#     def on_closing(self):
#         self.running = False
#         self.root.destroy()
        
# # Create and run the application
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = BatteryExperimentApp(root)
#     root.mainloop()

import tkinter as tk
from tkinter import messagebox
import threading
import time
import random

class BatteryExperimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battery Additives Experiment UI")  
        self.root.geometry("500x400")  
        self.root.config(bg="#f0f0f0")  

        # Create a Canvas and Scrollable Frame
        self.canvas = tk.Canvas(root, bg="#f0f0f0")
        self.scroll_frame = tk.Frame(self.canvas, bg="#f0f0f0")

        # Add Scrollbar
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Frame to hold all widgets
        self.inner_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Bind Mouse Wheel Scrolling
        self.root.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows/macOS
        self.root.bind("<Button-4>", lambda event: self.on_mouse_wheel(event, "up"))  # Linux scroll up
        self.root.bind("<Button-5>", lambda event: self.on_mouse_wheel(event, "down"))  # Linux scroll down
        
        # Global Variables
        self.iterations = 10
        self.compounds = []  
        self.conductivity_value = tk.StringVar()
        self.conductivity_value.set("0.00")
        self.experiment_parameters = {"iterations": 10, "compounds": []}  

        # Title Label
        tk.Label(self.inner_frame, text="Battery Additives Experiment UI",
                 font=("Helvetica", 18, "bold"),
                 bg="#f0f0f0", fg="#2C3E50").pack(pady=20)

        # Number of Iterations
        self.iterations_frame = tk.Frame(self.inner_frame, bg="#f0f0f0")
        self.iterations_frame.pack(pady=10)
        tk.Label(self.iterations_frame, text="Number of Iterations:",
                 font=("Helvetica", 12), bg="#f0f0f0").pack(side="left")
        self.iterations_entry = tk.Entry(self.iterations_frame, font=("Helvetica", 12), width=10)
        self.iterations_entry.insert(0, str(self.iterations))
        self.iterations_entry.pack(side="left", padx=5)

        # Compound Input Frame
        self.compound_input_frame = tk.Frame(self.inner_frame, bg="#f0f0f0")
        self.compound_input_frame.pack(pady=10)

        tk.Label(self.compound_input_frame, text="Compound Name:", font=("Helvetica", 12),
                 bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.compound_name_entry = tk.Entry(self.compound_input_frame, font=("Helvetica", 12), width=20)
        self.compound_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.compound_input_frame, text="Concentration (%):",
                 font=("Helvetica", 12), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.compound_conc_entry = tk.Entry(self.compound_input_frame, font=("Helvetica", 12), width=10)
        self.compound_conc_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.compound_input_frame, text="Add Compound",
                  command=self.add_compound, font=("Helvetica", 12),
                  bg="#2ECC71", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

        # Compounds List
        tk.Label(self.inner_frame, text="Compounds List:",
                 font=("Helvetica", 12, "bold"), bg="#f0f0f0").pack(pady=5)

        self.compounds_listbox = tk.Listbox(self.inner_frame, font=("Helvetica", 12), width=40, height=5)
        self.compounds_listbox.pack(pady=5)

        # Increase Concentrations
        tk.Button(self.inner_frame, text="Increase Concentrations by 10%",
                  command=self.increase_concentrations, font=("Helvetica", 12),
                  bg="#3498DB", fg="white").pack(pady=10)

        # Conductivity Monitor
        tk.Label(self.inner_frame, text="Conductivity: (Placeholder)",
                 font=("Helvetica", 14), bg="#f0f0f0").pack(pady=5)
        tk.Label(self.inner_frame, textvariable=self.conductivity_value,
                 font=("Helvetica", 14), bg="#f0f0f0", fg="#E74C3C").pack(pady=5)

        # Run Experiment Button
        tk.Button(self.inner_frame, text="Run Experiment", command=self.run_experiment,
                  font=("Helvetica", 12), bg="#2ECC71", fg="white").pack(pady=10)

        # Print Parameters Button
        tk.Button(self.inner_frame, text="Print Parameters", command=self.print_parameters,
                  font=("Helvetica", 12), bg="#F39C12", fg="white").pack(pady=10)

        # Start Conductivity Updates
        self.running = True
        threading.Thread(target=self.update_conductivity, daemon=True).start()

        # Update Scrollable Region
        self.inner_frame.bind("<Configure>", self.update_scroll_region)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_scroll_region(self, event=None):
        """ Update scrolling region when new elements are added. """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event, direction=None):
        """ Scroll the window using the mouse wheel. """
        if direction == "up":
            self.canvas.yview_scroll(-1, "units")
        elif direction == "down":
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def add_compound(self):
        name = self.compound_name_entry.get().strip()
        conc = self.compound_conc_entry.get().strip()
        if not name or not conc:
            messagebox.showerror("Invalid Input", "Please enter both compound name and concentration.")
            return
        try:
            conc = float(conc)
            if conc < 0:
                raise ValueError
            self.compounds.append({'name': name, 'concentration': conc})
            self.update_compounds_listbox()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid concentration.")

    def update_compounds_listbox(self):
        self.compounds_listbox.delete(0, tk.END)
        for compound in self.compounds:
            self.compounds_listbox.insert(tk.END, f"{compound['name']}: {compound['concentration']:.2f}%")

    def increase_concentrations(self):
        for compound in self.compounds:
            compound['concentration'] *= 1.10
        self.update_compounds_listbox()

    def update_conductivity(self):
        while self.running:
            self.conductivity_value.set(f"{random.uniform(0, 100):.2f}")
            time.sleep(1)

    def run_experiment(self):
        print("Running Experiment...")

    def print_parameters(self):
        print("Experiment Parameters:", self.compounds)

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BatteryExperimentApp(root)
    root.mainloop()
