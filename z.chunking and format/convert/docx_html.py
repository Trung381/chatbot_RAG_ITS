import mammoth
import os

def convert_docx_to_html(docx_path, output_path):
    """
    Chuyển đổi một file .docx thành file .html bằng thư viện mammoth.

    :param docx_path: Đường dẫn đến file .docx đầu vào.
    :param output_path: Đường dẫn để lưu file .html đầu ra.
    """
    # Kiểm tra xem file đầu vào có tồn tại không
    if not os.path.exists(docx_path):
        print(f"Lỗi: Không tìm thấy file '{docx_path}'")
        return

    print(f"🚀 Bắt đầu chuyển đổi '{docx_path}'...")

    try:
        # Mở file docx và thực hiện chuyển đổi
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html_content = result.value  # Lấy nội dung HTML

        # Ghi nội dung HTML vào file đầu ra
        with open(output_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

        print(f"✅ Chuyển đổi thành công! File HTML đã được lưu tại '{output_path}'")

    except Exception as e:
        print(f"💥 Đã xảy ra lỗi trong quá trình chuyển đổi: {e}")

# --- Cách sử dụng ---
if __name__ == "__main__":
    # Thay đổi tên file cho phù hợp với bạn
    input_file = "document/MLFinal.docx"
    output_file = "document_formatted/MLFinal.html"

    # Gọi hàm để thực hiện chuyển đổi
    convert_docx_to_html(input_file, output_file)