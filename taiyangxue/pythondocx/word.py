import re

from docx import Document

doc = Document(r"D:\论文.docx")
restr = '"(?:[^"])*"'

for p in doc.paragraphs:
    matchRet = re.findall(restr, p.text)
    for r in matchRet:
        p.text = p.text.replace(r, '“' + r[1:-1] + '”')
doc.save(r'D:\论文_修正.docx')
