import docx
import re
from docx.document import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.text.paragraph import Paragraph
from docx.table import Table

# --- CÁC HÀM XỬ LÝ LOGIC ---

def iter_block_items(parent):
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    else:
        raise ValueError("Parent type is not supported")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def is_paragraph_bold(paragraph):
    runs_with_text = [run for run in paragraph.runs if run.text.strip()]
    if not runs_with_text:
        return False
    return all(run.bold for run in runs_with_text)

# --- NHẬN DIỆN NHỮNG PHẦN NGƯỜI DÙNG KHÔNG NHẬP ---

def analyze_paragraph(para):
    """
    Phân tích một paragraph để xác định loại của nó (heading, list, normal, empty).
    Hàm này kết hợp kiểm tra định dạng (list tự động) và nội dung (regex).
    Trả về: (type, level, text)
    Ví dụ: ('heading', 1, 'Nội dung tiêu đề'), ('list', None, 'Nội dung mục'), ('normal', None, 'Văn bản thường')
    """
    text = para.text.strip()
    if not text:
        return 'empty', None, None

    # **ƯU TIÊN 1: KIỂM TRA DANH SÁCH TỰ ĐỘNG**
    # Kiểm tra sự tồn tại của thuộc tính numbering trong XML của paragraph.
    is_auto_list = False
    try:
        if para._p.pPr.numPr:
            is_auto_list = True
    except AttributeError:
        is_auto_list = False

    if is_auto_list:
        # Nếu là danh sách tự động, dùng độ đậm để phân biệt heading và list item
        if is_paragraph_bold(para):
            level = 1
            try:
                # Lấy cấp độ danh sách (indentation level) từ XML, cộng 1 để thành heading level
                level = para._p.pPr.numPr.ilvl.val + 1
                if level > 6: level = 6 # Giới hạn heading level
            except AttributeError:
                level = 2 # Nếu không lấy được, mặc định là level 2 cho các mục con in đậm
            return 'heading', level, text
        else:
            return 'list', None, text

    # **ƯU TIÊN 2: KIỂM TRA HEADING/LIST GÕ THỦ CÔNG (DÙNG REGEX)**
    # Logic này chỉ chạy khi không phải là danh sách tự động, lúc này para.text đáng tin cậy.
    
    # Pattern cho heading số: 1., 1.1, 1.1.1
    heading_pattern = re.compile(r'^(\d+(\.\d+)*)\.?\s')
    match = heading_pattern.match(text)
    if match:
        number_part = match.group(1)
        level = number_part.count('.') + 1
        if level > 6: level = 6
        clean_text = text[len(match.group(0)):].strip()
        
        # Nếu là heading cấp 1 gõ tay, vẫn cần in đậm để xác nhận
        if level == 1 and not is_paragraph_bold(para):
            return 'list', None, text # Coi là list item nếu không in đậm
        return 'heading', level, clean_text

    # **ƯU TIÊN 3: HEADING DẠNG CHỮ, KHÔNG ĐÁNH SỐ**
    # Ngưỡng 15 từ là hợp lý để tránh các đoạn văn dài được in đậm
    if is_paragraph_bold(para) and len(text.split()) < 15:
        level = 1 if text.isupper() else 2
        return 'heading', level, text

    # **ƯU TIÊN 4: LIST GÕ THỦ CÔNG DẠNG KÝ TỰ**
    # Pattern cho list: *, -, a., i.
    list_pattern = re.compile(r'^((\w\.|[ivx]+\.)|([*\-•]))\s', re.I)
    if list_pattern.match(text):
        return 'list', None, text

    # **MẶC ĐỊNH: VĂN BẢN THƯỜNG**
    return 'normal', None, text


# --- LOGIC XỬ LÝ CHÍNH ---

def format_document_ordered(input_path, output_path):
    """
    Đọc file docx, chuẩn hóa và ghi ra file mới với logic nhận diện đã được sửa lỗi.
    """
    doc = docx.Document(input_path)
    new_doc = docx.Document()

    for block in iter_block_items(doc):
        # A. XỬ LÝ NẾU KHỐI LÀ ĐOẠN VĂN (PARAGRAPH)
        if isinstance(block, Paragraph):
            para_type, level, content = analyze_paragraph(block)

            if para_type == 'heading':
                new_doc.add_heading(content, level=level)
            elif para_type == 'list':
                # Làm sạch ký tự đầu dòng nếu có (cho trường hợp gõ tay)
                clean_content = re.sub(r'^((\d+\.|\w\.|[ivx]+\.)|([*\-•]))\s*', '', content, re.I).strip()
                new_doc.add_paragraph(clean_content, style='List Bullet')
            elif para_type == 'normal':
                new_doc.add_paragraph(content, style='Normal')
            # Bỏ qua para_type == 'empty'

        # B. XỬ LÝ NẾU KHỐI LÀ BẢNG (TABLE)
        elif isinstance(block, Table):
            table = block
            new_table = new_doc.add_table(rows=len(table.rows), cols=len(table.columns), style='Table Grid')
            for i, row in enumerate(table.rows):
                for j, cell in enumerate(row.cells):
                    new_table.cell(i, j).text = cell.text
    
    new_doc.save(output_path)

# --- CÁCH SỬ DỤNG ---
try:
    # Hãy đảm bảo đường dẫn file là chính xác
    input_file = 'document/gan_chuan.docx'
    output_file = 'document_formatted/gan_chuan_formatted_fixed.docx'
    format_document_ordered(input_file, output_file)
    print(f"Hoàn tất định dạng tài liệu thành công! File đã được lưu tại: {output_file}")
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file đầu vào tại '{input_file}'. Vui lòng kiểm tra lại đường dẫn.")
except Exception as e:
    print(f"Đã xảy ra lỗi không mong muốn: {e}")