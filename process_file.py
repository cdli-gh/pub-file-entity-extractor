import pdfplumber
import pandas as pd
import re

class PubEntityExtractor():

    db_server = "mariadb+mariadbconnector://root@127.0.0.1:23306/cdli_db"

    def get_text(self, pdf, separator = " "):
        full_txt = ""
        for page in pdf.pages:
            full_txt += page.extract_text(x_tolerance = 1) + separator
        return full_txt

    def is_image_pdf(self, pdf):
        return len(self.get_text(pdf, "")) == 0

    def get_all_text(self, pdf):
        return self.get_text(pdf, " ")

    def get_provenience_occurences(self, full_txt, prov_location = "proveniences.csv"):
        # engine = sqlalchemy.create_engine(self.db_server)
        # connection = engine.connect()
        # proveniences = pd.read_sql('SELECT id, provenience FROM proveniences', connection, index_col = "id")
        proveniences = pd.read_csv(prov_location, index_col = "id")
        prov_names = proveniences["provenience"].str.findall(r"(.+) \(mod\. (.+)\)").str[0]
        proveniences["ancient_name"] = prov_names.str[0]
        proveniences["modern_name"] = prov_names.str[1]
        proveniences = proveniences.drop(207)
        proveniences.loc[242, "ancient_name"] = "Qattara"
        proveniences.loc[242, "modern_name"] = "Tell al Rimah"
        proveniences.loc[360, "ancient_name"] = "Kian"
        proveniences.loc[360, "modern_name"] = "Tell Shmid"

        def find_total_occurence(row):
            ancient_name = row["ancient_name"]
            modern_name = row["modern_name"]
            pattern_a = r'\b' + ancient_name + r'\b'
            occur_a = 0 if ancient_name == "uncertain" else len(re.findall(pattern_a, full_txt))
            pattern_b = r'\b' + modern_name + r'\b'
            occur_b = 0 if modern_name == "uncertain" else len(re.findall(pattern_b, full_txt))
            return occur_a + occur_b

        proveniences["total_occurences"] = proveniences.apply(find_total_occurence, axis = "columns")
        proveniences = proveniences.sort_values("total_occurences", ascending = False)
        return proveniences[proveniences["total_occurences"] > 0]

    def parse(self, file_name, prov_location = "proveniences.csv"):
        with pdfplumber.open(file_name) as pdf:
            if self.is_image_pdf(pdf):
                # TODO: Perform OCR on pdf.
                pass
            else:
                text = self.get_all_text(pdf)
                print(self.get_provenience_occurences(text, prov_location))

