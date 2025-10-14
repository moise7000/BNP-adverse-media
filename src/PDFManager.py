from pathlib import Path
from PyPDF2 import PdfMerger
import os

class PDFManager:
    def __init__(self, out_directory=None):
        self.out_directory = out_directory or Path.cwd()
        Path(self.out_directory).mkdir(parents=True, exist_ok=True)


    def merge_pdf_files(self, pdf_files, out_name="merged.pdf"):
        if not pdf_files:
            raise ValueError("No PDF files to merge")

        for pdf_file in pdf_files:
            if not Path(pdf_file).exists():
                raise ValueError(f"PDF file '{pdf_file}' does not exist")

        try:
            merger = PdfMerger(strict=False)
            for pdf_file in pdf_files:
                merger.append(pdf_file)

            out_path = Path(self.out_directory) / out_name
            with open(str(out_path), 'wb') as f:
                merger.write(f)
            merger.close()

            print(f"PDFs successfully merged : {out_path}")
            return str(out_path)
        except Exception as e:
            print(f"Error while merging PDFs: {e} ")
            return None


    def rename_pdf_file(self, pdf_path, name):
        source_path = Path(pdf_path)
        if not source_path.exists():
            raise ValueError(f"PDF file '{pdf_path}' does not exist")

        try:
            if not name.endswith(".pdf"):
                name = f"{name}.pdf"

            destination_path = source_path.parent / name

            if destination_path.exists():
                print(f"Pdf file {destination_path} already exists, it will be replaced.")

            source_path.rename(destination_path)
            print(f"Pdf file {destination_path} has been renamed.")
            return str(destination_path)
        except Exception as e:
            print(f"Error while renaming PDF: {e} ")
            return None


if __name__ == "__main__":
    pdf_manager = PDFManager(out_directory="./generated_pdfs")

    try:
        pdfs = ["../articlesBNP/Agence France Presse, 29-Jan-2025.pdf", "../articlesBNP/Associated Press Newswires, 04-Sep-2024.pdf"]
        pdf_manager.merge_pdf_files(pdfs, out_name="trump_merged.pdf")
    except ValueError as e:
        print(f"Erreur : {e}")





