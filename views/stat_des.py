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

    query = "SELECT * FROM logs"
    data = pl.read_database(query, conn)

    st.write(data.head())

    # ----------------------

    counts = data["action"].value_counts()
    categories = counts["action"]
    values = counts["count"]
    fig_actions = px.pie(
        counts,
        names=categories,
        values=values,
        color=categories,
        title="Répartition des actions",
        color_discrete_map={"PERMIT": "blue", "DENY": "red"},
    )

    # ----------------------

    counts = data["rule"].value_counts().sort(by="count", descending=True)
    categories = counts["rule"]
    values = counts["count"]
    rules_most_used = px.bar(
        counts, x="rule", y="count", title="Répartition des règles"
    )

    # ----------------------

    TCP = data.filter(data["proto"] == "TCP")
    count = TCP.group_by("rule").len().sort(by="len", descending=True).head(5)
    top5TCPrules = px.bar(
        count, x="rule", y="len", title="Top5 des règles pour le protocole TCP"
    )

    # ----------------------

    UDP = data.filter(data["proto"] == "UDP")
    count = UDP.group_by("rule").len().sort(by="len", descending=True).head(10)
    top10UDPrules = px.bar(
        count, x="rule", y="len", title="Top10 des règles pour le protocole UDP"
    )

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
        title="Distribution accès en fonction des règles, de l'action et du type de port(RC6056).",
        color_discrete_map={"PERMIT": "blue", "DENY": "red"},
    )

    # ----------------------

    df_grouped = data.group_by(["date", "action"]).agg(pl.len().alias("count"))

    df_pandas = df_grouped.to_pandas()
    df_pandas = df_pandas.sort_values("date")

    trafic_par_heure = px.line(
        df_pandas,
        x="date",
        y="count",
        color="action",
        markers=True,
        title="Trafic en fonction de l'heure",
        color_discrete_map={"PERMIT": "blue", "DENY": "red"},
    )

    # ----------------------

    df_grouped = data.group_by(["ipsrc", "rule"]).agg(pl.len().alias("count"))

    df_pandas = df_grouped.to_pandas()

    heatmap1 = px.density_heatmap(
        df_pandas,
        x="ipsrc",
        y="rule",
        z="count",
        color_continuous_scale="reds",
        title="Nombre de Hit en fonction de l'IP source et de la règle",
    )

    # ----------------

    df_grouped = data.group_by(["ipsrc", "portdst_range"]).agg(pl.len().alias("count"))

    df_pandas = df_grouped.to_pandas()

    heatmap2 = px.density_heatmap(
        df_pandas,
        x="ipsrc",
        y="portdst_range",
        z="count",
        color_continuous_scale="reds",
        title="Nombre de Hit en fonction de l'IP source et du port distant",
    )

    # ----------------------

    # Group the data by 'ip_classification' and 'action' to get the count of occurrences
    grouped_data = TCP.group_by(["isprivatesrc", "action"]).agg(pl.count())

    # Convert the grouped data to Pandas for easy use in Plotly
    grouped_data_pd = grouped_data.to_pandas()

    # Create a dictionary for node labels
    node_labels = ["Private", "Public", "Allow", "Deny"]

    # Create the Sankey plot
    sankey3 = go.Figure(
        go.Sankey(
            textfont=dict(color="white", size=14),
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=node_labels,
            ),
            link=dict(
                source=[0, 0, 1, 1],
                target=[3, 2, 2, 3],  # Indexes of the target nodes (Allow/Deny)
                value=grouped_data_pd["count"].tolist(),  # Link values are the counts
            ),
        )
    )

    # Update the layout for better display
    sankey3.update_layout(title_text="Flux IP et action", font_size=10)

    # ----------------------

    TCP = data.filter(data["proto"] == "TCP")
    count = (
        TCP.select(["action", "portsrc_range"])
        .group_by(["action", "portsrc_range"])
        .count()
    )
    TCP_bar1 = px.bar(
        count,
        x="action",
        y="count",
        color="portsrc_range",
        barmode="stack",
        title="action en fonction du port source (TCP)",
    )

    # ----------------------

    count = (
        TCP.select(["action", "portdst_range"])
        .group_by(["action", "portdst_range"])
        .count()
    )
    TCP_bar2 = px.bar(
        count,
        x="action",
        y="count",
        color="portdst_range",
        barmode="stack",
        title="action en fonction du port destination (TCP)",
    )

    # ----------------------

    rules = TCP.group_by(["ipsrc_class", "isprivatesrc", "action"]).agg(
        pl.len().alias("count")
    )
    TCP_bar3 = px.bar(
        rules,
        x="ipsrc_class",  # Grouping by 'rule'
        y="count",  # Y-axis: Count of occurrences
        color="action",  # Color by action type (e.g., allow/deny)
        barmode="stack",
        text="isprivatesrc",
        title="Actions en fonction des classes IP (TCP)",
        color_discrete_map={"PERMIT": "blue", "DENY": "red"},
    )

    # ----------------------

    UDP = data.filter(data["proto"] == "UDP")
    count = (
        UDP.select(["action", "portsrc_range"])
        .group_by(["action", "portsrc_range"])
        .count()
    )
    UDP_bar1 = px.bar(
        count,
        x="action",
        y="count",
        color="portsrc_range",
        barmode="stack",
        title="action en fonction du port source (UDP)",
    )

    # ----------------------

    count = (
        UDP.select(["action", "portdst_range"])
        .group_by(["action", "portdst_range"])
        .count()
    )
    UDP_bar2 = px.bar(
        count,
        x="action",
        y="count",
        color="portdst_range",
        barmode="stack",
        title="action en fonction du port destination (UDP)",
    )

    # ----------------------

    rules = UDP.group_by(["ipsrc_class", "isprivatesrc", "action"]).agg(
        pl.len().alias("count")
    )

    UDP_bar3 = px.bar(
        rules,
        x="ipsrc_class",  # Grouping by 'rule'
        y="count",  # Y-axis: Count of occurrences
        color="action",  # Color by action type (e.g., allow/deny)
        barmode="stack",
        text="isprivatesrc",
        title="Actions en fonction des classes IP (UDP)",
        color_discrete_map={"PERMIT": "blue", "DENY": "red"},
    )

    # ----------------------

    # Afficher les graphiques dans Streamlit côte à côte
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(rules_most_used)
        st.plotly_chart(heatmap1)
        st.plotly_chart(top10UDPrules)
        st.plotly_chart(UDP_bar1)
        st.plotly_chart(UDP_bar2)
        st.plotly_chart(UDP_bar3)

    with col2:
        st.plotly_chart(fig_actions)
        st.plotly_chart(heatmap2)
        st.plotly_chart(top5TCPrules)
        st.plotly_chart(TCP_bar1)
        st.plotly_chart(TCP_bar2)
        st.plotly_chart(TCP_bar3)

    st.plotly_chart(distribution1)
    st.plotly_chart(trafic_par_heure)
    st.plotly_chart(sankey3)
