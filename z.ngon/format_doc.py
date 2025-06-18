import docx 
import re 
from docx.document import Document 
from docx.oxml.text.paragraph import CT_P 
from docx.oxml.table import CT_Tbl 
from docx.text.paragraph import Paragraph 
from docx.table import Table 
from enum import Enum 

class ParagraphType(Enum): 
    HEADING = "heading" 
    NORMAL = "normal" 
    QUOTE = "quote" 
    EMPTY = "empty" 
    LIST = "list" 


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
        return ParagraphType.EMPTY, None, None

    # **ƯU TIÊN 1: KIỂM TRA DANH SÁCH TỰ ĐỘNG**
    # Logic này không thay đổi
    is_auto_list = False
    try:
        if para._p.pPr.numPr is not None:
            is_auto_list = True
    except AttributeError:
        is_auto_list = False

    if is_auto_list:
        if is_paragraph_bold(para):
            level = 1
            try:
                level = para._p.pPr.numPr.ilvl.val + 1
                if level > 6: level = 6
            except AttributeError:
                level = 2
            return ParagraphType.HEADING, level, text
        else:
            return ParagraphType.LIST, None, text

    # **ƯU TIÊN 2: KIỂM TRA HEADING/LIST GÕ THỦ CÔNG (DÙNG REGEX ĐÃ NÂNG CẤP)**
    # Logic này được cập nhật để nhận cả chỉ mục số và chữ.
    
    # Pattern mới: nhận diện chuỗi số (1.1) HOẶC chuỗi chữ (a.b) ở đầu dòng.
    # - Nhóm 1: (\d+(\.\d+)*) -> khớp "1", "1.1", "1.1.1"
    # - Nhóm 2: ([a-z](\.[a-z])*) -> khớp "a", "a.b", "a.b.c" (re.I để không phân biệt hoa thường)
    # - ( ... | ... ) -> kết hợp cả hai
    heading_pattern = re.compile(r'^((?:\d+(?:\.\d+)*)|(?:[a-z](?:\.[a-z])*))\.?\s+', re.IGNORECASE)
    match = heading_pattern.match(text)
    
    if match:
        # group(1) sẽ là toàn bộ phần chỉ mục, ví dụ "1.1.1" hoặc "a.b.c"
        index_part = match.group(1)
        # làm sạch text để trả về nội dung không bao gồm chỉ mục
        # clean_text = text[len(match.group(0)):].strip()

        # Đếm số dấu chấm để xác định cấp độ
        level = index_part.count('.') + 1
        if level > 6: level = 6

        # --- LOGIC MỚI THEO YÊU CẦU ---
        # 1. Nếu cấp độ lớn hơn 1 (1.1, a.b, ...) -> Luôn là HEADING
        if level > 1:
            # return ParagraphType.HEADING, level, clean_text
            return ParagraphType.HEADING, level, text
        # 2. Nếu cấp độ bằng 1 (1., a., ...) -> Chỉ là HEADING nếu in đậm
        else: # level == 1
            if is_paragraph_bold(para):
                # return ParagraphType.HEADING, level, clean_text
                return ParagraphType.HEADING, level, text
            else:
                # Nếu không in đậm, coi là một mục danh sách (LIST)
                # Trả về text gốc để logic sau có thể dọn dẹp ký tự đầu dòng
                return ParagraphType.LIST, None, text

    # **ƯU TIÊN 3: HEADING DẠNG CHỮ, KHÔNG ĐÁNH SỐ**
    # Ngưỡng 50 từ là hợp lý để tránh các đoạn văn dài được in đậm
    if is_paragraph_bold(para) and len(text.split()) < 50:
        level = 1 if text.isupper() else 2
        return ParagraphType.HEADING, level, text

    # **ƯU TIÊN 4: LIST GÕ THỦ CÔNG DẠNG KÝ TỰ**
    # Pattern cho list: *, -, i., v. (La Mã)
    # Pattern này được giữ lại để bắt các trường hợp không khớp heading ở trên
    list_pattern = re.compile(r'^((\w\.|[ivx]+\.)|([*\-•]))\s', re.I)
    if list_pattern.match(text):
        return ParagraphType.LIST, None, text

    # **MẶC ĐỊNH: VĂN BẢN THƯỜNG**
    return ParagraphType.NORMAL, None, text


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
            # Đoạn này đã được sửa để lấy content đã được làm sạch từ analyze_paragraph
            # cũng như kiểm tra các style heading mặc định của Word.
            if (block.style.name.startswith('Heading')): 
                try:
                    level = int(block.style.name[-1])
                except:
                    level = 1 # Mặc định nếu không lấy được số từ tên style
                para_type, content = ParagraphType.HEADING, block.text.strip() 
            else: 
                para_type, level, content = analyze_paragraph(block) 

            if para_type == ParagraphType.HEADING: 
                new_doc.add_heading(content, level=level) 
            elif para_type == ParagraphType.LIST: 
                # Làm sạch ký tự đầu dòng nếu có (cho trường hợp gõ tay) 
                clean_content = re.sub(r'^(?:(?:\d+(?:\.\d+)*)|(?:[a-z](?:\.[a-z])*)|[ivx]+)\.?\s*|([*\-•])\s*', '', content, re.I).strip()
                new_doc.add_paragraph(clean_content, style='List Bullet') 
            elif para_type == ParagraphType.NORMAL: 
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
FILE_NAME = 'gan_chuan' 
try: 
    # Hãy đảm bảo đường dẫn file là chính xác 
    input_file = f'document/{FILE_NAME}.docx' 
    output_file = f'document_formatted/{FILE_NAME}.docx' 
    format_document_ordered(input_file, output_file) 
    print(f"Hoàn tất định dạng tài liệu thành công! File đã được lưu tại: {output_file}") 
except FileNotFoundError: 
    print(f"Lỗi: Không tìm thấy file đầu vào tại '{input_file}'. Vui lòng kiểm tra lại đường dẫn.") 
except Exception as e: 
    print(f"Đã xảy ra lỗi không mong muốn: {e}")