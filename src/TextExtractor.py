import PyPDF2
import pprint
from pathlib import Path
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
    def _title(self) -> str:
        """
        Retourne le nom du fichier PDF sans l'extension.

        Returns:
            str: Nom du fichier sans extension.
        """
        return Path(self.pdf).stem

    @property
    def _text(self):
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

    def build_JSON(self):
        """
        Construit un objet JSON contenant le titre et le texte du PDF.

        Returns:
            str: Chaîne JSON formatée contenant les données extraites du PDF.
                 Structure: {"article": str, "input": str, "text": str, "output": str}
        """
        text = self._text
        data = {}
        data["article"] = self._title
        data["input"] = " "
        data["text"] = text
        data["output"] = " "
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        return json_data


if __name__ == "__main__":
    text_extractor = TextExtractor(pdf_file_path="uploads/articlesBNP/test.pdf")
    print(text_extractor.build_JSON())