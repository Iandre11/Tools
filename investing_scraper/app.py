import pandas as pd
import streamlit as st

from symbol_catalog import (
    ADR_COUNTRY_MAP,
    ADR_ORIGINAL_MAP,
    FLAGS_MAP,
    HOLIDAYS_DATA_FILE,
    PRICE_HISTORY_FILE,
)

st.set_page_config(
    page_title="Investing.com Holiday Calendar",
    page_icon="📅",
    layout="wide",
)

st.title("🌎 Global Stock Market Holiday Calendar")
st.markdown("Explore global stock exchange holidays for 2024 and 2025.")


@st.cache_data
def load_holidays_data():
    try:
        df = pd.read_csv(HOLIDAYS_DATA_FILE)
        df["Date_Parsed"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Year"] = df["Date_Parsed"].dt.year
        df["Month"] = df["Date_Parsed"].dt.month

        df["Exchange"] = df.apply(
            lambda row: f"{FLAGS_MAP.get(row['Country'], row['Country']).split(' ')[0]} {row['Exchange']}",
            axis=1,
        )
        df["Country"] = df["Country"].apply(lambda country: FLAGS_MAP.get(country, country))
        return df
    except Exception as exc:
        st.error(f"Error loading data: {exc}")
        return pd.DataFrame()


@st.cache_data
def load_price_history():
    if not PRICE_HISTORY_FILE.exists():
        return pd.DataFrame()

    try:
        price_df = pd.read_csv(PRICE_HISTORY_FILE)
        if price_df.empty:
            return pd.DataFrame()

        price_df["Date"] = pd.to_datetime(price_df["Date"], errors="coerce").dt.normalize()
        price_df = price_df.dropna(subset=["Date", "Ticker"]).sort_values(["Ticker", "Date"])
        return price_df
    except Exception as exc:
        st.error(f"Error loading local price history: {exc}")
        return pd.DataFrame()


def get_cached_history(price_df, ticker, start_date, end_date):
    if not ticker or price_df.empty:
        return None

    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)
    ticker_history = price_df[
        (price_df["Ticker"] == ticker)
        & (price_df["Date"] >= start_ts)
        & (price_df["Date"] <= end_ts)
    ].copy()

    if ticker_history.empty:
        return None

    ticker_history.set_index("Date", inplace=True)
    return ticker_history.sort_index()


def fmt_price(price, currency="$", base_url=""):
    if pd.isnull(price):
        return "N/A"
    return f"[{currency}{price:.2f}]({base_url})" if base_url else f"{currency}{price:.2f}"


def fmt_price_export(price):
    return round(price, 2) if pd.notnull(price) else None


def fmt_pct(value):
    return f"{value:+.2f}%" if pd.notnull(value) else "N/A"


holidays_df = load_holidays_data()
price_history_df = load_price_history()
available_price_tickers = set(price_history_df["Ticker"]) if not price_history_df.empty else set()
available_adrs = sorted([adr for adr in ADR_COUNTRY_MAP if adr in available_price_tickers])
missing_adrs = sorted([adr for adr in ADR_COUNTRY_MAP if adr not in available_price_tickers])

if holidays_df.empty:
    st.warning("No data found. Please ensure `holidays_data.csv` exists and has data.")
else:
    tab1, tab2 = st.tabs(["🌎 Global Calendar", "📈 ADR Holiday Analysis"])

    with tab1:
        st.sidebar.header("Filter Options")

        countries = sorted(holidays_df["Country"].dropna().unique().tolist())
        selected_countries = st.sidebar.multiselect("Select Country", options=countries)

        years = sorted(holidays_df["Year"].dropna().unique().tolist())
        selected_years = st.sidebar.multiselect("Select Year", options=years, default=years)

        if selected_countries:
            exchanges = sorted(
                holidays_df[holidays_df["Country"].isin(selected_countries)]["Exchange"].dropna().unique().tolist()
            )
        else:
            exchanges = sorted(holidays_df["Exchange"].dropna().unique().tolist())
        selected_exchanges = st.sidebar.multiselect("Select Exchange", options=exchanges)

        filtered_df = holidays_df.copy()

        if selected_countries:
            filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]

        if selected_years:
            filtered_df = filtered_df[filtered_df["Year"].isin(selected_years)]

        if selected_exchanges:
            filtered_df = filtered_df[filtered_df["Exchange"].isin(selected_exchanges)]

        filtered_df = filtered_df.sort_values(by="Date_Parsed")
        display_df = filtered_df[["Date", "Country", "Exchange", "Holiday"]].reset_index(drop=True)

        st.subheader(f"Showing {len(display_df)} Holidays")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    with tab2:
        st.header("Análisis de Festivos ADR (EE.UU vs Bolsa Local)")
        st.markdown(
            "Compara el comportamiento en precio de una empresa tanto en su ADR (EE. UU.) "
            "como en su Bolsa Local de origen alrededor de sus propios días festivos."
        )

        if price_history_df.empty:
            st.warning(
                "No existe `price_history.csv` o está vacío. Ejecuta "
                "`python3 investing_scraper/download_price_history.py` para descargar "
                "los precios de Yahoo Finance y vuelve a cargar la app."
            )
        else:
            price_min_date = price_history_df["Date"].min().date()
            price_max_date = price_history_df["Date"].max().date()
            st.caption(
                f"Fuente de precios: `{PRICE_HISTORY_FILE.name}` | "
                f"{price_history_df['Ticker'].nunique()} tickers | "
                f"{price_min_date} -> {price_max_date}"
            )
            st.caption(f"ADR con historico disponible: {len(available_adrs)} de {len(ADR_COUNTRY_MAP)}")
            if missing_adrs:
                with st.expander("ADR sin datos descargados"):
                    st.write(", ".join(missing_adrs))

        with st.expander("ℹ️ ¿Qué significan estos datos? (Guía para principiantes)"):
            st.markdown(
                """
            ### Entendiendo la Tabla
            * **ADR (EE. UU.):** Es el certificado que cotiza en dólares en Wall Street. Como sigue el horario de EE. UU., si el país de origen tiene un festivo, el ADR **sigue cotizando** normalmente (a menos que EE. UU. también tenga festivo).
            * **Ticker Local:** Es la acción original que cotiza en la propia moneda y bolsa del país (ej. Hong Kong, Brasil). El día del festivo local, el "**Ticker Local**" no cotiza porque su bolsa está cerrada.

            ### El Efecto de los Festivos (T0, T-N, T+N)
            * **T0 (Día del Festivo):** El día oficial del festivo en el país de la empresa. El Ticker Local estará "Cerrado", pero podrás ver cómo cotiza su versión ADR en EE. UU. ese día.
            * **T-N (Días Previos):** Los `N` días de bolsa abiertos *antes* del festivo.
            * **T+N (Días Posteriores):** Los `N` días de bolsa abiertos *después* del festivo.
            * **Retorno (T-N a T+N):** Representa tu rentabilidad potencial porcentual (%) si hubieras comprado acciones en el cierre de T-N y las hubieras vendido al final del día T+N.
            * **Fuente de precios:** Esta pestaña usa el CSV local `price_history.csv`, generado previamente desde Yahoo Finance.
            """
            )

        col_filter, col1, col2, col3 = st.columns(4)
        with col_filter:
            all_countries = sorted(set(ADR_COUNTRY_MAP.values()))
            selected_filter_countries = st.multiselect("Filtrar Tickers por País", options=all_countries, default=[])

        with col1:
            if selected_filter_countries:
                filtered_adrs = sorted(
                    [adr for adr, country in ADR_COUNTRY_MAP.items() if country in selected_filter_countries and adr in available_price_tickers]
                )
            else:
                filtered_adrs = available_adrs

            if filtered_adrs:
                selected_adr = st.selectbox("Selecciona un Ticker de ADR", filtered_adrs)
            else:
                st.warning("No hay ADR disponibles con datos descargados para ese filtro.")
                selected_adr = None
        with col2:
            days_to_analyze = st.slider("Días a analizar (T-N y T+N)", min_value=1, max_value=5, value=1)
        with col3:
            analyze_year = st.selectbox("Año a analizar", [2024, 2025])

        country_of_origin = ADR_COUNTRY_MAP[selected_adr] if selected_adr else None
        original_ticker = ADR_ORIGINAL_MAP.get(selected_adr) if selected_adr else None

        st.markdown("---")

        if st.button("Analizar Datos", disabled=price_history_df.empty or selected_adr is None):
            with st.spinner(f"Leyendo precios locales de {selected_adr} para {analyze_year}..."):
                try:
                    local_ticker_display = (
                        f"[{original_ticker}](https://finance.yahoo.com/quote/{original_ticker}/history/)"
                        if original_ticker
                        else "Desconocido"
                    )
                    st.info(
                        f"**ADR:** [{selected_adr}](https://finance.yahoo.com/quote/{selected_adr}/history/) | "
                        f"**Ticker Local:** {local_ticker_display} | "
                        f"**Mercado Local:** {FLAGS_MAP.get(country_of_origin, country_of_origin)} | "
                        f"**Fuente de precios:** `{PRICE_HISTORY_FILE.name}`"
                    )

                    country_holidays_df = holidays_df[
                        (holidays_df["Country"] == FLAGS_MAP.get(country_of_origin, country_of_origin))
                        & (holidays_df["Year"] == analyze_year)
                    ]

                    if country_holidays_df.empty:
                        st.warning(f"No se encontraron festivos en {analyze_year} para {country_of_origin}.")
                    else:
                        us_holidays_df = holidays_df[
                            (holidays_df["Country"] == FLAGS_MAP.get("United States"))
                            & (holidays_df["Year"] == analyze_year)
                        ]
                        us_holiday_dates = us_holidays_df["Date_Parsed"].dt.date.tolist()

                        start_date = f"{analyze_year - 1}-12-01"
                        end_date = f"{analyze_year + 1}-01-31"

                        history_adr = get_cached_history(price_history_df, selected_adr, start_date, end_date)
                        history_local = (
                            get_cached_history(price_history_df, original_ticker, start_date, end_date)
                            if original_ticker
                            else None
                        )

                        if history_adr is None or history_adr.empty:
                            st.error(
                                f"No hay precios descargados en `{PRICE_HISTORY_FILE.name}` para el ADR `{selected_adr}`."
                            )
                        else:
                            if original_ticker and history_local is None:
                                st.warning(
                                    f"Aviso: No hay precios descargados para el ticker local `{original_ticker}`."
                                )

                            results_adr_md = []
                            results_local_md = []
                            results_adr_export = []
                            results_local_export = []

                            unique_holiday_dates = sorted(country_holidays_df["Date_Parsed"].dt.date.unique())

                            def compute_row_for_dataset(
                                hist_df,
                                is_local_market=False,
                                h_date=None,
                                holiday_date_obj=None,
                                holiday_names=None,
                                is_us_holiday=False,
                            ):
                                row_md = {
                                    "Festivo Local": f"[{holiday_names}]({inv_calendar_url})",
                                    "Fecha": holiday_date_obj.strftime("%Y-%m-%d"),
                                    "Es Festivo": ("Sí" if is_local_market else ("Sí" if is_us_holiday else "No (Abierto)")),
                                }
                                row_export = {
                                    "Festivo Local": holiday_names,
                                    "Fecha Festivo": holiday_date_obj.strftime("%Y-%m-%d"),
                                }

                                currency = "" if is_local_market else "$"
                                base_url = base_loc_url if is_local_market else base_adr_url
                                if hist_df is None:
                                    return row_md, row_export, None

                                t_minus_dates = hist_df.index[hist_df.index < h_date]
                                initial_price = None

                                for offset in range(days_to_analyze, 0, -1):
                                    t_minus_date = t_minus_dates[-offset] if len(t_minus_dates) >= offset else None
                                    t_minus_close = hist_df.loc[t_minus_date]["Close"] if t_minus_date is not None else None
                                    row_md[f"T-{offset} Cierre"] = fmt_price(t_minus_close, currency, base_url)
                                    row_export[f"T-{offset} Cierre"] = fmt_price_export(t_minus_close)

                                    if offset == days_to_analyze:
                                        initial_price = t_minus_close

                                t0_price = hist_df.loc[h_date]["Close"] if h_date in hist_df.index else None
                                row_md["T0 Cierre"] = fmt_price(t0_price, currency, base_url) if pd.notnull(t0_price) else "Cerrado"
                                row_export["T0 Cierre"] = fmt_price_export(t0_price)

                                t_plus_dates = hist_df.index[hist_df.index > h_date]
                                final_price = None

                                for offset in range(1, days_to_analyze + 1):
                                    t_plus_date = t_plus_dates[offset - 1] if len(t_plus_dates) >= offset else None
                                    t_plus_close = hist_df.loc[t_plus_date]["Close"] if t_plus_date is not None else None
                                    row_md[f"T+{offset} Cierre"] = fmt_price(t_plus_close, currency, base_url)
                                    row_export[f"T+{offset} Cierre"] = fmt_price_export(t_plus_close)

                                    if offset == days_to_analyze:
                                        final_price = t_plus_close

                                ret_close = (
                                    (final_price - initial_price) / initial_price * 100
                                    if pd.notnull(final_price) and pd.notnull(initial_price)
                                    else None
                                )

                                row_md[f"Retorno (T-{days_to_analyze} a T+{days_to_analyze})"] = fmt_pct(ret_close)
                                row_export["Retorno (%)"] = round(ret_close, 2) if ret_close is not None else None
                                return row_md, row_export, ret_close

                            for holiday_date_obj in unique_holiday_dates:
                                h_date = pd.to_datetime(holiday_date_obj)
                                holiday_names = " / ".join(
                                    country_holidays_df[
                                        country_holidays_df["Date_Parsed"].dt.date == holiday_date_obj
                                    ]["Holiday"].unique()
                                )
                                is_us_holiday = holiday_date_obj in us_holiday_dates

                                base_adr_url = f"https://finance.yahoo.com/quote/{selected_adr}/history/"
                                base_loc_url = (
                                    f"https://finance.yahoo.com/quote/{original_ticker}/history/" if original_ticker else ""
                                )
                                inv_calendar_url = "https://es.investing.com/holiday-calendar/"

                                md_adr, export_adr, _ = compute_row_for_dataset(
                                    history_adr,
                                    False,
                                    h_date,
                                    holiday_date_obj,
                                    holiday_names,
                                    is_us_holiday,
                                )
                                results_adr_md.append(md_adr)
                                export_adr["Holiday"] = holiday_names
                                results_adr_export.append(export_adr)

                                if history_local is not None:
                                    md_loc, export_loc, _ = compute_row_for_dataset(
                                        history_local,
                                        True,
                                        h_date,
                                        holiday_date_obj,
                                        holiday_names,
                                        is_us_holiday,
                                    )
                                    results_local_md.append(md_loc)
                                    export_loc["Holiday"] = holiday_names
                                    results_local_export.append(export_loc)

                            def render_section(title, markdown_rows, export_rows, filename):
                                st.subheader(title)
                                if not markdown_rows:
                                    st.write("Sin datos disponibles.")
                                    return

                                markdown_df = pd.DataFrame(markdown_rows)
                                st.markdown(markdown_df.to_markdown(index=False))

                                export_df = pd.DataFrame(export_rows)
                                csv_data = export_df.to_csv(index=False).encode("utf-8")
                                st.download_button(
                                    label="📥 Descargar datos (CSV)",
                                    data=csv_data,
                                    file_name=filename,
                                    mime="text/csv",
                                )

                                chart_data = export_df[["Fecha Festivo", "Retorno (%)"]].copy()
                                chart_data.set_index("Fecha Festivo", inplace=True)
                                chart_data.dropna(inplace=True)

                                if not chart_data.empty:
                                    st.write(
                                        f"**Impacto del Festivo (% Cambio de T-{days_to_analyze} a T+{days_to_analyze})**"
                                    )
                                    st.bar_chart(chart_data)

                            render_section(
                                "📊 Comportamiento del ADR (Bolsa de Nueva York - USD)",
                                results_adr_md,
                                results_adr_export,
                                f"{selected_adr}_ADR_{analyze_year}.csv",
                            )

                            st.write("---")

                            if results_local_md:
                                render_section(
                                    f"📊 Comportamiento Acción Original (Bolsa Local de {country_of_origin} - Divisa Local)",
                                    results_local_md,
                                    results_local_export,
                                    f"{original_ticker}_LOCAL_{analyze_year}.csv",
                                )

                except Exception as exc:
                    st.error(f"Error procesando datos locales: {exc}")
