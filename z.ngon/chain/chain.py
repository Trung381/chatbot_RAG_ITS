'''
!pip uninstall -y google-generativeai
!pip install google-ai-generativelanguage==0.6.18
!pip install langchain_google_genai langchain_core
!pip install python-dotenv
'''

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from operator import itemgetter
from dotenv import load_dotenv
import os

guide = '''
  {
    "titleId": f9c914bbe5fe7cce8avjfkdkdkdkdkd,
    "title": "Tài liệu ôn tập", //Tên tài liệu
    "content": "",
    "children": [
        {
            "titleId": "f9c914bbe5fe7cce8abde153f607eaea", //ID duy nhất
            "title": "Chương 1: Giới thiệu về Lập trình hướng đối tượng",
            "content": "",
            "children": [
                {
                    "titleId": "ab2c809cc6f2cd1f114dd9fddbdae7b2",
                    "title": "1.1. Khái niệm cơ bản",
                    "content": "",
                    "children": [
                        {
                            "titleId": "b733d164cde1383eb28bbe4c59316a52",
                            "title": "1.1.1. Tính đóng gói (Encapsulation)",
                            "content": "",
                            "children": []
                        },
                        {
                            "titleId": "b30dc5276f6ca1380c3b57c0102127ea",
                            "title": "1.1.2. Tính thừa kế (Inheritance)",
                            "content": "",
                            "children": []
                        }
                    ]
                },
                {
                    "titleId": "c1d5a4449713cf436eead4a8daa4dbd4",
                    "title": "1.2. Lợi ích của OOP",
                    "content": "",
                    "children": []
                }
            ]
        },
        {
            "titleId": "b6798fbfc64e0ae5d67b04cb44f3a15a",
            "title": "Chương 2: Các ngôn ngữ lập trình hỗ trợ OOP",
            "content": "",
            "children": [
                {
                    "titleId": "146b463d45027036347b0458e8145fa8",
                    "title": "2.2. C++",
                    "content": "",
                    "children": []
                }
            ]
        },
        {
            "titleId": "a689649acc0d84b53319f408cb8bce62",
            "title": "Chương 3: Kết luận",
            "content": "",
            "children": []
        }
    ]
  }
'''

load_dotenv()

def format_prompt(raw_data):
    prompt = (
        """
        Bạn là một trợ lý thông minh chuyên cấu trúc, phân cấp lại dữ liệu tiếng Việt.\n
        Bạn được cung cấp dữ liệu là tập các tiêu đề có trong tài liệu DOCX hoặc PDF với cấu trúc ban đầu giống như 1 dictionary trong python, trong đó:\n
            - Key: Mỗi key là một ID duy nhất giúp phân biệt các tiêu đề\n
            - Value: Mỗi value là một tiêu đề ứng với key tương ứng\n
        Lưu ý rằng các tiêu đề có thể được đánh hoặc không đánh số đề mục, nếu được đánh đề mục thì có thể là số, chữ cái hoặc số la mã, ví dụ như '1', '1.2.1', 'a', 'II', 'A',...
        """
        f"Nhiệm vụ của bạn là phân tích, đánh giá tập dữ liệu được cung cấp và chuyển dữ liệu đó thành dữ liệu có cấu trúc như sau: ```{guide}```.\n"
        """
        Trong đó:\n
            - titleId: ID duy nhất của mỗi đề mục Với titleId đầu tiên thì title tương ứng là tên của tài liệu
            - title: Tên của đề mục
            - content: Nội dung của đề mục, luôn để giá trị trống
            - children: Danh sách các đề mục con, rỗng nếu không có đề mục con
        """
        """
        Tiêu chí dùng để đánh giá và cấu trúc lại dữ liệu có thể gồm:\n
            - Cách phân cấp đề mục
            - Sự liên quan giữa các đề mục
        """
        f"Dữ liệu cần cấu trúc lại như sau: ```{raw_data}``` và định dạng đầu ra mong đợi là: ```<Câu trả lời>```"
    )

    return {"prompt": prompt}

def build_chain() -> dict:
    api_key = os.getenv("OPEN_AI_KEY")
    model = ChatOpenAI(model="gpt-4o", temperature=0.5, api_key=api_key)
    chain = (
        RunnableLambda(format_prompt)
        | itemgetter('prompt')
        | model
        | JsonOutputParser() #Parse response thành kiểu DICT
    )

    return chain

# Call ChatGPT để sắp xếp lại đề mục
def restructure(raw_data) -> dict:
    chain = build_chain()
    return chain.invoke(raw_data)