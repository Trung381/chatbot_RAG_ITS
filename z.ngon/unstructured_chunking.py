import os
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx
from unstructured.partition.html import partition_html
from unstructured.documents.elements import Title, NarrativeText, ListItem, Table

def chunk_by_title(file_path: str):
    """
    Phân tích một file PDF, DOCX hoặc HTML và chia nhỏ nội dung dựa trên các tiêu đề (Title).
    Hàm này cũng xử lý các mục danh sách (ListItem) và bảng (Table) một cách đặc biệt.

    Args:
        file_path: Đường dẫn đến file .pdf, .docx hoặc .html.

    Returns:
        Một danh sách các chunk, mỗi chunk là một dictionary chứa 'title' và 'content'.
        Nội dung bảng sẽ được lưu dưới dạng HTML để giữ nguyên cấu trúc.
    """
    file_ext = os.path.splitext(file_path)[-1].lower()

    common_kwargs = {
        "strategy": "hi_res",
        "infer_table_structure": True,
    }

    if file_ext == ".pdf":
        # elements = partition_pdf(file_path, **common_kwargs)
        elements = partition_pdf(file_path, languages=["vie", "eng"], **common_kwargs)
    elif file_ext == ".docx":
        elements = partition_docx(file_path, **common_kwargs)
    elif file_ext == ".html":
        elements = partition_html(filename=file_path)
    else:
        raise ValueError("Loại file không được hỗ trợ. Vui lòng sử dụng .pdf, .docx hoặc .html")

    chunks = []
    current_chunk = {"title": "Phần mở đầu", "content": ""}

    for el in elements:
        if isinstance(el, Title):
            if current_chunk["content"].strip():
                chunks.append(current_chunk)
            current_chunk = {"title": el.text.strip(), "content": ""}

        elif isinstance(el, ListItem):
            current_chunk["content"] += f"- {el.text.strip()}\n"

        elif isinstance(el, Table):
            table_html = getattr(el.metadata, "text_as_html", None)
            if table_html:
                current_chunk["content"] += f"\n{table_html}\n"
            else:
                current_chunk["content"] += f"\n{el.text.strip()}\n"

        elif isinstance(el, NarrativeText):
            current_chunk["content"] += el.text.strip() + "\n"

    if current_chunk["title"] or current_chunk["content"].strip():
        chunks.append(current_chunk)

    return chunks

# --- VÍ DỤ SỬ DỤNG ---
try:
    file_path = "gan_chuan_formatted_fixed.pdf"  # thay đổi sang .pdf, .docx hoặc .html tùy bạn
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: '{file_path}'. Vui lòng tạo file này hoặc thay đổi đường dẫn.")

    chunks = chunk_by_title(file_path)

    print(f"Đã tìm thấy {len(chunks)} chunks từ file '{file_path}'.\n")
    for i, chunk in enumerate(chunks):
        print(f"=== CHUNK {i+1} ===")
        print(f"Title: {chunk['title']}")
        print(f"Content:\n{chunk['content']}")
        print("-" * 20)

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
    print("Hãy chắc chắn rằng bạn đã cài đặt tất cả các thư viện cần thiết.")