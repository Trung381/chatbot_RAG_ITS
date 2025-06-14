'''
!pip uninstall -y google-generativeai
!pip install google-ai-generativelanguage==0.6.18
!pip install langchain_google_genai langchain_core
!pip install python-dotenv
'''

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from operator import itemgetter
import os
from dotenv import load_dotenv

load_dotenv()

structure_guide = '''
        {
            "roots": ["d95624..."],  // danh sách id của các nút gốc
            "nodes": {
                "d95624...": {
                    "id": "d95624...",
                    "text": "TIÊU ĐỀ CHÍNH...",
                    "childrens": ["f9c914...", "ab2c80...", "f3ac81..."] // danh sách id của các nút con
                },
                "ab2c80...": {
                  "id": "ab2c80...",
                  "text": "PHẦN A...",
                  "childrens": ["b733d1...", "a68964..."]
                },
                ...
            }
        }
    '''

def format_prompt(raw_data):
    prompt = (
        "Bạn là một trợ lý thông minh giúp cấu trúc lại dữ liệu tiếng Việt được cung cấp theo yêu cầu.\n"
        '''Bạn được cung cấp dữ liệu dạng json, trong đó mỗi key là một id duy nhất và value tương ứng là một đề mục có trong tài liệu pdf hoặc docx, các cặp key-value đã sắp xếp theo thứ tự từ trên xuống của các đề mục như trong tài liệu gốc.
        Ở mỗi đề mục sẽ đánh hoặc không đánh đề mục, nếu có thì có thể là số, chữ cái hoặc số la mã và có thể có sự phân cấp.\n'''
        f"Nhiệm vụ của bạn là chuyển đổi dữ liệu được cung cấp thành cấu trúc dạng tree + flat map với cấu trúc như sau: ```{structure_guide}```.  Tiêu chí dùng để đánh giá và sắp xếp các đề mục có quan hệ với nhau là cách phân cấp đề mục nếu có, sự liên quan của các đề mục.\n"
        f"Dữ liệu cần định dạng lại cấu trúc: ```{raw_data}``` và định dạng đầu ra mong đợi như sau:\n"
        '''
        ```<Câu trả lời>```
        '''
    )

    return {"prompt": prompt}

def build_chain():
    api_key = os.getenv("GOOGLE_API_KEY")
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, api_key=api_key)
    chain = (
        RunnableLambda(format_prompt)
        | itemgetter('prompt')
        | model
        | JsonOutputParser()
    )

    return chain

def restructure(raw_data) -> dict:
    chain = build_chain()
    return chain.invoke(raw_data)