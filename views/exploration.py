import psycopg2
import time
import ipaddress
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
    st.markdown("# Page d'exploration résumant les trafics réseau")

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
    query_ips = "SELECT DISTINCT ipsrc FROM logs;"
    df_ips = pd.read_sql_query(query_ips, conn)

    # st.write(df_ips.shape)
    # st.write(df_ips)

    # st.write(df_ips["ipsrc"].str.split(".", expand=True).shape)

    df_ips[["octet1", "octet2", "octet3", "octet4"]] = df_ips["ipsrc"].str.split(
        ".", expand=True
    )
    select1 = df_ips.loc[:, "octet1"].unique()
    select2 = df_ips.loc[:, "octet2"].unique()
    select3 = df_ips.loc[:, "octet3"].unique()
    select4 = df_ips.loc[:, "octet4"].unique()
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

    query = f"""
    SELECT * FROM logs
    WHERE ipsrc BETWEEN '{octet1s}.{octet2s}.{octet3s}.{octet4s}' AND '{octet1f}.{octet2f}.{octet3f}.{octet4f}';
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    st.write("Tableau de données")
    st.dataframe(df)

    # --------------

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

    # --------------

    df_counted = df.groupby(["ipsrc", "ipdst"]).size().reset_index(name="count")

    unique_ips = list(set(df_counted["ipsrc"].tolist() + df_counted["ipdst"].tolist()))

    node_map = {ip: idx for idx, ip in enumerate(unique_ips)}

    df_counted["source_index"] = df_counted["ipsrc"].map(node_map)
    df_counted["target_index"] = df_counted["ipdst"].map(node_map)

    sankey1 = go.Figure(
        go.Sankey(
            textfont=dict(color="white", size=14),
            node=dict(
                pad=20,
                thickness=30,
                line=dict(color="black", width=0.5),
                label=unique_ips,
            ),
            link=dict(
                source=df_counted["source_index"],
                target=df_counted["target_index"],
                value=df_counted["count"],
            ),
        )
    )
    sankey1.update_layout(
        title_text="Trafic entre IP Source et IP Destination", font_size=10, height=800
    )

    # ---------------

    df_counted = df.groupby(["ipsrc", "portdst_range"]).size().reset_index(name="count")

    unique_ips = list(set(df_counted["ipsrc"].tolist()))
    unique_ports = list(set(df_counted["portdst_range"].tolist()))

    node_map = {ip: idx for idx, ip in enumerate(unique_ips)}
    node_map.update(
        {port: idx + len(unique_ips) for idx, port in enumerate(unique_ports)}
    )

    df_counted["source_index"] = df_counted["ipsrc"].map(node_map)
    df_counted["target_index"] = df_counted["portdst_range"].map(node_map)
    sankey2 = go.Figure(
        go.Sankey(
            textfont=dict(color="white", size=14),
            node=dict(
                label=unique_ips + unique_ports,
                pad=20,
                thickness=20,
            ),
            link=dict(
                source=df_counted["source_index"],
                target=df_counted["target_index"],
                value=df_counted["count"],
            ),
        )
    )

    sankey2.update_layout(
        title_text="Trafic entre IP Source et Port Destination",
        font_size=10,
        height=800,
    )

    st.plotly_chart(fig)
    st.plotly_chart(sankey1)
    st.plotly_chart(sankey2)
