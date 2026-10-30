import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import difflib
from core.hasher import Hasher

class MainWindow(tk.Frame):
    def __init__(self, parent, engine, db_manager):
        super().__init__(parent)
        self.parent = parent
        self.engine = engine
        self.db = db_manager
        
        self.target_dir = tk.StringVar()
        self.pack(fill="both", expand=True)
        self.setup_ui()

    def setup_ui(self):
        # 1. Top Section: Target Environment Configuration
        top_frame = ttk.LabelFrame(self, text=" Target Environment Configuration ", padding=10)
        top_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(top_frame, text="Target Path (File/Folder):").pack(side="left", padx=5)
        ttk.Entry(top_frame, textvariable=self.target_dir, width=60).pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(top_frame, text="Browse...", command=self.browse_directory).pack(side="left", padx=5)
        
        # 2. Control Action Buttons
        btn_frame = ttk.Frame(self, padding=5)
        btn_frame.pack(fill="x", padx=15, pady=5)
        
        ttk.Button(btn_frame, text="🛡️ Generate Baseline Matrix", command=self.run_baseline).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔍 Execute Integrity Verification Check", command=self.run_verification).pack(side="left", padx=5)

        # 3. Bottom Section: Split Workspace Panel
        workspace_frame = ttk.Frame(self)
        workspace_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # --- Left Panel: System Integrity Audit Log ---
        left_panel = ttk.LabelFrame(workspace_frame, text=" System Integrity Audit Log ", padding=10)
        left_panel.pack(side="left", fill="both", expand=True) 
        
        columns = ("filepath", "status")
        self.tree = ttk.Treeview(left_panel, columns=columns, show="headings")
        self.tree.heading("filepath", text="Monitored File Path")
        self.tree.heading("status", text="Integrity Status State")
        
        self.tree.column("filepath", width=250, anchor="w")
        self.tree.column("status", width=120, anchor="center")
        
        # Color Styling Configurations for alerts
        self.tree.tag_configure("Modified", background="#ffcccc", foreground="#990000")
        self.tree.tag_configure("Created", background="#d4edda", foreground="#155724")
        self.tree.tag_configure("Deleted", background="#fff3cd", foreground="#856404")
        self.tree.tag_configure("Unchanged", background="#ffffff", foreground="#333333")
        
        # Bind row selection to instantly load the diff view dynamically
        self.tree.bind("<<TreeviewSelect>>", self.handle_row_selection)
        
        left_scroll = ttk.Scrollbar(left_panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=left_scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        left_scroll.pack(side="right", fill="y")

        # --- Right Panel: Forensic Line-by-Line Diff Engine View ---
        right_panel = ttk.LabelFrame(workspace_frame, text=" Forensic Line-by-Line Diff Engine View ", padding=10)
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.diff_box = tk.Text(right_panel, wrap="none", font=("Courier", 10), bg="#ffffff")
        
        # UI Formatting Text Tags
        self.diff_box.tag_configure("addition", foreground="green")
        self.diff_box.tag_configure("deletion", foreground="red")
        self.diff_box.tag_configure("header", foreground="blue", font=("Courier", 10, "bold"))
        
        right_scroll_y = ttk.Scrollbar(right_panel, orient="vertical", command=self.diff_box.yview)
        right_scroll_x = ttk.Scrollbar(right_panel, orient="horizontal", command=self.diff_box.xview)
        self.diff_box.configure(yscrollcommand=right_scroll_y.set, xscrollcommand=right_scroll_x.set)
        
        # Packs elements inside the right panel frame container correctly
        right_scroll_x.pack(side="bottom", fill="x")
        self.diff_box.pack(side="left", fill="both", expand=True)
        right_scroll_y.pack(side="right", fill="y")
        
        # Initial instructional text inside the diff screen
        self.update_diff_view_text("Select a modified record from the left panel to review file transformations.")

    def browse_directory(self):
        # Ask the user what type of resource they want to monitor
        choice = messagebox.askyesnocancel(
            "Select Scan Type", 
            "Would you like to monitor an entire FOLDER?\n\n(Click 'Yes' for Folder, 'No' for a Single File)"
        )
        
        if choice is True:
            # User selected Folder monitoring
            directory = filedialog.askdirectory(title="Select Target Folder to Monitor")
            if directory:
                self.target_dir.set(directory)
        elif choice is False:
            # User selected Single File monitoring
            filepath = filedialog.askopenfilename(
                title="Select Specific Configuration File to Monitor",
                filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Config Files", "*.conf;*.ini;*.json")]
            )
            if filepath:
                self.target_dir.set(filepath)

    def run_baseline(self):
        target = self.target_dir.get()
        if not target:
            messagebox.showerror("Error", "Please pick a valid target path baseline source.")
            return
        count = self.engine.generate_baseline(target)
        messagebox.showinfo("Success", f"Baseline saved! {count} resource asset logs committed to the tracking grid matrix.")

    def run_verification(self):
        target = self.target_dir.get()
        if not target:
            messagebox.showerror("Error", "Please choose a deployment path to check.")
            return
            
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        self.update_diff_view_text("Select an audit entry row to run comparative analytics.")
            
        matches = self.engine.verify_integrity(target)
        for filepath, _, status, _ in matches:
            # Matches columns: "Monitored File Path" and "Integrity Status State"
            self.tree.insert("", "end", values=(filepath, status), tags=(status,))

    def handle_row_selection(self, event):
        selected = self.tree.selection()
        if not selected:
            return
            
        item_values = self.tree.item(selected, "values")
        if not item_values:
            return
            
        filepath, status = item_values
        
        if status != "Modified":
            self.update_diff_view_text(f"File status state is currently [{status}].\nDiff line tracing is isolated only to files flagged as 'Modified'.")
            return
            
        old_content_raw = self.db.get_file_content(filepath)
        _, current_content_raw = Hasher.calculate_sha256(filepath)
        
        # Handling database tuple unpacked content returns cleanly
        old_str = old_content_raw[0] if isinstance(old_content_raw, tuple) else old_content_raw
        
        old_lines = old_str.splitlines() if old_str else []
        new_lines = current_content_raw.splitlines() if current_content_raw else []
        
        # Generate line structural alterations
        delta = difflib.unified_diff(
            old_lines, 
            new_lines, 
            fromfile="Baseline Snapshot DB", 
            tofile="Live Discovered File State", 
            lineterm=""
        )
        
        # Push changes to the embedded text container panel securely
        self.diff_box.config(state="normal")
        self.diff_box.delete("1.0", "end")
        
        has_changes = False
        for line in delta:
            has_changes = True
            if line.startswith("+") and not line.startswith("+++"):
                self.diff_box.insert("end", line + "\n", "addition")
            elif line.startswith("-") and not line.startswith("---"):
                self.diff_box.insert("end", line + "\n", "deletion")
            elif line.startswith("@@") or line.startswith("---") or line.startswith("+++"):
                self.diff_box.insert("end", line + "\n", "header")
            else:
                self.diff_box.insert("end", line + "\n")
                
        if not has_changes:
            self.diff_box.insert("end", "[Information Notice] Minor hash mismatch detected, but binary text sequences contain no printable unified row variances.")
            
        self.diff_box.config(state="disabled")

    def update_diff_view_text(self, plain_text):
        """Helper method to update notification descriptions on the screen."""
        self.diff_box.config(state="normal")
        self.diff_box.delete("1.0", "end")
        self.diff_box.insert("end", plain_text)
        self.diff_box.config(state="disabled")
