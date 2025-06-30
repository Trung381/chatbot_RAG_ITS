import os
import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

# Tải các biến môi trường từ file .env (chứa OPENAI_API_KEY)
load_dotenv()

# --- Định nghĩa System Prompt ---
SYSTEM_PROMPT = f"""
    ### ROLE AND MAIN TASK

    You are a professional, precise, and reliable AI assistant. Your task is to ANALYZE the user's question and, BASED ONLY on the provided context chunks, generate an answer following the JSON format with 2 attributes is content and code (0: no answer, 1: have answer) and the strict rules below.

    ### PROVIDED CONTEXT

    {{context}}

    ### MANDATORY RULES

    YOU MUST STRICTLY FOLLOW the rules below when generating the answer:

    1. **READ AND SYNTHESIZE:** YOU MUST read, analyze, and synthesize information from ALL context chunks ([CONTEXT 1], [CONTEXT 2], etc.) to produce the most comprehensive answer possible. Do not omit any relevant information present in the context.

    2. **ABSOLUTE HONESTY:** Your answer MUST be entirely based on the information within the "PROVIDED CONTEXT". DO NOT infer, fabricate, guess, or use any external knowledge not present in the context.

    3. **HANDLE MISSING INFORMATION:** If none of the context chunks contain information relevant to answering the question, the `content` must be "".

    4. **HANDLE GENERAL QUESTIONS:** If the user's question is general AND you find multiple contexts covering different aspects, the `content` must be a clarifying question suggesting the topics found. Example: "Anh, chị muốn biết thông tin cụ thể nào về [topic]? Em tìm thấy thông tin về: [topic 1], [topic 2]..v.v"

    5. **ANSWER SPECIFIC QUESTIONS:** If the question is clear and relevant information is present, the `content` must be a complete, synthesized answer from ALL related contexts.

    6. **Tone Guideline:** When delivering the answer in `content`, please use a friendly and respectful Vietnamese tone, such as:
    - Start your reply with words like “Dạ”, “Vâng” or “Thông tin em tìm thấy là…”;
    - Write as if you are kindly assisting someone, but **do not** invent any facts outside the context.
    - Friendly closing such as “Anh, chị còn thắc mắc nào cần em hỗ trợ thêm không ạ?”, “Nếu anh, chị cần biết thêm thông tin gì, em sẵn lòng hỗ trợ tiếp ạ.” or “Nếu còn yêu cầu nào khác, anh, chị cứ nói để em hỗ trợ thêm ạ.” to maintain engagement.
    - You must always address the user as 'Anh, Chị' and refer to yourself as 'em'. Disregard any other forms of address or pronouns provided in the context, adhering strictly to 'Anh, Chị' for the user and 'em' for yourself.

    ### SELF-EVALUATION AND OUTPUT GENERATION PROCESS (IMPORTANT)

    Once you've determined the `content` based on the above rules, follow the process below to create the final output:

    **Step 1: Generate `content`.**  
    Reason using the context and the 'MANDATORY RULES' above to create the answer content.

    **IMPORTANT OVERRIDE:**  
    * If the user's question is general AND you find multiple contexts covering different aspects, you must ask the user for clarification (ACCORDING TO RULE 4).

    ### USER QUESTION

    {{question}}

    ### OUTPUT:
"""


def get_rag_response(context: str, question: str) -> dict:
    """
    Sử dụng LangChain và GPT-4o để phân tích context và question, trả về OUTPUT.

    Args:
        context (str): Chuỗi chứa các đoạn ngữ cảnh đã được truy xuất.
        question (str): Câu hỏi của người dùng.

    Returns:
        dict: Một dictionary Python với hai key là "content" và "confident".
              Trả về một dictionary lỗi nếu có vấn đề xảy ra.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY chưa được thiết lập. Vui lòng tạo file .env hoặc export biến môi trường.")

    # 1. Khởi tạo Model GPT-4o
    # temperature=0 để câu trả lời có tính nhất quán và bám sát chỉ dẫn cao nhất
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.6)

    # 2. Khởi tạo Output Parser để đảm bảo đầu ra luôn là JSON
    parser = JsonOutputParser()

    # 3. Tạo Prompt Template
    # Kết hợp system prompt và câu hỏi của người dùng
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}")
    ])

    # 4. Tạo chuỗi xử lý (Chain) bằng LangChain Expression Language (LCEL)
    chain = prompt | model | parser

    # 5. Thực thi chuỗi xử lý và xử lý lỗi
    try:
        response = chain.invoke({
            "context": context,
            "question": question
        })
        return response
    except Exception as e:
        print(f"Đã có lỗi không xác định xảy ra: {e}")
        return {"content": "Lỗi hệ thống: Không thể xử lý yêu cầu."}


# --- VÍ DỤ SỬ DỤNG ---
if __name__ == "__main__":
    # --- Trường hợp 1: Câu hỏi cụ thể, ngữ cảnh đầy đủ ---
    print("--- TRƯỜNG HỢP 1: CÂU HỎI CỤ THỂ ---")
    context_1 = """
    [NGỮ CẢNH 1]: Công dụng chính của thuốc Panadol Extra là giảm đau và hạ sốt. Các cơn đau được chỉ định bao gồm đau đầu, đau nửa đầu, đau cơ, đau bụng kinh.
    [NGỮ CẢNH 2]: Thành phần hoạt chất của Panadol Extra bao gồm 500mg Paracetamol và 65mg Caffeine. Caffeine giúp tăng cường tác dụng giảm đau của Paracetamol.
    [NGỮ CẢNH 3]: Panadol Extra vẫn có tác dụng phụ ở hệ tiêu hóa như buồn nôn, nôn, đau bụng, tiêu chảy,… hoặc ở hệ thần kinh như chóng mặt, mệt mỏi, lo lắng, bồn chồn, dễ kích động,…
    [NGỮ CẢNH 4]: Bạn phải sử dụng Panadol đúng liều lượng quy định trên vỏ thuốc là Người lớn (kể cả người cao tuổi) và trẻ em từ 12 tuổi trở lên: uống 1 hoặc 2 viên mỗi 4 đến 6 giờ nếu cần. Liều tối đa hàng ngày: 8 viên. Không khuyến nghị dùng thuốc này cho trẻ em dưới 12 tuổi.
    """
    question_1 = "Thành phần và công dụng của Panadol Extra là gì?"
    response_1 = get_rag_response(context_1, question_1)
    print(json.dumps(response_1, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    # --- Trường hợp 2: Câu hỏi chung chung, cần làm rõ ---
    print("--- TRƯỜNG HỢP 2: CÂU HỎI CHUNG CHUNG ---")
    context_2 = context_1 # Sử dụng lại context ở trên
    question_2 = "Cho tôi biết về Panadol Extra"
    response_2 = get_rag_response(context_2, question_2)
    print(json.dumps(response_2, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    # --- Trường hợp 3: Không có thông tin trong ngữ cảnh ---
    print("--- TRƯỜNG HỢP 3: THIẾU THÔNG TIN ---")
    context_3 = context_1 # Sử dụng lại context ở trên
    question_3 = "Liều dùng của Panadol Extra cho trẻ em là bao nhiêu?"
    response_3 = get_rag_response(context_3, question_3)
    print(json.dumps(response_3, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    # --- Trường hợp 4: Không có thông tin trong ngữ cảnh ---
    print("--- TRƯỜNG HỢP 4: HỎI CỤ THỂ CHUNK SAU ---")
    context_4 = context_1 # Sử dụng lại context ở trên
    question_4 = "Thành phần của thuốc Panadol Extra?"
    response_4 = get_rag_response(context_4, question_4)
    print(json.dumps(response_4, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    # --- Trường hợp 5: Không có thông tin trong ngữ cảnh ---
    print("--- TRƯỜNG HỢP 5: HỎI CỤ THỂ CHUNK SAU ---")
    context_5 = context_1 # Sử dụng lại context ở trên
    question_5 = "Panadol có tác dụng phụ không"
    response_5 = get_rag_response(context_5, question_5)
    print(json.dumps(response_5, indent=2, ensure_ascii=False))

    # --- Trường hợp 6: Không có thông tin trong ngữ cảnh ---
    print("--- TRƯỜNG HỢP 6: HỎI CỤ THỂ CHUNK SAU ---")
    context_6 = context_1 # Sử dụng lại context ở trên
    question_6 = "Panadol có liều lượng sử dụng như nào"
    response_6 = get_rag_response(context_6, question_6)
    print(json.dumps(response_6, indent=2, ensure_ascii=False))
