"""
EEA Industrial Emissions Search App
Searchable interface over the EEA E-PRTR database (~100k facilities, 550k+ emission records)
"""

import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────
DB_PATH = Path(__file__).parent / "data" / "processed" / "converted_database.db"

COUNTRY_NAMES = {
    "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "CH": "Switzerland",
    "CY": "Cyprus", "CZ": "Czech Republic", "DE": "Germany", "DK": "Denmark",
    "EE": "Estonia", "ES": "Spain", "FI": "Finland", "FR": "France",
    "GB": "United Kingdom", "GR": "Greece", "HR": "Croatia", "HU": "Hungary",
    "IE": "Ireland", "IS": "Iceland", "IT": "Italy", "LI": "Liechtenstein",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "MT": "Malta",
    "NL": "Netherlands", "NO": "Norway", "PL": "Poland", "PT": "Portugal",
    "RO": "Romania", "RS": "Serbia", "SE": "Sweden", "SI": "Slovenia", "SK": "Slovakia",
}

st.set_page_config(
    page_title="EEA Industrial Emissions Search",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DB helpers ─────────────────────────────────────────────────────────────────

@st.cache_resource
def get_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def query(sql: str, params=()) -> pd.DataFrame:
    conn = get_conn()
    return pd.read_sql_query(sql, conn, params=params)


@st.cache_data(ttl=3600)
def load_filter_options():
    """Load distinct values for sidebar filters (cached for 1 h)."""
    countries_raw = query(
        'SELECT DISTINCT countryCode FROM "2_ProductionFacility" WHERE countryCode IS NOT NULL ORDER BY countryCode'
    )["countryCode"].tolist()
    countries = {f"{COUNTRY_NAMES.get(c, c)} ({c})": c for c in countries_raw}

    pollutants = query(
        'SELECT DISTINCT pollutantName FROM "2f_PollutantRelease" '
        "WHERE pollutantName IS NOT NULL AND pollutantName != 'CONFIDENTIAL' ORDER BY pollutantName"
    )["pollutantName"].tolist()

    years = query(
        'SELECT DISTINCT reportingYear FROM "2f_PollutantRelease" ORDER BY reportingYear'
    )["reportingYear"].tolist()

    # Shorten long activity names for display
    activities_raw = query(
        'SELECT DISTINCT mainActivityCode, mainActivityName FROM "2_ProductionFacility" '
        "WHERE mainActivityCode IS NOT NULL ORDER BY mainActivityCode"
    )
    activities = {}
    for _, row in activities_raw.iterrows():
        code = row["mainActivityCode"]
        name = row["mainActivityName"] or ""
        label = f"{code} – {name[:60]}{'…' if len(name) > 60 else ''}" if name else code
        activities[label] = code

    return countries, pollutants, years, activities


# ── Sidebar ────────────────────────────────────────────────────────────────────

st.sidebar.title("EEA Emissions Search")
st.sidebar.caption("E-PRTR database · 100k facilities · 550k+ records")
st.sidebar.markdown("---")

countries, pollutants, years, activities = load_filter_options()

sel_countries = st.sidebar.multiselect(
    "Country", options=list(countries.keys()),
    placeholder="All countries"
)
country_codes = [countries[c] for c in sel_countries] if sel_countries else []

sel_year_range = st.sidebar.select_slider(
    "Reporting years", options=years,
    value=(years[0], years[-1])
)

sel_medium = st.sidebar.multiselect(
    "Emission medium", options=["AIR", "WATER", "LAND"],
    placeholder="All mediums"
)

st.sidebar.markdown("---")
st.sidebar.caption(f"DB: `{DB_PATH.name}` · {DB_PATH.stat().st_size / 1e6:.0f} MB")

# ── Tabs ───────────────────────────────────────────────────────────────────────

tab_fac, tab_em, tab_top, tab_leads = st.tabs([
    "Facilities",
    "Emissions",
    "Top Emitters",
    "Lead Finder",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – FACILITY SEARCH
# ══════════════════════════════════════════════════════════════════════════════
with tab_fac:
    st.header("Facility Search")

    c1, c2 = st.columns([3, 1])
    with c1:
        name_q = st.text_input("Search facility / company name", placeholder="e.g. SSAB, Vattenfall, paper mill…")
    with c2:
        fac_limit = st.selectbox("Max results", [100, 500, 1000, 5000], index=0)

    # Optional: filter by activity
    sel_activity_label = st.selectbox(
        "Filter by sector / activity (optional)",
        options=["— All sectors —"] + list(activities.keys()),
    )
    sel_activity_code = activities.get(sel_activity_label) if sel_activity_label != "— All sectors —" else None

    # Build query
    where, params = ["1=1"], []

    if name_q.strip():
        where.append('(LOWER(nameOfFeature) LIKE ? OR LOWER(parentCompanyName) LIKE ? OR LOWER(city) LIKE ?)')
        like = f"%{name_q.strip().lower()}%"
        params += [like, like, like]

    if country_codes:
        placeholders = ",".join("?" * len(country_codes))
        where.append(f'countryCode IN ({placeholders})')
        params += country_codes

    if sel_activity_code:
        where.append('mainActivityCode = ?')
        params.append(sel_activity_code)

    sql_fac = f"""
        SELECT
            nameOfFeature        AS "Facility",
            parentCompanyName    AS "Parent company",
            city                 AS "City",
            countryCode          AS "CC",
            mainActivityCode     AS "Activity code",
            mainActivityName     AS "Sector",
            dateOfStartOfOperation AS "Start",
            pointGeometryLat     AS "Lat",
            pointGeometryLon     AS "Lon",
            Facility_INSPIRE_ID  AS "_inspire_id"
        FROM "2_ProductionFacility"
        WHERE {' AND '.join(where)}
        ORDER BY nameOfFeature
        LIMIT {fac_limit}
    """

    df_fac = query(sql_fac, params)

    st.caption(f"Showing {len(df_fac):,} facilities (capped at {fac_limit})")

    if df_fac.empty:
        st.info("No facilities matched your filters.")
    else:
        # Show table (hide internal id column)
        display_cols = [c for c in df_fac.columns if not c.startswith("_")]
        st.dataframe(
            df_fac[display_cols],
            use_container_width=True,
            height=420,
            column_config={
                "Sector": st.column_config.TextColumn(width="large"),
            },
        )

        # Download button
        csv = df_fac[display_cols].to_csv(index=False).encode()
        st.download_button("Download results as CSV", csv, "facilities.csv", "text/csv")

        # Map (if lat/lon available)
        df_map = df_fac.dropna(subset=["Lat", "Lon"])
        if not df_map.empty:
            with st.expander(f"Show map ({len(df_map):,} locations)"):
                fig_map = px.scatter_mapbox(
                    df_map,
                    lat="Lat", lon="Lon",
                    hover_name="Facility",
                    hover_data={"City": True, "CC": True, "Sector": True, "Lat": False, "Lon": False},
                    zoom=3, height=450,
                    color_discrete_sequence=["#e63946"],
                )
                fig_map.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
                st.plotly_chart(fig_map, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – EMISSION EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab_em:
    st.header("Emission Explorer")

    ec1, ec2 = st.columns([3, 1])
    with ec1:
        fac_name_em = st.text_input("Facility or company name", key="em_name",
                                    placeholder="Leave blank to search by pollutant only")
    with ec2:
        em_limit = st.selectbox("Max results", [200, 500, 1000, 5000], index=0, key="em_limit")

    sel_pollutants = st.multiselect("Pollutant(s)", options=pollutants,
                                    placeholder="Select one or more…")

    where_em, params_em = ["1=1"], []

    # Year range (from sidebar slider)
    where_em.append("pr.reportingYear BETWEEN ? AND ?")
    params_em += [sel_year_range[0], sel_year_range[1]]

    if sel_medium:
        placeholders = ",".join("?" * len(sel_medium))
        where_em.append(f"pr.medium IN ({placeholders})")
        params_em += sel_medium

    if sel_pollutants:
        placeholders = ",".join("?" * len(sel_pollutants))
        where_em.append(f"pr.pollutantName IN ({placeholders})")
        params_em += sel_pollutants

    if fac_name_em.strip():
        where_em.append('(LOWER(f.nameOfFeature) LIKE ? OR LOWER(f.parentCompanyName) LIKE ?)')
        like = f"%{fac_name_em.strip().lower()}%"
        params_em += [like, like]

    if country_codes:
        placeholders = ",".join("?" * len(country_codes))
        where_em.append(f"f.countryCode IN ({placeholders})")
        params_em += country_codes

    sql_em = f"""
        SELECT
            f.nameOfFeature          AS "Facility",
            f.parentCompanyName      AS "Parent company",
            f.city                   AS "City",
            f.countryCode            AS "CC",
            pr.reportingYear         AS "Year",
            pr.pollutantName         AS "Pollutant",
            pr.medium                AS "Medium",
            ROUND(pr.totalPollutantQuantityKg, 2)  AS "Total (kg)",
            ROUND(pr.totalPollutantQuantityKg / 1000, 4) AS "Total (t)",
            pr.methodName            AS "Method"
        FROM "2f_PollutantRelease" pr
        JOIN "2_ProductionFacility" f ON pr.Facility_INSPIRE_ID = f.Facility_INSPIRE_ID
        WHERE {' AND '.join(where_em)}
        ORDER BY pr.totalPollutantQuantityKg DESC
        LIMIT {em_limit}
    """

    df_em = query(sql_em, params_em)

    st.caption(f"Showing {len(df_em):,} emission records (capped at {em_limit})")

    if df_em.empty:
        st.info("No records matched. Try broadening your filters.")
    else:
        st.dataframe(
            df_em,
            use_container_width=True,
            height=420,
            column_config={
                "Total (kg)": st.column_config.NumberColumn(format="%.0f"),
                "Total (t)": st.column_config.NumberColumn(format="%.2f"),
            },
        )

        csv_em = df_em.to_csv(index=False).encode()
        st.download_button("Download results as CSV", csv_em, "emissions.csv", "text/csv",
                           key="dl_em")

        # Quick chart: total by year (only if not too scattered)
        if sel_pollutants and len(sel_pollutants) <= 5:
            with st.expander("Trend by year"):
                df_trend = df_em.groupby(["Year", "Pollutant"])["Total (t)"].sum().reset_index()
                fig_trend = px.line(
                    df_trend, x="Year", y="Total (t)", color="Pollutant",
                    title="Total emissions (tonnes) per year",
                    markers=True,
                )
                st.plotly_chart(fig_trend, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – TOP EMITTERS
# ══════════════════════════════════════════════════════════════════════════════
with tab_top:
    st.header("Top Emitters")

    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        top_pollutant = st.selectbox("Pollutant", options=pollutants,
                                     index=pollutants.index("Carbon dioxide") if "Carbon dioxide" in pollutants else 0,
                                     key="top_poll")
    with tc2:
        top_medium = st.selectbox("Medium", ["AIR", "WATER", "LAND"], key="top_med")
    with tc3:
        top_n = st.selectbox("Top N facilities", [10, 20, 50], index=0, key="top_n")

    where_top, params_top = [], []
    where_top.append("pr.pollutantName = ?")
    params_top.append(top_pollutant)
    where_top.append("pr.medium = ?")
    params_top.append(top_medium)
    where_top.append("pr.reportingYear BETWEEN ? AND ?")
    params_top += [sel_year_range[0], sel_year_range[1]]
    if country_codes:
        placeholders = ",".join("?" * len(country_codes))
        where_top.append(f"f.countryCode IN ({placeholders})")
        params_top += country_codes

    sql_top = f"""
        SELECT
            f.nameOfFeature     AS "Facility",
            f.city              AS "City",
            f.countryCode       AS "CC",
            f.mainActivityName  AS "Sector",
            ROUND(SUM(pr.totalPollutantQuantityKg) / 1000, 1) AS "Total (t)"
        FROM "2f_PollutantRelease" pr
        JOIN "2_ProductionFacility" f ON pr.Facility_INSPIRE_ID = f.Facility_INSPIRE_ID
        WHERE {' AND '.join(where_top)}
        GROUP BY pr.Facility_INSPIRE_ID
        ORDER BY SUM(pr.totalPollutantQuantityKg) DESC
        LIMIT {top_n}
    """

    df_top = query(sql_top, params_top)

    if df_top.empty:
        st.info("No data for selected filters.")
    else:
        fig_bar = px.bar(
            df_top.iloc[::-1],   # reverse so largest is at top
            x="Total (t)", y="Facility",
            orientation="h",
            color="CC",
            title=f"Top {len(df_top)} emitters – {top_pollutant} into {top_medium} "
                  f"({sel_year_range[0]}–{sel_year_range[1]})",
            labels={"Total (t)": "Total emissions (tonnes)", "CC": "Country"},
            height=max(350, len(df_top) * 28),
            text="Total (t)",
        )
        fig_bar.update_traces(texttemplate="%{text:,.0f} t", textposition="outside")
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_bar, use_container_width=True)

        st.dataframe(df_top, use_container_width=True, height=320,
                     column_config={"Total (t)": st.column_config.NumberColumn(format="%.1f")})
        csv_top = df_top.to_csv(index=False).encode()
        st.download_button("Download as CSV", csv_top, "top_emitters.csv", "text/csv", key="dl_top")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 – LEAD FINDER
# ══════════════════════════════════════════════════════════════════════════════
with tab_leads:
    st.header("Lead Finder")
    st.caption("Identify target facilities based on sector, country, and emission profile.")

    lc1, lc2 = st.columns(2)
    with lc1:
        lead_sector_label = st.selectbox(
            "Sector / activity",
            ["— All sectors —"] + list(activities.keys()),
            key="lead_sector",
        )
        lead_activity_code = activities.get(lead_sector_label) if lead_sector_label != "— All sectors —" else None

        lead_countries = st.multiselect(
            "Country", options=list(countries.keys()),
            placeholder="All countries", key="lead_countries"
        )
        lead_country_codes = [countries[c] for c in lead_countries] if lead_countries else []

    with lc2:
        min_emissions_t = st.number_input(
            "Min total emissions over period (tonnes)", min_value=0.0, value=0.0, step=100.0,
            help="Only show facilities that emitted at least this much in the selected years",
        )
        lead_pollutants = st.multiselect(
            "Pollutant(s) to score on", options=pollutants,
            default=["Carbon dioxide"] if "Carbon dioxide" in pollutants else [],
            key="lead_polls"
        )

    lead_limit = st.selectbox("Max leads", [50, 100, 250, 500], index=1, key="lead_limit")

    where_ld, params_ld = [], []
    where_ld.append("pr.reportingYear BETWEEN ? AND ?")
    params_ld += [sel_year_range[0], sel_year_range[1]]

    if lead_pollutants:
        placeholders = ",".join("?" * len(lead_pollutants))
        where_ld.append(f"pr.pollutantName IN ({placeholders})")
        params_ld += lead_pollutants

    if lead_country_codes:
        placeholders = ",".join("?" * len(lead_country_codes))
        where_ld.append(f"f.countryCode IN ({placeholders})")
        params_ld += lead_country_codes

    if lead_activity_code:
        where_ld.append("f.mainActivityCode = ?")
        params_ld.append(lead_activity_code)

    having_clause = ""
    if min_emissions_t > 0:
        having_clause = f"HAVING SUM(pr.totalPollutantQuantityKg) / 1000 >= {min_emissions_t}"

    sql_leads = f"""
        SELECT
            f.nameOfFeature         AS "Facility",
            f.parentCompanyName     AS "Parent company",
            f.city                  AS "City",
            f.countryCode           AS "CC",
            f.mainActivityName      AS "Sector",
            f.dateOfStartOfOperation AS "Start",
            COUNT(DISTINCT pr.reportingYear) AS "Years reported",
            COUNT(DISTINCT pr.pollutantName) AS "# Pollutants",
            ROUND(SUM(pr.totalPollutantQuantityKg) / 1000, 1) AS "Total emissions (t)",
            f.pointGeometryLat      AS "Lat",
            f.pointGeometryLon      AS "Lon"
        FROM "2_ProductionFacility" f
        JOIN "2f_PollutantRelease" pr ON pr.Facility_INSPIRE_ID = f.Facility_INSPIRE_ID
        WHERE {' AND '.join(where_ld) if where_ld else '1=1'}
        GROUP BY f.Facility_INSPIRE_ID
        {having_clause}
        ORDER BY SUM(pr.totalPollutantQuantityKg) DESC
        LIMIT {lead_limit}
    """

    run_leads = st.button("Find leads", type="primary")

    if run_leads:
        with st.spinner("Querying…"):
            df_leads = query(sql_leads, params_ld)

        st.caption(f"{len(df_leads):,} leads found")

        if df_leads.empty:
            st.info("No leads matched. Try relaxing your filters.")
        else:
            display_leads = [c for c in df_leads.columns if c not in ("Lat", "Lon")]
            st.dataframe(
                df_leads[display_leads],
                use_container_width=True,
                height=420,
                column_config={
                    "Total emissions (t)": st.column_config.NumberColumn(format="%.1f"),
                    "Sector": st.column_config.TextColumn(width="large"),
                },
            )

            csv_leads = df_leads[display_leads].to_csv(index=False).encode()
            st.download_button("Download leads as CSV", csv_leads, "leads.csv", "text/csv",
                               key="dl_leads")

            # Map
            df_lmap = df_leads.dropna(subset=["Lat", "Lon"])
            if not df_lmap.empty:
                with st.expander(f"Map ({len(df_lmap):,} locations)"):
                    fig_lmap = px.scatter_mapbox(
                        df_lmap,
                        lat="Lat", lon="Lon",
                        hover_name="Facility",
                        size="Total emissions (t)",
                        size_max=25,
                        hover_data={"City": True, "CC": True, "Total emissions (t)": True,
                                    "Lat": False, "Lon": False},
                        color="CC",
                        zoom=3, height=480,
                    )
                    fig_lmap.update_layout(mapbox_style="open-street-map",
                                           margin={"r": 0, "t": 0, "l": 0, "b": 0})
                    st.plotly_chart(fig_lmap, use_container_width=True)
    else:
        st.info("Set your filters above and press **Find leads**.")
