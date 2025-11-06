import json
import TextExtractor
from pathlib import Path


class JSONBuilder:
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path
        self.text = TextExtractor.TextExtractor(pdf_file_path).text

    @property
    def _filename(self) -> str:
        """
        Retourne le nom du fichier PDF sans l'extension.

        Returns:
            str: Nom du fichier sans extension.
        """
        return Path(self.pdf_file_path).stem


    def build(self):
        """
        Construit un objet JSON contenant le titre et le texte du PDF.

        Returns:
            str: Chaîne JSON formatée contenant les données extraites du PDF.
                 Structure: {"article": str, "input": str, "text": str, "output": str}
        """
        text = self.text
        data = {}
        data["article"] = self._filename
        data["prompt"] = " "
        data["text"] = text
        data["output"] = " "
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        return json_data


if __name__ == "__main__":
    json_builder = JSONBuilder("uploads/articlesBNP/test.pdf")
    print(json_builder.build())