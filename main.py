import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog 
import cv2  
from pyzbar.pyzbar import decode
import datetime
import webbrowser
import os
import Generation  

def scan_and_open():
    file_path = filedialog.askopenfilename(   
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )

    if not file_path:
        return

    try:
        # Read image using OpenCV
        img = cv2.imread(file_path)

        if img is None:
            messagebox.showerror("Error", "Could not load image. Please check the file path!")
            return

        # Decode the code from the OpenCV matrix
        detected_codes = decode(img)

        if not detected_codes:
            messagebox.showwarning("Warning", "No code found in this image!")
            return

        for code in detected_codes:
            content = code.data.decode('utf-8').strip()
            
            # URL Detection Logic
            if "." in content and " " not in content:
                full_url = content if content.startswith("http") else "http://" + content
                webbrowser.open(full_url)
                messagebox.showinfo("Scan Successful", f"URL detected and opened:\n{full_url}")
            else:
                messagebox.showinfo("Code Content", f"Type: {code.type}\nContent: {content}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during processing: {e}")

# Static Directory for saving images
SAVE_DIR = r"C:\Users\sh1\OneDrive\Desktop\Lern\QR code Project\The Generation image" 

# Create directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def create_qr_ui():
    data = simpledialog.askstring("Generate QR", "Enter text or URL:")
    if data:
        # Timestamped filename to prevent duplicates
        filename = f"QR_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        full_path = os.path.join(SAVE_DIR, filename)
        
        path = Generation.generate_qr(data, full_path)
        messagebox.showinfo("Success", f"QR Code saved automatically to:\n{path}")

def create_barcode_ui():
    data = simpledialog.askstring("Generate Barcode", "Enter data (Numbers/Text):")
    if data:
        filename = f"Barcode_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        full_path = os.path.join(SAVE_DIR, filename)
        
        try:
            path = Generation.generate_barcode(data, full_path)
            messagebox.showinfo("Success", f"Barcode saved automatically to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate Barcode: {e}")

# Window Setup
root = tk.Tk()
root.title("QR & Barcode System")
root.geometry("400x450")
root.configure(bg="#213c24")
title_label = tk.Label(root, text="QR & Barcode Manager", font=("Arial", 16, "bold"), pady=20,bg="#213c24",fg="#ffffff")
title_label.pack()
# Scan Button
scan_btn = tk.Button(
    root,
    text="Select File (Scan)",
    command=scan_and_open,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20,
    pady=10
)
scan_btn.pack(pady=10)

# Generate QR Button
qr_btn = tk.Button(
    root,
    text="Generate QR Code",
    command=create_qr_ui,
    bg="#2196F3",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20,
    pady=10
)
qr_btn.pack(pady=10)

# Generate Barcode Button
barcode_btn = tk.Button(
    root,
    text="Generate Barcode",
    command=create_barcode_ui,
    bg="#FF9800",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20,
    pady=10
)
barcode_btn.pack(pady=10)

root.mainloop()