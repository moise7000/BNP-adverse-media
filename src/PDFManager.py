from pathlib import Path
from PyPDF2 import PdfMerger
import os


class PDFManager:
    def __init__(self, out_directory=None):
        """
        Initialise une instance de PDFManager.

        Args:
            out_directory (str, optional): Le répertoire de sortie pour les fichiers générés.
                                          Par défaut, utilise le répertoire courant.

        Raises:
            Crée le répertoire s'il n'existe pas.
        """
        self.out_directory = out_directory or Path.cwd()
        Path(self.out_directory).mkdir(parents=True, exist_ok=True)

    def merge_pdf_files(self, pdf_files, out_name="merged.pdf"):
        """
        Fusionne une liste de fichiers PDF en un seul fichier.

        Args:
            pdf_files (list): Liste des chemins vers les fichiers PDF à fusionner.
            out_name (str, optional): Nom du fichier PDF de sortie. Par défaut, "merged.pdf".

        Returns:
            str: Le chemin complet du fichier fusionné en cas de succès, None en cas d'erreur.

        Raises:
            ValueError: Si la liste pdf_files est vide ou si un fichier n'existe pas.

        Example:
            >>> manager = PDFManager()
            >>> manager.merge_pdf_files(["file1.pdf", "file2.pdf"], "output.pdf")
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
        Renomme un fichier PDF existant.

        Args:
            pdf_path (str): Le chemin complet du fichier PDF à renommer.
            name (str): Le nouveau nom pour le fichier (avec ou sans extension .pdf).

        Returns:
            str: Le chemin complet du fichier renommé en cas de succès, None en cas d'erreur.

        Raises:
            ValueError: Si le fichier PDF n'existe pas.

        Note:
            Si un fichier avec le même nom existe déjà, il sera remplacé.
            L'extension ".pdf" est ajoutée automatiquement si elle n'est pas présente.

        Example:
            >>> manager = PDFManager()
            >>> manager.rename_pdf_file("old_name.pdf", "new_name")
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
        Fusionne tous les fichiers PDF d'un répertoire en un seul fichier.

        Args:
            directory (str): Le chemin du répertoire contenant les fichiers PDF.
            out_name (str, optional): Nom du fichier PDF de sortie. Par défaut, "merged.pdf".

        Returns:
            str: Le chemin complet du fichier fusionné en cas de succès, None en cas d'erreur.

        Raises:
            ValueError: Si le répertoire n'existe pas, n'est pas un répertoire,
                       ou ne contient aucun fichier PDF.

        Note:
            Les fichiers PDF sont traités dans l'ordre alphabétique croissant.
            Le fichier de sortie est sauvegardé dans le répertoire de sortie
            défini lors de l'initialisation de PDFManager.

        Example:
            >>> manager = PDFManager("./output")
            >>> manager.merge_directory("./pdfs_to_merge", "merged_all.pdf")
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