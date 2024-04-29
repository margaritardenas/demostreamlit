import streamlit as st
import pandas as pd
from difflib import SequenceMatcher as SM

def search_by_matching(name1, name2):
    """Calcula la similitud entre dos nombres completos utilizando SequenceMatcher."""
    return SM(None, name1, name2).ratio()

def main():
    st.title("Cargar y visualizar CSV en Streamlit")
    uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Archivo cargado con éxito:")
        st.dataframe(df)
        
        umbral = 0.8  # 80% de similitud
        grupos = []
        for i, row1 in df.iterrows():
            # Concatenar nombre y apellidos
            nombre_completo1 = f"{row1['nombre']} {row1['apellidos']}"
            
            agrupado = False
            for grupo in grupos:
                for idx in grupo['indices']:
                    row2 = df.loc[idx]
                    nombre_completo2 = f"{row2['nombre']} {row2['apellidos']}"
                    similitud = search_by_matching(nombre_completo1, nombre_completo2)                    
                    if similitud >= umbral:
                        grupo['indices'].append(i)
                        grupo['porcentajes'].append(similitud * 100)
                        agrupado = True
                        break
                if agrupado:
                    break

            # Si no se agrupa, crear un nuevo grupo
            if not agrupado:
                grupo = {'indices': [i], 'porcentajes': [100]}
                grupos.append(grupo)
        st.write(f"Grupos de registros según similitud de nombres completos (umbral >= {umbral * 100}%):")
        for idx, grupo in enumerate(grupos):
            st.write(f"Grupo {idx + 1}:")
            group_df = df.loc[grupo['indices']].copy()
            group_df['Porcentaje de coincidencia'] = grupo['porcentajes']
            st.dataframe(group_df)

if __name__ == "__main__":
    main()
