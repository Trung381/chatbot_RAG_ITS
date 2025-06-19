import os # for parse_document
import pdfplumber
import docx2txt # không đọc được data dạng bảng
from docx import Document # đọc data dạng bảng mượt hơn sunsilk

"""
remove '\n' from a string
"""
def remove_newlines(string):
    return string.replace('\n', ' ')

# print(remove_newlines("Hello\nWorld"))

"""
string for table data with pdfplumber, docx2txt
example table data:
STT | Name | Date of birth | Address
1   | John | 20/01/2000    | Hanoi
2   | Jane | 21/02/2001    | Haiphong

string output: [TABLE]STT: 1, Name: John, Date of birth: 20/01/2000, Address: Hanoi\n[TABLE]STT: 2, Name: Jane, Date of birth: 21/02/2001, Address: Haiphong"

best practice cho string output:
- header: value rõ ràng
- Dấu phẩy phân tách field
- Dấu : có khoảng trắng sau
"""

def parse_pdf_table(filepath):
    rows = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                headers = table[0]
                for row in table[1:]:
                    row_str = ", ".join(f"{headers[i]}: {row[i]}" for i in range(len(headers)))
                    rows.append(row_str)
    return "\\n".join(rows)


def parse_docx_table(filepath):
    doc = Document(filepath)
    rows = []
    for table in doc.tables:
        headers = [cell.text.strip() for cell in table.rows[0].cells]
        for row in table.rows[1:]:
            cells = [cell.text.strip() for cell in row.cells]
            row_str = ", ".join(f"{headers[i]}: {cells[i]}" for i in range(len(headers)))
            rows.append(row_str)
    return "\\n".join(rows)


def parse_document(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        return parse_pdf_table(filepath)
    elif ext == '.docx':
        return parse_docx_table(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    output_docx = parse_document("document/example_data.docx")
    output_pdf = parse_document("document/example_data.pdf")
    print("DOCX Output:\n", output_docx)
    print("\nPDF Output:\n", output_pdf)

