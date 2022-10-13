from typing import List

from fpdf import FPDF


def to_pdf(lines: List[str], filename: str) -> None:
    pdf = FPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    for i in range(len(lines)):
        pdf.cell(0, 10, lines[i], 0, 1)
    pdf.output(filename.split(".")[0] + ".pdf", 'F')

# if __name__ == "__main__":
#     with open('model.py') as f:
#         lines = f.readlines()
#     to_pdf(lines, 'tuto2.pdf')
