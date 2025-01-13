from PyPDF2 import PdfReader, PdfWriter
import os
import re

# Variables
PATH = './[EASL] EW 2025 Handbook Version 1.pdf'
OUTPATH = 'output/'

# Consts
MARKER_REGEX = r'02\s+EVENT\s+RULES\s+AND\s+GUIDELINES'
NAME_REGEX = r'EVENT\s+NAME\s+([\s\S]*)\s+EVENT\s+DESCRIPTION'

def main():
    with open(PATH, 'rb') as f:
        reader = PdfReader(f)
        info = reader.metadata
        n_pages = len(reader.pages)
        
        print(f"Parsing {info.title}")

        count = 0
        entries = []

        for i in range(n_pages):
            page = reader.pages[i]
            text = page.extract_text()
            marker_match = re.search(MARKER_REGEX, text)

            if marker_match:
                count += 1

                try:
                    name_match = re.search(NAME_REGEX, text)
                    name = name_match.group(1).replace('\n', ' ').strip()
                    name = re.sub(r'[\\/:*?\"<>|]', '', name)
                    print(f"Found {name} at page {i + 1}")

                    if entries:
                        entries[-1].append(i - 1)

                    entries.append([name, i])
                    
                except AttributeError:
                    break

        entries[-1].append(n_pages - 1)

        print(f"Found {count} matches in {n_pages} pages")

        if not os.path.exists(OUTPATH):
            os.makedirs(OUTPATH)

        for entry in entries:
            writer = PdfWriter()
            name, start, end = entry

            for i in range(start, end + 1):
                writer.add_page(reader.pages[i])
            
            with open(OUTPATH + f"{name}.pdf", 'wb') as f:
                writer.write(f)


if __name__ == '__main__':
    main()