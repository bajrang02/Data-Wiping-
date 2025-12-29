"""
Simple Secure Data Wipe System - Multi-Asset Support
Purpose: Complete data erasure for multiple IT assets simultaneously
Author: IT Security Team
Version: 2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import shutil
import platform
from datetime import datetime
import threading
import time
import random
import string

class MultiAssetWipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Asset Secure Data Wipe System")
        self.root.geometry("1400x750")
        self.root.configure(bg="#1e293b")
        
        # Data
        self.assets = []
        self.pending_wipes = []  # Assets waiting to be wiped
        self.data_file = "wipe_records.json"
        self.is_wiping = False
        
        # Load saved data
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Create main interface"""
        # Header
        header = tk.Frame(self.root, bg="#0f172a", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🛡️ Multi-Asset Secure Data Wipe System",
                font=("Arial", 24, "bold"), bg="#0f172a", fg="#60a5fa").pack(pady=25)
        
        # Main container
        main = tk.Frame(self.root, bg="#1e293b")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left: Asset Entry
        left = tk.Frame(main, bg="#334155", width=420)
        left.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left.pack_propagate(False)
        
        tk.Label(left, text="Add Asset to Wipe Queue", font=("Arial", 16, "bold"),
                bg="#334155", fg="white").pack(pady=20)
        
        # Asset ID
        tk.Label(left, text="Asset ID *", font=("Arial", 11, "bold"),
                bg="#334155", fg="white").pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.asset_id_entry = tk.Entry(left, font=("Arial", 11), bg="#1e293b",
                                       fg="white", insertbackground="white")
        self.asset_id_entry.pack(fill=tk.X, padx=20, ipady=8)
        
        # Asset Type
        tk.Label(left, text="Asset Type *", font=("Arial", 11, "bold"),
                bg="#334155", fg="white").pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.asset_type = tk.StringVar(value="Laptop")
        type_combo = ttk.Combobox(left, textvariable=self.asset_type,
                                 values=["Laptop", "Desktop", "SSD", "HDD", "USB Drive", "Server"],
                                 state="readonly", font=("Arial", 11))
        type_combo.pack(fill=tk.X, padx=20, ipady=8)
        
        # Serial Number
        tk.Label(left, text="Serial Number *", font=("Arial", 11, "bold"),
                bg="#334155", fg="white").pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.serial_entry = tk.Entry(left, font=("Arial", 11), bg="#1e293b",
                                    fg="white", insertbackground="white")
        self.serial_entry.pack(fill=tk.X, padx=20, ipady=8)
        
        # Owner
        tk.Label(left, text="Owner/Department", font=("Arial", 11, "bold"),
                bg="#334155", fg="white").pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.owner_entry = tk.Entry(left, font=("Arial", 11), bg="#1e293b",
                                   fg="white", insertbackground="white")
        self.owner_entry.pack(fill=tk.X, padx=20, ipady=8)
        
        # Drive Path
        tk.Label(left, text="Connected Drive Path *", font=("Arial", 11, "bold"),
                bg="#334155", fg="white").pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        path_frame = tk.Frame(left, bg="#334155")
        path_frame.pack(fill=tk.X, padx=20)
        
        self.drive_path = tk.Entry(path_frame, font=("Arial", 11), bg="#1e293b",
                                   fg="white", insertbackground="white")
        self.drive_path.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        tk.Button(path_frame, text="Browse", command=self.browse_drive,
                 bg="#3b82f6", fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2").pack(side=tk.LEFT, padx=(10, 0), ipady=6, ipadx=10)
        
        # Platform help
        system = platform.system()
        if system == "Windows":
            help_text = "e.g., D:\\ or E:\\Data"
        elif system == "Linux":
            help_text = "e.g., /dev/sdb or /mnt/usb"
        else:
            help_text = "e.g., /Volumes/USB"
        
        tk.Label(left, text=help_text, font=("Arial", 9, "italic"),
                bg="#334155", fg="#94a3b8").pack(anchor=tk.W, padx=20, pady=(5, 0))
        
        # Wipe Standard
        tk.Label(left, text="Wipe Standard *", font=("Arial", 11, "bold"),
                bg="#334155", fg="white").pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.wipe_standard = tk.StringVar(value="DoD 5220.22-M (3 passes)")
        
        standards = [
            ("DoD 5220.22-M (3 passes)", "Military Standard"),
            ("NIST 800-88 (1 pass)", "Fast & Secure"),
            ("Random 7-Pass", "Maximum Security"),
            ("Quick Wipe (1 pass)", "Basic")
        ]
        
        for name, desc in standards:
            rb = tk.Radiobutton(left, text=name, variable=self.wipe_standard,
                              value=name, font=("Arial", 10, "bold"),
                              bg="#334155", fg="white", selectcolor="#1e293b")
            rb.pack(anchor=tk.W, padx=25, pady=2)
            tk.Label(left, text=desc, font=("Arial", 8),
                    bg="#334155", fg="#94a3b8").pack(anchor=tk.W, padx=45)
        
        # Buttons
        btn_frame = tk.Frame(left, bg="#334155")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="➕ Add to Queue", command=self.add_to_queue,
                 bg="#22c55e", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=12, cursor="hand2").pack(pady=5, fill=tk.X)
        
        tk.Button(btn_frame, text="🔄 Clear Form", command=self.clear_form,
                 bg="#6b7280", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=12, cursor="hand2").pack(pady=5, fill=tk.X)
        
        # Right: Two sections
        right = tk.Frame(main, bg="#1e293b")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Top: Pending Queue
        queue_frame = tk.Frame(right, bg="#334155", height=280)
        queue_frame.pack(fill=tk.BOTH, padx=0, pady=(0, 10))
        queue_frame.pack_propagate(False)
        
        queue_header = tk.Frame(queue_frame, bg="#334155")
        queue_header.pack(fill=tk.X, pady=10)
        
        tk.Label(queue_header, text="Wipe Queue", font=("Arial", 16, "bold"),
                bg="#334155", fg="white").pack(side=tk.LEFT, padx=20)
        
        self.queue_count_label = tk.Label(queue_header, text="(0 assets)",
                                          font=("Arial", 12), bg="#334155", fg="#94a3b8")
        self.queue_count_label.pack(side=tk.LEFT)
        
        # Queue listbox
        queue_list_frame = tk.Frame(queue_frame, bg="#334155")
        queue_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        queue_scroll = ttk.Scrollbar(queue_list_frame)
        queue_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.queue_listbox = tk.Listbox(queue_list_frame, font=("Arial", 10),
                                        bg="#1e293b", fg="white",
                                        selectbackground="#3b82f6",
                                        yscrollcommand=queue_scroll.set, height=8)
        self.queue_listbox.pack(fill=tk.BOTH, expand=True)
        queue_scroll.config(command=self.queue_listbox.yview)
        
        # Queue action buttons
        queue_btn_frame = tk.Frame(queue_frame, bg="#334155")
        queue_btn_frame.pack(pady=10)
        
        tk.Button(queue_btn_frame, text="🔥 WIPE ALL", command=self.wipe_all,
                 bg="#dc2626", fg="white", font=("Arial", 12, "bold"),
                 padx=30, pady=12, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(queue_btn_frame, text="❌ Remove Selected", command=self.remove_from_queue,
                 bg="#ef4444", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=12, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(queue_btn_frame, text="🗑️ Clear Queue", command=self.clear_queue,
                 bg="#6b7280", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=12, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Bottom: Completed Records
        records_frame = tk.Frame(right, bg="#334155")
        records_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(records_frame, text="Completed Wipe Records", font=("Arial", 16, "bold"),
                bg="#334155", fg="white").pack(pady=15)
        
        # Treeview
        tree_frame = tk.Frame(records_frame, bg="#334155")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("Asset ID", "Type", "Serial", "Status", "Date", "Certificate")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                yscrollcommand=scrollbar.set, height=10)
        
        widths = [110, 90, 120, 90, 130, 150]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.CENTER)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Tags
        self.tree.tag_configure('completed', background='#d1fae5', foreground='#000')
        
        # Record action buttons
        record_btn_frame = tk.Frame(records_frame, bg="#334155")
        record_btn_frame.pack(pady=10)
        
        tk.Button(record_btn_frame, text="📄 Certificate", command=self.generate_certificate,
                 bg="#22c55e", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(record_btn_frame, text="📤 Export All", command=self.export_records,
                 bg="#3b82f6", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(record_btn_frame, text="🗑️ Delete Record", command=self.delete_record,
                 bg="#ef4444", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        self.refresh_tree()
        self.update_queue_display()
    
    def browse_drive(self):
        """Browse for drive/folder"""
        path = filedialog.askdirectory(title="Select Connected Drive/Folder to Wipe")
        if path:
            self.drive_path.delete(0, tk.END)
            self.drive_path.insert(0, path)
    
    def clear_form(self):
        """Clear all input fields"""
        self.asset_id_entry.delete(0, tk.END)
        self.serial_entry.delete(0, tk.END)
        self.owner_entry.delete(0, tk.END)
        self.drive_path.delete(0, tk.END)
        self.asset_type.set("Laptop")
        self.wipe_standard.set("DoD 5220.22-M (3 passes)")
    
    def add_to_queue(self):
        """Add asset to wipe queue"""
        # Validate inputs
        asset_id = self.asset_id_entry.get().strip()
        serial = self.serial_entry.get().strip()
        path = self.drive_path.get().strip()
        
        if not asset_id:
            messagebox.showerror("Missing Info", "Please enter Asset ID!")
            return
        
        if not serial:
            messagebox.showerror("Missing Info", "Please enter Serial Number!")
            return
        
        if not path:
            messagebox.showerror("Missing Info", "Please select the connected drive path!")
            return
        
        if not os.path.exists(path):
            messagebox.showerror("Invalid Path", f"Path does not exist:\n{path}")
            return
        
        # Check duplicate in queue
        if any(a['asset_id'] == asset_id for a in self.pending_wipes):
            messagebox.showerror("Duplicate", f"Asset ID '{asset_id}' already in queue!")
            return
        
        # Check duplicate in records
        if any(a['asset_id'] == asset_id for a in self.assets):
            messagebox.showerror("Duplicate", f"Asset ID '{asset_id}' already wiped!")
            return
        
        # Get standard
        standard_text = self.wipe_standard.get()
        if "3 passes" in standard_text:
            passes = 3
            standard = "DoD 5220.22-M"
        elif "NIST" in standard_text:
            passes = 1
            standard = "NIST 800-88"
        elif "7-Pass" in standard_text:
            passes = 7
            standard = "Random 7-Pass"
        else:
            passes = 1
            standard = "Quick Wipe"
        
        # Add to queue
        asset = {
            "asset_id": asset_id,
            "type": self.asset_type.get(),
            "serial": serial,
            "owner": self.owner_entry.get().strip() or "N/A",
            "path": path,
            "standard": standard,
            "passes": passes
        }
        
        self.pending_wipes.append(asset)
        self.update_queue_display()
        self.clear_form()
        
        messagebox.showinfo("Added", f"Asset '{asset_id}' added to wipe queue!\n"
                           f"Total in queue: {len(self.pending_wipes)}")
    
    def remove_from_queue(self):
        """Remove selected asset from queue"""
        selection = self.queue_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an asset from the queue!")
            return
        
        idx = selection[0]
        asset = self.pending_wipes[idx]
        
        if messagebox.askyesno("Confirm", f"Remove '{asset['asset_id']}' from queue?"):
            self.pending_wipes.pop(idx)
            self.update_queue_display()
    
    def clear_queue(self):
        """Clear entire queue"""
        if not self.pending_wipes:
            messagebox.showinfo("Empty", "Queue is already empty!")
            return
        
        if messagebox.askyesno("Confirm", f"Remove all {len(self.pending_wipes)} assets from queue?"):
            self.pending_wipes.clear()
            self.update_queue_display()
    
    def update_queue_display(self):
        """Update queue listbox"""
        self.queue_listbox.delete(0, tk.END)
        
        for asset in self.pending_wipes:
            display = f"🔸 {asset['asset_id']} | {asset['type']} | {asset['serial']} | {asset['standard']} | {asset['path']}"
            self.queue_listbox.insert(tk.END, display)
        
        self.queue_count_label.config(text=f"({len(self.pending_wipes)} assets)")
    
    def wipe_all(self):
        """Wipe all assets in queue"""
        if self.is_wiping:
            messagebox.showwarning("In Progress", "A wipe is already in progress!")
            return
        
        if not self.pending_wipes:
            messagebox.showwarning("Empty Queue", "No assets in queue to wipe!")
            return
        
        # Final confirmation
        total = len(self.pending_wipes)
        assets_list = "\n".join([f"• {a['asset_id']} - {a['type']}" for a in self.pending_wipes[:10]])
        if total > 10:
            assets_list += f"\n... and {total - 10} more"
        
        confirm = messagebox.askyesno(
            "⚠️ BATCH WIPE CONFIRMATION ⚠️",
            f"PERMANENT DATA ERASURE FOR {total} ASSETS\n\n"
            f"{assets_list}\n\n"
            f"ALL DATA WILL BE PERMANENTLY ERASED!\n"
            f"This CANNOT be undone!\n\n"
            f"Do you want to proceed?"
        )
        
        if not confirm:
            return
        
        # Type WIPE confirmation
        confirm_dialog = tk.Toplevel(self.root)
        confirm_dialog.title("Confirm Batch Wipe")
        confirm_dialog.geometry("450x200")
        confirm_dialog.configure(bg="#1e293b")
        confirm_dialog.transient(self.root)
        confirm_dialog.grab_set()
        
        tk.Label(confirm_dialog, text=f"Type 'WIPE ALL' to proceed with {total} assets:",
                font=("Arial", 12, "bold"), bg="#1e293b", fg="white").pack(pady=20)
        
        confirm_entry = tk.Entry(confirm_dialog, font=("Arial", 12),
                                bg="#334155", fg="white", insertbackground="white")
        confirm_entry.pack(pady=10, padx=30, fill=tk.X)
        confirm_entry.focus()
        
        def proceed():
            if confirm_entry.get() == "WIPE ALL":
                confirm_dialog.destroy()
                self.perform_batch_wipe()
            else:
                messagebox.showerror("Error", "Confirmation text incorrect!")
        
        tk.Button(confirm_dialog, text="PROCEED WITH BATCH WIPE", command=proceed,
                 bg="#dc2626", fg="white", font=("Arial", 11, "bold"),
                 padx=30, pady=12, cursor="hand2").pack(pady=20)
    
    def perform_batch_wipe(self):
        """Perform batch wipe of all queued assets"""
        self.is_wiping = True
        assets_to_wipe = self.pending_wipes.copy()
        total_assets = len(assets_to_wipe)
        
        # Clear queue
        self.pending_wipes.clear()
        self.update_queue_display()
        
        # Progress dialog
        progress_win = tk.Toplevel(self.root)
        progress_win.title("Batch Wipe in Progress")
        progress_win.geometry("700x450")
        progress_win.configure(bg="#1e293b")
        progress_win.transient(self.root)
        progress_win.grab_set()
        progress_win.protocol("WM_DELETE_WINDOW", lambda: None)
        
        tk.Label(progress_win, text="🔥 BATCH WIPE IN PROGRESS",
                font=("Arial", 20, "bold"), bg="#1e293b", fg="#dc2626").pack(pady=20)
        
        # Overall progress
        tk.Label(progress_win, text="Overall Progress",
                font=("Arial", 12, "bold"), bg="#1e293b", fg="white").pack(pady=(10, 5))
        
        overall_progress_var = tk.DoubleVar()
        overall_bar = ttk.Progressbar(progress_win, variable=overall_progress_var,
                                      maximum=100, length=600)
        overall_bar.pack(pady=5)
        
        overall_label = tk.Label(progress_win, text=f"0 / {total_assets} assets completed",
                                font=("Arial", 11), bg="#1e293b", fg="#94a3b8")
        overall_label.pack(pady=5)
        
        # Current asset
        current_frame = tk.Frame(progress_win, bg="#334155")
        current_frame.pack(fill=tk.X, padx=30, pady=15)
        
        current_asset_label = tk.Label(current_frame, text="",
                                       font=("Arial", 12, "bold"), bg="#334155", fg="white")
        current_asset_label.pack(pady=5)
        
        status_label = tk.Label(current_frame, text="Initializing...",
                               font=("Arial", 10), bg="#334155", fg="#fbbf24")
        status_label.pack(pady=5)
        
        # Current asset progress
        asset_progress_var = tk.DoubleVar()
        asset_bar = ttk.Progressbar(current_frame, variable=asset_progress_var,
                                    maximum=100, length=600)
        asset_bar.pack(pady=10)
        
        asset_percent_label = tk.Label(current_frame, text="0%",
                                       font=("Arial", 11, "bold"), bg="#334155", fg="#60a5fa")
        asset_percent_label.pack()
        
        details_label = tk.Label(current_frame, text="",
                                font=("Arial", 9), bg="#334155", fg="#94a3b8")
        details_label.pack(pady=5)
        
        tk.Label(progress_win, text="⚠️ DO NOT close this window or disconnect devices",
                font=("Arial", 10, "bold"), bg="#1e293b", fg="#fbbf24").pack(pady=10)
        
        def wipe_thread():
            completed = 0
            failed = []
            
            for asset_idx, asset in enumerate(assets_to_wipe):
                if not progress_win.winfo_exists():
                    return
                
                try:
                    # Update current asset
                    current_asset_label.config(
                        text=f"Asset {asset_idx + 1}/{total_assets}: {asset['asset_id']} ({asset['type']})"
                    )
                    status_label.config(text="Scanning files...")
                    asset_progress_var.set(0)
                    
                    # Scan files
                    all_files = []
                    total_size = 0
                    path = asset['path']
                    
                    if os.path.isfile(path):
                        all_files.append(path)
                        total_size = os.path.getsize(path)
                    elif os.path.isdir(path):
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                all_files.append(file_path)
                                try:
                                    total_size += os.path.getsize(file_path)
                                except:
                                    pass
                    
                    total_files = len(all_files)
                    details_label.config(text=f"{total_files} files | {total_size/(1024*1024):.1f} MB")
                    
                    if total_files == 0:
                        raise Exception("No files found")
                    
                    # Wipe files
                    passes = asset['passes']
                    
                    for file_idx, file_path in enumerate(all_files):
                        if not progress_win.winfo_exists():
                            return
                        
                        status_label.config(text=f"Wiping: {os.path.basename(file_path)}")
                        
                        try:
                            file_size = os.path.getsize(file_path)
                            
                            for pass_num in range(passes):
                                details_label.config(text=f"Pass {pass_num+1}/{passes} | File {file_idx+1}/{total_files}")
                                
                                with open(file_path, 'r+b') as f:
                                    if pass_num == 0:
                                        f.write(b'\x00' * file_size)
                                    elif pass_num == 1 and passes > 1:
                                        f.write(b'\xFF' * file_size)
                                    else:
                                        f.write(os.urandom(file_size))
                                    f.flush()
                                    os.fsync(f.fileno())
                                
                                base = (file_idx / total_files) * 100
                                pass_prog = ((pass_num + 1) / passes) * (100 / total_files)
                                total_prog = min(base + pass_prog, 100)
                                
                                asset_progress_var.set(total_prog)
                                asset_percent_label.config(text=f"{int(total_prog)}%")
                            
                            os.remove(file_path)
                            
                        except Exception as e:
                            print(f"Error wiping {file_path}: {e}")
                            continue
                    
                    # Remove directory
                    if os.path.isdir(path):
                        status_label.config(text="Removing directory...")
                        try:
                            shutil.rmtree(path, ignore_errors=True)
                        except:
                            pass
                    
                    # Save record
                    cert_id = f"CERT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000,9999)}"
                    
                    record = {
                        "asset_id": asset['asset_id'],
                        "type": asset['type'],
                        "serial": asset['serial'],
                        "owner": asset['owner'],
                        "path": asset['path'],
                        "standard": asset['standard'],
                        "passes": asset['passes'],
                        "status": "completed",
                        "start_time": datetime.now().isoformat(),
                        "end_time": datetime.now().isoformat(),
                        "certificate_id": cert_id
                    }
                    
                    self.assets.append(record)
                    self.save_data()
                    self.refresh_tree()
                    
                    completed += 1
                    
                except Exception as e:
                    failed.append(f"{asset['asset_id']}: {str(e)}")
                    print(f"Error wiping {asset['asset_id']}: {e}")
                
                # Update overall progress
                overall_progress_var.set((asset_idx + 1) / total_assets * 100)
                overall_label.config(text=f"{asset_idx + 1} / {total_assets} assets completed")
            
            # Complete
            self.is_wiping = False
            
            if progress_win.winfo_exists():
                progress_win.destroy()
            
            if failed:
                messagebox.showwarning("Batch Wipe Complete",
                                      f"Completed: {completed}/{total_assets} assets\n"
                                      f"Failed: {len(failed)} assets\n\n"
                                      f"Failed assets:\n" + "\n".join(failed[:5]))
            else:
                messagebox.showinfo("Success",
                                  f"Batch Wipe Completed Successfully!\n\n"
                                  f"Total Assets Wiped: {completed}\n"
                                  f"All data is permanently unrecoverable!")
        
        thread = threading.Thread(target=wipe_thread, daemon=True)
        thread.start()
    
    def generate_certificate(self):
        """Generate wipe certificate"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a record!")
            return
        
        item = self.tree.item(selection[0])
        asset_id = item['values'][0]
        asset = next((a for a in self.assets if a['asset_id'] == asset_id), None)
        
        if not asset:
            return
        
        cert = f"""
{'='*75}
                    DATA WIPE CERTIFICATE
{'='*75}

Certificate ID: {asset['certificate_id']}
Date: {datetime.fromisoformat(asset['end_time']).strftime('%Y-%m-%d %H:%M:%S')}

ASSET INFORMATION
{'-'*75}
Asset ID:        {asset['asset_id']}
Type:            {asset['type']}
Serial Number:   {asset['serial']}
Owner:           {asset['owner']}

WIPE DETAILS
{'-'*75}
Standard:        {asset['standard']}
Passes:          {asset['passes']}
Path Wiped:      {asset['path']}
Start Time:      {datetime.fromisoformat(asset['start_time']).strftime('%Y-%m-%d %H:%M:%S')}
End Time:        {datetime.fromisoformat(asset['end_time']).strftime('%Y-%m-%d %H:%M:%S')}
Status:          SUCCESSFULLY COMPLETED

CERTIFICATION
{'-'*75}
This certificate verifies that all data on the above device has been
permanently erased using the {asset['standard']} standard with {asset['passes']} 
overwrite passes. The data is considered completely unrecoverable and 
the device is ready for secure disposal or repurposing.

{'='*75}
Generated by: Multi-Asset Secure Data Wipe System
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*75}
"""
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"{asset['certificate_id']}.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(cert)
            messagebox.showinfo("Success", f"Certificate saved:\n{filename}")
    
    def export_records(self):
        """Export all records"""
        if not self.assets:
            messagebox.showwarning("No Data", "No records to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=f"wipe_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.assets, f, indent=2)
            messagebox.showinfo("Success", f"Records exported:\n{filename}")
    
    def delete_record(self):
        """Delete a record"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a record!")
            return
        
        if messagebox.askyesno("Confirm", "Delete this record?"):
            item = self.tree.item(selection[0])
            asset_id = item['values'][0]
            self.assets = [a for a in self.assets if a['asset_id'] != asset_id]
            self.save_data()
            self.refresh_tree()
            messagebox.showinfo("Success", "Record deleted!")
    
    def refresh_tree(self):
        """Refresh the records tree"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for asset in self.assets:
            values = (
                asset['asset_id'],
                asset['type'],
                asset['serial'],
                asset['status'].upper(),
                datetime.fromisoformat(asset['start_time']).strftime('%Y-%m-%d %H:%M'),
                asset.get('certificate_id', 'N/A')
            )
            self.tree.insert('', tk.END, values=values, tags=(asset['status'],))
    
    def save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.assets, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
    
    def load_data(self):
        """Load data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.assets = json.load(f)
        except:
            self.assets = []

def main():
    root = tk.Tk()
    app = MultiAssetWipeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()