from fpdf import FPDF
from tkinter import messagebox

# Function to generate an invoice
def create_invoice(client_name, amount):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Invoice", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Client: {client_name}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Amount: ${amount}", ln=True, align='L')
        filename = f"{client_name}_invoice.pdf"
        pdf.output(filename)
        messagebox.showinfo("Success", f"Invoice created: {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create invoice: {e}")