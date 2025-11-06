import PyPDF2
import pprint
import json


class TextExtractor:
    """
    Classe pour extraire le texte d'un fichier PDF et le formater en JSON.

    Attributes:
        pdf (str): Chemin vers le fichier PDF à traiter.
    """

    def __init__(self, pdf_file_path: str) -> None:
        """
        Initialise l'extracteur avec le chemin du fichier PDF.

        Args:
            pdf_file_path (str): Chemin vers le fichier PDF.
        """
        self.pdf = pdf_file_path



    @property
    def text(self):
        """
        Extrait et retourne tout le texte du PDF.

        Returns:
            str: Texte complet extrait de toutes les pages du PDF.
        """
        with open(self.pdf, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text




if __name__ == "__main__":
    text_extractor = TextExtractor(pdf_file_path="uploads/articlesBNP/test.pdf")
    print(text_extractor.text)