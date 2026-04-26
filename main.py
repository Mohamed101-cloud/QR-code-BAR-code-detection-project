import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from pyzbar.pyzbar import decode
import webbrowser

def scan_and_open():
    file_path = filedialog.askopenfilename(
        title="اختر صورة QR Code أو Barcode",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )

    if not file_path:
        return

    try:
        img = Image.open(file_path)
        detected_codes = decode(img)

        if not detected_codes:
            messagebox.showwarning("تنبيه", "لم يتم العثور على أي كود في هذه الصورة!")
            return

        for code in detected_codes:
            content = code.data.decode('utf-8').strip()
            # --- هذا هو الجزء الذي تم تحديثه ---
            # التحقق إذا كان المحتوى يحتوي على نقطة (كروابط المواقع) ولا يحتوي على مسافات
            if "." in content and " " not in content:
                # إذا كان الرابط لا يبدأ بـ http، نضيفها له ليفتح بشكل صحيح
                full_url = content if content.startswith("http") else "http://" + content
                webbrowser.open(full_url)
                messagebox.showinfo("تم المسح", f"تم التعرف على رابط وفتحه:\n{full_url}")
            else:
                messagebox.showinfo("محتوى الكود", f"النوع: {code.type}\nالمحتوى: {content}")
            # -----------------------------------

    except Exception as e:
        messagebox.showerror("خطأ", f"حدثت مشكلة أثناء المعالجة: {e}")

# إعداد نافذة البرنامج
root = tk.Tk()
root.title("QR & Barcode Detected")
root.geometry("400x250")

title_label = tk.Label(root, text="QR & Barcode Scanner", font=("Arial", 16, "bold"), pady=20)
title_label.pack()

scan_btn = tk.Button(
    root,
    text="Select File",
    command=scan_and_open,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10
)
scan_btn.pack(pady=20)
root.mainloop()