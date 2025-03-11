"""This module contains the "Home" page."""

import streamlit as st


def home_page():
    """
    Renders the Home page.
    """
    # Titre principal
    st.markdown("# OPSISE - Data Science for Cybersecurity Experts")
    st.write(
        """
        <div style="margin-left: 40px;">
        **Projet réalisé par Romain Audureau (OPSIE), Pierre Bourbon (SISE), Maxence Liogier (SISE), Robin Martin (OPSIE), Joël Sollari (SISE) dans le cadre du challenge sécurité 2025.**
        </div>
        """,
        unsafe_allow_html=True  
    )
    # Section des pages
    st.markdown("## 🚀 Naviguez facilement dans les sections de l'application :")

    # Page 1 : Exploration des logs
    st.markdown("### 1. **Exploration des Logs**")
    st.markdown(
        """
        <div style="margin-left: 40px;">
            La page *Exploration* vous permet de naviguer directement dans une table de logs, avec des filtres et des options de recherche pour vous aider à trouver rapidement ce que vous cherchez.
        </div>
    """,
    unsafe_allow_html=True
    )

    # Page 2 : Statistiques descriptives
    st.markdown("### 2. **Statistiques Descriptives**")
    st.write(
        """
        <div style="margin-left: 40px;">
    La page *Statistiques Descriptives* permet d'approfondir l'analyse des logs. Vous y trouverez des visualisations avancées et des résumés statistiques pour vous aider à mieux comprendre les tendances et les comportements des utilisateurs dans vos logs.

    Vous y trouverez également des statistiques pratiques :
    - Les **TOP 5 des IP sources les plus émettrices**.
    - Les **TOP 10 des ports (inférieurs à 1024)** avec un accès autorisé.
    </div>
    """,
    unsafe_allow_html=True
    )

    # Page 3 : Machine Learning (DBSCAN & Isolation Forest)
    st.markdown("### 3. **Machine Learning - Détection d'anomalies**")
    st.write(
        """
        <div style="margin-left: 40px;">
    La page *Machine Learning* vous permet d'utiliser des modèles de détection d'anomalies basés sur les algorithmes DBSCAN et Isolation Forest. Ces modèles sont capables de détecter des comportements anormaux et de vous aider à mieux comprendre les patterns dans vos logs.
    </div>
    """,
    unsafe_allow_html=True
    )

    # Section d'explication de l'utilisation
    st.markdown("## 📚 Comment Utiliser l'Application ?")

    st.write(
        """
        <div style="margin-left: 40px;">
    L'application est conçue pour être simple et intuitive. Chaque page vous guidera à travers les différentes étapes d'analyse.

    1. **Commencez par la page d'exploration** pour naviguer dans vos logs, obtenir des statistiques de base et investiguer les trafics réseau.
    2. **Passez à la page des statistiques descriptives** pour des analyses plus poussées.
    3. **Enfin, entraînez vos modèles de Machine Learning** pour découvrir des comportements anormaux et appliquer des techniques d'auto-apprentissage sur vos logs.
    </div>
    """,
    unsafe_allow_html=True
    )

    # Section de conclusion
    st.markdown("## 🎯 Pourquoi utiliser cette application ?")
    st.write(
        """
        <div style="margin-left: 40px;">
    Cette application a été créée pour faciliter l'analyse de logs en utilisant les techniques modernes de Data Science. Grâce à un parcours fluide, vous pouvez rapidement analyser vos logs, découvrir des anomalies et utiliser des modèles prédictifs pour améliorer la sécurité et la gestion de vos systèmes.

    Nous espérons que vous trouverez cette plateforme utile et facile à utiliser. N'hésitez pas à nous faire part de vos retours pour améliorer encore l'expérience utilisateur.
    </div>
    """,
    unsafe_allow_html=True
    )

    # Ajouter un peu de convivialité
    st.write(
        """
        <div style="margin-left: 40px;">
            Bonne exploration et analyse de vos logs ! ✨
        </div>
        """,
        unsafe_allow_html=True

        )