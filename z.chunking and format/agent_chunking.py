from langchain_experimental.text_splitter import SemanticChunker # Sẽ không dùng trực tiếp nữa
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from temp_test import * # Giả sử file này chứa hàm parse_document_sequential

os.environ["OPENAI_API_KEY"] = "" # Thay bằng API KEY của bạn

# Hàm sử dụng Agent (LLM) để xem xét và chia lại chunks
def rechunk_with_agent(full_document_content: str, model_name: str = "gpt-3.5-turbo-0125") -> list[str]:
    """
    Sử dụng LLM làm agent để chia toàn bộ nội dung tài liệu thành các chunks lớn hơn,
    tập trung vào các đề mục chính.
    """
    print("=== AGENTIC CHUNKING (Revised for Larger Chunks) ===")
    if not full_document_content.strip():
        print("Document content is empty.")
        return []

    # --- Thiết kế Prompt cho Agent (ĐÃ CẬP NHẬT) ---
    system_prompt = """Bạn là một chuyên gia phân tích và biên tập tài liệu có cấu trúc.
Nhiệm vụ của bạn là nhận toàn bộ nội dung của một tài liệu và chia nó thành các chunks (đoạn) lớn, mạch lạc về ngữ nghĩa, dựa trên cấu trúc đề mục chính của tài liệu.
Các chunks mới cần đảm bảo các tiêu chí sau:
1.  **Theo Đề Mục Chính:** Cố gắng tạo mỗi chunk tương ứng với một đề mục lớn (ví dụ: Chương 1, Chương 2, hoặc các mục chính như 1.1, 1.2, 2.1).
    * Nếu một đề mục chính (ví dụ: 1.1) có các tiểu mục con (ví dụ: 1.1.1, 1.1.2), hãy gộp tất cả các tiểu mục con này vào chung chunk với đề mục cha của chúng (tức là toàn bộ nội dung từ đầu mục 1.1 đến trước mục 1.2 sẽ là một chunk).
    * Chỉ chia nhỏ hơn một đề mục chính nếu đề mục đó quá dài và chứa nhiều ý tưởng rất khác biệt mà không thể gộp chung một cách hợp lý.
2.  **Ngữ cảnh Toàn vẹn:** Mỗi chunk nên cung cấp đủ ngữ cảnh về chủ đề nó bao hàm.
3.  **Độ dài Cân đối:** Ưu tiên các chunks lớn hơn là các chunks quá nhỏ và chi tiết. Một chunk có thể kéo dài nhiều đoạn văn nếu chúng cùng thuộc một đề mục chính.
4.  **Ranh giới Rõ ràng:** Chia tại các điểm chuyển tiếp giữa các chương hoặc các mục lớn.
5.  **Bao quát Toàn bộ:** Đảm bảo không bỏ sót nội dung nào của tài liệu gốc.

Mục tiêu là tạo ra các chunks đủ lớn để chứa đựng thông tin toàn diện về một phần chính của tài liệu, giúp người đọc (hoặc một AI khác) có cái nhìn tổng thể về phần đó.
"""

    human_prompt_template = """Dưới đây là toàn bộ nội dung của tài liệu:

--- BEGIN DOCUMENT CONTENT ---
{document_content}
--- END DOCUMENT CONTENT ---

Hãy chia lại toàn bộ nội dung trên thành các chunks mới, lớn hơn, dựa trên các đề mục chính và các tiêu chí đã nêu trong vai trò của bạn.
Quan trọng: Với mỗi chunk mới bạn tạo ra, hãy bắt đầu chunk đó bằng một dấu phân cách duy nhất là '======NEW CHUNK======'. Ví dụ:
======NEW CHUNK======
Nội dung của chunk thứ nhất (ví dụ: toàn bộ Chương 1 hoặc toàn bộ Mục 1.1 bao gồm các tiểu mục con của nó)...
======NEW CHUNK======
Nội dung của chunk thứ hai (ví dụ: toàn bộ Chương 2 hoặc toàn bộ Mục 1.2 bao gồm các tiểu mục con của nó)...
======NEW CHUNK======
...

Không thêm bất kỳ lời bình luận hay giải thích nào trước hoặc sau kết quả chia chunk của bạn, chỉ trả về các chunks được phân tách bằng '======NEW CHUNK======'.
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_prompt_template)
    ])

    # --- Khởi tạo LLM Agent ---
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
    llm = ChatOpenAI(model_name=model_name, temperature=0.0) # temperature=0.0 để kết quả nhất quán nhất có thể

    # --- Tạo chuỗi xử lý (Chain) ---
    chain = prompt | llm | StrOutputParser()

    print(f"Sending {len(full_document_content)} characters (approx. {len(full_document_content)/4} tokens) to LLM agent for re-chunking...") # Ước tính token thô
    
    # !!! CẢNH BÁO VỀ GIỚI HẠN CONTEXT WINDOW VÀ CHI PHÍ !!!
    # Vẫn cần lưu ý giới hạn context window. GPT-3.5-turbo là 16K tokens.
    # Nếu tài liệu của bạn lớn hơn nhiều (ví dụ, một cuốn sách vài trăm trang), bạn cần
    # một bước chia sơ bộ thành các phần lớn (ví dụ, từng chương) trước khi đưa vào đây.

    try:
        agent_response = chain.invoke({"document_content": full_document_content})
    except Exception as e:
        print(f"Error calling LLM agent: {e}")
        # Nếu có lỗi, bạn có thể muốn có một chiến lược fallback, ví dụ:
        # sử dụng một phương pháp chunking đơn giản hơn như RecursiveCharacterTextSplitter
        # return fallback_chunking_method(full_document_content) 
        raise e

    # --- Xử lý kết quả từ Agent ---
    refined_chunks_text = []
    if agent_response:
        raw_chunks = agent_response.split("======NEW CHUNK======")
        for raw_chunk in raw_chunks:
            cleaned_chunk = raw_chunk.strip() 
            if cleaned_chunk: 
                refined_chunks_text.append(cleaned_chunk)
    
    print("\n=== AGENTIC RE-CHUNKED RESULT (Larger Chunks) ===")
    for i, chunk_text in enumerate(refined_chunks_text):
        print(f"[Refined Agentic Chunk {i+1}]\n{chunk_text}\n")
    print(f"Total refined agentic chunks: {len(refined_chunks_text)}\n")
    
    return refined_chunks_text

# Gọi xử lý thử
if __name__ == "__main__":
    filepath = "document/test_lien.docx" # Hoặc file PDF của bạn
    
    print(f"Processing document: {filepath}")
    content = parse_document_sequential(filepath) 

    if content and content.strip(): 
        # Bước 1: Không cần initial_semantic_chunking nữa nếu toàn bộ content có thể xử lý bởi agent
        # Chúng ta sẽ đưa thẳng toàn bộ `content` cho agent.
        
        # Ước tính số token (rất thô, chỉ để tham khảo)
        # Một token thường tương ứng với khoảng 4 ký tự trong tiếng Anh. 
        # Tiếng Việt có thể khác, nhưng đây là một ước tính.
        estimated_tokens = len(content) / 2.5 # Ước tính rộng hơn cho tiếng Việt
        print(f"Estimated tokens for the entire document: {int(estimated_tokens)}")
        
        # Kiểm tra sơ bộ nếu có vẻ quá lớn cho gpt-3.5-turbo (16385 tokens)
        # Chừa khoảng 1000-2000 tokens cho prompt và output
        if estimated_tokens > 14000: # Ngưỡng an toàn
            print("Warning: Document might be too large for a single gpt-3.5-turbo call.")
            print("Consider implementing a pre-splitting step for very large documents (e.g., by chapter).")
            # Tại đây bạn có thể quyết định dừng, hoặc thử chạy và chấp nhận rủi ro lỗi context window
            # Hoặc triển khai logic chia sơ bộ tài liệu thành các phần lớn hơn nếu cần.
            # For now, we'll proceed, but this is a critical check for production.

        # Sử dụng Agent để chia lại toàn bộ nội dung
        refined_chunks = rechunk_with_agent(content, model_name="gpt-3.5-turbo") 
        # Bạn có thể thay model_name="gpt-4o" hoặc "gpt-4-turbo" để có kết quả tốt hơn, nhưng chi phí cao hơn
        
        print("--- FINAL REFINED CHUNKS (after agent review for larger chunks) ---")
        if refined_chunks:
            for i, chunk in enumerate(refined_chunks):
                print(f"Final Chunk {i+1} (Length: {len(chunk)} chars):\n{chunk}\n----------")
        else:
            print("Agent did not return any refined chunks.")
            # Có thể thêm logic fallback ở đây nếu muốn
    else:
        print("Document is empty or could not be parsed.")




# from langchain_text_splitters import RecursiveCharacterTextSplitter # Thay thế SemanticChunker cho bước sơ bộ
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# import os
# from temp_test import * # Giả sử file này chứa hàm parse_document_sequential
# import tiktoken # Để ước tính token chính xác hơn (tùy chọn nhưng tốt hơn)

# os.environ["OPENAI_API_KEY"] = "" # Thay bằng API KEY của bạn

# # Hàm ước tính số token cho một đoạn văn bản sử dụng tiktoken (cho các model OpenAI)
# def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
#     """Trả về số lượng token trong một chuỗi văn bản."""
#     try:
#         encoding = tiktoken.get_encoding(encoding_name)
#         num_tokens = len(encoding.encode(string))
#         return num_tokens
#     except Exception:
#         # Fallback nếu tiktoken có vấn đề hoặc cho model không phải OpenAI
#         return len(string) // 3 # Ước tính thô: 3 ký tự ~ 1 token

# # Hàm chia tài liệu thành các phân đoạn lớn (coarse segments)
# def split_into_coarse_segments(text: str, model_name_for_agent: str = "gpt-3.5-turbo", target_tokens_per_segment: int = 10000) -> list[str]:
#     """
#     Chia văn bản thành các phân đoạn lớn, mỗi phân đoạn gần với target_tokens_per_segment.
#     Sử dụng RecursiveCharacterTextSplitter.
#     """
#     print(f"=== COARSE-GRAINED PRE-CHUNKING (Targeting ~{target_tokens_per_segment} tokens/segment) ===")
    
#     # Ước tính số ký tự dựa trên số token mục tiêu
#     # Con số này có thể cần điều chỉnh tùy theo ngôn ngữ và tokenizer
#     # Ví dụ: 1 token ~ 2.5-4 ký tự. Chọn một giá trị an toàn, ví dụ 3.
#     # Cho tiếng Việt, 1 token có thể là 1 âm tiết, nên số ký tự/token có thể thấp hơn tiếng Anh.
#     # Thử nghiệm với giá trị chars_per_token thấp hơn, ví dụ 2.5
#     chars_per_token_estimate = 2.5 
#     char_chunk_size = int(target_tokens_per_segment * chars_per_token_estimate)
#     char_chunk_overlap = int(char_chunk_size * 0.1) # Overlap 10%

#     print(f"RecursiveCharacterTextSplitter: char_chunk_size={char_chunk_size}, char_chunk_overlap={char_chunk_overlap}")

#     r_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=char_chunk_size,
#         chunk_overlap=char_chunk_overlap,
#         separators=["\n\n\n", "\n\n", "\n", ". ", " ", ""], # Ưu tiên các dấu ngắt đoạn lớn
#         length_function=len # Sử dụng số ký tự cho chunk_size
#     )
    
#     coarse_segments = r_splitter.split_text(text)
    
#     print(f"Document split into {len(coarse_segments)} coarse segments.")
#     for i, segment in enumerate(coarse_segments):
#         segment_tokens = num_tokens_from_string(segment, "cl100k_base" if "gpt" in model_name_for_agent else "p50k_base")
#         print(f"Coarse Segment {i+1}: Length={len(segment)} chars, Approx Tokens={segment_tokens}")
#     print("---")
#     return coarse_segments

# # Hàm sử dụng Agent (LLM) để xem xét và chia lại một phân đoạn văn bản
# def rechunk_segment_with_agent(text_segment_to_refine: str, model_name: str = "gpt-3.5-turbo") -> list[str]:
#     """
#     Sử dụng LLM làm agent để chia một phân đoạn văn bản thành các chunks tối ưu.
#     Prompt đã được tổng quát hóa.
#     """
#     print(f"=== AGENTIC RE-CHUNKING FOR SEGMENT (Length: {len(text_segment_to_refine)} chars) ===")
#     if not text_segment_to_refine.strip():
#         print("Text segment is empty.")
#         return []

#     # --- Thiết kế Prompt cho Agent (ĐÃ CẬP NHẬT - Tổng quát hơn) ---
#     system_prompt = """Bạn là một chuyên gia phân tích và biên tập tài liệu thông minh.
# Nhiệm vụ của bạn là nhận một đoạn văn bản (có thể là một phần của một tài liệu lớn hơn) và chia nó thành các chunks (đoạn) mới, tối ưu nhất.
# Các chunks mới cần đảm bảo các tiêu chí sau:
# 1.  **Mạch lạc về Ngữ nghĩa:** Mỗi chunk nên tập trung vào một chủ đề, một ý tưởng hoặc một dòng suy nghĩ chính liên tục và riêng biệt. Tránh trộn lẫn nhiều chủ đề không liên quan chặt chẽ trong cùng một chunk.
# 2.  **Tính Toàn vẹn:** Cố gắng giữ cho các ý tưởng, luận điểm hoặc các bước trong một quy trình được trình bày trọn vẹn trong cùng một chunk nếu có thể. Đừng cắt ngang đột ngột giữa chừng một câu hoặc một ý quan trọng, trừ khi đó là điểm chuyển sang một chủ đề mới rõ rệt.
# 3.  **Kích thước Hợp lý:** Các chunks nên đủ lớn để cung cấp ngữ cảnh cần thiết và chứa đựng một lượng thông tin đáng kể, nhưng không quá dài đến mức trở nên dàn trải hoặc bao gồm quá nhiều điểm không liên quan. Hãy tìm sự cân bằng, tránh tạo ra các chunks quá vụn vặt hoặc quá bao quát.
# 4.  **Ranh giới Tự nhiên:** Ưu tiên việc chia tại các điểm ngắt tự nhiên trong văn bản, ví dụ như khi có sự chuyển đổi rõ ràng về chủ đề, kết thúc một phần giải thích, hoặc trước khi bắt đầu một luận điểm mới. Nếu tài liệu có các dấu hiệu cấu trúc như tiêu đề phụ hoặc đoạn văn được phân tách rõ ràng, hãy cân nhắc sử dụng chúng làm gợi ý, nhưng không bắt buộc phải tuân theo một cách máy móc nếu việc đó làm giảm chất lượng ngữ nghĩa của chunk.
# 5.  **Bao quát Toàn bộ:** Đảm bảo toàn bộ nội dung của đoạn văn bản đầu vào được bao phủ bởi các chunks mới bạn tạo ra, không bỏ sót thông tin.

# Mục tiêu là tạo ra các chunks chất lượng cao, dễ hiểu, và hữu ích cho việc truy xuất thông tin hoặc cung cấp ngữ cảnh cho các tác vụ xử lý ngôn ngữ tiếp theo.
# """

#     human_prompt_template = """Dưới đây là một đoạn văn bản cần được chia lại:

# --- BEGIN TEXT SEGMENT ---
# {document_segment}
# --- END TEXT SEGMENT ---

# Hãy chia lại toàn bộ nội dung của đoạn văn bản trên thành các chunks mới, tối ưu nhất theo các tiêu chí đã nêu trong vai trò của bạn.
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

#     if not os.getenv("OPENAI_API_KEY"):
#         raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
#     llm = ChatOpenAI(model_name=model_name, temperature=0.0) 

#     chain = prompt | llm | StrOutputParser()
    
#     segment_tokens = num_tokens_from_string(text_segment_to_refine, "cl100k_base" if "gpt" in model_name else "p50k_base")
#     print(f"Sending segment of {len(text_segment_to_refine)} chars (Approx Tokens: {segment_tokens}) to LLM agent...")
    
#     # Context window check (GPT-3.5-turbo has 16385 tokens)
#     # Prompt itself also consumes tokens. A safe margin is good.
#     # The coarse chunker should ideally handle this, but a check here is also useful.
#     # Max input tokens for gpt-3.5-turbo is 16385. We need space for prompt and output.
#     # Let's say max input content tokens = 14000.
#     if segment_tokens > 14000 and "3.5-turbo" in model_name: # Check specific to 3.5-turbo's known limit
#          print(f"Warning: Segment with {segment_tokens} tokens might be too large for {model_name}'s context window after accounting for prompt tokens. Trying anyway...")
#     elif segment_tokens > 100000 and ("gpt-4" in model_name or "gpt-4o" in model_name) : # gpt-4 models have larger context
#          print(f"Warning: Segment with {segment_tokens} tokens is very large, even for GPT-4 models. Trying anyway...")


#     try:
#         agent_response = chain.invoke({"document_segment": text_segment_to_refine})
#     except Exception as e:
#         print(f"Error calling LLM agent for segment: {e}")
#         # Fallback: return the segment itself as a single chunk if agent fails
#         print("Fallback: Returning the original segment as one chunk due to agent error.")
#         return [text_segment_to_refine.strip()] if text_segment_to_refine.strip() else []

#     refined_chunks_text = []
#     if agent_response:
#         raw_chunks = agent_response.split("======NEW CHUNK======")
#         for raw_chunk in raw_chunks:
#             cleaned_chunk = raw_chunk.strip() 
#             if cleaned_chunk: 
#                 refined_chunks_text.append(cleaned_chunk)
    
#     print(f"Segment re-chunked into {len(refined_chunks_text)} refined chunks.")
#     for i, chunk_text in enumerate(refined_chunks_text):
#         print(f"  [Refined Sub-Chunk {i+1} from Agent]\n  {chunk_text[:100]}...\n") # Print only a preview
#     print("---")
    
#     return refined_chunks_text

# # Gọi xử lý thử
# if __name__ == "__main__":
#     filepath = "document/test_border.pdf" # Hoặc file PDF của bạn
#     # filepath = "document/Workflow.pdf"
#     # filepath = "document/SQL_Server_Advanced_Troubleshooting_and_Performance_Tuning_Dmitri.pdf" # Thử với file lớn hơn
    
#     # Cấu hình cho agent
#     AGENT_MODEL_NAME = "gpt-3.5-turbo" # Hoặc "gpt-4o", "gpt-4-turbo"
#     # GPT-3.5-turbo context window is 16,385 tokens.
#     # Để an toàn, target tokens cho mỗi phân đoạn lớn để agent xử lý nên nhỏ hơn, ví dụ 10,000 - 12,000 tokens.
#     # Điều này để lại không gian cho prompt và output của LLM.
#     TARGET_TOKENS_PER_COARSE_SEGMENT = 10000 


#     print(f"Processing document: {filepath} with agent model: {AGENT_MODEL_NAME}")
#     content = parse_document_sequential(filepath) 

#     all_refined_chunks = []

#     if content and content.strip(): 
#         document_tokens = num_tokens_from_string(content, "cl100k_base" if "gpt" in AGENT_MODEL_NAME else "p50k_base")
#         print(f"Total document tokens (estimated): {document_tokens}")

#         # Bước 1: Chia tài liệu thành các phân đoạn lớn (coarse segments)
#         # Điều này đặc biệt quan trọng nếu toàn bộ tài liệu quá lớn cho một lần gọi LLM agent.
#         coarse_segments = split_into_coarse_segments(
#             content, 
#             model_name_for_agent=AGENT_MODEL_NAME, 
#             target_tokens_per_segment=TARGET_TOKENS_PER_COARSE_SEGMENT
#         )

#         # Bước 2: Sử dụng Agent để chia lại từng phân đoạn lớn
#         for i, segment in enumerate(coarse_segments):
#             print(f"\nProcessing Coarse Segment {i+1}/{len(coarse_segments)} with Agent...")
#             refined_chunks_from_segment = rechunk_segment_with_agent(segment, model_name=AGENT_MODEL_NAME)
#             all_refined_chunks.extend(refined_chunks_from_segment)
        
#         print("\n\n--- FINAL AGENT-REFINED CHUNKS (from all segments) ---")
#         if all_refined_chunks:
#             for i, chunk in enumerate(all_refined_chunks):
#                 chunk_tokens = num_tokens_from_string(chunk, "cl100k_base" if "gpt" in AGENT_MODEL_NAME else "p50k_base")
#                 print(f"Final Chunk {i+1} (Length: {len(chunk)} chars, Approx Tokens: {chunk_tokens}):\n{chunk}\n----------")
#             print(f"Total final refined chunks: {len(all_refined_chunks)}")
#         else:
#             print("Agent did not return any refined chunks for any segment.")
#             # Fallback: có thể sử dụng lại các coarse_segments hoặc một phương pháp chunking đơn giản hơn
#             # print("Fallback: Using coarse segments as final chunks.")
#             # for i, seg in enumerate(coarse_segments):
#             #    print(f"Coarse Segment (Fallback) {i+1}:\n{seg}\n----------")

#     else:
#         print("Document is empty or could not be parsed.")