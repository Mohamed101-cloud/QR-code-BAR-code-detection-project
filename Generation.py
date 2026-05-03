import qrcode
import barcode
from barcode.writer import ImageWriter
import os

def generate_qr(data, full_path):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(full_path)
    return full_path

def generate_barcode(data, full_path):
    # نزيل الامتداد لأن المكتبة تضيفه تلقائياً
    path_without_ext = full_path.replace(".png", "")
    code_class = barcode.get_barcode_class('code128')
    my_barcode = code_class(data, writer=ImageWriter())
    my_barcode.save(path_without_ext)
    return f"{path_without_ext}.png"