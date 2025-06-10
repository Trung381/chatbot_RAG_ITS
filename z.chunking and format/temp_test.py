# import os
# import pdfplumber
# import docx2txt
# from docx import Document

# # Hàm xử lý 1 bảng PDF thành string format chuẩn
# def parse_pdf_table_single(table):
#     if not table or len(table) < 2:
#         return ""
#     headers = table[0]
#     rows = []
#     for row in table[1:]:
#         row_str = ", ".join(f"{headers[i]}: {row[i]}" for i in range(len(headers)))
#         rows.append(row_str)
#     return "\n".join(rows)

# # Hàm xử lý 1 bảng DOCX thành string format chuẩn
# def parse_docx_table_single(table):
#     headers = [cell.text.strip() for cell in table.rows[0].cells]
#     rows = []
#     for row in table.rows[1:]:
#         cells = [cell.text.strip() for cell in row.cells]
#         row_str = ", ".join(f"{headers[i]}: {cells[i]}" for i in range(len(headers)))
#         rows.append(row_str)
#     return "\n".join(rows)

# # Đọc file DOCX giữ đúng thứ tự paragraph/table
# def parse_docx_sequential(filepath):
#     doc = Document(filepath)
#     output = []
#     for block in iter_block_items(doc):
#         if isinstance(block, Paragraph):
#             text = block.text.strip()
#             if text:
#                 output.append(text)
#         elif isinstance(block, Table):
#             table_str = parse_docx_table_single(block)
#             if table_str:
#                 output.append(table_str)
#     return "\n".join(output)

# # Helper: iterate paragraph/table đúng thứ tự trong docx
# from docx.oxml.table import CT_Tbl
# from docx.oxml.text.paragraph import CT_P
# from docx.table import Table
# from docx.text.paragraph import Paragraph

# def iter_block_items(parent):
#     for child in parent.element.body.iterchildren():
#         if isinstance(child, CT_P):
#             yield Paragraph(child, parent)
#         elif isinstance(child, CT_Tbl):
#             yield Table(child, parent)

# # Đọc file PDF giữ đúng thứ tự paragraph/table
# # Chỉ lấy text ngoài bảng, và bảng đúng vị trí
# # Lưu ý: pdfplumber không phân biệt paragraph rõ ràng, nên sẽ lấy text giữa các bảng

# def parse_pdf_sequential(filepath):
#     output = []
#     with pdfplumber.open(filepath) as pdf:
#         for page in pdf.pages:
#             tables = page.find_tables()
#             table_bboxes = [t.bbox for t in tables]
#             # Lấy text ngoài bảng
#             if table_bboxes:
#                 prev_bottom = 0
#                 for i, bbox in enumerate(table_bboxes):
#                     # Text phía trên bảng
#                     top = bbox[1]
#                     if top > prev_bottom:
#                         text = page.within_bbox((0, prev_bottom, page.width, top)).extract_text()
#                         if text:
#                             output.append(text.strip())
#                     # Bảng
#                     table = tables[i].extract()
#                     table_str = parse_pdf_table_single(table)
#                     if table_str:
#                         output.append(table_str)
#                     prev_bottom = bbox[3]
#                 # Text phía dưới bảng cuối
#                 if prev_bottom < page.height:
#                     text = page.within_bbox((0, prev_bottom, page.width, page.height)).extract_text()
#                     if text:
#                         output.append(text.strip())
#             else:
#                 # Không có bảng, lấy toàn bộ text
#                 text = page.extract_text()
#                 if text:
#                     output.append(text.strip())
#     return "\n".join(output)

# # Hàm tổng

# def parse_document_sequential(filepath):
#     ext = os.path.splitext(filepath)[1].lower()
#     if ext == '.pdf':
#         return parse_pdf_sequential(filepath)
#     elif ext == '.docx':
#         return parse_docx_sequential(filepath)
#     else:
#         raise ValueError(f"Unsupported file type: {ext}")

# if __name__ == "__main__":
#     # output_docx = parse_document_sequential("document/test.docx")
#     output_pdf = parse_document_sequential("document/test.pdf")
#     # print("DOCX Output:\n", output_docx)
#     print("\nPDF Output:\n", output_pdf) 



import os
import pdfplumber
import docx2txt
from docx import Document
import re
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

# ====================================
# 🧠 Xử lý thông minh để giữ layout hợp lý
def smart_merge_paragraphs(text: str) -> str:
    lines = text.split('\n')
    merged_paragraphs = []
    buffer = ""

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buffer:
                merged_paragraphs.append(buffer.strip())
                buffer = ""
            continue

        is_title_like = (
            len(stripped) < 40 or
            re.match(r"^(Chương|Mục|Phần|[IVX]+\.|[0-9]+\.)", stripped) or
            stripped.isupper()
        )

        if is_title_like:
            if buffer:
                merged_paragraphs.append(buffer.strip())
                buffer = ""
            merged_paragraphs.append(stripped)
        else:
            if buffer:
                buffer += " " + stripped
            else:
                buffer = stripped

    if buffer:
        merged_paragraphs.append(buffer.strip())

    return "\n".join(merged_paragraphs)

# ====================================
# 📄 Xử lý bảng trong PDF
def parse_pdf_table_single(table):
    if not table or len(table) < 2:
        return ""
    headers = table[0]
    rows = []
    for row in table[1:]:
        row_str = ", ".join(f"{headers[i]}: {row[i]}" for i in range(len(headers)))
        rows.append(row_str)
    return "\n".join(rows)

# 📄 Xử lý bảng trong DOCX
def parse_docx_table_single(table):
    headers = [cell.text.strip() for cell in table.rows[0].cells]
    rows = []
    for row in table.rows[1:]:
        cells = [cell.text.strip() for cell in row.cells]
        row_str = ", ".join(f"{headers[i]}: {cells[i]}" for i in range(len(headers)))
        rows.append(row_str)
    return "\n".join(rows)

# 📄 Helper để đọc đoạn văn và bảng đúng thứ tự trong DOCX
def iter_block_items(parent):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

# 📄 Xử lý file DOCX
def parse_docx_sequential(filepath):
    doc = Document(filepath)
    output = []
    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if text:
                output.append(text)
        elif isinstance(block, Table):
            table_str = parse_docx_table_single(block)
            if table_str:
                output.append(table_str)
    return smart_merge_paragraphs("\n".join(output))

# 📄 Xử lý file PDF
def parse_pdf_sequential(filepath):
    output = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            tables = page.find_tables()
            table_bboxes = [t.bbox for t in tables]
            if table_bboxes:
                prev_bottom = 0
                for i, bbox in enumerate(table_bboxes):
                    top = bbox[1]
                    if top > prev_bottom:
                        text = page.within_bbox((0, prev_bottom, page.width, top)).extract_text()
                        if text:
                            output.append(text.strip())
                    table = tables[i].extract()
                    table_str = parse_pdf_table_single(table)
                    if table_str:
                        output.append(table_str)
                    prev_bottom = bbox[3]
                if prev_bottom < page.height:
                    text = page.within_bbox((0, prev_bottom, page.width, page.height)).extract_text()
                    if text:
                        output.append(text.strip())
            else:
                text = page.extract_text()
                if text:
                    output.append(text.strip())
    return smart_merge_paragraphs("\n".join(output))

# ====================================
# 📁 Hàm tổng xử lý file
def parse_document_sequential(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        return parse_pdf_sequential(filepath)
    elif ext == '.docx':
        return parse_docx_sequential(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# ====================================
# 🧪 Demo test
if __name__ == "__main__":
    filepath = "document/test_lien.docx"
    # filepath = "document/test.pdf"
    output = parse_document_sequential(filepath)
    print(output)
