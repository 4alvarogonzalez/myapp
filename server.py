# pip install streamlit
# python -m streamlit run server.py
# ctrl c para parar
import streamlit as st
import pandas as pd
import xgboost as xgb
import pickle
import base64

st.set_page_config(page_title="Repositorio de Assets", page_icon="logo.png")

#elimina la marca de agua de la app
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Verificar si el usuario ha proporcionado las credenciales correctas
if 'valid_login' not in st.session_state:
    st.session_state.valid_login = False

# Comprobar si el usuario ha iniciado sesión
if not st.session_state.logged_in:
    st.image("logo.png", width=200)
    st.title("Iniciar sesión")

    # Campo de entrada para el nombre de usuario
    username = st.text_input("Nombre de usuario")

    # Campo de entrada para la contraseña
    password = st.text_input("Contraseña", type="password")

    # Botón para iniciar sesión
    if st.button("Iniciar sesión"):
        if username == "admin" and password == "password":
            st.session_state.logged_in = True
            st.session_state.valid_login = True
            st.success("Inicio de sesión exitoso")
        else:
            st.session_state.logged_in = False
            st.session_state.valid_login = False
            st.error("Nombre de usuario o contraseña incorrectos")

# Verificar si el usuario ha iniciado sesión correctamente
if st.session_state.logged_in and st.session_state.valid_login:

    with open('modelo_xgb.pkl', 'rb') as file:
        modelo_xgb = pickle.load(file)

    with open('modelo_xgb2.pkl', 'rb') as file2:
        modelo_xgb2 = pickle.load(file2)


    # Define la interfaz de la aplicación
    def main():
        
        if 'option' not in st.session_state:
            st.session_state.option = "Inicio"

        st.sidebar.image("logo.png", width=100)
        
        # Opciones del desplegable
        option = st.sidebar.selectbox("Selecciona una opción:", ("Inicio","¿Cómo funciona la aplicación?","24 variables: Archivo Excel", "24 variables: Datos Manuales" ,"5 variables: Archivo Excel", "5 variables: Datos Manuales", "About Me"))
        
        uploaded_file = None  # Si no ponemos esto nos obliga a que aparezca el upload file en cada pantalla
        uploaded_file2 = None  # Si no ponemos esto nos obliga a que aparezca el upload file en cada pantalla

        if option == "Inicio":
            st.title("Predicción de Quiebra")
            st.subheader("Descubre si una empresa está en riesgo de quiebra")

            # Agregar una imagen o ilustración para hacerla más atractiva
            st.image("logo.png", width=100)

            # Agregar una descripción atractiva de la aplicación
            st.markdown("Esta aplicación utiliza un modelo de Machine Learning para categorizar las empresas que se encuentran en situación de quiebra."
                        "Puedes cargar un archivo Excel con los datos de la empresa o introducir los datos manualmente. "
                        "El modelo calculará la probabilidad de quiebra y te mostrará el resultado en función de la seguridad estimada.")

            # Agregar una llamada a la acción para animar a los usuarios a utilizar la aplicación
            st.markdown("**¡Comienza ahora y descubre la salud financiera de una empresa en segundos!**")

            # Agregar secciones adicionales, como beneficios o características destacadas de la aplicación
            st.header("Beneficios de utilizar esta aplicación:")
            st.markdown("- Ahorro de tiempo en el análisis financiero de una empresa.")
            st.markdown("- Predicciones precisas basadas en el modelo de Machine Learning XGBoost.")
            st.markdown("- Interfaz intuitiva y fácil de usar.")

            st.header("Características destacadas:")
            st.markdown("- Carga rápida y sencilla de datos desde un archivo Excel.")
            st.markdown("- Opción de introducir datos manualmente para análisis inmediato.")
            st.markdown("- Visualización clara de los resultados de predicción y seguridad estimada.")

            # Agregar información de contacto o enlace a recursos adicionales
            st.markdown("Para más información, contáctame, tienes los datos en la pestaña de about me")


        # Pestaña "¿Cómo funciona la aplicación?"


        if option == "¿Cómo funciona la aplicación?":
            st.header("¿Cómo funciona la aplicación?")
            st.video("video2.webm")


        # Código para la opción "24 variables: Archivo Excel"
        if option == "24 variables: Archivo Excel":
            st.header("24 variables: Archivo Excel")

            def download_csv():
                df = pd.read_csv("plantilla.csv", encoding="ISO-8859-1")
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="plantilla.csv">Descargar plantilla</a>'
                
                return href

            # Mostrar botón de descarga de plantilla
            st.markdown(download_csv(), unsafe_allow_html=True)


            # Carga del archivo Excel
            uploaded_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx", "xls","csv"], key="file_uploader_1")

        # Descargar plantilla
        
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)

            if st.button("Calcular"):
                # Realiza la predicción utilizando el modelo cargado
                prediction = modelo_xgb.predict(xgb.DMatrix(df))
                prediction_binary = [round(value) for value in prediction]
                probability = prediction[0]

                # Imprime el resultado de la predicción y la seguridad
                st.subheader("Resultado de la predicción:")
                if prediction_binary[0] == 0:
                    st.write("La empresa no quiebra. Seguridad:", 1 - probability)
                elif prediction_binary[0] == 1:
                    st.write("La empresa sí quiebra. Seguridad:", probability)
                else:
                    st.write("La predicción no es clara. Probabilidad de quiebra:", probability)

        elif option == "24 variables: Datos Manuales":
            st.header("24 variables: Datos Manuales")
        
            expense_rate = st.number_input("Operating Expense Rate:", -1.0, 1.0, 0.0)
            rd_expense_rate = st.number_input("Research and development expense rate:", -1.0, 1.0, 0.0)
            interest_rate = st.number_input("Interest-bearing debt interest rate:", -1.0, 1.0, 0.0)
            revenue_per_share = st.number_input("Revenue Per Share (Yuan ¥):", value=0.0)
            asset_growth_rate = st.number_input("Total Asset Growth Rate:", -1.0, 1.0, 0.0)
            value_growth_rate = st.number_input("Net Value Growth Rate:", -1.0, 1.0, 0.0)
            current_ratio = st.number_input("Current Ratio:", -1.0, 1.0, 0.0)
            quick_ratio = st.number_input("Quick Ratio:", -1.0, 1.0, 0.0)
            debt_net_worth_ratio = st.number_input("Total debt/Total net worth:", -1.0, 1.0, 0.0)
            receivable_turnover = st.number_input("Accounts Receivable Turnover:", 0.0, 1.0, 0.0)
            collection_days = st.number_input("Average Collection Days:", 0, 365, 0)
            inventory_turnover = st.number_input("Inventory Turnover Rate (times):", 0.0, 1.0, 0.0)
            fixed_assets_turnover = st.number_input("Fixed Assets Turnover Frequency:", 0.0, 1.0, 0.0)
            revenue_per_person = st.number_input("Revenue per person:", value=0.0)
            allocation_per_person = st.number_input("Allocation rate per person:", value=0.0)
            quick_assets_liability = st.number_input("Quick Assets/Current Liability:", 0.0, 1.0, 0.0)
            cash_liability = st.number_input("Cash/Current Liability:", 0.0, 1.0, 0.0)
            inventory_liability = st.number_input("Inventory/Current Liability:", 0.0, 1.0, 0.0)
            longterm_liability_assets = st.number_input("Long-term Liability to Current Assets:", -1.0, 1.0, 0.0)
            current_asset_turnover = st.number_input("Current Asset Turnover Rate:", 0.0, 1.0, 0.0)
            quick_asset_turnover = st.number_input("Quick Asset Turnover Rate:", 0.0, 1.0, 0.0)
            cash_turnover = st.number_input("Cash Turnover Rate:", 0.0, 1.0, 0.0)
            fixed_assets_ratio = st.number_input("Fixed Assets to Assets:", 0.0, 1.0, 0.0)
            total_assets_ratio = st.number_input("Total assets to GNP price:", 0.0, 1.0, 0.0)

            if st.button("Calcular"):
                # Crea un diccionario con los valores ingresados
                new_data = {
                    ' Operating Expense Rate': expense_rate,
                    ' Research and development expense rate': rd_expense_rate,
                    ' Interest-bearing debt interest rate': interest_rate,
                    ' Revenue Per Share (Yuan ¥)': revenue_per_share,
                    ' Total Asset Growth Rate': asset_growth_rate,
                    ' Net Value Growth Rate': value_growth_rate,
                    ' Current Ratio': current_ratio,
                    ' Quick Ratio': quick_ratio,
                    ' Total debt/Total net worth': debt_net_worth_ratio,
                    ' Accounts Receivable Turnover': receivable_turnover,
                    ' Average Collection Days': collection_days,
                    ' Inventory Turnover Rate (times)': inventory_turnover,
                    ' Fixed Assets Turnover Frequency': fixed_assets_turnover,
                    ' Revenue per person': revenue_per_person,
                    ' Allocation rate per person': allocation_per_person,
                    ' Quick Assets/Current Liability': quick_assets_liability,
                    ' Cash/Current Liability': cash_liability,
                    ' Inventory/Current Liability': inventory_liability,
                    ' Long-term Liability to Current Assets': longterm_liability_assets,
                    ' Current Asset Turnover Rate': current_asset_turnover,
                    ' Quick Asset Turnover Rate': quick_asset_turnover,
                    ' Cash Turnover Rate': cash_turnover,
                    ' Fixed Assets to Assets': fixed_assets_ratio,
                    ' Total assets to GNP price': total_assets_ratio
                }

                # Realiza la predicción utilizando el modelo cargado
                df = pd.DataFrame(new_data, index=[0])
                prediction = modelo_xgb.predict(xgb.DMatrix(df))
                prediction_binary = [round(value) for value in prediction]
                probability = prediction[0]

                # Imprime el resultado de la predicción y la seguridad
                st.subheader("Resultado de la predicción:")
                if prediction_binary[0] == 0:
                    st.write("La empresa no quiebra. Seguridad:", 1 - probability)
                elif prediction_binary[0] == 1:
                    st.write("La empresa sí quiebra. Seguridad:", probability)
                else:
                    st.write("La predicción no es clara. Probabilidad de quiebra:", probability)

        if option == "5 variables: Archivo Excel":
            st.header("5 variables: Archivo Excel")

            def download_csv2():
                # Load the content of the two CSV files
                plantilla_df2 = pd.read_csv("plantilla 2.csv", encoding="ISO-8859-1")
                prueba_df2 = pd.read_csv("prueba_2.csv", encoding="ISO-8859-1")

                # Encode the CSV content to base64
                plantilla_b64 = base64.b64encode(plantilla_df2.to_csv(index=False).encode()).decode()
                prueba_b64 = base64.b64encode(prueba_df2.to_csv(index=False).encode()).decode()

                # Create two different download links for each file
                href = f'<a href="data:file/csv;base64,{plantilla_b64}" download="plantilla_2.csv">Descargar plantilla</a>'


                return href

            # Mostrar botón de descarga de plantilla
            st.markdown(download_csv2(), unsafe_allow_html=True)


            # Carga del archivo Excel
            uploaded_file2 = st.file_uploader("Selecciona un archivo Excel", type=["xlsx", "xls","csv"], key="file_uploader_2")

        # Descargar plantilla
        
        if uploaded_file2 is not None:
            df = pd.read_excel(uploaded_file2)

            if st.button("Calcular"):
                # Realiza la predicción utilizando el modelo cargado
                prediction = modelo_xgb2.predict(xgb.DMatrix(df))
                prediction_binary = [round(value) for value in prediction]
                probability = prediction[0]

                # Imprime el resultado de la predicción y la seguridad
                st.subheader("Resultado de la predicción:")
                if prediction_binary[0] == 0:
                    st.write("La empresa no quiebra. Seguridad:", 1 - probability)
                elif prediction_binary[0] == 1:
                    st.write("La empresa sí quiebra. Seguridad:", probability)
                else:
                    st.write("La predicción no es clara. Probabilidad de quiebra:", probability)

        elif option == "5 variables: Datos Manuales":
                st.header("5 variables: Datos Manuales")
            
                net_value_growth_rate = st.number_input("Net Value Growth Rate:", -1.0, 1.0, 0.0)
                interest_expense_ratio = st.number_input("Interest Expense Ratio:", -1.0, 1.0, 0.0)
                realized_sales_gross_margin = st.number_input("Realized Sales Gross Margin:", -1.0, 1.0, 0.0)
                current_liabilities_equity = st.number_input("Current Liabilities/Equity:", -1.0, 1.0, 0.0)
                roa_before_interest_tax = st.number_input("ROA(A) before interest and % after tax:", -1.0, 1.0, 0.0)


                if st.button("Calcular"):
                    # Crea un diccionario con los valores ingresados
                    new_data2 = {
                            ' Net Value Growth Rate': net_value_growth_rate,
                            ' Interest Expense Ratio': interest_expense_ratio,
                            ' Realized Sales Gross Margin': realized_sales_gross_margin,
                            ' Current Liabilities/Equity': current_liabilities_equity,
                            ' ROA(A) before interest and % after tax': roa_before_interest_tax,
                                }

                    # Realiza la predicción utilizando el modelo cargado
                    df = pd.DataFrame(new_data2, index=[0])
                    prediction = modelo_xgb2.predict(xgb.DMatrix(df))
                    prediction_binary = [round(value) for value in prediction]
                    probability = prediction[0]

                    # Imprime el resultado de la predicción y la seguridad
                    st.subheader("Resultado de la predicción:")
                    if prediction_binary[0] == 0:
                        st.write("La empresa no quiebra. Seguridad:", 1 - probability)
                    elif prediction_binary[0] == 1:
                        st.write("La empresa sí quiebra. Seguridad:", probability)
                    else:
                        st.write("La predicción no es clara. Probabilidad de quiebra:", probability)



        if option == "About Me":
            st.header("About Me")
            st.markdown("Bienvenido a mi modelo de clasificación de empresas en quiebra. Mi nombre es Álvaro González Muñoz y soy estudiante de Matemáticas-Estadística y Economía de la Universidad Complutense de Madrid.\n\n" 
                        "Actualmente trabajo como Data and AI Strategy Consultant en Capgemini invent.\n\n"
                        "Cualquier duda sobre la funcionalidad de esta aplicación, no dudes en ponerte en contacto conmigo a través de mi correo electrónico:\n\n alvgon21@ucm.es\n\n"
                        "o de mi linkedin: \n\n https://www.linkedin.com/in/%C3%A1lvaro-gonz%C3%A1lez-mu%C3%B1oz-0a7435244/")
    

    if __name__ == '__main__':
            main()