import psycopg2
import time
import ipaddress
import streamlit as st
import pandas as pd
import plotly.express as px

# import plotly.graph_objects as go


def ip_to_int(ip):
    """Convertit une adresse IP en entier"""
    return int(ipaddress.IPv4Address(ip))


def int_to_ip(ip_int):
    """Convertit un entier en adresse IP"""
    return str(ipaddress.IPv4Address(ip_int))


def exploration_page():
    """
    Renders the Data Exploration page
    """
    st.markdown("# Page exploration résumant les stats principales")

    st.write("Tableau de données")
    st.write("Visualisation interactive des données")
    st.write(
        "IP source avec le nombre d’occurrences de destination contactées, incluant le nombre de flux rejetés et autorisés"
    )
    st.write("Globalement : Tableau, graphs et filtres")

    MAX_RETRIES = 10  # Nombre maximum de tentatives
    WAIT_SECONDS = 4  # Temps d'attente entre chaque tentative

    for i in range(MAX_RETRIES):
        try:
            conn = psycopg2.connect(
                host="postgres",
                database="challenge_secu",
                user="admin",
                password="admin",
                port=5432,
            )
            print("Connexion réussie à PostgreSQL !")
            break  # Sort de la boucle dès que la connexion est établie
        except psycopg2.OperationalError:
            st.write(
                f"🔄 Tentative {i+1}/{MAX_RETRIES} : PostgreSQL n'est pas encore prêt..."
            )
            time.sleep(WAIT_SECONDS)
    else:
        st.write("Impossible de se connecter à PostgreSQL après plusieurs tentatives.")
        exit(1)

    # Récupération des IPs uniques pour aider l'utilisateur à filtrer
    query_ips = "SELECT DISTINCT ipsrc FROM logs LIMIT 1000;"
    df_ips = pd.read_sql_query(query_ips, conn)

    # st.write(df_ips.shape)
    # st.write(df_ips)
    
    # st.write(df_ips["ipsrc"].str.split(".", expand=True).shape)

    df_ips[["octet1", "octet2", "octet3", "octet4"]] = df_ips["ipsrc"].str.split(".", expand=True)
    select1 = df_ips.loc[:,"octet1"].unique()
    select2 = df_ips.loc[:,"octet2"].unique()
    select3 = df_ips.loc[:,"octet3"].unique()
    select4 = df_ips.loc[:,"octet4"].unique()
    st.write("Filtres avancés")
    st.write("Début de la plage IP")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        octet1s = st.selectbox("Octet1", select1)
    with col2:
        octet2s = st.selectbox("Octet2", select2)
    with col3:
        octet3s = st.selectbox("Octet3", select3)
    with col4:
        octet4s = st.selectbox("Octet4", select4)

    st.write("Fin de la plage IP")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        octet1f = st.selectbox("Octet 1", select1)
    with col6:
        octet2f = st.selectbox("Octet 2", select2)
    with col7:
        octet3f = st.selectbox("Octet 3", select3)
    with col8:
        octet4f = st.selectbox("Octet 4", select4)

    # ip_list = sorted(df_ips["ipsrc"].tolist())  # Trier les IPs pour l'affichage
    # col1, col2 = st.columns(2)
    # start_ip = col1.selectbox("IP de début", ip_list, index=0)
    # end_ip = col2.selectbox("IP de fin", ip_list, index=len(ip_list) - 1)
    
    # df_ips["ip_num"] = df_ips["ipsrc"].apply(ip_to_int)
    # start_ip, end_ip = df_ips["ip_num"].min(), df_ips["ip_num"].max()
    # start_ip_num, end_ip_num = st.slider(
    #     "Sélectionnez une plage d'IP",
    #     min_value=start_ip,
    #     max_value=end_ip,
    #     value=(start_ip, end_ip),
    #     format="%d",
    # )
    # ip_start, ip_end = int_to_ip(start_ip_num), int_to_ip(end_ip_num)




    query = f"""
    SELECT * FROM logs
    WHERE ipsrc BETWEEN '{octet1s}.{octet2s}.{octet3s}.{octet4s}' AND '{octet1f}.{octet2f}.{octet3f}.{octet4f}'
    ORDER BY RANDOM()
    LIMIT 1000;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    st.write("Tableau de données")
    st.dataframe(df)

    # groupby ipsrc et action
    df_grouped = df.groupby(["ipsrc", "action"]).size().reset_index(name="count")
    df_grouped["ip_num"] = df_grouped["ipsrc"].apply(ip_to_int)
    df_grouped = df_grouped.sort_values("ip_num")

    # Histogramme des occurrences des IP sources, selon l'action
    couleurs = {"PERMIT": "blue", "DENY": "red"}
    fig = px.bar(
        df_grouped,
        x="ipsrc",
        y="count",
        color="action",
        title="Nombre d'opérations par IP source, selon l'action",
        labels={
            "ipsrc": "IP Source",
            "count": "Nombre d'opérations",
            "action": "Action",
        },
        barmode="stack",  # Mode empilé
        color_discrete_map=couleurs,
    )
    st.plotly_chart(fig)
