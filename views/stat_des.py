import psycopg2
import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import polars as pl


def stat_des_page():
    """
    Renders the Descriptive Statistics page
    """
    st.markdown("# Page de statistiques descriptives")

    st.write("Tableau de données")
    st.write(
        "Colonnes : IP Source, Port, Type de flux (rejeté/autorisé), Date et heure, etc."
    )
    st.write("Statistiques détaillées")
    st.write("Nombre d'occurrences pour chaque IP source contactée.")
    st.write("Répartition des flux rejetés et autorisés par IP source.")
    st.write("Graphiques détaillés")
    st.write("Histogramme des occurrences des IP sources.")
    st.write("Graphique en secteurs des types de flux par IP source.")
    st.write("Filtres avancés")
    st.write("Permet de filtrer les données par plages de dates, types de flux, etc.")

    # # Se connecter à la base de données SQLite
    # MAX_RETRIES = 10  # Nombre maximum de tentatives
    # WAIT_SECONDS = 2  # Temps d'attente entre chaque tentative

    # for i in range(MAX_RETRIES):
    #     try:
    #         conn = psycopg2.connect(
    #             host="postgres",
    #             database="challenge_secu",
    #             user="admin",
    #             password="admin",
    #             port=5432,
    #         )
    #         print("Connexion réussie à PostgreSQL !")
    #         break  # Sort de la boucle dès que la connexion est établie
    #     except psycopg2.OperationalError:
    #         st.write(
    #             f"🔄 Tentative {i+1}/{MAX_RETRIES} : PostgreSQL n'est pas encore prêt..."
    #         )
    #         time.sleep(WAIT_SECONDS)
    # else:
    #     st.write("Impossible de se connecter à PostgreSQL après plusieurs tentatives.")
    #     exit(1)

    # query = "SELECT * FROM logs ORDER BY RANDOM() LIMIT 100000;"
    # # on échantillonne pour des raisons de performance
    # df = pd.read_sql_query(query, conn)
    # conn.close()

    # # Créer un piechart pour 'proto'
    # proto_counts = df["proto"].value_counts()
    # fig_proto = go.Figure(
    #     data=[go.Pie(labels=proto_counts.index, values=proto_counts.values)],
    #     layout=go.Layout(title="Répartition des protocoles", width=600, height=400),
    # )

    # # Créer un graphique en secteurs pour 'action'
    # action_counts = df["action"].value_counts()
    # fig_action = go.Figure(
    #     data=[go.Pie(labels=action_counts.index, values=action_counts.values)],
    #     layout=go.Layout(title="Répartition des actions", width=600, height=400),
    # )

    
    data = pl.read_parquet(r"data\logs_processed.parquet")
    data = data.with_columns(
        year = data["date"].dt.year().cast(pl.Utf8),
        month = data['date'].dt.month().cast(pl.Utf8),
        day = data["date"].dt.day().cast(pl.Utf8),
        timestamp = data["date"].dt.time(),
        rule = data["rule"].cast(pl.Utf8),
        portsrc_range = data["portsrc"].map_elements(lambda x: "well-known" if x < 1024 else 
                                            "Registered" if x < 49152 else 
                                            "Dynamic").alias("portsrc_range"),
        portdst_range = data["portdst"].map_elements(lambda x: "well-known" if x < 1024 else 
                                            "Registered" if x < 49152 else 
                                            "Dynamic").alias("portdst_range")
    )


    st.write(data.head())

    #----------------------
    
    counts = data["action"].value_counts()
    categories = counts["action"]
    values = counts["count"]
    fig_actions = px.pie(counts, names=categories, values=values, title="Répartition des actions")

    #----------------------
    
    counts = data["rule"].value_counts().sort(by="count", descending=True)
    categories = counts["rule"]
    values = counts["count"]
    rules_most_used = px.bar(counts, x="rule", y="count", title="Répartition des règles")

    #----------------------
    
    TCP = data.filter(data["proto"]=="TCP")
    count = TCP.group_by("rule").len().sort(by="len", descending=True).head(5)
    top5TCPrules = px.bar(count, x="rule", y="len", title="Top5 des règles pour le protocole TCP")

    #----------------------
    
    UDP = data.filter(data["proto"]=="UDP")
    count = UDP.group_by("rule").len().sort(by="len", descending=True).head(10)
    top10UDPrules = px.bar(count, x="rule", y="len", title="Top10 des règles pour le protocole UDP")

    rules = data.group_by(["rule", "portdst_range", "action"]).agg(
    pl.len().alias("count")
    )

    distribution1 = px.bar(
        rules,
        x="rule",
        y="count",
        color="action", 
        barmode="stack",
        text="portdst_range",
        title= "Distribution accès en fonction des règles, de l'action et du type de port(RC6056)."
    )

    #----------------------
    
    df_grouped = data.group_by(["date", "action"]).agg(
        pl.len().alias("count")
    )

    df_pandas = df_grouped.to_pandas()
    df_pandas = df_pandas.sort_values("date")

    traffic_par_heure = px.line(
        df_pandas,
        x="date", 
        y="count", 
        color="action", 
        markers=True, 
        title="Traffic en fonction de l'heure"
    )

    #----------------------

    df_grouped = data.group_by(["ipsrc", "rule"]).agg(
        pl.len().alias("count")
    )

    df_pandas = df_grouped.to_pandas()


    heatmap1 = px.density_heatmap(
        df_pandas,
        x="ipsrc",
        y="rule",
        z="count",
        color_continuous_scale="reds",
        title="Nombre de Hit en fonction de l'IP source et de la règle"
    )

    #----------------

    df_grouped = data.group_by(["ipsrc", "portdst_range"]).agg(
        pl.len().alias("count")
    )

    df_pandas = df_grouped.to_pandas()


    heatmap2 = px.density_heatmap(
        df_pandas,
        x="ipsrc",
        y="portdst_range",
        z="count",
        color_continuous_scale="reds",
        title="Nombre de Hit en fonction de l'IP source et du port distant"
    )

    #--------------

    df_pandas = data.to_pandas()
    df_counted = df_pandas.groupby(['ipsrc', 'ipdst']).size().reset_index(name='count')


    unique_ips = list(set(df_counted["ipsrc"].tolist() + df_counted["ipdst"].tolist()))

    node_map = {ip: idx for idx, ip in enumerate(unique_ips)}

    df_counted["source_index"] = df_counted["ipsrc"].map(node_map)
    df_counted["target_index"] = df_counted["ipdst"].map(node_map)


    sankey1 = go.Figure(go.Sankey(
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
        )        
    ))
    sankey1.update_layout(
        title_text="Traffic entre IP Source et IP Destination",
        font_size=10,
        height=800)
    
    #---------------

    df_counted = df_pandas.groupby(['ipsrc', 'portdst_range']).size().reset_index(name='count')

    unique_ips = list(set(df_counted["ipsrc"].tolist()))
    unique_ports = list(set(df_counted["portdst_range"].tolist()))


    node_map = {ip: idx for idx, ip in enumerate(unique_ips)}
    node_map.update({port: idx + len(unique_ips) for idx, port in enumerate(unique_ports)})

    df_counted["source_index"] = df_counted["ipsrc"].map(node_map)
    df_counted["target_index"] = df_counted["portdst_range"].map(node_map)
    sankey2 = go.Figure(go.Sankey(
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
        )
    ))

    sankey2.update_layout(
        title_text="Traffic entre Source IP et Destination Port",
        font_size=10,
        height=800)

    #----------------------

    # Group the data by 'ip_classification' and 'action' to get the count of occurrences
    grouped_data = TCP.group_by(["isprivatesrc", "action"]).agg(pl.count())

    # Convert the grouped data to Pandas for easy use in Plotly
    grouped_data_pd = grouped_data.to_pandas()

    # Create a dictionary for node labels
    node_labels = ["Private", "Public", "Allow", "Deny"]

    # Create the Sankey plot
    sankey3 = go.Figure(go.Sankey(
        textfont=dict(color="white", size=14),
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels
        ),
        link=dict(
            source=[0, 0, 1, 1],
            target=[3,2,2,3],  # Indexes of the target nodes (Allow/Deny)
            value=grouped_data_pd["count"].tolist()  # Link values are the counts
        )
    ))

    # Update the layout for better display
    sankey3.update_layout(title_text="Flux IP et action", font_size=10)

    #----------------------

    
    TCP = data.filter(data["proto"] == "TCP")
    count = TCP.select(["action", "portsrc_range"]).group_by(["action", "portsrc_range"]).count()
    TCP_bar1 = px.bar(count, x="action", y="count", color="portsrc_range", barmode="stack", title="action en fonction du port source (TCP)")

    #----------------------

    count = TCP.select(["action", "portdst_range"]).group_by(["action", "portdst_range"]).count()
    TCP_bar2 = px.bar(count, x="action", y="count", color="portdst_range", barmode="stack", title="action en fonction du port destination (TCP)")

    #----------------------

    rules = TCP.group_by(["ipsrc_class", "isprivatesrc", "action"]).agg(
        pl.len().alias("count")
    )
    TCP_bar3 = px.bar(
        rules,
        x="ipsrc_class",       # Grouping by 'rule'
        y="count",      # Y-axis: Count of occurrences
        color="isprivatesrc", # Color by action type (e.g., allow/deny)
        barmode="stack",
        text="action",
        title= "Distribution actions en fonction des classes IP, de l'action et de la nature du réseau."
    )

    #----------------------

    UDP = data.filter(data["proto"] == "UDP")
    count = UDP.select(["action", "portsrc_range"]).group_by(["action", "portsrc_range"]).count()
    UDP_bar1 = px.bar(count, x="action", y="count", color="portsrc_range", barmode="stack", title="action en fonction du port source (UDP)")

    #----------------------

    count = UDP.select(["action", "portdst_range"]).group_by(["action", "portdst_range"]).count()
    UDP_bar2 = px.bar(count, x="action", y="count", color="portdst_range", barmode="stack", title="action en fonction du port destination (UDP)")

    #----------------------

    rules = UDP.group_by(["ipsrc_class", "isprivatesrc", "action"]).agg(
        pl.len().alias("count")
    )
    
    UDP_bar3 = px.bar(
        rules,
        x="ipsrc_class",       # Grouping by 'rule'
        y="count",      # Y-axis: Count of occurrences
        color="isprivatesrc", # Color by action type (e.g., allow/deny)
        barmode="stack",
        text="action",
        title= "Distribution actions en fonction des classes IP, de l'action et de la nature du réseau."
    )

    #----------------------


    # Afficher les graphiques dans Streamlit côte à côte
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(rules_most_used)
        st.plotly_chart(top5TCPrules)
        st.plotly_chart(top10UDPrules)

    with col2:
        st.plotly_chart(fig_actions)
        st.plotly_chart(heatmap1)
        st.plotly_chart(heatmap2)
        st.plotly_chart(TCP_bar1)
        st.plotly_chart(TCP_bar2)
        st.plotly_chart(TCP_bar3)
        st.plotly_chart(UDP_bar1)
        st.plotly_chart(UDP_bar2)
        st.plotly_chart(UDP_bar3)
    
    st.plotly_chart(distribution1)
    st.plotly_chart(traffic_par_heure)
    st.plotly_chart(sankey1)
    st.plotly_chart(sankey2)
    st.plotly_chart(sankey3)

