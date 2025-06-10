# import os
# import pdfplumber
# from docx import Document

# # ======================= #
# # --- DOC/PDF PARSING --- #
# # ======================= #

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

# # Đọc file PDF giữ đúng thứ tự paragraph/table
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

# # Hàm tổng: đọc file DOCX hoặc PDF
# def parse_document_sequential(filepath):
#     ext = os.path.splitext(filepath)[1].lower()
#     if ext == '.pdf':
#         return parse_pdf_sequential(filepath)
#     elif ext == '.docx':
#         return parse_docx_sequential(filepath)
#     else:
#         raise ValueError(f"Unsupported file type: {ext}")

# # ============================= #
# # --- CHUNKING WITH LANGCHAIN --- #
# # ============================= #
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings


# def split_text_with_langchain(text):
#     print("\n=== 🔹 STRUCTURE-AWARE CHUNKING (RecursiveCharacterTextSplitter) ===")
#     r_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50,
#         separators=["\n\n", "\n", ".", "!", "?", " ", ""]
#     )
#     structure_chunks = r_splitter.split_text(text)
#     for i, chunk in enumerate(structure_chunks):
#         print(f"\n[Structure Chunk {i+1}]\n{chunk}")

#     print("\n=== 🔸 SEMANTIC-AWARE CHUNKING (SemanticChunker) ===")
#     embeddings = OpenAIEmbeddings()  # Ensure you have API key in env
#     s_splitter = SemanticChunker(embeddings)
#     semantic_chunks = s_splitter.split_text(text)
#     for i, chunk in enumerate(semantic_chunks):
#         print(f"\n[Semantic Chunk {i+1}]\n{chunk}")

# # ======================= #
# # --- MAIN PROGRAM --- #
# # ======================= #

# if __name__ == "__main__":
#     os.environ["OPENAI_API_KEY"] = ""  # 🔑 Nhập API key ở đây

#     filepath = "document/test.pdf"  # Hoặc test.docx
#     content = parse_document_sequential(filepath)
#     print("📄 Full Parsed Content:\n", content)
#     split_text_with_langchain(content)


### -------------------------------------------------------------------

# from langchain_experimental.text_splitter import SemanticChunker
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# import os
# from temp_test import *

# # Thêm khóa API của OpenAI nếu bạn dùng SemanticChunker
# os.environ["OPENAI_API_KEY"] = ""  # Thay bằng API KEY của bạn

# # Hàm chia văn bản thành chunk theo structure và semantic
# def split_text_with_langchain(text):
#     print("=== STRUCTURE-AWARE CHUNKING ===")
#     r_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=0,
#         separators=["\n\n", "\n", ".", "!", "?", " ", ""]
#     )
#     structure_chunks = r_splitter.split_text(text)
#     for i, chunk in enumerate(structure_chunks):
#         print(f"[Structure Chunk {i+1}]\n{chunk}\n")

#     print("=== SEMANTIC-AWARE CHUNKING ===")
#     # Semantic chunking cần embedding để hiểu nội dung
#     embeddings = OpenAIEmbeddings()
#     s_splitter = SemanticChunker(embeddings, min_chunk_size=500)
#     semantic_chunks = s_splitter.split_text(text)
#     for i, chunk in enumerate(semantic_chunks):
#         print(f"[Semantic Chunk {i+1}]\n{chunk}\n")

# # Gọi xử lý thử
# if __name__ == "__main__":
#     # filepath = "document/test_border.pdf"  # hoặc test.docx
#     filepath = "document/test_border.pdf"
#     # filepath = "document/SQL_Server_Advanced_Troubleshooting_and_Performance_Tuning_Dmitri.pdf"
#     content = parse_document_sequential(filepath)
#     split_text_with_langchain(content)





### -------------------------------------------------------------------

# import os
# from typing import List
# import pandas as pd

# # Unstructured
# from unstructured.partition.pdf import partition_pdf
# from unstructured.partition.docx import partition_docx

# # LangChain
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_openai import OpenAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # ==== CONFIGURATION ====
# os.environ["OPENAI_API_KEY"] = ""  # <-- Replace with your key

# # ==== UTILITIES ====

# def serialize_table(table: List[List[str]]) -> str:
#     """Chuyển bảng thành chuỗi tự nhiên gắn prefix [TABLE]"""
#     if not table or len(table) < 2:
#         return ""
#     headers = table[0]
#     rows = []
#     for row in table[1:]:
#         if len(row) != len(headers):
#             continue
#         row_text = ", ".join(f"{headers[i]}: {row[i]}" for i in range(len(headers)))
#         rows.append(row_text)
#     return "[TABLE] " + "\n".join(rows)


# # ==== STEP 1: UNSTRUCTURED PARSING ====

# def parse_with_unstructured(filepath: str) -> List[str]:
#     ext = os.path.splitext(filepath)[1].lower()
#     if ext == ".pdf":
#         elements = partition_pdf(filename=filepath)
#     elif ext == ".docx":
#         elements = partition_docx(filename=filepath)
#     else:
#         raise ValueError(f"Unsupported file type: {ext}")

#     chunks = []
#     for el in elements:
#         if el.category == "Table":
#             table_data = el.metadata.text_as_html or el.text
#             try:
#                 df = pd.read_html(table_data)[0]
#                 serialized = serialize_table([df.columns.tolist()] + df.values.tolist())
#             except Exception:
#                 serialized = f"[TABLE] {el.text.strip()}"
#             chunks.append(serialized)
#         else:
#             if el.text and el.text.strip():
#                 chunks.append(el.text.strip())
#     return chunks


# # ==== STEP 2: HYBRID CHUNKING ====

# def hybrid_chunking(blocks: List[str], chunk_token_threshold: int = 500) -> List[str]:
#     embeddings = OpenAIEmbeddings()
#     s_splitter = SemanticChunker(embeddings)

#     final_chunks = []
#     for block in blocks:
#         if block.startswith("[TABLE]"):
#             final_chunks.append(block)
#         elif len(block.split()) < chunk_token_threshold:
#             final_chunks.append(block)
#         else:
#             sub_chunks = s_splitter.split_text(block)
#             final_chunks.extend(sub_chunks)
#     return final_chunks


# # ==== STEP 3: FULL PIPELINE ====

# def process_document(filepath: str) -> List[str]:
#     raw_blocks = parse_with_unstructured(filepath)
#     final_chunks = hybrid_chunking(raw_blocks)
#     return final_chunks


# # ==== MAIN TEST ====

# if __name__ == "__main__":
#     filepath = "document/test.pdf"  # or "document/test.docx"
#     chunks = process_document(filepath)
#     for i, chunk in enumerate(chunks):
#         print(f"\n=== Chunk {i+1} ===\n{chunk}")





# from langchain.agents import Tool, initialize_agent
# from langchain.chat_models import ChatOpenAI
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_openai import OpenAIEmbeddings
# import os

# # Đảm bảo đã có API key
# os.environ["OPENAI_API_KEY"] = ""

# # Hàm chunk semantic (dùng embeddings)
# def semantic_chunking(text: str):
#     embeddings = OpenAIEmbeddings()
#     splitter = SemanticChunker(embeddings)
#     chunks = splitter.split_text(text)
#     return chunks

# # Tool cho agent gọi chunk semantic
# def chunk_tool_fn(text):
#     chunks = semantic_chunking(text)
#     return "\n\n".join(f"[Chunk {i+1}]\n{chunk}" for i, chunk in enumerate(chunks))

# chunk_tool = Tool(
#     name="Semantic Chunker",
#     func=chunk_tool_fn,
#     description="Dùng để chia văn bản thành các chunk semantic dựa trên embeddings."
# )

# # Khởi tạo LLM (GPT-4 hoặc GPT-3.5-turbo)
# llm = ChatOpenAI(model="gpt-4", temperature=0)

# # Tạo agent với tool chunking
# agent = initialize_agent(
#     tools=[chunk_tool],
#     llm=llm,
#     agent="zero-shot-react-description",
#     verbose=True
# )

# if __name__ == "__main__":
#     from temp_test import parse_document_sequential

#     filepath = "document/test.pdf"
#     text = parse_document_sequential(filepath)

#     # Gọi agent để chunk
#     print("=== Agent xử lý chunking ===")
#     output = agent.run(f"Hãy chia nội dung sau thành các chunk semantic:\n\n{text[:2000]}")  # giới hạn input cho agent nếu text dài
#     print(output)




# from langchain_experimental.text_splitter import SemanticChunker
# # from langchain.text_splitter import RecursiveCharacterTextSplitter # Hiện tại chưa dùng trong flow này
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# import os
# from temp_test import *


# os.environ["OPENAI_API_KEY"] = "" # Thay bằng API KEY của bạn

# # Hàm chia văn bản thành chunk ban đầu bằng Semantic Chunker
# def initial_semantic_chunking(text: str) -> list[str]:
#     """
#     Thực hiện chia văn bản thành các chunks ban đầu sử dụng SemanticChunker.
#     """
#     print("=== INITIAL SEMANTIC CHUNKING ===")
#     # Semantic chunking cần embedding để hiểu nội dung
#     # Sử dụng key từ môi trường
#     if not os.getenv("OPENAI_API_KEY"):
#         raise ValueError("OPENAI_API_KEY not found in environment variables.")
    
#     embeddings = OpenAIEmbeddings() # Mặc định sẽ tìm key OPENAI_API_KEY trong env
#     s_splitter = SemanticChunker(embeddings)
#     semantic_chunks = s_splitter.create_documents([text])
    
#     # Chuyển từ Document objects sang list of strings
#     semantic_chunks_text = [doc.page_content for doc in semantic_chunks]

#     for i, chunk_text in enumerate(semantic_chunks_text):
#         print(f"[Initial Semantic Chunk {i+1}]\n{chunk_text}\n")
#     print(f"Total initial semantic chunks: {len(semantic_chunks_text)}\n")
#     return semantic_chunks_text

# # Hàm sử dụng Agent (LLM) để xem xét và chia lại chunks
# def rechunk_with_agent(initial_chunks: list[str], model_name: str = "gpt-3.5-turbo") -> list[str]:
#     """
#     Sử dụng LLM làm agent để xem xét và có thể chia lại các chunks ban đầu.
#     """
#     print("=== AGENTIC RE-CHUNKING ===")
#     if not initial_chunks:
#         print("No initial chunks to process.")
#         return []

#     # Kết hợp tất cả các initial_chunks thành một văn bản lớn duy nhất
#     # Chúng ta sẽ yêu cầu agent chia lại TOÀN BỘ văn bản này
#     # thay vì yêu cầu agent sửa từng chunk riêng lẻ (việc này phức tạp hơn về prompt và xử lý)
#     full_text_from_initial_chunks = "\n\n".join(initial_chunks)

#     # --- Thiết kế Prompt cho Agent ---
#     system_prompt = """Bạn là một chuyên gia phân tích và biên tập tài liệu.
# Nhiệm vụ của bạn là nhận một đoạn văn bản lớn (đã được chia thành các chunk ban đầu) và chia lại toàn bộ văn bản đó thành một tập hợp các chunks mới, tối ưu nhất.
# Các chunks mới cần đảm bảo các tiêu chí sau:
# 1.  **Mạch lạc về ngữ nghĩa:** Mỗi chunk nên tập trung vào một chủ đề hoặc ý tưởng con rõ ràng, trọn vẹn.
# 2.  **Độ dài hợp lý:** Không quá dài gây khó hiểu, không quá ngắn làm mất ngữ cảnh. Ưu tiên các đoạn văn hoàn chỉnh.
# 3.  **Ranh giới tự nhiên:** Cố gắng chia tại các điểm ngắt tự nhiên trong văn bản (ví dụ: kết thúc một ý, chuyển sang ý mới).
# 4.  **Giữ trọn vẹn thông tin:** Tránh cắt ngang câu hoặc ý tưởng quan trọng.
# 5.  **Tính bao quát:** Đảm bảo toàn bộ nội dung của văn bản gốc được bao phủ bởi các chunks mới.

# Các chunk ban đầu có thể chưa tối ưu, đó là lý do bạn cần xem xét và phân chia lại toàn bộ.
# """

#     human_prompt_template = """Dưới đây là toàn bộ nội dung văn bản được tạo thành từ việc nối các chunk ban đầu:

# --- BEGIN DOCUMENT CONTENT ---
# {document_content}
# --- END DOCUMENT CONTENT ---

# Hãy chia lại toàn bộ nội dung trên thành các chunks mới, tối ưu nhất theo các tiêu chí đã nêu.
# Quan trọng: Với mỗi chunk mới bạn tạo ra, hãy bắt đầu chunk đó bằng một dấu phân cách duy nhất là '======NEW CHUNK======'. Ví dụ:
# ======NEW CHUNK======
# Nội dung của chunk thứ nhất...
# ======NEW CHUNK======
# Nội dung của chunk thứ hai...
# ======NEW CHUNK======
# ...

# Không thêm bất kỳ lời bình luận hay giải thích nào trước hoặc sau kết quả chia chunk của bạn, chỉ trả về các chunks được phân tách bằng '======NEW CHUNK======'.
# """
    
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", system_prompt),
#         ("human", human_prompt_template)
#     ])

#     # --- Khởi tạo LLM Agent ---
#     # Sử dụng key từ môi trường
#     if not os.getenv("OPENAI_API_KEY"):
#         raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
#     llm = ChatOpenAI(model_name=model_name, temperature=0.0) # temperature thấp để kết quả nhất quán hơn

#     # --- Tạo chuỗi xử lý (Chain) ---
#     chain = prompt | llm | StrOutputParser()

#     print(f"Sending {len(full_text_from_initial_chunks)} characters to LLM agent for re-chunking...")
    
#     # !!! CẢNH BÁO VỀ GIỚI HẠN CONTEXT WINDOW VÀ CHI PHÍ !!!
#     # Nếu `full_text_from_initial_chunks` quá lớn, nó có thể vượt quá giới hạn context window của LLM.
#     # Bạn có thể cần chiến lược xử lý phức tạp hơn (ví dụ: chia nhỏ `full_text_from_initial_chunks`
#     # và cho agent xử lý từng phần, nhưng điều này khó đảm bảo tính nhất quán toàn cục).
#     # Đồng thời, việc này có thể tốn kém chi phí API.

#     try:
#         agent_response = chain.invoke({"document_content": full_text_from_initial_chunks})
#     except Exception as e:
#         print(f"Error calling LLM agent: {e}")
#         # Có thể trả về chunks ban đầu nếu agent lỗi, hoặc xử lý lỗi khác
#         # return initial_chunks 
#         raise e # Hoặc raise lỗi để dừng chương trình

#     # --- Xử lý kết quả từ Agent ---
#     refined_chunks_text = []
#     if agent_response:
#         # Tách các chunks dựa trên delimiter đã yêu cầu
#         raw_chunks = agent_response.split("======NEW CHUNK======")
#         for raw_chunk in raw_chunks:
#             cleaned_chunk = raw_chunk.strip() # Loại bỏ khoảng trắng thừa ở đầu/cuối
#             if cleaned_chunk: # Chỉ thêm nếu chunk không rỗng
#                 refined_chunks_text.append(cleaned_chunk)
    
#     print("\n=== AGENTIC RE-CHUNKED RESULT ===")
#     for i, chunk_text in enumerate(refined_chunks_text):
#         print(f"[Refined Agentic Chunk {i+1}]\n{chunk_text}\n")
#     print(f"Total refined agentic chunks: {len(refined_chunks_text)}\n")
    
#     return refined_chunks_text

# # Gọi xử lý thử
# if __name__ == "__main__":
#     # filepath = "document/test_border.pdf"
#     filepath = "document/test_lien.docx"
#     # filepath = "document/SQL_Server_Advanced_Troubleshooting_and_Performance_Tuning_Dmitri.pdf"
    
#     print(f"Processing document: {filepath}")
#     content = parse_document_sequential(filepath) # Hàm này từ file temp_test.py của bạn

#     if content.strip(): # Chỉ xử lý nếu có nội dung
#         # Bước 1: Chia chunk ban đầu bằng Semantic Chunker
#         initial_chunks = initial_semantic_chunking(content)

#         # Bước 2: Sử dụng Agent để xem xét và chia lại (nếu cần)
#         # Bạn có thể chọn model khác nếu muốn, ví dụ "gpt-4o" hoặc "gpt-4-turbo" nếu có API access và muốn chất lượng cao hơn (chi phí cũng cao hơn)
#         refined_chunks = rechunk_with_agent(initial_chunks, model_name="gpt-3.5-turbo")
        
#         print("--- FINAL REFINED CHUNKS (after agent review) ---")
#         if refined_chunks:
#             for i, chunk in enumerate(refined_chunks):
#                 print(f"Final Chunk {i+1} (Length: {len(chunk)} chars):\n{chunk}\n----------")
#         else:
#             print("Agent did not return any refined chunks.")
#             print("Using initial semantic chunks as final chunks.")
#             # Fallback to initial_chunks if agent fails or returns empty
#             # (hoặc bạn có thể quyết định xử lý khác)
#             # for i, chunk in enumerate(initial_chunks):
#             #    print(f"Initial Semantic Chunk {i+1} (Length: {len(chunk)} chars):\n{chunk}\n----------")

#     else:
#         print("Document is empty or could not be parsed.")




# from unstructured.partition.pdf import partition_pdf
# from unstructured.partition.docx import partition_docx
# from unstructured.documents.elements import Title, NarrativeText

# def chunk_by_title(file_path: str):
#     # Chọn hàm partition tùy loại file
#     if file_path.endswith(".pdf"):
#         elements = partition_pdf(file_path)
#     elif file_path.endswith(".docx"):
#         elements = partition_docx(file_path)
#     else:
#         raise ValueError("Unsupported file type. Use .pdf or .docx")

#     chunks = []
#     current_chunk = {"title": None, "content": ""}

#     for el in elements:
#         if isinstance(el, Title):
#             # Nếu có title mới, lưu chunk cũ và bắt đầu chunk mới
#             if current_chunk["title"] or current_chunk["content"].strip():
#                 chunks.append(current_chunk)
#             current_chunk = {"title": el.text.strip(), "content": ""}
#         elif isinstance(el, NarrativeText):
#             current_chunk["content"] += el.text.strip() + "\n"

#     # Đừng quên lưu chunk cuối
#     if current_chunk["title"] or current_chunk["content"].strip():
#         chunks.append(current_chunk)

#     return chunks

# file_path = "test_border.pdf"
# chunks = chunk_by_title(file_path)

# # In kết quả
# for i, chunk in enumerate(chunks):
#     print(f"\n=== CHUNK {i+1} ===")
#     print(f"Title: {chunk['title']}")
#     print(f"Content:\n{chunk['content']}")





import tiktoken
from langchain_experimental.text_splitter import SemanticChunker
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import os
from temp_test import *

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-..."  # <-- Thay bằng key thật nếu chưa

# Tokenizer phù hợp với OpenAI models (GPT-3.5/4)
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text):
    return len(encoding.encode(text))

def split_text_with_langchain(text):
    print("=== STRUCTURE-AWARE CHUNKING ===")
    r_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=0,
        # separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        separators=["\n\n", "\n", " ", ""]
    )
    structure_chunks = r_splitter.split_text(text)
    for i, chunk in enumerate(structure_chunks):
        print(f"[Structure Chunk {i+1}] - {count_tokens(chunk)} tokens\n{chunk}\n")

    print("=== SEMANTIC-AWARE CHUNKING ===")
    embeddings = OpenAIEmbeddings()
    s_splitter = SemanticChunker(embeddings, min_chunk_size=500)
    semantic_chunks = s_splitter.split_text(text)
    for i, chunk in enumerate(semantic_chunks):
        print(f"[Semantic Chunk {i+1}] - {count_tokens(chunk)} tokens\n{chunk}\n")

# Main
if __name__ == "__main__":
    filepath = "document/test_border.pdf"
    content = parse_document_sequential(filepath)
    split_text_with_langchain(content)
