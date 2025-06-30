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
SYSTEM_PROMPT = (
        "You are a professional, precise, and reliable AI assistant. Your task is to ANALYZE the user's question and, BASED ONLY on the provided context chunks, generate an answer following the JSON format with 2 attributes is content and code (0: no answer, 1: have answer) and the strict rules below.\n"
        f"This is context: ```{{context}}```\n\n"
        """This is MANDATORY RULES and YOU MUST STRICTLY FOLLOW the rules below:\n
        1. YOU MUST read, analyze, and synthesize information from ALL context chunks ([CONTEXT 1], [CONTEXT 2], etc.) to produce the most comprehensive answer possible. Do not omit any relevant information present in the context.\n
        2. Your answer MUST be entirely based on the information within the context. DO NOT infer, fabricate, guess, or use any external knowledge not present in the context.\n
        3. If none of the context chunks contain information relevant to answering the question, the `content` must be "".\n
        4. If the user's question is general AND you find multiple contexts covering different aspects, the `content` must be a clarifying question suggesting the topics found. Example: "Bạn muốn biết thông tin cụ thể nào về [topic]? Các thông tin mà tôi biết gồm: [topic 1], [topic 2]..v.v"\n
        5. If the question is clear and relevant information is present, the `content` must be a complete, synthesized answer from ALL related contexts.\n
        6. 6. **Tone Guideline:** When delivering the answer in `content`, please use a friendly and respectful Vietnamese tone, such as:
        - Start your reply with words like “Dạ”, “Vâng” or “Thông tin em tìm thấy là…”;
        - Write as if you are kindly assisting someone, but **do not** invent any facts outside the context.
        - Friendly closing such as “Anh/chị còn thắc mắc nào cần em hỗ trợ thêm không ạ?”, “Nếu anh/chị cần biết thêm thông tin gì, em sẵn lòng hỗ trợ tiếp ạ.” or “Nếu còn yêu cầu nào khác, anh/chị cứ nói để em hỗ trợ thêm ạ.” to maintain engagement.\n\n
        """
        """
        Once you've determined the `content` based on the above rules, follow the process below to create the final output:\n
        Step 1. Generate `content: Reason using the context and the 'MANDATORY RULES' above to create the answer content.
        """
        "If the user's question is general AND you find multiple contexts covering different aspects, you must ask the user for clarification (according to rule 3).\n\n"
        """
        This is the user's question: ```{{question}}```. And the desired output is: ```<response>```"
        """
    )


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
    model = ChatOpenAI(model="gpt-4o", temperature=0.6)

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
    # context_1 = """
    # [NGỮ CẢNH 1]: Công dụng chính của thuốc Panadol Extra là giảm đau và hạ sốt. Các cơn đau được chỉ định bao gồm đau đầu, đau nửa đầu, đau cơ, đau bụng kinh.
    # [NGỮ CẢNH 2]: Thành phần hoạt chất của Panadol Extra bao gồm 500mg Paracetamol và 65mg Caffeine. Caffeine giúp tăng cường tác dụng giảm đau của Paracetamol.
    # [NGỮ CẢNH 2]: Pandol Extra vẫn có tác dụng phụ ở hệ tiêu hóa như buồn nôn, nôn, đau bụng, tiêu chảy,… hoặc ở hệ thần kinh như chóng mặt, mệt mỏi, lo lắng, bồn chồn, dễ kích động,…
    # """

    context_1 = """
    [NGỮ CẢNH 1]: Công dụng chính của thuốc Panadol Extra là giảm đau và hạ sốt. Các cơn đau được chỉ định bao gồm đau đầu, đau nửa đầu, đau cơ, đau bụng kinh.
    [NGỮ CẢNH 2]: Thành phần hoạt chất của Panadol Extra bao gồm 500mg Paracetamol và 65mg Caffeine. Caffeine giúp tăng cường tác dụng giảm đau của Paracetamol.
    [NGỮ CẢNH 2]: Panadol Extra vẫn có tác dụng phụ ở hệ tiêu hóa như buồn nôn, nôn, đau bụng, tiêu chảy,… hoặc ở hệ thần kinh như chóng mặt, mệt mỏi, lo lắng, bồn chồn, dễ kích động,…
    """
    question_1 = "Thành phần và công dụng của Panadol Extra là gì?"
    response_1 = get_rag_response(context_1, question_1)
    # print(response_1.get("content"))
    print(json.dumps(response_1, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    # --- Trường hợp 2: Câu hỏi chung chung, cần làm rõ ---
    print("--- TRƯỜNG HỢP 2: CÂU HỎI CHUNG CHUNG ---")
    context_2 = context_1 # Sử dụng lại context ở trên
    question_2 = "Cho tôi biết về Panadol Extra"
    response_2 = get_rag_response(context_2, question_2)
    # print(response_2.get("content"))
    print(json.dumps(response_2, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    # --- Trường hợp 3: Không có thông tin trong ngữ cảnh ---
    print("--- TRƯỜNG HỢP 3: THIẾU THÔNG TIN ---")
    context_3 = context_1 # Sử dụng lại context ở trên
    question_3 = "Liều dùng của Panadol Extra cho trẻ em là bao nhiêu?"
    response_3 = get_rag_response(context_3, question_3)
    # print(response_3.get("content"))
    print(json.dumps(response_3, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    # --- Trường hợp 3: Không có thông tin trong ngữ cảnh ---
    print("--- TRƯỜNG HỢP 4: HỎI CỤ THỂ CHUNK SAU ---")
    context_4 = context_1 # Sử dụng lại context ở trên
    question_4 = "Thành phần của thuốc Panadol Extra?"
    response_4 = get_rag_response(context_4, question_4)
    # print(response_4.get("content"))
    print(json.dumps(response_4, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    # --- Trường hợp 3: Không có thông tin trong ngữ cảnh ---
    print("--- TRƯỜNG HỢP 5: HỎI CỤ THỂ CHUNK SAU ---")
    context_5 = context_1 # Sử dụng lại context ở trên
    question_5 = "Panadol có tác dụng phụ không"
    response_5 = get_rag_response(context_5, question_5)
    # print(response_5.get("content"))
    print(json.dumps(response_5, indent=2, ensure_ascii=False))
