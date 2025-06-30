from unstructured.partition.html import partition_html
from unstructured.partition.md import partition_md
from unstructured.documents.elements import Title, NarrativeText, ListItem, Table, Text
import os
from chain.chain import restructure
from schema.Chunk import Chunk

# class Chunk:
#     def __init__(self, title_id=None, title="", content=""):
#         self.title_id = title_id
#         self.title = title
#         self.content = content

def merge_content(node, chunks, depth=0):
    '''
    Sau khi nhận respone cấu trúc lại đề mục từ ChatGPT, gọi hàm này để set lại content ứng với từng đề mục

    Tham số:
    - node: Dạng { 'title': <title>, 'content': <Nội dung của node hiện tại>, 'childen': <List các node con> } //Xem cấu trúc của GUIDE ở trên
    - chunks: DICT với key (title_id) và value (Chunk)
    '''
    if depth != 0:  # Không xét đề mục đầu tiên (tên file/đề mục level 0)
        node["content"] = chunks.get(node["titleId"]).content

    children = node.get("children", None)
    if not children: # Dừng khi children rỗng (duyệt đến đề mục cấp thấp nhất)
        if depth != 0:
            node["content"] = chunks.get(node["titleId"]).content
        return

    depth += 1
    for child in children:
        merge_content(child, chunks, depth)


def chunk_by_title(file_path: str) -> dict:
    """
    Phân tích một file .md hoặc .html và chia nhỏ nội dung dựa trên các tiêu đề (Title).

    Args:
        file_path: Đường dẫn đến file .md hoặc .html.

    Returns:
        Một DICT với cấu trúc như phần guide ở trên (https://colab.research.google.com/drive/1qQAXI8RxxfFm7CPXYkMs--7X8szsAj6Z#scrollTo=TbJHvXkfd5FG&line=3&uniqifier=1)
        Nội dung bảng sẽ được lưu dưới dạng HTML để giữ nguyên cấu trúc.
    """
    file_ext = os.path.splitext(file_path)[-1].lower()

    common_kwargs = {
        "strategy": "hi_res",
        "infer_table_structure": True,
    }

    match file_ext:
        case ".html":
            elements = partition_html(filename=file_path)
        case ".md":
            elements = partition_md(filename=file_path, **common_kwargs)
        case _: raise ValueError("Loại file không được hỗ trợ. Vui lòng sử dụng .md hoặc .html")

    chunks = dict()
    current_chunk = None
    titles = dict() # id - title
    titles["1"] = "Tài liệu ôn tập" # Sử dụng tên file, key tự do

    # unstructured đọc tài liệu => Trả về các element: https://docs.unstructured.io/open-source/concepts/document-elements
    for el in elements:
        match el:
            case Title():
                titles[el.id] = el.text.strip()
                if current_chunk:
                    chunks[current_chunk.title_id] = current_chunk
                current_chunk = Chunk(el.id, el.text.strip())
            case ListItem():
                if not current_chunk:
                    current_chunk = Chunk(el.id)
                current_chunk.content += f"- {el.text.strip()}\n"
            case Table():
                if not current_chunk:
                    current_chunk = Chunk(el.id)
                table_html = getattr(el.metadata, "text_as_html", None)
                if table_html:
                    current_chunk.content += f"\n{table_html}\n"
                else:
                    current_chunk.content += f"\n{el.text.strip()}\n"
            case Text() | NarrativeText():
                if not current_chunk:
                    current_chunk = Chunk(el.id)
                current_chunk.content += el.text.strip() + "\n"

    if current_chunk and current_chunk.title_id:
        chunks[current_chunk.title_id] = current_chunk

    node = restructure(titles)
    merge_content(node, chunks)

    return node


if __name__ == "__main__":
    data = chunk_by_title('document_formatted/Đường sắt Việt Nam.md') # .md hoặc .html
    '''Đưa data (DICT) vào chunk hoặc sử dụng cho mục đích khác'''

    # Ví dụ
    import json
    data = json.dumps(data, ensure_ascii=False, indent=4)
    print(data)
