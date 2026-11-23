"""
Prototype Streamlit - Bulletin statistique trimestriel de l'économie et des finances
Burkina Faso - 3e trimestre 2026
Données extraites du bulletin officiel (DGESS / MEF)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="Bulletin ASEF - Burkina Faso",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS léger
st.markdown("""
<style>
    .main-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a365d;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #4a5568;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f7fafc;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #2b6cb0;
    }
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid="stToolbar"] {
        display: none !important;
    }
    header [data-testid="stMainMenu"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DONNÉES EXTRAITES DU BULLETIN T3 2026
# ============================================================

# --- Comptes nationaux (Tableau I.1) - en milliards FCFA ---
df_pib = pd.DataFrame({
    "Trimestre": ["T2_2024", "T3_2024", "T4_2024", "T1_2025", "T2_2025"],
    "Secteur primaire": [504.0, 520.5, 527.5, 528.9, 543.9],
    "Secteur secondaire": [583.3, 591.0, 643.0, 610.7, 582.0],
    "Secteur tertiaire": [1226.6, 1263.9, 1276.8, 1241.5, 1246.4],
    "Impôts et taxes": [299.4, 293.4, 320.1, 284.7, 311.2],
    "PIB": [2615.4, 2674.5, 2769.2, 2676.0, 2683.7]
})

# Contributions à la croissance (Graphique 1)
df_contrib = pd.DataFrame({
    "Trimestre": ["T3_2024", "T4_2024", "T1_2025", "T2_2025"],
    "Primaire": [0.63, 0.26, 0.05, 0.56],
    "Secondaire": [0.30, 1.94, -1.16, -1.07],
    "Tertiaire": [1.43, 0.48, -1.27, 0.18],
    "Impôts et taxes": [-0.23, 1.00, -1.28, 0.99],
    "Croissance PIB": [2.26, 3.54, -3.37, 0.29]
})

# --- IPI (Tableau I.2) - base 100 en 2015 ---
df_ipi = pd.DataFrame({
    "Branche": [
        "Industries extractives", "Extraction de minerais métalliques",
        "Activités de soutien aux industries extractives",
        "Industries manufacturières", "Fabrication de produits alimentaires",
        "Fabrication de boissons", "Fabrication de produits à base de tabac",
        "Activités de fabrication de textiles", "Fabrication d'articles d'habillement",
        "Travail du bois", "Fabrication de produits chimiques",
        "Métallurgie", "Industries électricité/gaz/eau",
        "Production et distribution d'électricité et de gaz",
        "Captage, traitement et distribution d'eau",
        "Indice Global"
    ],
    "T3_2024": [116.2, 109.6, 177.5, 201.8, 203.1, 198.4, 68.1, 116.0, 200.6, 401.0, 640.0, 86.1, 415.7, 436.4, 226.9, 149.0],
    "T2_2025": [79.0, 74.9, 90.2, 197.1, 196.5, 75.0, 165.3, 125.3, 606.0, 462.8, 549.6, 124.7, 590.6, 777.1, 228.3, 133.9],
    "T3_2025": [90.7, 85.8, 125.1, 174.9, 222.8, 60.4, 106.7, 120.9, 556.4, 602.5, 970.2, 35.3, 454.7, 532.8, 226.8, 129.0],
    "Glissement_trim_%": [14.8, 14.6, 38.7, -11.3, 13.4, -19.5, -35.5, -3.5, -8.2, 30.2, 76.5, -71.7, -23.0, -31.4, -0.7, -3.7],
    "Glissement_an_%": [-21.9, -21.7, -29.5, -13.3, 9.7, -69.6, 56.7, 4.2, 177.4, 50.2, 51.6, -59.0, 9.4, 22.1, 0.0, -13.4]
})

# --- IHPC (Tableau I.4) ---
df_ihpc = pd.DataFrame({
    "Fonction": [
        "Produits alimentaires et boissons non alcoolisées",
        "Boissons alcoolisées, tabac et stupéfiants",
        "Articles d'habillement et chaussures",
        "Logement, eau, gaz, électricité et autres combustibles",
        "Meubles, articles de ménage",
        "Santé", "Transports", "Communication",
        "Loisirs et culture", "Enseignement",
        "Restaurants et hôtels", "Biens et services divers",
        "Indice global"
    ],
    "T1_2025": [106.32, 107.28, 100.07, 101.46, 100.62, 101.19, 101.44, 100.81, 99.71, 101.39, 102.27, 101.61, 102.90],
    "T4_2025": [105.17, 107.90, 100.73, 103.37, 101.27, 102.17, 101.47, 95.97, 100.57, 101.60, 105.10, 101.70, 103.00],
    "T1_2026": [104.22, 110.20, 100.93, 104.95, 101.44, 102.13, 101.75, 99.80, 100.60, 97.62, 106.39, 101.81, 103.36],
    "Glissement_trim_%": [-0.90, 2.13, 0.20, 1.53, 0.17, -0.04, 0.28, 3.99, 0.03, -3.92, 1.23, 0.11, 0.35],
    "Glissement_an_%": [-1.98, 2.72, 0.87, 3.44, 0.82, 0.93, 0.30, -1.01, 0.89, -3.72, 4.03, 0.20, 0.45]
})

# --- Recettes ordinaires (Tableau II.1) ---
df_recettes = pd.DataFrame({
    "Catégorie": ["Recettes fiscales", "Recettes non fiscales", "Recettes en capital", "Total Général"],
    "Prév_LFR_2026": [3007.02, 327.29, 7.22, 3341.53],
    "T3_2025": [709.29, 217.25, 1.49, 928.03],
    "T1_2026": [717.99, 74.56, 0.02, 792.57],
    "T2_2026": [930.88, 212.78, 1.62, 1145.28],
    "T3_2026": [897.31, 165.94, 0.62, 1063.87],
    "Cumul_fin_sept_2026": [2546.19, 453.27, 2.26, 3001.72],
    "Taux_exécution_%": [83.59, 91.55, 31.30, 84.59]
})

# --- Taux de recouvrement par régie ---
df_taux_regie = pd.DataFrame({
    "Régie": ["DGD", "DGI", "DGTCP"],
    "Fin sept 2025": [70.77, 75.38, 133.60],
    "Fin juin 2026": [57.99, 57.50, 89.15],
    "Fin sept 2026": [78.30, 88.38, 90.87]
})

# --- TOFE Soldes (Tableau I.18) ---
df_tofe = pd.DataFrame({
    "Indicateur": [
        "Solde global (base engagement)",
        "Solde global hors dons (base engagement)",
        "Solde primaire de base",
        "Solde de base",
        "Solde global base caisse",
        "Solde global base caisse hors dons",
        "Financement net"
    ],
    "T3_2025": [-47.09, -119.48, 160.64, 73.04, -210.12, -282.51, 213.42],
    "T1_2026": [171.76, 154.06, 301.78, 236.44, 148.17, 130.48, -147.35],
    "T2_2026": [53.89, 22.02, 264.71, 150.03, -56.41, -88.28, 58.14],
    "T3_2026": [-161.35, -197.29, 55.48, -22.67, 64.54, 28.60, -66.09]
})

# --- Balance des paiements (extrait Tableau I.6) ---
df_bop = pd.DataFrame({
    "Poste": [
        "Compte des transactions courantes",
        "Biens",
        "Services",
        "Revenu primaire",
        "Revenu secondaire",
        "Compte de capital",
        "Solde global"
    ],
    "T2_2025": [351.97, 602.09, -137.21, -219.81, 106.90, 56.41, 89.38],
    "T1_2026": [1451.46, 1483.96, -152.76, 4.79, 115.47, 33.46, 839.72],
    "T2_2026": [946.89, 1356.31, -163.67, -347.11, 101.37, 43.97, 224.74]
})

# ============================================================
# SIDEBAR - NAVIGATION
# ============================================================
st.sidebar.markdown("### 📊 Bulletin ASEF")
st.sidebar.caption("Burkina Faso · MEF / DGESS · T3 2026")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Tableau de bord",
        "📈 I.1 Comptes nationaux",
        "🏭 I.2 Industrie (IPI)",
        "💰 I.3 Prix (IHPC)",
        "🌍 I.4 Balance des paiements",
        "💵 II. Mobilisation des ressources",
        "📑 III. TOFE & Finances publiques"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Source** : Bulletin statistique trimestriel de l'économie et des finances – 3e trimestre 2026\n\n"
    "Direction Générale des Études et des Statistiques Sectorielles (DGESS)"
)

# ============================================================
# PAGE : TABLEAU DE BORD
# ============================================================
if page == "🏠 Tableau de bord":
    st.markdown('<p class="main-header">Bulletin des statistiques économiques et financières</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Vue d\'ensemble · 3e trimestre 2026 · Données extraites du bulletin officiel</p>', unsafe_allow_html=True)

    # --- KPI Cards ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Taux de réalisation des recettes",
            value="84,6 %",
            delta="Cumul fin sept. 2026",
            help="Recettes ordinaires totales / Prévisions LFR 2026"
        )

    with col2:
        st.metric(
            label="PIB réel (T2 2025)",
            value="2 683,7 Mds",
            delta="+0,3 % trim. / +2,6 % an.",
            help="En volume, CVS, milliards FCFA"
        )

    with col3:
        st.metric(
            label="IHPC (T1 2026)",
            value="103,36",
            delta="+0,35 % trim. / +0,45 % an.",
            help="Indice harmonisé des prix à la consommation (base 100 en 2023)"
        )

    with col4:
        st.metric(
            label="IPI Global (T3 2025)",
            value="129,0",
            delta="-3,7 % trim. / -13,4 % an.",
            help="Indice de la production industrielle (base 100 en 2015)"
        )

    st.markdown("---")

    # --- Graphique PIB ---
    st.subheader("Évolution du PIB trimestriel (milliards FCFA, CVS)")

    fig_pib = go.Figure()
    fig_pib.add_trace(go.Scatter(
        x=df_pib["Trimestre"],
        y=df_pib["PIB"],
        mode="lines+markers",
        name="PIB",
        line=dict(color="#2b6cb0", width=3),
        marker=dict(size=10)
    ))
    fig_pib.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis_title="Milliards FCFA",
        xaxis_title="",
        template="plotly_white",
        hovermode="x unified"
    )
    st.plotly_chart(fig_pib, use_container_width=True)

    # --- Deux colonnes : contributions + recettes ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Contributions à la croissance du PIB (points de %)")
        fig_contrib = px.bar(
            df_contrib.melt(id_vars="Trimestre", var_name="Secteur", value_name="Contribution"),
            x="Trimestre",
            y="Contribution",
            color="Secteur",
            barmode="relative",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_contrib.update_layout(height=360, margin=dict(l=10, r=10, t=20, b=10), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_contrib, use_container_width=True)

    with c2:
        st.subheader("Taux de recouvrement par régie (%)")
        fig_taux = px.bar(
            df_taux_regie.melt(id_vars="Régie", var_name="Période", value_name="Taux"),
            x="Régie",
            y="Taux",
            color="Période",
            barmode="group",
            text_auto=".1f",
            color_discrete_sequence=["#a0aec0", "#63b3ed", "#2b6cb0"]
        )
        fig_taux.update_layout(height=360, margin=dict(l=10, r=10, t=20, b=10), yaxis_title="Taux (%)")
        st.plotly_chart(fig_taux, use_container_width=True)

    # --- Résumé textuel ---
    st.markdown("---")
    st.markdown("""
    **Points clés du 3e trimestre 2026 (et données les plus récentes disponibles) :**
    - Les recettes ordinaires totales atteignent **1 063,87 milliards FCFA** au T3 2026 (−81,4 Mds vs T2).
    - Taux de réalisation cumulé à fin septembre : **84,6 %** des prévisions LFR.
    - Le PIB réel au T2 2025 progresse légèrement (+0,3 % trim.), porté par le primaire et les impôts.
    - L’IPI global recule de 3,7 % au T3 2025, principalement sous l’effet des industries manufacturières et de l’énergie.
    - L’IHPC reste stable (+0,35 % au T1 2026).
    """)

# ============================================================
# PAGE : COMPTES NATIONAUX
# ============================================================
elif page == "📈 I.1 Comptes nationaux":
    st.markdown("## I.1 Comptes économiques de la Nation")
    st.caption("Valeur ajoutée brute par branche d’activités en volume (prix de l’année précédente, chaînés, CVS) — milliards FCFA")

    st.dataframe(
        df_pib.style.format("{:.1f}"),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("#### Évolution des secteurs")
    fig = px.line(
        df_pib.melt(id_vars="Trimestre", var_name="Secteur", value_name="Valeur"),
        x="Trimestre", y="Valeur", color="Secteur",
        markers=True
    )
    fig.update_layout(height=420, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Contributions à la croissance (points de pourcentage)")
    st.dataframe(df_contrib.style.format("{:.2f}"), use_container_width=True, hide_index=True)

    st.info("""
    **Lecture** : Au T2 2025, le PIB réel progresse de **+7,75 milliards FCFA** par rapport au T1 2025 (+0,3 %).  
    En glissement annuel, la hausse est de **+68,34 milliards FCFA** (+2,6 %).  
    Le secteur primaire et les impôts nets sur les produits sont les principaux moteurs.
    """)

# ============================================================
# PAGE : IPI
# ============================================================
elif page == "🏭 I.2 Industrie (IPI)":
    st.markdown("## I.2 Statistiques relatives aux activités industrielles")
    st.caption("Indice de la production industrielle (IPI) — base 100 en 2015")

    # Filtre
    branches = st.multiselect(
        "Sélectionner des branches",
        options=df_ipi["Branche"].tolist(),
        default=["Indice Global", "Industries extractives", "Industries manufacturières", "Industries électricité/gaz/eau"]
    )

    df_filtered = df_ipi[df_ipi["Branche"].isin(branches)] if branches else df_ipi

    st.dataframe(
        df_filtered.style.format({
            "T3_2024": "{:.1f}", "T2_2025": "{:.1f}", "T3_2025": "{:.1f}",
            "Glissement_trim_%": "{:+.1f}", "Glissement_an_%": "{:+.1f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    # Graphique glissements
    st.subheader("Glissements trimestriel et annuel (T3 2025)")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Glissement trimestriel",
        x=df_filtered["Branche"],
        y=df_filtered["Glissement_trim_%"],
        marker_color="#3182ce"
    ))
    fig.add_trace(go.Bar(
        name="Glissement annuel",
        x=df_filtered["Branche"],
        y=df_filtered["Glissement_an_%"],
        marker_color="#e53e3e"
    ))
    fig.update_layout(
        barmode="group",
        height=450,
        xaxis_tickangle=-35,
        yaxis_title="Variation (%)",
        template="plotly_white",
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.warning("""
    **Faits marquants T3 2025** :  
    - IPI global : **−3,7 %** en variation trimestrielle et **−13,4 %** en glissement annuel.  
    - Forte baisse dans les industries manufacturières (−11,3 %) et l’électricité/gaz/eau (−23,0 %).  
    - Rebond des industries extractives (+14,8 % trim.), notamment les activités de soutien (+38,7 %).
    """)

# ============================================================
# PAGE : IHPC
# ============================================================
elif page == "💰 I.3 Prix (IHPC)":
    st.markdown("## I.3 Niveau général des prix")
    st.caption("Indice harmonisé des prix à la consommation (IHPC) — Base 100 en 2023 à partir de 2025")

    st.dataframe(
        df_ihpc.style.format({
            "T1_2025": "{:.2f}", "T4_2025": "{:.2f}", "T1_2026": "{:.2f}",
            "Glissement_trim_%": "{:+.2f}", "Glissement_an_%": "{:+.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    # Graphique des glissements
    st.subheader("Glissements par fonction (T1 2026)")
    fig = px.bar(
        df_ihpc[df_ihpc["Fonction"] != "Indice global"],
        x="Fonction",
        y=["Glissement_trim_%", "Glissement_an_%"],
        barmode="group",
        labels={"value": "Variation (%)", "variable": "Type"}
    )
    fig.update_layout(height=480, xaxis_tickangle=-40, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.success("""
    **Synthèse T1 2026** :  
    L’IHPC s’établit à **103,36** (+0,35 % en variation trimestrielle, +0,45 % en glissement annuel).  
    Principales hausses : Communication (+4,0 %), Boissons alcoolisées/tabac (+2,1 %), Restaurants & hôtels (+1,2 %).
    """)

# ============================================================
# PAGE : BALANCE DES PAIEMENTS
# ============================================================
elif page == "🌍 I.4 Balance des paiements":
    st.markdown("## I.4 Balance des paiements")
    st.caption("Soldes en milliards FCFA (termes de règlements)")

    st.dataframe(
        df_bop.style.format("{:.2f}"),
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        df_bop.melt(id_vars="Poste", var_name="Trimestre", value_name="Solde"),
        x="Poste", y="Solde", color="Trimestre",
        barmode="group",
        color_discrete_sequence=["#a0aec0", "#63b3ed", "#2b6cb0"]
    )
    fig.update_layout(height=450, xaxis_tickangle=-25, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **T2 2026** : Solde global de **+224,74 milliards FCFA**, en forte baisse par rapport au T1 2026 (+839,72 Mds).  
    La détérioration vient principalement du revenu primaire (−347,11 Mds).  
    Le compte des biens reste très excédentaire (+1 356 Mds).
    """)

# ============================================================
# PAGE : MOBILISATION DES RESSOURCES
# ============================================================
elif page == "💵 II. Mobilisation des ressources":
    st.markdown("## II. Mobilisation des ressources intérieures")
    st.caption("Recettes ordinaires totales mobilisées — milliards FCFA")

    st.dataframe(
        df_recettes.style.format({
            "Prév_LFR_2026": "{:.2f}",
            "T3_2025": "{:.2f}", "T1_2026": "{:.2f}", "T2_2026": "{:.2f}", "T3_2026": "{:.2f}",
            "Cumul_fin_sept_2026": "{:.2f}", "Taux_exécution_%": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Évolution trimestrielle des recettes")
        fig = px.bar(
            df_recettes[df_recettes["Catégorie"] != "Total Général"].melt(
                id_vars="Catégorie",
                value_vars=["T3_2025", "T1_2026", "T2_2026", "T3_2026"],
                var_name="Trimestre", value_name="Montant"
            ),
            x="Trimestre", y="Montant", color="Catégorie",
            barmode="stack"
        )
        fig.update_layout(height=380, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Taux de recouvrement par régie")
        fig2 = px.line(
            df_taux_regie.melt(id_vars="Régie", var_name="Période", value_name="Taux"),
            x="Période", y="Taux", color="Régie", markers=True
        )
        fig2.update_layout(height=380, template="plotly_white", yaxis_title="Taux (%)")
        st.plotly_chart(fig2, use_container_width=True)

    st.success("""
    **Fin septembre 2026** :  
    - Total recettes ordinaires cumulées : **3 001,72 milliards FCFA** (taux de réalisation **84,6 %**).  
    - DGI : 88,4 % · DGTCP : 90,9 % · DGD : 78,3 %.  
    - Recettes minières T3 2026 : **228,70 milliards FCFA**.
    """)

# ============================================================
# PAGE : TOFE
# ============================================================
elif page == "📑 III. TOFE & Finances publiques":
    st.markdown("## III. Tableau des opérations financières de l’État (TOFE)")
    st.caption("Soldes caractéristiques — milliards FCFA")

    st.dataframe(
        df_tofe.style.format("{:.2f}"),
        use_container_width=True,
        hide_index=True
    )

    fig = px.line(
        df_tofe.melt(id_vars="Indicateur", var_name="Trimestre", value_name="Montant"),
        x="Trimestre", y="Montant", color="Indicateur", markers=True
    )
    fig.update_layout(height=480, template="plotly_white", legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig, use_container_width=True)

    st.warning("""
    **T3 2026** :  
    - Solde global (base engagement) : **−161,35 milliards FCFA** (détérioration de 215 Mds vs T2).  
    - Solde global base caisse : **+64,54 milliards FCFA** (amélioration).  
    - Financement net : **−66,09 milliards FCFA**.
    """)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Prototype Streamlit · Données du Bulletin statistique trimestriel T3 2026 · DGESS / MEF Burkina Faso · À des fins de démonstration")
