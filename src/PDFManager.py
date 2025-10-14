from pathlib import Path
from PyPDF2 import PdfMerger
import os


class PDFManager:
    def __init__(self, out_directory=None):
        """
        Initializes a PDFManager instance.

        Args:
            out_directory (str, optional): The output directory for generated PDF files.
                                          Defaults to the current working directory if not provided.

        Raises:
            Creates the directory if it does not exist.
        """
        self.out_directory = out_directory or Path.cwd()
        Path(self.out_directory).mkdir(parents=True, exist_ok=True)

    def merge_pdf_files(self, pdf_files, out_name="merged.pdf"):
        """
        Merges a list of PDF files into a single PDF document.

        Args:
            pdf_files (list): List of file paths to PDF files to be merged.
            out_name (str, optional): Name of the output PDF file. Defaults to "merged.pdf".

        Returns:
            str: The full path of the merged PDF file on success, None on error.

        Raises:
            ValueError: If pdf_files list is empty or if any PDF file does not exist.

        Example:
            >>> manager = PDFManager()
            >>> manager.merge_pdf_files(["file1.pdf", "file2.pdf"], "output.pdf")
            PDFs successfully merged : /path/to/merged/output.pdf
        """
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
        """
        Renames an existing PDF file.

        Args:
            pdf_path (str): The full file path of the PDF file to be renamed.
            name (str): The new name for the file (with or without .pdf extension).

        Returns:
            str: The full path of the renamed PDF file on success, None on error.

        Raises:
            ValueError: If the PDF file does not exist.

        Note:
            If a file with the same name already exists, it will be replaced.
            The .pdf extension is automatically added if not present in the provided name.

        Example:
            >>> manager = PDFManager()
            >>> manager.rename_pdf_file("old_name.pdf", "new_name")
            Pdf file /path/to/new_name.pdf has been renamed.
        """
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

    def merge_directory(self, directory, out_name="merged.pdf"):
        """
        Merges all PDF files from a directory into a single PDF document.

        Args:
            directory (str): The file path of the directory containing PDF files.
            out_name (str, optional): Name of the output PDF file. Defaults to "merged.pdf".

        Returns:
            str: The full path of the merged PDF file on success, None on error.

        Raises:
            ValueError: If the directory does not exist, is not a directory,
                       or contains no PDF files.

        Note:
            PDF files are processed in alphabetical order.
            The output file is saved to the output directory specified during
            PDFManager initialization.

        Example:
            >>> manager = PDFManager("./output")
            >>> manager.merge_directory("./pdfs_to_merge", "merged_all.pdf")
            PDFs found and ready to be merged : ['/path/to/file1.pdf', '/path/to/file2.pdf']
        """
        dir_path = Path(directory)

        if not dir_path.exists():
            raise ValueError(f"Directory '{directory}' does not exist")

        if not dir_path.is_dir():
            raise ValueError(f"Directory '{directory}' is not a directory")

        try:
            pdf_files = sorted(dir_path.glob("*.pdf"))

            if not pdf_files:
                raise ValueError("No PDF files to merge")

            pdf_paths = [str(pdf) for pdf in pdf_files]
            print(f"PDFs found and ready to be merged : {pdf_paths}")

            return self.merge_pdf_files(pdf_paths, out_name=out_name)

        except Exception as e:
            print(f"Error while merging PDFs: {e}")
            return None


if __name__ == "__main__":
    pdf_manager = PDFManager(out_directory="./generated_pdfs")

    try:
        pdfs = ["../articlesBNP/Agence France Presse, 29-Jan-2025.pdf",
                "../articlesBNP/Associated Press Newswires, 04-Sep-2024.pdf"]
        pdf_manager.merge_pdf_files(pdfs, out_name="trump_merged.pdf")

        pdf_manager.merge_directory("../articlesBNP/trump", out_name="trump_articles.pdf")
    except ValueError as e:
        print(f"Erreur : {e}")