import tkinter as tk
import difflib

def populate_diff(viewer, status, current_text, baseline_text):
    """Populates the text console frame dynamically using line diffing."""
    viewer.delete("1.0", tk.END)
    
    if status == "UNCHANGED":
        viewer.insert(tk.END, "[✓] File contents exactly match baseline matrix configurations.")
    elif status == "CREATED":
        viewer.insert(tk.END, "[+] Entirely New File Identified. Content:\n\n" + "\n".join(current_text))
    elif status == "DELETED":
        viewer.insert(tk.END, "[-] Monitored File Missing/Purged from directory.")
    elif status == "MODIFIED":
        diff = difflib.unified_diff(
            baseline_text, current_text, 
            fromfile="SECURE_BASELINE", tofile="TAMPERED_CURRENT", 
            lineterm=""
        )
        
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                viewer.insert(tk.END, line + "\n", "addition")
            elif line.startswith('-') and not line.startswith('---'):
                viewer.insert(tk.END, line + "\n", "deletion")
            else:
                viewer.insert(tk.END, line + "\n")
                
        viewer.tag_config("addition", foreground="green")
        viewer.tag_config("deletion", foreground="red")
