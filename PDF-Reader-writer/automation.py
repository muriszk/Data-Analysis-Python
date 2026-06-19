import re
import pandas as pd
from PyPDF2 import PdfReader

#passar estas informações no .env
pdf_path = ""
output_excel = ""

reader = PdfReader(pdf_path)
raw_text = []

for page in reader.pages:
    text = page.extract_text()
    if text:
        raw_text.append(text)

text = "\n".join(raw_text)

text = text.replace("\r", "\n")
text = re.sub(r'\n+', '\n', text)
text = re.sub(r'[ \t]+', ' ', text)

def is_header_noise(line):
    keywords = [
        "COMISSÃO DE VALORES MOBILIÁRIOS",
        "Rua Sete de Setembro",
        "Cincinato Braga",
        "SCN Q.02",
        "Corporate Financial Center",
        "Brasília/DF",
        "São Paulo/SP",
        "Rio de Janeiro/RJ",
        "CEP:",
        "Tel.:",
        "www.cvm.gov.br",
        "RESOLUÇÃO CVM Nº 50"
    ]

    # Remove qualquer linha que contenha vários desses sinais
    count = sum(1 for k in keywords if k.lower() in line.lower())

    # critério: linha tem 2+ palavras-chave OU parece endereço
    if count >= 2:
        return True

    if re.search(r'Tel\.\s*\(?\d+\)?', line):
        return True

    # detecta padrão de CEP
    if re.search(r'\d{5}-\d{3}', line):
        return True

    # detecta endereço longo (rua + número)
    if re.search(r'Rua|Andar|Bl\.|Ed\.', line):
        if len(line) > 50:
            return True

    return False

patterns = {
    "capitulo": re.compile(r'^CAP[IÍ]TULO.*'),
    "secao": re.compile(r'^Seção.*', re.IGNORECASE),
    "artigo": re.compile(r'^Art\.\s*\d+.*'),
    "paragrafo": re.compile(r'^§\s*\d+º?.*'),
    "inciso": re.compile(r'^[IVXLCDM]+\s*[–-].*'),
    "alinea": re.compile(r'^[a-z]\)\s*.*')
}

def is_new_item(line):
    return (
        patterns["capitulo"].match(line) or
        patterns["secao"].match(line) or
        patterns["artigo"].match(line) or
        patterns["paragrafo"].match(line) or
        patterns["inciso"].match(line) or
        patterns["alinea"].match(line)
    )

# ===== PROCESSAMENTO =====
lines = []
current_line = ""

for raw_line in text.split("\n"):
    line = raw_line.strip()

    if not line:
        continue

    # 🚨 REMOVE CABEÇALHO AQUI
    if is_header_noise(line):
        continue

    # evita lixo muito pequeno
    if len(line) < 3:
        continue

    # NOVO ITEM
    if is_new_item(line):
        if current_line:
            lines.append(current_line.strip())
        current_line = line

    else:
        if current_line:
            current_line += " " + line
        else:
            current_line = line

# última linha
if current_line:
    lines.append(current_line.strip())

seen = set()
final_lines = []

for line in lines:
    if line not in seen:
        final_lines.append(line)
        seen.add(line)

def clean_text(line):
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'\s*-\s*', '-', line)
    line = re.sub(r'\s*–\s*', ' – ', line)
    return line.strip()

final_lines = [clean_text(l) for l in final_lines]

df = pd.DataFrame(final_lines, columns=["Texto"])
df.to_excel(output_excel, index=False)

print(f"✅ Arquivo gerado: {output_excel}")
print(f"📊 Linhas finais: {len(final_lines)}")
