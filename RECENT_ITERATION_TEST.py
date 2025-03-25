import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random

# --- Global Variables ---
global_compounds = []  # Truly global list of compounds

class BatteryExperimentApp:
    def __init__(self, root):
        """Initialize the main application window and layout."""
        self.root = root
        self.root.title("Battery Additives Experiment UI")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Fade in the window from 0% to 100% opacity
        self.root.attributes("-alpha", 0.0)
        self.root.after(50, lambda: self.fade_in_step(0.0))
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Outer frame that fills the entire window
        self.main_frame = tk.Frame(self.root, bg="#2C3E50")
        self.main_frame.pack(fill="both", expand=True)

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True)

        # Manual Tab
        self.manual_frame = tk.Frame(self.notebook, bg="#2C3E50")
        self.notebook.add(self.manual_frame, text="Manual")
        
        # Automatic Tab
        self.automatic_frame = tk.Frame(self.notebook, bg="#2C3E50")
        self.notebook.add(self.automatic_frame, text="Automatic")

        # --- Shared Variables ---
        self.is_manual = False  # Will be True if user submits Manual, False if Automatic
        self.selected_default_compound = tk.StringVar(value="Compound 1")
        self.total_additive_concentration = tk.StringVar(value="0.00")
        self.selected_compounds = []  # Shared list of added compounds

        # Other variables
        self.conductivity_value = tk.StringVar(value="0.00")
        self.experiment_count = 0
        self.iterations = 10
        self.compounds = global_compounds  # still global

        # Build the UIs
        self.create_manual_ui()
        self.create_automatic_ui()

    # ---------- Shared Helper Functions ----------
    def add_compound(self, compound, concentration):
        """Helper to add a compound to the shared list and update both listboxes."""
        compound_entry = f"{compound}: {concentration:.2f}%"
        self.selected_compounds.append(compound_entry)
        if hasattr(self, 'manual_compounds_listbox'):
            self.manual_compounds_listbox.insert(tk.END, compound_entry)
        if hasattr(self, 'auto_compounds_listbox'):
            self.auto_compounds_listbox.insert(tk.END, compound_entry)

    def clear_compounds_list(self):
        """Clears the shared compounds list and both listboxes."""
        self.selected_compounds.clear()
        if hasattr(self, 'manual_compounds_listbox'):
            self.manual_compounds_listbox.delete(0, tk.END)
        if hasattr(self, 'auto_compounds_listbox'):
            self.auto_compounds_listbox.delete(0, tk.END)
        messagebox.showinfo("Cleared", "Compounds list has been cleared for both tabs.")

    # ---------- Manual Tab UI ----------
    def create_manual_ui(self):
        """Creates the UI for the manual experiment mode."""
        # A container that expands and uses a grid for centered alignment
        self.form_container = tk.Frame(self.manual_frame, bg="#2C3E50")
        self.form_container.pack(fill="both", expand=True)
        
        # Configure 4 columns for symmetry (columns 0 and 3 are margins)
        for col in range(4):
            self.form_container.columnconfigure(col, weight=1)

        # Row 0: Title Label (spans all 4 columns)
        self.title_label = tk.Label(
            self.form_container,
            text="Battery Additives Experiment UI (Manual Mode)",
            font=("Helvetica", 18, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        self.title_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Row 1: Number of Iterations
        label_iterations = tk.Label(
            self.form_container, 
            text="Number of Iterations:", 
            font=("Helvetica", 14), 
            bg="#2C3E50", 
            fg="#ECF0F1"
        )
        label_iterations.grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.iterations_entry = tk.Entry(
            self.form_container, 
            font=("Helvetica", 14), 
            width=15, 
            bg="#3B4B5C", fg="#ECF0F1", 
            insertbackground="#ECF0F1"
        )
        self.iterations_entry.insert(0, str(self.iterations))
        self.iterations_entry.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        # Row 2: Select Default Compound
        label_default_compound = tk.Label(
            self.form_container, 
            text="Select Default Compound:", 
            font=("Helvetica", 14), 
            bg="#2C3E50", fg="#ECF0F1"
        )
        label_default_compound.grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self.default_compounds = ["Compound 1", "Compound 2", "Compound 3"]
        self.default_compound_menu = ttk.Combobox(
            self.form_container, 
            textvariable=self.selected_default_compound, 
            values=self.default_compounds, 
            font=("Helvetica", 14), 
            state="readonly", width=17
        )
        self.default_compound_menu.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        # Row 3: Concentration (%)
        label_concentration = tk.Label(
            self.form_container, 
            text="Concentration (%):", 
            font=("Helvetica", 14), 
            bg="#2C3E50", fg="#ECF0F1"
        )
        label_concentration.grid(row=3, column=1, sticky="e", padx=5, pady=5)
        self.concentration_entry = tk.Entry(
            self.form_container, 
            font=("Helvetica", 14), width=15, 
            bg="#3B4B5C", fg="#ECF0F1", 
            insertbackground="#ECF0F1"
        )
        self.concentration_entry.grid(row=3, column=2, sticky="w", padx=5, pady=5)

        # Row 4: Total Additive Concentration
        label_total_concentration = tk.Label(
            self.form_container,
            text="Total Additive Concentration (%):",
            font=("Helvetica", 14),
            bg="#2C3E50", fg="#ECF0F1"
        )
        label_total_concentration.grid(row=4, column=1, sticky="e", padx=5, pady=5)
        self.total_additive_concentration_entry = tk.Entry(
            self.form_container,
            font=("Helvetica", 14), width=15,
            bg="#3B4B5C", fg="#ECF0F1",
            insertbackground="#ECF0F1",
            textvariable=self.total_additive_concentration
        )
        self.total_additive_concentration_entry.grid(row=4, column=2, sticky="w", padx=5, pady=5)

        # Row 5: Add Selected Compound button (Manual)
        self.add_compound_button_manual = tk.Button(
            self.form_container, 
            text="Add Selected Compound", 
            font=("Helvetica", 12), 
            bg="#3498DB", fg="#FFFFFF",
            command=self.add_selected_compound_manual
        )
        self.add_compound_button_manual.grid(row=5, column=1, columnspan=2, pady=5)

        # Row 6: Run Experiment button
        self.run_button = tk.Button(
            self.form_container, 
            text="Run Experiment", 
            command=self.run_experiment, 
            font=("Helvetica", 12, "bold"), 
            bg="#2ECC71", fg="#FFFFFF", height=1
        )
        self.run_button.grid(row=6, column=1, columnspan=2, pady=5)

        # Row 7: Compounds List Label
        compounds_label = tk.Label(
            self.form_container, 
            text="Compounds List:", 
            font=("Helvetica", 12, "bold"), 
            bg="#2C3E50", fg="#ECF0F1"
        )
        compounds_label.grid(row=7, column=1, columnspan=2, pady=5)
        # Row 8: Compounds Listbox (Manual)
        self.manual_compounds_listbox = tk.Listbox(
            self.form_container, 
            font=("Helvetica", 12), width=40, height=5, 
            bg="#3B4B5C", fg="#ECF0F1"
        )
        self.manual_compounds_listbox.grid(row=8, column=1, columnspan=2, pady=5)
        # Row 9: Clear Compounds List button (Manual)
        self.clear_compounds_button_manual = tk.Button(
            self.form_container,
            text="Clear Compounds List",
            font=("Helvetica", 12),
            bg="#E74C3C", fg="#FFFFFF",
            command=self.clear_compounds_list
        )
        self.clear_compounds_button_manual.grid(row=9, column=1, columnspan=2, pady=5)
        # Row 10: Submit (Manual) button moved to the bottom
        self.submit_manual_button = tk.Button(
            self.form_container,
            text="Submit (Manual)",
            font=("Helvetica", 12, "bold"),
            bg="#9B59B6", fg="#FFFFFF",
            command=self.set_manual_true
        )
        self.submit_manual_button.grid(row=10, column=1, columnspan=2, pady=5)

        # The conductivity placeholder UI remains commented out.
        # -----------------------------------
        # # Row 11: Conductivity Label
        # self.conductivity_label = tk.Label(
        #     self.form_container, 
        #     text="Conductivity: (Placeholder)", 
        #     font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1"
        # )
        # self.conductivity_label.grid(row=11, column=1, columnspan=2, pady=5)
        #
        # # Row 12: Conductivity Value
        # self.conductivity_value_label = tk.Label(
        #     self.form_container, 
        #     textvariable=self.conductivity_value, 
        #     font=("Helvetica", 14), bg="#2C3E50", fg="#E74C3C"
        # )
        # self.conductivity_value_label.grid(row=12, column=1, columnspan=2, pady=5)

    def add_selected_compound_manual(self):
        """Reads the concentration from the manual tab and adds the compound."""
        compound = self.selected_default_compound.get()
        conc_str = self.concentration_entry.get()
        if not conc_str:
            messagebox.showerror("Invalid Input", "Please enter a concentration for the compound.")
            return
        try:
            concentration = float(conc_str)
            if concentration < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Concentration must be a valid non-negative number.")
            return
        self.add_compound(compound, concentration)
        self.concentration_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Added {compound} with {concentration:.2f}% concentration.")

    def set_manual_true(self):
        """Sets is_manual to True and shows a confirmation message."""
        self.is_manual = True
        messagebox.showinfo("Mode Set", "Mode set to Manual (is_manual = True)")

    # ---------- Automatic Tab UI ----------
    def create_automatic_ui(self):
        """Creates the UI for the automatic experiment mode."""
        # A container that expands and uses a grid for centered alignment
        auto_container = tk.Frame(self.automatic_frame, bg="#2C3E50")
        auto_container.pack(fill="both", expand=True)
        
        # Configure 4 columns for symmetry
        for col in range(4):
            auto_container.columnconfigure(col, weight=1)

        # Row 0: Title (spans all 4 columns)
        title_auto = tk.Label(
            auto_container, 
            text="Automatic Experiment Mode", 
            font=("Helvetica", 18, "bold"), 
            bg="#2C3E50", fg="#ECF0F1"
        )
        title_auto.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Row 1: Select Default Compound
        label_auto_compound = tk.Label(
            auto_container,
            text="Select Default Compound:",
            font=("Helvetica", 14),
            bg="#2C3E50", fg="#ECF0F1"
        )
        label_auto_compound.grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.auto_compound_menu = ttk.Combobox(
            auto_container,
            textvariable=self.selected_default_compound,  # shared variable
            values=["Compound 1", "Compound 2", "Compound 3"],
            font=("Helvetica", 14),
            state="readonly", width=17
        )
        self.auto_compound_menu.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        # Row 2: Total Additive Concentration
        label_auto_total = tk.Label(
            auto_container,
            text="Total Additive Concentration (%):",
            font=("Helvetica", 14),
            bg="#2C3E50", fg="#ECF0F1"
        )
        label_auto_total.grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self.auto_total_additive_entry = tk.Entry(
            auto_container,
            textvariable=self.total_additive_concentration,
            font=("Helvetica", 14), width=15,
            bg="#3B4B5C", fg="#ECF0F1", insertbackground="#ECF0F1"
        )
        self.auto_total_additive_entry.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        # Row 3: Add Selected Compound button (Automatic)
        self.add_compound_button_auto = tk.Button(
            auto_container,
            text="Add Selected Compound",
            font=("Helvetica", 12),
            bg="#3498DB", fg="#FFFFFF",
            command=self.add_selected_compound_auto
        )
        self.add_compound_button_auto.grid(row=3, column=1, columnspan=2, pady=5)

        # Row 4: Compounds List Label
        auto_compounds_label = tk.Label(
            auto_container,
            text="Compounds List:",
            font=("Helvetica", 12, "bold"),
            bg="#2C3E50", fg="#ECF0F1"
        )
        auto_compounds_label.grid(row=4, column=1, columnspan=2, pady=5)
        # Row 5: Compounds Listbox (Automatic)
        self.auto_compounds_listbox = tk.Listbox(
            auto_container,
            font=("Helvetica", 12), width=40, height=5,
            bg="#3B4B5C", fg="#ECF0F1"
        )
        self.auto_compounds_listbox.grid(row=5, column=1, columnspan=2, pady=5)

        # Row 6: Clear Compounds List button (Automatic)
        self.clear_compounds_button_auto = tk.Button(
            auto_container,
            text="Clear Compounds List",
            font=("Helvetica", 12),
            bg="#E74C3C", fg="#FFFFFF",
            command=self.clear_compounds_list
        )
        self.clear_compounds_button_auto.grid(row=6, column=1, columnspan=2, pady=5)
        # Row 7: Submit (Automatic) button moved to the bottom
        self.submit_automatic_button = tk.Button(
            auto_container,
            text="Submit (Automatic)",
            font=("Helvetica", 12, "bold"),
            bg="#9B59B6", fg="#FFFFFF",
            command=self.set_manual_false
        )
        self.submit_automatic_button.grid(row=7, column=1, columnspan=2, pady=5)

    def add_selected_compound_auto(self):
        """Adds the compound with a default concentration of 0.0 (for automatic mode)."""
        compound = self.selected_default_compound.get()
        concentration = 0.0  # default concentration in automatic mode
        self.add_compound(compound, concentration)
        messagebox.showinfo("Success", f"Added {compound} with {concentration:.2f}% concentration.")

    def set_manual_false(self):
        """Sets is_manual to False and shows a confirmation message."""
        # If total concentration is blank, default to "0.00"
        if not self.total_additive_concentration.get().strip():
            self.total_additive_concentration.set("0.00")
        self.is_manual = False
        messagebox.showinfo("Mode Set", "Mode set to Automatic (is_manual = False)")

    # ---------- Run Experiment and Misc Functions ----------
    def run_experiment(self):
        """Runs the manual experiment with user-defined parameters."""
        self.experiment_count += 1
        try:
            self.iterations = int(self.iterations_entry.get())
            if self.iterations < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please ensure iterations is a valid positive integer.")
            return

        print(f"Running Experiment #{self.experiment_count} with {self.iterations} iterations.")
        print(f"Mode: {'Manual' if self.is_manual else 'Automatic'}")
        print(f"Selected Compound: {self.selected_default_compound.get()}")
        print(f"Total Additive Concentration: {self.total_additive_concentration.get()}%")

        # Simulate measuring conductivity (updates the hidden variable)
        for i in range(self.iterations):
            conductivity = random.uniform(0, 100)
            self.conductivity_value.set(f"{conductivity:.2f}")
            self.root.update()
            time.sleep(0.5)

    def fade_in_step(self, alpha):
        if alpha < 1.0:
            alpha += 0.05
            self.root.attributes("-alpha", alpha)
            self.root.after(50, lambda: self.fade_in_step(alpha))
        else:
            self.root.attributes("-alpha", 1.0)

    def on_closing(self):
        self.root.destroy()

# --- Main App Entry Point ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BatteryExperimentApp(root)
    root.mainloop()
