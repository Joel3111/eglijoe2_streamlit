import streamlit as st
import pandas as pd

# Titel der Anwendung
st.title("CSV Datenanzeige und Filterung")

# Dateipfad zur CSV-Datei
file_path = "Data.csv"

try:
    # Einlesen der CSV-Datei in einen DataFrame
    df = pd.read_csv(file_path, encoding='latin1')

    # Anzeige der ersten Zeilen der Datei
    st.write("Erste Zeilen der Datei:")
    st.dataframe(df.head())

    # Anzeige der gesamten Tabelle mit der Möglichkeit zu scrollen
    st.write("Gesamte Tabelle:")
    st.dataframe(df)

    # Suchfunktion
    search_term = st.text_input("Suchbegriff eingeben:")
    if search_term:
        search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        st.write(f"Suchergebnisse für '{search_term}':")
        st.dataframe(search_results)

    # Filterfunktion
    st.sidebar.header("Filteroptionen")
    filter_columns = st.sidebar.multiselect("Spalten zum Filtern auswählen", df.columns)
    
    filter_query = ""
    for column in filter_columns:
        unique_values = df[column].unique()
        selected_value = st.sidebar.selectbox(f"Wert für {column} auswählen", unique_values, key=column)
        filter_query += f"({column} == @selected_value) & "

    if filter_query:
        filter_query = filter_query[:-3]  # Letzte ' & ' entfernen
        filtered_df = df.query(filter_query)
        st.write("Gefilterte Tabelle:")
        st.dataframe(filtered_df)
    else:
        st.write("Keine Filter angewendet.")
except FileNotFoundError:
    st.error(f"Die Datei '{file_path}' wurde nicht gefunden. Stelle sicher, dass sich die Datei im selben Ordner wie dieses Skript befindet.")
except Exception as e:
    st.error(f"Ein Fehler ist aufgetreten: {e}")
