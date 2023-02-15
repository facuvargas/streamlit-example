
import os
from PyPDF2 import PdfReader
import streamlit as st
import pandas as pd
import re

pdf_dir = r""


# Función para buscar las palabras clave en un archivo PDF
def buscar_palabras_clave(pdf_path, palabras_clave):
    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        for palabra_clave in palabras_clave:
            if palabra_clave in text:
                return True

def search_word_in_pdf(pdf_path, search_word):
    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        total_count = 0
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            matches = re.findall(rf"(\b{search_word}\b)", text, re.IGNORECASE)
            if matches:
                st.write(f"La palabra '{search_word}' aparece en la página {i+1}:")
                for match in matches:
                    start = text.lower().rfind(match.lower()) - 250
                    end = text.lower().rfind(match.lower()) + len(match) + 250
                    if start < 0:
                        start = 0
                    if end > len(text):
                        end = len(text)
                    context = text[start:end].strip()
                    st.write(context)
                total_count += len(matches)
        if total_count == 0:
            st.write(f"La palabra '{search_word}' no fue encontrada en el archivo.")
        else:
            st.write(f"La palabra '{search_word}' aparece {total_count} veces en total en el archivo.")


def search_phrase_in_pdf(pdf_path, search_phrase):
    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        total_count = 0
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            matches = re.findall(search_phrase, text, re.IGNORECASE)
            if len(matches) > 0:
                st.write(f"La frase '{search_phrase}' aparece {len(matches)} veces en la página {i+1}.")
                total_count += len(matches)
                for match in re.finditer(search_phrase, text, re.IGNORECASE):
                    start = max(0, match.start() - 250)
                    end = min(len(text), match.end() + 250)
                    phrase = text[start:end].strip()
                    st.write(f"  '{phrase}'")
        if total_count == 0:
            st.write(f"La frase '{search_phrase}' no fue encontrada en el archivo.")
        else:
            st.write(f"La frase '{search_phrase}' aparece {total_count} veces en total en el archivo.")


def main():
    st.set_page_config(page_title="Buscador de PDF", page_icon=":mag:", layout="wide")
    st.title("Búsqueda de palabras clave en archivos PDF")

    # Obtener la lista de archivos PDF en la carpeta especificada
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

    # Pedir al usuario que elija si quiere buscar por palabra o por frase
    buscar_por = st.sidebar.selectbox("Buscar por", ["Palabra", "Frase"])

    # Pedir al usuario que ingrese la palabra o frase a buscar
    if buscar_por == "Palabra":
        search_term = st.sidebar.text_input("Ingrese la palabra a buscar")
    else:
        search_term = st.sidebar.text_input("Ingrese la frase a buscar")

    # Buscar la palabra o frase en cada archivo PDF
    rows= []
    encontrados = False
    for pdf_file in pdf_files:
        with open(os.path.join(pdf_dir, pdf_file), 'rb') as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if buscar_por == "Palabra":
                    if search_term.lower() in text.lower():
                        encontrados = True
                        rows.append([pdf_file, page+1, search_term])
                else:
                    if search_term.lower() in text.lower():
                        encontrados = True
                        rows.append([pdf_file, page+1, search_term])
    # Mostrar los resultados
    if encontrados:
        st.write("Resultados de la búsqueda:")
        df = pd.DataFrame(rows, columns=["Archivo PDF", "Página", "Término"])
        st.dataframe(df)
        st.download_button(
            label="Descargar resultados",
            data=df.to_csv().encode("utf-8"),
            file_name="resultados.csv",
            mime="text/csv"
        )
    else:
        st.write("No se encontraron resultados para la búsqueda realizada.")
        
if __name__ == "__main__":
    main()
