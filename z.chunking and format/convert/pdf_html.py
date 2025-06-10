import fitz # Tên thư viện là PyMuPDF, nhưng import là fitz

def convert_pdf_to_html_pymupdf(pdf_path, html_path):
    """Chuyển đổi PDF sang HTML bằng PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        html_content = ""
        for page in doc:
            # page.get_text("html") là hàm chính để chuyển đổi
            # Nó tạo ra một file HTML hoàn chỉnh cho mỗi trang
            html_content += page.get_text("html")
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Chuyển đổi thành công với PyMuPDF: {html_path}")
    except Exception as e:
        print(f"💥 Lỗi với PyMuPDF: {e}")

# Sử dụng
convert_pdf_to_html_pymupdf("document/gan_chuan.pdf", "document_formatted/gan_chuan_pymupdf.html")