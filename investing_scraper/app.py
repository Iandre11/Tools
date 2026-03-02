import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(
    page_title="Investing.com Holiday Calendar",
    page_icon="📅",
    layout="wide"
)

st.title("🌎 Global Stock Market Holiday Calendar")
st.markdown("Explore global stock exchange holidays for 2024 and 2025.")

FLAGS_MAP = {
    "Argentina": "🇦🇷 Argentina", "Australia": "🇦🇺 Australia", "Austria": "🇦🇹 Austria",
    "Bahrain": "🇧🇭 Bahrain", "Bangladesh": "🇧🇩 Bangladesh", "Belgium": "🇧🇪 Belgium",
    "Bermuda": "🇧🇲 Bermuda", "Bosnia-Herzegovina": "🇧🇦 Bosnia-Herzegovina", "Botswana": "🇧🇼 Botswana",
    "Brazil": "🇧🇷 Brazil", "Bulgaria": "🇧🇬 Bulgaria", "Canada": "🇨🇦 Canada",
    "Cayman Islands": "🇰🇾 Cayman Islands", "Chile": "🇨🇱 Chile", "China": "🇨🇳 China",
    "Colombia": "🇨🇴 Colombia", "Costa Rica": "🇨🇷 Costa Rica", "Croatia": "🇭🇷 Croatia",
    "Cyprus": "🇨🇾 Cyprus", "Czech Republic": "🇨🇿 Czech Republic", "Denmark": "🇩🇰 Denmark",
    "Ecuador": "🇪🇨 Ecuador", "Egypt": "🇪🇬 Egypt", "Estonia": "🇪🇪 Estonia",
    "Finland": "🇫🇮 Finland", "France": "🇫🇷 France", "Germany": "🇩🇪 Germany",
    "Greece": "🇬🇷 Greece", "Hong Kong": "🇭🇰 Hong Kong", "Hungary": "🇭🇺 Hungary",
    "Iceland": "🇮🇸 Iceland", "India": "🇮🇳 India", "Indonesia": "🇮🇩 Indonesia",
    "Ireland": "🇮🇪 Ireland", "Israel": "🇮🇱 Israel", "Italy": "🇮🇹 Italy",
    "Jamaica": "🇯🇲 Jamaica", "Japan": "🇯🇵 Japan", "Jordan": "🇯🇴 Jordan",
    "Kazakhstan": "🇰🇿 Kazakhstan", "Kenya": "🇰🇪 Kenya", "Kuwait": "🇰🇼 Kuwait",
    "Latvia": "🇱🇻 Latvia", "Lebanon": "🇱🇧 Lebanon", "Lithuania": "🇱🇹 Lithuania",
    "Luxembourg": "🇱🇺 Luxembourg", "Malaysia": "🇲🇾 Malaysia", "Malta": "🇲🇹 Malta",
    "Mauritius": "🇲🇺 Mauritius", "Mexico": "🇲🇽 Mexico", "Mongolia": "🇲🇳 Mongolia",
    "Montenegro": "🇲🇪 Montenegro", "Morocco": "🇲🇦 Morocco", "Namibia": "🇳🇦 Namibia",
    "Netherlands": "🇳🇱 Netherlands", "New Zealand": "🇳🇿 New Zealand", "Nigeria": "🇳🇬 Nigeria",
    "Norway": "🇳🇴 Norway", "Oman": "🇴🇲 Oman", "Pakistan": "🇵🇰 Pakistan",
    "Palestinian Territory": "🇵🇸 Palestinian Territory", "Peru": "🇵🇪 Peru", "Philippines": "🇵🇭 Philippines",
    "Poland": "🇵🇱 Poland", "Portugal": "🇵🇹 Portugal", "Qatar": "🇶🇦 Qatar",
    "Romania": "🇷🇴 Romania", "Russia": "🇷🇺 Russia", "Rwanda": "🇷🇼 Rwanda",
    "Saudi Arabia": "🇸🇦 Saudi Arabia", "Serbia": "🇷🇸 Serbia", "Singapore": "🇸🇬 Singapore",
    "Slovakia": "🇸🇰 Slovakia", "Slovenia": "🇸🇮 Slovenia", "South Africa": "🇿🇦 South Africa",
    "South Korea": "🇰🇷 South Korea", "Spain": "🇪🇸 Spain", "Sri Lanka": "🇱🇰 Sri Lanka",
    "Sweden": "🇸🇪 Sweden", "Switzerland": "🇨🇭 Switzerland", "Taiwan": "🇹🇼 Taiwan",
    "Tanzania": "🇹🇿 Tanzania", "Thailand": "🇹🇭 Thailand", "Tunisia": "🇹🇳 Tunisia",
    "Türkiye": "🇹🇷 Türkiye", "Ukraine": "🇺🇦 Ukraine", "United Arab Emirates": "🇦🇪 United Arab Emirates",
    "United Kingdom": "🇬🇧 United Kingdom", "United States": "🇺🇸 United States",
    "Venezuela": "🇻🇪 Venezuela", "Vietnam": "🇻🇳 Vietnam", "Zimbabwe": "🇿🇼 Zimbabwe",
}

ADR_COUNTRY_MAP = {
    'ABB': 'Switzerland',
    'ABEV': 'Brazil', 'AC': 'Canada', 'AEM': 'Canada', 'AIQUY': 'France', 'ARM': 'United Kingdom',
    'ASX': 'Taiwan', 'AUO': 'Taiwan', 'AXAHY': 'France', 'AZN': 'United Kingdom', 'BABA': 'China',
    'BASFY': 'Germany', 'BAYRY': 'Germany', 'BBD': 'Brazil', 'BBDO': 'Brazil', 'BCE': 'Canada',
    'BEKE': 'China', 'BGNE': 'China', 'BHP': 'Australia', 'BIDU': 'China', 'BILI': 'China',
    'BMO': 'Canada', 'BMWYY': 'Germany', 'BNPQY': 'France', 'BNS': 'Canada', 'BP': 'United Kingdom',
    'BSBR': 'Brazil', 'BTI': 'United Kingdom', 'CAJ': 'Japan', 'CAN': 'China', 'CHT': 'Taiwan',
    'CIG': 'Brazil', 'CM': 'Canada', 'CNQ': 'Canada', 'DAO': 'China', 'DB': 'Germany',
    'DEO': 'United Kingdom', 'DTEGY': 'Germany', 'EBR': 'Brazil', 'EDU': 'China', 'ENB': 'Canada',
    'ERJ': 'Brazil', 'FUTU': 'China', 'GGB': 'Brazil', 'GOLD': 'Canada', 'GSK': 'United Kingdom',
    'HDB': 'India', 'HMC': 'Japan', 'HSBC': 'United Kingdom', 'HTHT': 'China', 'HUYA': 'China',
    'IBN': 'India', 'INFY': 'India', 'IQ': 'China', 'ITUB': 'Brazil', 'IX': 'Japan',
    'JD': 'China', 'KB': 'South Korea', 'KEP': 'South Korea', 'KMTUY': 'Japan', 'KNBWY': 'Japan',
    'KT': 'South Korea', 'LI': 'China', 'LPL': 'South Korea', 'LU': 'China', 'LYG': 'United Kingdom',
    'MBGYY': 'Germany', 'MFC': 'Canada', 'MFG': 'Japan', 'MNSO': 'China', 'MUFG': 'Japan',
    'NGG': 'United Kingdom', 'NIO': 'China', 'NSRGY': 'Switzerland', 'NTDOY': 'Japan', 'NTES': 'China',
    'NVS': 'Switzerland', 'ORAN': 'France', 'PBR': 'Brazil', 'PDD': 'China', 'PKX': 'South Korea',
    'QFIN': 'China', 'RDY': 'India', 'RELX': 'United Kingdom', 'RENOY': 'France', 'RHHBY': 'Switzerland',
    'RIO': 'Australia', 'RY': 'Canada', 'SAN': 'Spain', 'SAP': 'Germany', 'SBS': 'Brazil',
    'SFTBY': 'Japan', 'SHEL': 'United Kingdom', 'SHG': 'South Korea', 'SHOP': 'Canada', 'SID': 'Brazil',
    'SIEGY': 'Germany', 'SKM': 'South Korea', 'SMFG': 'Japan', 'SONY': 'Japan', 'SU': 'Canada',
    'TAL': 'China', 'TCLRY': 'Australia', 'TCOM': 'China', 'TD': 'Canada', 'TECK': 'Canada',
    'TIGR': 'China', 'TIMB': 'Brazil', 'TLSYY': 'Australia', 'TM': 'Japan', 'TME': 'China',
    'TRP': 'Canada', 'TSM': 'Taiwan', 'TTNDY': 'Hong Kong', 'TU': 'Canada', 'TUYA': 'China',
    'UBS': 'Switzerland', 'UL': 'United Kingdom', 'UMC': 'Taiwan', 'VALE': 'Brazil', 'VEDL': 'India',
    'VOD': 'United Kingdom', 'VWAGY': 'Germany', 'WB': 'China', 'WIT': 'India', 'WOWOY': 'Australia',
    'WPM': 'Canada', 'XP': 'Brazil', 'XPEV': 'China', 'YMM': 'China', 'YSG': 'China',
    'ZLAB': 'China', 'ZTO': 'China'
}

ADR_ORIGINAL_MAP = {
    'BHP': 'BHP.AX', 'RIO': 'RIO.AX', 'TCLRY': 'TLC.AX', 'TLSYY': 'TLS.AX', 'WOWOY': 'WOW.AX',
    'ABEV': 'ABEV3.SA', 'ITUB': 'ITUB4.SA', 'PBR': 'PETR4.SA', 'VALE': 'VALE3.SA', 'XP': 'XP',
    'AC': 'AC.TO', 'BMO': 'BMO.TO', 'ENB': 'ENB.TO', 'SHOP': 'SHOP.TO', 'TD': 'TD.TO',
    'BABA': '9988.HK', 'BIDU': '9888.HK', 'JD': '9618.HK', 'NIO': '9866.HK', 'PDD': 'PDD', 'XPEV': '9868.HK',
    'ORAN': 'ORA.PA', 'SAN': 'SAN.PA', 'AIQUY': 'AI.PA',
    'SAP': 'SAP.DE', 'VWAGY': 'VOW3.DE', 'BMWYY': 'BMW.DE', 'DB': 'DBK.DE',
    'ARM': 'ARM.L', 'AZN': 'AZN.L', 'BP': 'BP.L', 'SHEL': 'SHEL.L', 'UL': 'ULVR.L',
    'SONY': '6758.T', 'TM': '7203.T', 'HMC': '7267.T', 'NTDOY': '7974.T',
    'TSM': '2330.TW', 'UMC': '2303.TW', 'ASX': '3711.TW', 'AUO': '2409.TW', 'CHT': '2412.TW'
}

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("investing_scraper/holidays_data.csv")
        df['Date_Parsed'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = df['Date_Parsed'].dt.year
        df['Month'] = df['Date_Parsed'].dt.month
        
        # Add flags to Exchange first (using the original Country name)
        df['Exchange'] = df.apply(lambda row: f"{FLAGS_MAP.get(row['Country'], row['Country']).split(' ')[0]} {row['Exchange']}", axis=1)
        
        # Add flags to Country
        df['Country'] = df['Country'].apply(lambda x: FLAGS_MAP.get(x, x))
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data found. Please ensure `holidays_data.csv` exists and has data.")
else:
    tab1, tab2 = st.tabs(["🌎 Global Calendar", "📈 ADR Holiday Analysis"])
    
    with tab1:
        # --- Sidebar Filters ---
        st.sidebar.header("Filter Options")
        
        countries = sorted(df['Country'].dropna().unique().tolist())
        selected_countries = st.sidebar.multiselect("Select Country", options=countries)
        
        years = sorted(df['Year'].dropna().unique().tolist())
        selected_years = st.sidebar.multiselect("Select Year", options=years, default=years)
        
        if selected_countries:
            exchanges = sorted(df[df['Country'].isin(selected_countries)]['Exchange'].dropna().unique().tolist())
        else:
            exchanges = sorted(df['Exchange'].dropna().unique().tolist())
        selected_exchanges = st.sidebar.multiselect("Select Exchange", options=exchanges)
        
        filtered_df = df.copy()
        
        if selected_countries:
            filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
        
        if selected_years:
            filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]
            
        if selected_exchanges:
            filtered_df = filtered_df[filtered_df['Exchange'].isin(selected_exchanges)]
            
        filtered_df = filtered_df.sort_values(by='Date_Parsed')
        display_df = filtered_df[['Date', 'Country', 'Exchange', 'Holiday']].reset_index(drop=True)
        
        st.subheader(f"Showing {len(display_df)} Holidays")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    with tab2:
        st.header("Análisis de Festivos ADR (EE.UU vs Bolsa Local)")
        st.markdown("Compara el comportamiento en precio de una empresa tanto en su ADR (EE. UU.) como en su Bolsa Local de origen alrededor de sus propios días festivos.")
        
        with st.expander("ℹ️ ¿Qué significan estos datos? (Guía para principiantes)"):
            st.markdown("""
            ### Entendiendo la Tabla
            * **ADR (EE. UU.):** Es el certificado que cotiza en dólares en Wall Street. Como sigue el horario de EE. UU., si el país de origen tiene un festivo, el ADR **sigue cotizando** normalmente (a menos que EE. UU. también tenga festivo).
            * **Ticker Local:** Es la acción original que cotiza en la propia moneda y bolsa del país (ej. Hong Kong, Brasil). El día del festivo local, el "**Ticker Local**" no cotiza porque su bolsa está cerrada.
            
            ### El Efecto de los Festivos (T0, T-N, T+N)
            * **T0 (Día del Festivo):** El día oficial del festivo en el país de la empresa. El Ticker Local estará "Cerrado", pero podrás ver cómo cotiza su versión ADR en EE. UU. ese día.
            * **T-N (Días Previos):** Los `N` días de bolsa abiertos *antes* del festivo.
            * **T+N (Días Posteriores):** Los `N` días de bolsa abiertos *después* del festivo.
            * **Retorno (T-N a T+N):** Representa tu rentabilidad potencial porcentual (%) si hubieras comprado acciones en el cierre de T-N (el día de más a la izquierda de la tabla) y las hubieras vendido al final del día T+N (el día de más a la derecha).
            * **Enlaces a Fuentes:** Esta tabla incluye enlaces interactivos (color azul). Haz clic en el nombre del festivo para abrir el Calendario de Investing.com, o en cualquier precio/ticker para ver su gráfico histórico en *Yahoo Finance*.
            """)
        
        col_filter, col1, col2, col3 = st.columns(4)
        with col_filter:
            all_countries = sorted(list(set(ADR_COUNTRY_MAP.values())))
            selected_filter_countries = st.multiselect("Filtrar Tickers por País", options=all_countries, default=[])
            
        with col1:
            if selected_filter_countries:
                filtered_adrs = sorted([adr for adr, c in ADR_COUNTRY_MAP.items() if c in selected_filter_countries])
            else:
                filtered_adrs = sorted(list(ADR_COUNTRY_MAP.keys()))
                
            selected_adr = st.selectbox("Selecciona un Ticker de ADR", filtered_adrs)
        with col2:
            days_to_analyze = st.slider("Días a analizar (T-N y T+N)", min_value=1, max_value=5, value=1)
        with col3:
            analyze_year = st.selectbox("Año a analizar", [2024, 2025])
            
        country_of_origin = ADR_COUNTRY_MAP[selected_adr]
        
        st.markdown("---")
        
        if st.button("Analizar Datos"):
            with st.spinner(f"Obteniendo información de la empresa y precios de {selected_adr} para {analyze_year}..."):
                try:
                    ticker_obj = yf.Ticker(selected_adr)
                    info = ticker_obj.info
                    company_name = info.get('longName', 'Desconocido')
                    
                    original_ticker = ADR_ORIGINAL_MAP.get(selected_adr, None)
                    
                    st.info(f"**ADR:** [{selected_adr}](https://finance.yahoo.com/quote/{selected_adr}/history/) | "
                            f"**Ticker Local:** [{original_ticker if original_ticker else 'Desconocido'}](https://finance.yahoo.com/quote/{original_ticker}/history/) | "
                            f"**Compañía:** {company_name} | **Mercado Local:** {FLAGS_MAP.get(country_of_origin, country_of_origin)}")
                            
                    country_holidays_df = df[(df['Country'] == FLAGS_MAP.get(country_of_origin, country_of_origin)) & (df['Year'] == analyze_year)]
                    
                    if country_holidays_df.empty:
                        st.warning(f"No se encontraron festivos en {analyze_year} para {country_of_origin}.")
                    else:
                        us_holidays_df = df[(df['Country'] == FLAGS_MAP.get("United States")) & (df['Year'] == analyze_year)]
                        us_holiday_dates = us_holidays_df['Date_Parsed'].dt.date.tolist()
                        
                        start_date = f'{analyze_year - 1}-12-01'
                        end_date = f'{analyze_year + 1}-01-31'
                        
                        history_adr = ticker_obj.history(start=start_date, end=end_date)
                        history_local = yf.Ticker(original_ticker).history(start=start_date, end=end_date) if original_ticker else None
                        
                        if history_adr.empty:
                            st.error(f"No se pudo descargar el histórico del ADR {selected_adr}.")
                        else:
                            history_adr.index = history_adr.index.tz_localize(None).normalize()
                            if history_local is not None and not history_local.empty:
                                history_local.index = history_local.index.tz_localize(None).normalize()
                            else:
                                history_local = None
                                st.warning(f"Aviso: No se pudieron obtener precios del mercado local para el ticker `{original_ticker}` en Yahoo Finance.")
                                
                            results_adr_md = []
                            results_local_md = []
                            results_adr_export = []
                            results_local_export = []
                            
                            unique_holiday_dates = sorted(country_holidays_df['Date_Parsed'].dt.date.unique())
                            
                            def fmt_price(p, curr="$", base_url=""):
                                if pd.isnull(p): return "N/A"
                                return f"[{curr}{p:.2f}]({base_url})" if base_url else f"{curr}{p:.2f}"
                            
                            def fmt_price_export(p):
                                return round(p, 2) if pd.notnull(p) else None
                                
                            def fmt_pct(p):
                                return f"{p:+.2f}%" if pd.notnull(p) else "N/A"
                            
                            def compute_row_for_dataset(hist_df, is_local_market=False, h_date=None, holiday_date_obj=None, holiday_names=None, is_us_holiday=False):
                                row_md = {
                                    "Festivo Local": f"[{holiday_names}]({inv_calendar_url})",
                                    "Fecha": holiday_date_obj.strftime('%Y-%m-%d'),
                                    "Es Festivo": ("Sí" if is_local_market else ("Sí" if is_us_holiday else "No (Abierto)"))
                                }
                                row_export = {
                                    "Festivo Local": holiday_names,
                                    "Fecha Festivo": holiday_date_obj.strftime('%Y-%m-%d'),
                                }
                                
                                curr = "" if is_local_market else "$"
                                base_url = base_loc_url if is_local_market else base_adr_url
                                if hist_df is None: return row_md, row_export
                                
                                t_minus_1_dates = hist_df.index[hist_df.index < h_date]
                                initial_price = None # To evaluate from extreme T-N
                                
                                for n in range(days_to_analyze, 0, -1):
                                    t_m_date = t_minus_1_dates[-n] if len(t_minus_1_dates) >= n else None
                                    t_m_close_val = hist_df.loc[t_m_date]['Close'] if t_m_date else None
                                    row_md[f"T-{n} Cierre"] = fmt_price(t_m_close_val, curr, base_url)
                                    row_export[f"T-{n} Cierre"] = fmt_price_export(t_m_close_val)
                                    
                                    if n == days_to_analyze: # This sets the initial price to T-N
                                        initial_price = t_m_close_val
                                
                                t0_price = hist_df.loc[h_date]['Close'] if h_date in hist_df.index else None
                                row_md["T0 Cierre"] = fmt_price(t0_price, curr, base_url) if t0_price else "Cerrado"
                                row_export["T0 Cierre"] = fmt_price_export(t0_price) if t0_price else None
                                
                                t_plus_1_dates = hist_df.index[hist_df.index > h_date]
                                final_price = None # To evaluate to the extreme T+N
                                
                                for n in range(1, days_to_analyze + 1):
                                    t_p_date = t_plus_1_dates[n-1] if len(t_plus_1_dates) >= n else None
                                    t_p_close_val = hist_df.loc[t_p_date]['Close'] if t_p_date else None
                                    row_md[f"T+{n} Cierre"] = fmt_price(t_p_close_val, curr, base_url)
                                    row_export[f"T+{n} Cierre"] = fmt_price_export(t_p_close_val)
                                    
                                    if n == days_to_analyze: # This sets the final price to T+N
                                        final_price = t_p_close_val
                                
                                # Dynamic Return Calculation `((precio final - precio inicial) / precio inicial) × 100`
                                ret_close = ((final_price - initial_price) / initial_price * 100) if (pd.notnull(final_price) and pd.notnull(initial_price)) else None
                                
                                row_md[f"Retorno (T-{days_to_analyze} a T+{days_to_analyze})"] = fmt_pct(ret_close)
                                row_export[f"Retorno (%)"] = round(ret_close, 2) if ret_close is not None else None
                                
                                # Also return the raw return number for charting
                                return row_md, row_export, ret_close
                            
                            for holiday_date_obj in unique_holiday_dates:
                                h_date = pd.to_datetime(holiday_date_obj)
                                holiday_names = " / ".join(country_holidays_df[country_holidays_df['Date_Parsed'].dt.date == holiday_date_obj]['Holiday'].unique())
                                is_us_holiday = holiday_date_obj in us_holiday_dates
                                
                                base_adr_url = f"https://finance.yahoo.com/quote/{selected_adr}/history/"
                                base_loc_url = f"https://finance.yahoo.com/quote/{original_ticker}/history/" if original_ticker else ""
                                inv_calendar_url = "https://es.investing.com/holiday-calendar/"
                                
                                md_adr, export_adr, ret_adr = compute_row_for_dataset(history_adr, False, h_date, holiday_date_obj, holiday_names, is_us_holiday)
                                results_adr_md.append(md_adr)
                                # Append holiday info to export and keep ret_adr
                                export_adr['Holiday'] = holiday_names
                                results_adr_export.append(export_adr)
                                
                                if history_local is not None:
                                    md_loc, export_loc, ret_loc = compute_row_for_dataset(history_local, True, h_date, holiday_date_obj, holiday_names, is_us_holiday)
                                    results_local_md.append(md_loc)
                                    export_loc['Holiday'] = holiday_names
                                    results_local_export.append(export_loc)
                            
                            st.info("💡 **Nota interactiva:** Todos los precios mostrados y el nombre del festivo son enlaces clickables que te llevarán de vuelta a Yahoo Finance (para ver el gráfico) o al Calendario de Investing.com.")
                            
                            # Renderer helper
                            def render_section(title, md_dict, export_dict, filename):
                                st.subheader(title)
                                if not md_dict:
                                    st.write("Sin datos disponibles.")
                                    return
                                
                                # 1. Table
                                df_res = pd.DataFrame(md_dict)
                                st.markdown(df_res.to_markdown(index=False))
                                
                                # 2. Download Button
                                df_exp = pd.DataFrame(export_dict)
                                csv_data = df_exp.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label=f"📥 Descargar datos (CSV)",
                                    data=csv_data,
                                    file_name=filename,
                                    mime='text/csv'
                                )
                                
                                # 3. Chart
                                # Get dates and returns for the bar chart
                                chart_data = df_exp[['Fecha Festivo', 'Retorno (%)']].copy()
                                chart_data.set_index('Fecha Festivo', inplace=True)
                                chart_data.dropna(inplace=True)
                                
                                if not chart_data.empty:
                                    st.write(f"**Impacto del Festivo (% Cambio de T-{days_to_analyze} a T+{days_to_analyze})**")
                                    st.bar_chart(chart_data)
                            
                            # Render ADR
                            render_section(
                                "📊 Comportamiento del ADR (Bolsa de Nueva York - USD)",
                                results_adr_md,
                                results_adr_export,
                                f"{selected_adr}_ADR_{analyze_year}.csv"
                            )
                            
                            st.write("---")
                            
                            # Render Local
                            if results_local_md:
                                render_section(
                                    f"📊 Comportamiento Acción Original (Bolsa Local de {country_of_origin} - Divisa Local)",
                                    results_local_md,
                                    results_local_export,
                                    f"{original_ticker}_LOCAL_{analyze_year}.csv"
                                )
                            
                except Exception as e:
                    st.error(f"Error procesando datos: {str(e)}")
