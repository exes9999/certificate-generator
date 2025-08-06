
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import black, lightgrey
from PIL import Image as PILImage
import qrcode
import io
import os

st.set_page_config(page_title="Certificate Generator", layout="centered")

st.title("🪪 Certificate Generator")

with st.form("certificate_form"):
    cert_number = st.text_input("Certificate Number", "FL-000001")
    product_name = st.text_input("Product Name", "RING GOLD")
    conclusion = st.text_input("Conclusion", "14K")
    total_mass = st.text_input("Total Mass", "2.65 g")
    metal = st.text_input("Precious Metal", "14K GOLD")
    magnification = st.text_input("Magnification", "N/A")
    made_in = st.text_input("Made In", "THAILAND")
    jewelry_image = st.file_uploader("Upload Jewelry Image", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Generate Certificate")

if submitted:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(30 * mm, height - 30 * mm, "FLAVIA CO., LTD")
    c.setFont("Helvetica", 14)
    c.drawString(30 * mm, height - 40 * mm, "CERTIFICATE OF AUTHENTICITY")

    # Jewelry image
    if jewelry_image:
        image = PILImage.open(jewelry_image)
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        c.drawImage(img_buffer, width - 60 * mm, height - 60 * mm, 40 * mm, 30 * mm)
    else:
        c.setFillColor(lightgrey)
        c.rect(width - 60 * mm, height - 60 * mm, 40 * mm, 30 * mm, fill=1)
        c.setFillColor(black)
        c.setFont("Helvetica", 8)
        c.drawString(width - 59 * mm, height - 63 * mm, "Jewelry Image")

    # Text fields
    c.setFont("Helvetica", 10)
    labels = [
        ("Certificate Number", cert_number),
        ("Product Name", product_name),
        ("Conclusion", conclusion),
        ("Total Mass", total_mass),
        ("Precious Metal", metal),
        ("Magnification", magnification),
        ("Made In", made_in)
    ]
    start_y = height - 70 * mm
    for i, (label, value) in enumerate(labels):
        c.drawString(30 * mm, start_y - i * 8 * mm, f"{label}:")
        c.drawString(80 * mm, start_y - i * 8 * mm, value)

    # QR code
    qr_data = f"https://yourdomain.com/certificates/{cert_number}"
    qr = qrcode.make(qr_data)
    qr_io = io.BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    c.drawImage(qr_io, width - 60 * mm, 30 * mm, 40 * mm, 40 * mm)

    # Disclaimer
    c.setFont("Helvetica", 7)
    disclaimer = "This certificate only release to the sample referred to within.\nPhotocopy, reproduction and alternation are invalid."
    text_object = c.beginText(30 * mm, 20 * mm)
    for line in disclaimer.split("\n"):
        text_object.textLine(line)
    c.drawText(text_object)

    # Finalize
    c.showPage()
    c.save()
    buffer.seek(0)

    st.success("✅ Certificate generated!")

    
    # PNG export
    from reportlab.graphics import renderPM
    from svglib.svglib import svg2rlg
    from reportlab.graphics.shapes import Drawing
    from reportlab.pdfgen.canvas import Canvas

    # Rebuild certificate as image
    img_canvas = canvas.Canvas("temp_cert.pdf", pagesize=A4)
    img_canvas.setFont("Helvetica-Bold", 18)
    img_canvas.drawString(30 * mm, height - 30 * mm, "FLAVIA CO., LTD")
    img_canvas.setFont("Helvetica", 14)
    img_canvas.drawString(30 * mm, height - 40 * mm, "CERTIFICATE OF AUTHENTICITY")
    img_canvas.save()

    from pdf2image import convert_from_bytes
    png_images = convert_from_bytes(buffer.getvalue(), dpi=300)
    png_buffer = io.BytesIO()
    png_images[0].save(png_buffer, format="PNG")
    png_buffer.seek(0)

    st.download_button(
        label="🖼️ Download PNG",
        data=png_buffer,
        file_name=f"{cert_number}.png",
        mime="image/png"
    )

    st.download_button(

        label="📥 Download PDF",
        data=buffer,
        file_name=f"{cert_number}.pdf",
        mime="application/pdf"
    )
