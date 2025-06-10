# # import docx
# # import re

# # # ===============================================================
# # # HELPER FUNCTIONS (CÁC HÀM HỖ TRỢ)
# # # ===============================================================

# # def is_paragraph_bold(paragraph):
# #     """Kiểm tra xem toàn bộ đoạn văn có được in đậm không."""
# #     return all(run.bold for run in paragraph.runs if run.text.strip())

# # def get_paragraph_font_size(paragraph):
# #     """Lấy cỡ chữ phổ biến nhất trong đoạn văn."""
# #     # Logic có thể phức tạp hơn, đây là ví dụ đơn giản
# #     if paragraph.runs:
# #         # Giả sử run đầu tiên đại diện cho cả đoạn
# #         return paragraph.runs[0].font.size
# #     return None

# # def get_normalized_text(paragraph):
# #     """Lấy toàn bộ text của paragraph, loại bỏ định dạng inline."""
# #     return "".join(run.text for run in paragraph.runs)
    
# # def is_list_item(paragraph):
# #     """Kiểm tra xem đoạn văn có phải là một mục trong danh sách không."""
# #     text = paragraph.text.strip()
# #     # Regex cho ordered list (1., a., I.) and unordered list (*, -, •)
# #     list_pattern = re.compile(r'^((\d+\.|\w\.|[ivx]+\.)|([*\-•]))\s', re.I)
# #     return bool(list_pattern.match(text))

# # # ===============================================================
# # # MAIN LOGIC
# # # ===============================================================

# # def format_document(input_path, output_path):
# #     """
# #     Đọc một file docx chưa định dạng và tạo ra file mới đã được chuẩn hóa.
# #     """
# #     doc = docx.Document(input_path)
# #     new_doc = docx.Document()

# #     # Bước 1: Phân tích (ví dụ đơn giản: tìm cỡ chữ của các heading)
# #     bold_sizes = set()
# #     for para in doc.paragraphs:
# #         if is_paragraph_bold(para):
# #             size = get_paragraph_font_size(para)
# #             if size:
# #                 bold_sizes.add(size.pt)
    
# #     # Sắp xếp để xác định cấp độ heading
# #     sorted_bold_sizes = sorted(list(bold_sizes), reverse=True)
    
# #     heading_level_map = {}
# #     if len(sorted_bold_sizes) > 0:
# #         heading_level_map[sorted_bold_sizes[0]] = 1 # Lớn nhất là H1
# #     if len(sorted_bold_sizes) > 1:
# #         heading_level_map[sorted_bold_sizes[1]] = 2 # Lớn nhì là H2
# #     # ... thêm các level khác nếu cần

# #     # Bước 2: Xử lý và tạo tài liệu mới
# #     for para in doc.paragraphs:
# #         text = para.text.strip()
# #         if not text:
# #             # Bỏ qua các dòng trống
# #             continue

# #         is_bold = is_paragraph_bold(para)
# #         font_size = get_paragraph_font_size(para)
# #         font_size_pt = font_size.pt if font_size else 0

# #         # 1. Quy tắc cho Headings
# #         if is_bold and font_size_pt in heading_level_map:
# #             level = heading_level_map[font_size_pt]
# #             new_doc.add_heading(text, level=level)
        
# #         # 2. Quy tắc cho Lists
# #         elif is_list_item(para):
# #             # Lấy text sạch, bỏ đi phần ký hiệu đầu dòng
# #             clean_text = re.sub(r'^((\d+\.|\w\.|[ivx]+\.)|([*\-•]))\s*', '', text, re.I)
# #             # Áp dụng style 'List Bullet' hoặc 'List Number' để có <li>
# #             # Cần logic phức tạp hơn để xử lý indent
# #             new_doc.add_paragraph(clean_text, style='List Bullet')

# #         # 3. Quy tắc cho Body Text (văn bản thường)
# #         else:
# #             # Chuẩn hóa, chỉ lấy text, bỏ bold/italic inline
# #             normalized_text = get_normalized_text(para)
# #             new_doc.add_paragraph(normalized_text, style='Body Text')

# #     # 4. Quy tắc cho Tables (ví dụ sao chép bảng)
# #     for table in doc.tables:
# #         new_table = new_doc.add_table(rows=len(table.rows), cols=len(table.columns))
# #         # Style cho table để dễ nhìn
# #         new_table.style = 'Table Grid' 
# #         for i, row in enumerate(table.rows):
# #             for j, cell in enumerate(row.cells):
# #                 new_table.cell(i, j).text = cell.text

# #     new_doc.save(output_path)

# # # Sử dụng
# # format_document('document/gan_chuan.docx', 'document_formatted/gan_chuan_formatted.docx')




# import docx
# import re
# from docx.document import Document
# from docx.oxml.text.paragraph import CT_P
# from docx.oxml.table import CT_Tbl
# from docx.text.paragraph import Paragraph
# from docx.table import Table

# # --- CÁC HÀM HỖ TRỢ (Giữ nguyên và bổ sung) ---

# def iter_block_items(parent):
#     # ... (code của hàm này đã được trình bày ở trên) ...
#     if isinstance(parent, Document):
#         parent_elm = parent.element.body
#     else:
#         raise ValueError("Parent unsupported")

#     for child in parent_elm.iterchildren():
#         if isinstance(child, CT_P):
#             yield Paragraph(child, parent)
#         elif isinstance(child, CT_Tbl):
#             yield Table(child, parent)

# def is_paragraph_bold(paragraph):
#     """Kiểm tra xem toàn bộ các run có chữ của đoạn văn có được in đậm không."""
#     # Chỉ kiểm tra các run có chứa ký tự, bỏ qua các run chỉ có khoảng trắng
#     runs_with_text = [run for run in paragraph.runs if run.text.strip()]
#     if not runs_with_text:
#         return False
#     return all(run.bold for run in runs_with_text)

# def get_normalized_text(paragraph):
#     """Lấy text của paragraph, loại bỏ định dạng inline."""
#     return "".join(run.text for run in paragraph.runs)

# def is_list_item(paragraph):
#     """Kiểm tra xem đoạn văn có phải là một mục trong danh sách không."""
#     text = paragraph.text.strip()
#     list_pattern = re.compile(r'^((\d+\.|\w\.|[ivx]+\.)|([*\-•]))\s', re.I)
#     return bool(list_pattern.match(text))

# # --- LOGIC XỬ LÝ CHÍNH ĐÃ ĐƯỢC CẬP NHẬT ---

# def format_document_ordered(input_path, output_path):
#     """
#     Đọc file docx, chuẩn hóa và ghi ra file mới,
#     giữ nguyên thứ tự và xử lý trường hợp chỉ dùng bold.
#     """
#     doc = docx.Document(input_path)
#     new_doc = docx.Document()

#     # Vòng lặp chính duy nhất, duyệt qua các khối theo đúng thứ tự
#     for block in iter_block_items(doc):
#         # A. XỬ LÝ NẾU KHỐI LÀ ĐOẠN VĂN (PARAGRAPH)
#         if isinstance(block, Paragraph):
#             para = block
#             text = para.text.strip()
            
#             if not text: # Bỏ qua các dòng trống
#                 continue

#             # QUY TẮC MỚI: Ưu tiên nhận diện heading bằng bold và độ dài ngắn
#             # Ngưỡng: dưới 15 từ được coi là ngắn (có thể thay đổi)
#             if is_paragraph_bold(para) and len(text.split()) < 15:
#                 # Nếu là heading, ta có thể phân cấp nhỏ hơn nếu muốn
#                 # Ví dụ: nếu text viết HOA toàn bộ thì là Heading 1, còn không là Heading 2
#                 if text.isupper():
#                     new_doc.add_heading(text, level=1)
#                 else:
#                     new_doc.add_heading(text, level=2)
            
#             # Quy tắc nhận diện danh sách
#             elif is_list_item(para):
#                 clean_text = re.sub(r'^((\d+\.|\w\.|[ivx]+\.)|([*\-•]))\s*', '', text, re.I)
#                 new_doc.add_paragraph(clean_text, style='List Bullet')

#             # Mặc định là văn bản thường
#             else:
#                 normalized_text = get_normalized_text(para)
#                 new_doc.add_paragraph(normalized_text, style='Normal')

#         # B. XỬ LÝ NẾU KHỐI LÀ BẢNG (TABLE)
#         elif isinstance(block, Table):
#             table = block
#             new_table = new_doc.add_table(rows=len(table.rows), cols=len(table.columns))
#             new_table.style = 'Table Grid'
#             for i, row in enumerate(table.rows):
#                 for j, cell in enumerate(row.cells):
#                     new_table.cell(i, j).text = cell.text
    
#     new_doc.save(output_path)

# # --- CÁCH SỬ DỤNG ---
# format_document_ordered('document/gan_chuan.docx', 'document_formatted/gan_chuan_formatted.docx')

import docx
import re
from docx.document import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.text.paragraph import Paragraph
from docx.table import Table

# --- CÁC HÀM HỖ TRỢ (Đã cập nhật và bổ sung) ---

def iter_block_items(parent):
    """
    Duyệt qua các block-level items (paragraph và table) trong một document hoặc cell.
    Giữ nguyên thứ tự gốc của chúng.
    """
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    # Có thể mở rộng để xử lý cell trong table nếu cần
    # elif isinstance(parent, _Cell):
    #     parent_elm = parent._tc
    else:
        raise ValueError("Parent type is not supported")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def is_paragraph_bold(paragraph):
    """Kiểm tra xem toàn bộ các run có chữ của đoạn văn có được in đậm không."""
    runs_with_text = [run for run in paragraph.runs if run.text.strip()]
    if not runs_with_text:
        return False
    return all(run.bold for run in runs_with_text)

def get_normalized_text(paragraph):
    """Lấy text của paragraph, loại bỏ định dạng inline."""
    return "".join(run.text for run in paragraph.runs)

def is_list_item(paragraph):
    """Kiểm tra xem đoạn văn có phải là một mục trong danh sách không (không bao gồm heading số)."""
    text = paragraph.text.strip()
    # Pattern này giờ đây chủ yếu dùng cho danh sách ký tự, dấu đầu dòng, hoặc số La Mã
    list_pattern = re.compile(r'^((\w\.|[ivx]+\.)|([*\-•]))\s', re.I)
    return bool(list_pattern.match(text))

def get_heading_level_from_number(paragraph):
    """
    Kiểm tra xem paragraph có phải là heading dạng số (1.1, 1.1.1) hay không.
    Trả về (level, clean_text) nếu là heading, ngược lại trả về (None, None).
    """
    text = paragraph.text.strip()
    # Pattern để khớp với các chỉ mục như 1., 1.1, 1.1., 1.1.1, 1.1.1.
    heading_pattern = re.compile(r'^(\d+(\.\d+)*)\.?\s')
    match = heading_pattern.match(text)

    if match:
        number_part = match.group(1) # Lấy phần số, ví dụ '1.1.1'
        level = number_part.count('.') + 1
        
        # Giới hạn cấp độ heading để tránh lỗi (ví dụ, level 7, 8, 9 không có sẵn)
        if level > 6:
            level = 6

        clean_text = text[len(match.group(0)):].strip()
        return level, clean_text
        
    return None, None

# --- LOGIC XỬ LÝ CHÍNH ĐÃ ĐƯỢC CẬP NHẬT ---

def format_document_ordered(input_path, output_path):
    """
    Đọc file docx, chuẩn hóa và ghi ra file mới với logic nhận diện heading phức tạp hơn.
    """
    doc = docx.Document(input_path)
    new_doc = docx.Document()

    for block in iter_block_items(doc):
        # A. XỬ LÝ NẾU KHỐI LÀ ĐOẠN VĂN (PARAGRAPH)
        if isinstance(block, Paragraph):
            para = block
            text = para.text.strip()
            
            if not text: # Bỏ qua các dòng trống
                continue

            # QUY TẮC 1 (ƯU TIÊN CAO NHẤT): Nhận diện heading theo chỉ mục số (1., 1.1., 1.1.1)
            level, clean_text = get_heading_level_from_number(para)
            if level is not None:
                # Điều kiện bổ sung: Nếu là heading cấp 1 (ví dụ "1. Giới thiệu"),
                # nó phải được in đậm để phân biệt với danh sách liệt kê ("1. Táo").
                if level == 1 and not is_paragraph_bold(para):
                    # Nếu không in đậm, coi nó là danh sách và xử lý ở dưới
                    pass
                else:
                    new_doc.add_heading(clean_text, level=level)
                    continue # Đã xử lý xong, chuyển sang block tiếp theo

            # # QUY TẮC 2: Nhận diện heading bằng bold, chữ hoa, độ dài ngắn (cho các tiêu đề không đánh số)
            # # Ngưỡng: dưới 15 từ được coi là ngắn
            # if is_paragraph_bold(para) and len(text.split()) < 15:
            #     if text.isupper():
            #         new_doc.add_heading(text, level=1)
            #     else:
            #         new_doc.add_heading(text, level=2)
            
            # QUY TẮC 3: Nhận diện danh sách liệt kê (bao gồm cả "1." không in đậm từ quy tắc 1)
            elif is_list_item(para) or (level == 1 and not is_paragraph_bold(para)):
                # Làm sạch các ký tự đầu dòng
                clean_text = re.sub(r'^((\d+\.|\w\.|[ivx]+\.)|([*\-•]))\s*', '', text, re.I).strip()
                new_doc.add_paragraph(clean_text, style='List Bullet')

            # QUY TẮC 4 (MẶC ĐỊNH): Là văn bản thường
            else:
                normalized_text = get_normalized_text(para)
                new_doc.add_paragraph(normalized_text, style='Normal')

        # B. XỬ LÝ NẾU KHỐI LÀ BẢNG (TABLE)
        elif isinstance(block, Table):
            table = block
            new_table = new_doc.add_table(rows=len(table.rows), cols=len(table.columns), style='Table Grid')
            for i, row in enumerate(table.rows):
                for j, cell in enumerate(row.cells):
                    new_table.cell(i, j).text = cell.text
    
    new_doc.save(output_path)

# --- CÁCH SỬ DỤNG ---
# Thay đổi đường dẫn file input và output cho phù hợp
try:
    format_document_ordered('document/gan_chuan.docx', 'document_formatted/gan_chuan_formatted_v2.docx')
    print("Hoàn tất định dạng tài liệu thành công!")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")