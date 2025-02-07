import tkinter as tk
from tkinter import ttk
from pcgsLookupFunction import PCGSRegistry, CoinInfo
from pathlib import Path
import pickle

class PCGSLookupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PCGS Coin Lookup")
        
        # Load the registry when the GUI starts
        self.registry = self.load_registry()
        
        # Create main frames
        self.number_frame = ttk.LabelFrame(root, text="Lookup by PCGS Number", padding="10")
        self.number_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        self.search_frame = ttk.LabelFrame(root, text="Search by Coin Details", padding="10")
        self.search_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.results_frame = ttk.LabelFrame(root, text="Results", padding="10")
        self.results_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")
        
        # Configure PCGS Number lookup
        self.setup_number_lookup()
        
        # Configure Search by Details
        self.setup_search_by_details()
        
        # Configure Results area
        self.setup_results_area()
        
        # Configure grid weights
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(1, weight=1)
        
        # Store full lists of values
        self.all_dates = sorted(set(coin.date for coin in self.registry.number_to_coin.values()))
        self.all_denoms = sorted(set(coin.denomination for coin in self.registry.number_to_coin.values()))
        self.all_varieties = sorted(set(coin.variety for coin in self.registry.number_to_coin.values() if coin.variety))
        self.all_designations = sorted(set(coin.designation for coin in self.registry.number_to_coin.values() if coin.designation))
    
    def load_registry(self):
        registry = PCGSRegistry()
        cache_path = Path(__file__).parent / 'pcgs_registry_cache.pkl'
        with open(cache_path, 'rb') as f:
            registry.number_to_coin, registry.coin_to_number, _ = pickle.load(f)
        return registry
    
    def setup_number_lookup(self):
        # PCGS Number entry
        ttk.Label(self.number_frame, text="PCGS#:").grid(row=0, column=0, padx=5)
        self.number_entry = ttk.Entry(self.number_frame, width=10)
        self.number_entry.grid(row=0, column=1, padx=5)
        ttk.Button(self.number_frame, text="Search", command=self.lookup_number).grid(row=0, column=2, padx=5)
    
    def setup_search_by_details(self):
        # Date entry and dropdown
        ttk.Label(self.search_frame, text="Date:").grid(row=0, column=0, padx=5, pady=2)
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(self.search_frame, textvariable=self.date_var)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Configure listbox with selection mode and colors
        self.date_listbox = tk.Listbox(
            self.search_frame, 
            height=10, 
            width=30,
            selectmode=tk.SINGLE,
            activestyle='none',  # Removes underline from active selection
            selectbackground='#0078D7',  # Modern blue selection color
            selectforeground='white'
        )
        self.date_listbox.grid(row=1, column=1, padx=5, pady=2)
        
        # Bind events for dynamic filtering
        self.date_var.trace_add('write', self.filter_dates)
        
        # Bind listbox selection
        self.date_listbox.bind('<<ListboxSelect>>', self.on_date_select)
        
        # Button frame for Search and Clear
        button_frame = ttk.Frame(self.search_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Search button
        ttk.Button(button_frame, text="Search", command=self.search_details).pack(side=tk.LEFT, padx=5)
        
        # Clear button
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
    
    def filter_dates(self, *args):
        """Filter dates based on search text and maintain highlighting"""
        search_text = self.date_var.get().lower()
        
        # Clear current listbox
        self.date_listbox.delete(0, tk.END)
        
        # Add only matching dates to listbox
        for date in self.all_dates:
            if not search_text or search_text in date.lower():
                self.date_listbox.insert(tk.END, date)
                # Find the index of this item
                idx = self.date_listbox.get(0, tk.END).index(date)
                self.date_listbox.itemconfig(idx, bg='white', fg='black')
    
    def on_date_select(self, event):
        """Handle date selection and automatically show results"""
        selection = self.date_listbox.curselection()
        if selection:
            # Get selected item
            selected_date = self.date_listbox.get(selection[0])
            
            # Configure all items back to default
            for i in range(self.date_listbox.size()):
                self.date_listbox.itemconfig(i, bg='white', fg='black')
            
            # Configure selected item with blue background
            self.date_listbox.itemconfig(selection[0], bg='#0078D7', fg='white')
            
            # Automatically perform search with the selected date
            matches = self.registry.search_coins(date=selected_date)
            
            # Clear previous results
            self.results_text.delete(1.0, tk.END)
            
            # Display results
            if matches:
                for pcgs_number, coin in matches:
                    self.results_text.insert(tk.END, f"PCGS# {pcgs_number}: {coin}\n")
            else:
                self.results_text.insert(tk.END, "No matches found.")
    
    def setup_results_area(self):
        # Results text area
        self.results_text = tk.Text(self.results_frame, width=40, height=20)
        self.results_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure results frame grid
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)
    
    def lookup_number(self):
        self.results_text.delete(1.0, tk.END)
        try:
            number = int(self.number_entry.get())
            coin = self.registry.get_coin_info(number)
            if coin:
                self.results_text.insert(tk.END, f"PCGS #{number}:\n{str(coin)}")
            else:
                self.results_text.insert(tk.END, f"No coin found for PCGS #{number}")
        except ValueError:
            self.results_text.insert(tk.END, "Please enter a valid PCGS number")
    
    def search_details(self):
        self.results_text.delete(1.0, tk.END)
        matches = self.registry.search_coins(date=self.date_var.get())
        
        if matches:
            self.results_text.insert(tk.END, f"Found {len(matches)} coins from {self.date_var.get()}:\n\n")
            for pcgs_number, coin in matches:
                self.results_text.insert(tk.END, f"PCGS #{pcgs_number}: {str(coin)}\n")
        else:
            self.results_text.insert(tk.END, f"No coins found from {self.date_var.get()}")

    def clear_fields(self):
        """Clear all input fields and results"""
        self.number_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
        self.date_listbox.selection_clear(0, tk.END)

def main():
    root = tk.Tk()
    app = PCGSLookupGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
