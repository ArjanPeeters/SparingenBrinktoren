import streamlit as st
import duckdb
import os

st.set_page_config(layout="wide")

st.title("🔍 Sparingen zoeken in CSV (BIM-model)")

# 📁 Map waarin je CSV's staan
map_pad = "data/"  # <-- pas aan naar jouw map
csv_bestanden = os.path.join(map_pad, "*.csv")

# 🔎 Zoek-ID
zoek_id = st.text_input("Voer een ID in om te zoeken:")

if zoek_id:
    # ✍️ Pas de kolomnamen hieronder aan
    kolom1 = "Element_GlobalId"
    kolom2 = "Element_badId"
    datum_kolom = "Trimble_TimeStamp"
    extra_kolommen = ["Element_GlobalId","Element_badId","Trimble_fileVersion", "Element_Name", "level"]

    # 🧠 Bouw kolomnamen string voor de SELECT
    kolommen = ", ".join([datum_kolom] + extra_kolommen)

    # ✅ DuckDB-query (deels matchen met LIKE, case-insensitive)
    query = f"""
        SELECT {kolommen}
        FROM read_csv_auto('{csv_bestanden}', union_by_name=True, all_varchar=True)
        WHERE lower(CAST({kolom1} AS VARCHAR)) LIKE lower('%{zoek_id}%')
           OR lower(CAST({kolom2} AS VARCHAR)) LIKE lower('%{zoek_id}%')
    """

    try:
        resultaat = duckdb.query(query).to_df()

        if resultaat.empty:
            st.warning("Geen resultaat gevonden voor die ID.")
        else:
            st.success("Gevonden:")
            st.dataframe(resultaat)

    except Exception as e:
        st.error(f"Er ging iets mis bij het uitvoeren van de zoekopdracht: {e}")
