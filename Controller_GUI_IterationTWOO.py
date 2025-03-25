import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random

# ------------------------------------------------------------------
# PYTHON CONTROLLER VARIABLES & PLACEHOLDERS (from your controller)
# ------------------------------------------------------------------
import math  # just in case we need it

# Ports, volumes, and placeholders
ARDUINO_PORT = "/dev/tty.usbserial-1110"
COND_METER_PORT = "COM15"
BAUD_RATE = 115200
TOTAL_VOLUME = 3.00  # ml

PORT_ELECTROLYTE_LP30 = 1
PORT_ADDITIVE_TEP = 2
PORT_ARGON_GAS = 3
PORT_ADDITIVE_X = 4
PORT_ADDITIVE_Y = 5

# Dictionary to store additives and their properties
# (Will be updated by the GUI selections)
additives = {
    "TEP": {
        "port": PORT_ADDITIVE_TEP,
        "used": False,
        "percentage": 0,
        "volume": 0.0
    },
    "ADDITIVE_X": {
        "port": PORT_ADDITIVE_X,
        "used": False,
        "percentage": 0,
        "volume": 0.0
    },
    "ADDITIVE_Y": {
        "port": PORT_ADDITIVE_Y,
        "used": False,
        "percentage": 0,
        "volume": 0.0
    },
    "LP30": {
        "port": PORT_ELECTROLYTE_LP30,
        "used": True,
        "percentage": 100,  # LP30 is always used by default
        "volume": 0.0
    },
}

# This dict is updated by the GUI to store user selections (like {"TEP": 50, "ADDITIVE_X": 30})
selected_additives_from_ui = {}

# For demonstration, we track the entire experiment list here
experiments = []

# ------------------------------------------------------------------
# GUI CLASS
# ------------------------------------------------------------------
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
        self.is_manual = False  # True if user submits Manual, False if Automatic
        self.selected_default_compound = tk.StringVar(value="Compound 1")
        self.total_additive_concentration = tk.StringVar(value="0.00")
        self.selected_compounds = []  # Shared list of added compounds

        # Additional variables
        self.conductivity_value = tk.StringVar(value="0.00")
        self.experiment_count = 0
        self.iterations = 10
        self.compounds = []  # Not used as heavily now, but retained

        # Keep a log of all experiments for console output
        self.experiments_log = []

        # Build the UIs
        self.create_manual_ui()
        self.create_automatic_ui()

    # ---------- Shared Helper Functions ----------
    def add_compound(self, compound, concentration):
        """Add a compound to the shared list and update both listboxes."""
        compound_entry = f"{compound}: {concentration:.2f}%"
        self.selected_compounds.append(compound_entry)
        if hasattr(self, 'manual_compounds_listbox'):
            self.manual_compounds_listbox.insert(tk.END, compound_entry)
        if hasattr(self, 'auto_compounds_listbox'):
            self.auto_compounds_listbox.insert(tk.END, compound_entry)

    def clear_compounds_list(self):
        """Clear the shared compounds list and both listboxes."""
        self.selected_compounds.clear()
        if hasattr(self, 'manual_compounds_listbox'):
            self.manual_compounds_listbox.delete(0, tk.END)
        if hasattr(self, 'auto_compounds_listbox'):
            self.auto_compounds_listbox.delete(0, tk.END)
        messagebox.showinfo("Cleared", "Compounds list has been cleared for both tabs.")

    # ---------- Manual Tab UI ----------
    def create_manual_ui(self):
        """Creates the UI for the manual experiment mode."""
        self.form_container = tk.Frame(self.manual_frame, bg="#2C3E50")
        self.form_container.pack(fill="both", expand=True)
        
        for col in range(4):
            self.form_container.columnconfigure(col, weight=1)

        self.title_label = tk.Label(
            self.form_container,
            text="Battery Additives Experiment UI (Manual Mode)",
            font=("Helvetica", 18, "bold"),
            bg="#2C3E50", fg="#ECF0F1"
        )
        self.title_label.grid(row=0, column=0, columnspan=4, pady=10)

        label_iterations = tk.Label(
            self.form_container, text="Number of Iterations:", 
            font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1"
        )
        label_iterations.grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.iterations_entry = tk.Entry(
            self.form_container, font=("Helvetica", 14), width=15, 
            bg="#3B4B5C", fg="#ECF0F1", insertbackground="#ECF0F1"
        )
        self.iterations_entry.insert(0, str(self.iterations))
        self.iterations_entry.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        label_default_compound = tk.Label(
            self.form_container, text="Select Default Compound:", 
            font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1"
        )
        label_default_compound.grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self.default_compounds = ["Compound 1", "Compound 2", "Compound 3"]
        self.default_compound_menu = ttk.Combobox(
            self.form_container, textvariable=self.selected_default_compound, 
            values=self.default_compounds, font=("Helvetica", 14), 
            state="readonly", width=17
        )
        self.default_compound_menu.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        label_concentration = tk.Label(
            self.form_container, text="Concentration (%):", 
            font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1"
        )
        label_concentration.grid(row=3, column=1, sticky="e", padx=5, pady=5)
        self.concentration_entry = tk.Entry(
            self.form_container, font=("Helvetica", 14), width=15, 
            bg="#3B4B5C", fg="#ECF0F1", insertbackground="#ECF0F1"
        )
        self.concentration_entry.grid(row=3, column=2, sticky="w", padx=5, pady=5)

        label_total_concentration = tk.Label(
            self.form_container,
            text="Total Additive Concentration (%):",
            font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1"
        )
        label_total_concentration.grid(row=4, column=1, sticky="e", padx=5, pady=5)
        self.total_additive_concentration_entry = tk.Entry(
            self.form_container, font=("Helvetica", 14), width=15,
            bg="#3B4B5C", fg="#ECF0F1", insertbackground="#ECF0F1",
            textvariable=self.total_additive_concentration
        )
        self.total_additive_concentration_entry.grid(row=4, column=2, sticky="w", padx=5, pady=5)

        self.add_compound_button_manual = tk.Button(
            self.form_container, text="Add Selected Compound", 
            font=("Helvetica", 12), bg="#3498DB", fg="#FFFFFF",
            command=self.add_selected_compound_manual
        )
        self.add_compound_button_manual.grid(row=5, column=1, columnspan=2, pady=5)

        self.run_button = tk.Button(
            self.form_container, text="Run Experiment", 
            command=self.run_experiment, font=("Helvetica", 12, "bold"), 
            bg="#2ECC71", fg="#FFFFFF", height=1
        )
        self.run_button.grid(row=6, column=1, columnspan=2, pady=5)

        compounds_label = tk.Label(
            self.form_container, text="Compounds List:", 
            font=("Helvetica", 12, "bold"), bg="#2C3E50", fg="#ECF0F1"
        )
        compounds_label.grid(row=7, column=1, columnspan=2, pady=5)
        self.manual_compounds_listbox = tk.Listbox(
            self.form_container, font=("Helvetica", 12), width=40, height=5, 
            bg="#3B4B5C", fg="#ECF0F1"
        )
        self.manual_compounds_listbox.grid(row=8, column=1, columnspan=2, pady=5)

        self.clear_compounds_button_manual = tk.Button(
            self.form_container, text="Clear Compounds List",
            font=("Helvetica", 12), bg="#E74C3C", fg="#FFFFFF",
            command=self.clear_compounds_list
        )
        self.clear_compounds_button_manual.grid(row=9, column=1, columnspan=2, pady=5)

        self.submit_manual_button = tk.Button(
            self.form_container, text="Submit (Manual)",
            font=("Helvetica", 12, "bold"), bg="#9B59B6", fg="#FFFFFF",
            command=self.set_manual_true
        )
        self.submit_manual_button.grid(row=10, column=1, columnspan=2, pady=5)

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
        auto_container = tk.Frame(self.automatic_frame, bg="#2C3E50")
        auto_container.pack(fill="both", expand=True)
        
        for col in range(4):
            auto_container.columnconfigure(col, weight=1)

        title_auto = tk.Label(
            auto_container, text="Automatic Experiment Mode", 
            font=("Helvetica", 18, "bold"), bg="#2C3E50", fg="#ECF0F1"
        )
        title_auto.grid(row=0, column=0, columnspan=4, pady=10)
        
        label_auto_compound = tk.Label(
            auto_container, text="Select Default Compound:",
            font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1"
        )
        label_auto_compound.grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.auto_compound_menu = ttk.Combobox(
            auto_container, textvariable=self.selected_default_compound,
            values=["Compound 1", "Compound 2", "Compound 3"],
            font=("Helvetica", 14), state="readonly", width=17
        )
        self.auto_compound_menu.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        label_auto_total = tk.Label(
            auto_container, text="Total Additive Concentration (%):",
            font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1"
        )
        label_auto_total.grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self.auto_total_additive_entry = tk.Entry(
            auto_container, textvariable=self.total_additive_concentration,
            font=("Helvetica", 14), width=15,
            bg="#3B4B5C", fg="#ECF0F1", insertbackground="#ECF0F1"
        )
        self.auto_total_additive_entry.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        self.add_compound_button_auto = tk.Button(
            auto_container, text="Add Selected Compound",
            font=("Helvetica", 12), bg="#3498DB", fg="#FFFFFF",
            command=self.add_selected_compound_auto
        )
        self.add_compound_button_auto.grid(row=3, column=1, columnspan=2, pady=5)

        auto_compounds_label = tk.Label(
            auto_container, text="Compounds List:",
            font=("Helvetica", 12, "bold"), bg="#2C3E50", fg="#ECF0F1"
        )
        auto_compounds_label.grid(row=4, column=1, columnspan=2, pady=5)
        self.auto_compounds_listbox = tk.Listbox(
            auto_container, font=("Helvetica", 12), width=40, height=5,
            bg="#3B4B5C", fg="#ECF0F1"
        )
        self.auto_compounds_listbox.grid(row=5, column=1, columnspan=2, pady=5)

        self.clear_compounds_button_auto = tk.Button(
            auto_container, text="Clear Compounds List",
            font=("Helvetica", 12), bg="#E74C3C", fg="#FFFFFF",
            command=self.clear_compounds_list
        )
        self.clear_compounds_button_auto.grid(row=6, column=1, columnspan=2, pady=5)
        
        self.submit_automatic_button = tk.Button(
            auto_container, text="Submit (Automatic)",
            font=("Helvetica", 12, "bold"), bg="#9B59B6", fg="#FFFFFF",
            command=self.set_manual_false
        )
        self.submit_automatic_button.grid(row=7, column=1, columnspan=2, pady=5)

    def add_selected_compound_auto(self):
        """Adds the compound with a default concentration of 0.0 (for automatic mode)."""
        compound = self.selected_default_compound.get()
        concentration = 0.0
        self.add_compound(compound, concentration)
        messagebox.showinfo("Success", f"Added {compound} with {concentration:.2f}% concentration.")

    def set_manual_false(self):
        """Sets is_manual to False and shows a confirmation message."""
        if not self.total_additive_concentration.get().strip():
            self.total_additive_concentration.set("0.00")
        self.is_manual = False
        messagebox.showinfo("Mode Set", "Mode set to Automatic (is_manual = False)")

    # ---------- Run Experiment & Integration with "Controller" ----------
    def run_experiment(self):
        """
        Runs the experiment, checks manual constraints, logs the experiment,
        and prints a combined output: immediate summary + full log.
        
        Also updates the 'additives' dictionary from your controller snippet
        with the user’s selected compounds.
        """
        self.experiment_count += 1
        try:
            self.iterations = int(self.iterations_entry.get())
            if self.iterations < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please ensure iterations is a valid positive integer.")
            return

        mode_str = "Manual" if self.is_manual else "Automatic"

        # Prepare variables for manual checks
        total_add_pct = 0.0
        total_compound_pct = 0.0

        # MANUAL MODE CHECKS
        if self.is_manual:
            try:
                total_add_pct = float(self.total_additive_concentration.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Total Additive Concentration must be a valid number.")
                return

            # Sum up the individual compound percentages
            for item in self.selected_compounds:
                try:
                    parts = item.split(":")
                    if len(parts) == 2:
                        pct = float(parts[1].strip().replace("%", ""))
                        total_compound_pct += pct
                except:
                    continue

            # If sum of compounds > user-entered total
            if total_compound_pct > total_add_pct + 1e-9:
                proceed_exceed = messagebox.askyesno(
                    "Compounds Exceed Entered Total",
                    f"The sum of your selected compounds is {total_compound_pct:.2f}%, "
                    f"which exceeds the total additive concentration you entered ({total_add_pct:.2f}%).\n\n"
                    "It is recommended to clear or correct your compound list before proceeding.\n"
                    "Do you want to continue anyway?"
                )
                if not proceed_exceed:
                    return

            # If total_add_pct != 10, ask
            if abs(total_add_pct - 10.0) > 0.001:
                proceed_total = messagebox.askyesno(
                    "Confirm Total Concentration",
                    f"You entered {total_add_pct:.2f}% as the total additive concentration.\n"
                    "The recommended value is 10%.\nDo you want to proceed?"
                )
                if not proceed_total:
                    return

            # If sum of compounds != 10, ask
            if abs(total_compound_pct - 10.0) > 0.01:
                proceed_compounds = messagebox.askyesno(
                    "Confirm Compound Percentages",
                    f"The sum of individual compound percentages is {total_compound_pct:.2f}%.\n"
                    "It is suggested to have a total of 10%.\nDo you want to proceed?"
                )
                if not proceed_compounds:
                    return

        # PRINT AN IMMEDIATE SUMMARY
        print(f"\n=== Running Experiment #{self.experiment_count} ({mode_str} Mode) ===")
        print(f"Number of Iterations: {self.iterations}")
        print("Compounds selected:")
        for c in self.selected_compounds:
            print(f"  - {c}")
        print(f"Total Additive Concentration (overall): {self.total_additive_concentration.get()}%")

        # Simulate measuring conductivity
        for i in range(self.iterations):
            conductivity = random.uniform(0, 100)
            self.conductivity_value.set(f"{conductivity:.2f}")
            self.root.update()
            time.sleep(0.5)

        # --------------------------------------------------------------------
        # INTEGRATE WITH YOUR "CONTROLLER" ADDITIVES DICTIONARY
        # (like your snippet, but simplified for demonstration)
        # --------------------------------------------------------------------
        # 1) Clear out old values
        for ad in additives:
            additives[ad]["used"] = False
            additives[ad]["percentage"] = 0
            additives[ad]["volume"] = 0.0

        # 2) Convert self.selected_compounds into a dictionary, e.g. {"TEP": 30, ...}
        #    We need a mapping from "Compound 1" -> "TEP", etc. Adjust as needed.
        selected_additives_from_ui.clear()
        for item in self.selected_compounds:
            try:
                name, val = item.split(":")
                name = name.strip()                 # "Compound 1"
                val = float(val.strip().replace("%", ""))  # e.g. 3.0
            except:
                continue
            # Simple mapping for demonstration
            # "Compound 1" -> "TEP", "Compound 2" -> "ADDITIVE_X", "Compound 3" -> "ADDITIVE_Y"
            if name == "Compound 1":
                additive_key = "TEP"
            elif name == "Compound 2":
                additive_key = "ADDITIVE_X"
            elif name == "Compound 3":
                additive_key = "ADDITIVE_Y"
            else:
                additive_key = name.upper().replace(" ", "_")

            selected_additives_from_ui[additive_key] = val

        # 3) Mark these additives as used
        for additive_key, percentage in selected_additives_from_ui.items():
            if additive_key in additives:
                additives[additive_key]["used"] = True
                additives[additive_key]["percentage"] = percentage

        # LP30 is always used, filling leftover if you want
        try:
            user_total = float(self.total_additive_concentration.get())
        except:
            user_total = 0.0
        leftover_lp30 = 100 - user_total
        if leftover_lp30 < 0:
            leftover_lp30 = 0
        additives["LP30"]["used"] = True
        additives["LP30"]["percentage"] = leftover_lp30

        # 4) Compute volumes (example)
        for k, v in additives.items():
            if v["used"]:
                v["volume"] = (v["percentage"] / 100) * TOTAL_VOLUME

        # Print final "additives" dictionary
        print("[Controller] Final 'additives' dictionary after integration:")
        for k, v in additives.items():
            if v["used"]:
                print(f"  {k}: port={v['port']}, used={v['used']}, "
                      f"percentage={v['percentage']}, volume={v['volume']:.2f} ml")
        # --------------------------------------------------------------------

        # CREATE A LOG ENTRY FOR THIS EXPERIMENT
        # parse each compound from self.selected_compounds into a dict
        additives_dict = {}
        for item in self.selected_compounds:
            try:
                cname, val = item.split(":")
                cname = cname.strip()
                val = float(val.strip().replace("%", ""))
                additives_dict[cname] = val
            except:
                continue

        exp_data = {
            "experiment_number": self.experiment_count,
            "mode": mode_str,
            "iterations": self.iterations,
            "gui_compounds": self.selected_compounds.copy(),
            "parsed_compounds": additives_dict,
            "controller_additives": {  # from the actual 'additives' dictionary
                k: dict(v) for k, v in additives.items() if v["used"]
            }
        }
        self.experiments_log.append(exp_data)

        # PRINT EXPERIMENTS LOG SO FAR
        print("\n[Experiments Log] So far:")
        for e in self.experiments_log:
            print(f"  Experiment #{e['experiment_number']} ({e['mode']}) -> Iterations: {e['iterations']}")
            print(f"    GUI compounds: {e['gui_compounds']}")
            print(f"    Parsed (GUI -> dict): {e['parsed_compounds']}")
            print("    Controller 'additives' used:")
            for add_name, add_vals in e["controller_additives"].items():
                print(f"      {add_name}: {add_vals}")
        print("=== End of this experiment's summary ===\n")

    def fade_in_step(self, alpha):
        if alpha < 1.0:
            alpha += 0.05
            self.root.attributes("-alpha", alpha)
            self.root.after(50, lambda: self.fade_in_step(alpha))
        else:
            self.root.attributes("-alpha", 1.0)

    def on_closing(self):
        self.root.destroy()

# --- MAIN APP ENTRY POINT ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BatteryExperimentApp(root)
    root.mainloop()
