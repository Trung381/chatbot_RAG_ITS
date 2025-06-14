import os
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx
from unstructured.partition.html import partition_html
from unstructured.partition.md import partition_md
from unstructured.documents.elements import Title, NarrativeText, ListItem, Table, Text, Element
from schema.Chunk import Chunk
from chain import restructure

def merge_chunk_processor(chunk_id, chunks, nodes):
    childs = nodes[chunk_id].get("childrens", None)
    if not childs: # Neu het node con (cap nho nhat roi)
        return chunk_id

    leaf_ids = [merge_chunk_processor(id, chunks, nodes) for id in childs]

    i, j = 0, 1
    while (i < len(leaf_ids) and j < len(leaf_ids) - 1):
        chunk_1 = chunks.get(leaf_ids[i])
        while chunk_1 and chunk_1.num_tokens() >= 500 and i < len(leaf_ids):
            i, j = i + 1, i + 2
            chunk_1 = chunks.get(leaf_ids[i])

        chunk_2 = chunks.get(leaf_ids[j])
        while chunk_2 and chunk_2.num_tokens() >= 500 and j < len(leaf_ids)-1:
            j += 1
            chunk_2 = chunks.get(leaf_ids[j])

        if chunk_1 and chunk_2 and chunk_1.merge_chunk(chunk_2): # merged
            chunks.pop(chunk_2.title_id, None)
            j += 1
        else:
            i, j = j + 1, j + 2

    parent_chunk = chunks.get(chunk_id)
    if parent_chunk:
        for child_id in leaf_ids:
            if child_id != chunk_id:
                child_chunk = chunks.get(child_id)
                if child_chunk and child_chunk.num_tokens() < 500:
                    if parent_chunk.merge_chunk(child_chunk):
                        chunks.pop(child_id, None)

    return chunk_id

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

    match file_ext:
        case ".pdf":
            elements = partition_pdf(file_path,  languages=["vie", "eng"], **common_kwargs)
        case ".docx":
            elements = partition_docx(file_path, **common_kwargs)
        case ".html":
            elements = partition_html(filename=file_path)
        case ".md":
            elements = partition_md(filename=file_path, **common_kwargs)
        case _: raise ValueError("Loại file không được hỗ trợ. Vui lòng sử dụng .pdf, .docx, .md hoặc .html")

    chunks = dict()
    current_chunk = None
    titles = dict()

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

    tree_title = restructure(titles)
    # print(tree_title)
    for root_id in tree_title["roots"]:
        merge_chunk_processor(root_id, chunks, tree_title["nodes"])

    return chunks

# --- VÍ DỤ SỬ DỤNG ---
try:
    file_path = "output.md"  # thay đổi sang .pdf, .docx, .md hoặc .html
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: '{file_path}'. Vui lòng tạo file này hoặc thay đổi đường dẫn.")

    chunks = chunk_by_title(file_path)

    print(f"Đã tìm thấy {len(chunks)} chunks từ file '{file_path}'.\n")
    for i, key in enumerate(chunks):
        print(f"=== CHUNK {i+1} ===")
        print(f"Title: {chunks[key].title_id}")
        print(f"Title: {chunks[key].title}")
        print(f"Content:\n{chunks[key].content}")
        print("-" * 20)

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
    print("Hãy chắc chắn rằng bạn đã cài đặt tất cả các thư viện cần thiết.")