from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HOLIDAYS_DATA_FILE = BASE_DIR / "holidays_data.csv"
PRICE_HISTORY_FILE = BASE_DIR / "price_history.csv"

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
    "ABB": "Switzerland",
    "ABEV": "Brazil", "AC": "Canada", "AEM": "Canada", "AIQUY": "France", "ARM": "United Kingdom",
    "ASX": "Taiwan", "AUO": "Taiwan", "AXAHY": "France", "AZN": "United Kingdom", "BABA": "China",
    "BASFY": "Germany", "BAYRY": "Germany", "BBD": "Brazil", "BBDO": "Brazil", "BCE": "Canada",
    "BEKE": "China", "BGNE": "China", "BHP": "Australia", "BIDU": "China", "BILI": "China",
    "BMO": "Canada", "BMWYY": "Germany", "BNPQY": "France", "BNS": "Canada", "BP": "United Kingdom",
    "BSBR": "Brazil", "BTI": "United Kingdom", "CAJ": "Japan", "CAN": "China", "CHT": "Taiwan",
    "CIG": "Brazil", "CM": "Canada", "CNQ": "Canada", "DAO": "China", "DB": "Germany",
    "DEO": "United Kingdom", "DTEGY": "Germany", "EBR": "Brazil", "EDU": "China", "ENB": "Canada",
    "ERJ": "Brazil", "FUTU": "China", "GGB": "Brazil", "GOLD": "Canada", "GSK": "United Kingdom",
    "HDB": "India", "HMC": "Japan", "HSBC": "United Kingdom", "HTHT": "China", "HUYA": "China",
    "IBN": "India", "INFY": "India", "IQ": "China", "ITUB": "Brazil", "IX": "Japan",
    "JD": "China", "KB": "South Korea", "KEP": "South Korea", "KMTUY": "Japan", "KNBWY": "Japan",
    "KT": "South Korea", "LI": "China", "LPL": "South Korea", "LU": "China", "LYG": "United Kingdom",
    "MBGYY": "Germany", "MFC": "Canada", "MFG": "Japan", "MNSO": "China", "MUFG": "Japan",
    "NGG": "United Kingdom", "NIO": "China", "NSRGY": "Switzerland", "NTDOY": "Japan", "NTES": "China",
    "NVS": "Switzerland", "ORAN": "France", "PBR": "Brazil", "PDD": "China", "PKX": "South Korea",
    "QFIN": "China", "RDY": "India", "RELX": "United Kingdom", "RENOY": "France", "RHHBY": "Switzerland",
    "RIO": "Australia", "RY": "Canada", "SAN": "Spain", "SAP": "Germany", "SBS": "Brazil",
    "SFTBY": "Japan", "SHEL": "United Kingdom", "SHG": "South Korea", "SHOP": "Canada", "SID": "Brazil",
    "SIEGY": "Germany", "SKM": "South Korea", "SMFG": "Japan", "SONY": "Japan", "SU": "Canada",
    "TAL": "China", "TCLRY": "Australia", "TCOM": "China", "TD": "Canada", "TECK": "Canada",
    "TIGR": "China", "TIMB": "Brazil", "TLSYY": "Australia", "TM": "Japan", "TME": "China",
    "TRP": "Canada", "TSM": "Taiwan", "TTNDY": "Hong Kong", "TU": "Canada", "TUYA": "China",
    "UBS": "Switzerland", "UL": "United Kingdom", "UMC": "Taiwan", "VALE": "Brazil", "VEDL": "India",
    "VOD": "United Kingdom", "VWAGY": "Germany", "WB": "China", "WIT": "India", "WOWOY": "Australia",
    "WPM": "Canada", "XP": "Brazil", "XPEV": "China", "YMM": "China", "YSG": "China",
    "ZLAB": "China", "ZTO": "China",
}

ADR_ORIGINAL_MAP = {
    "BHP": "BHP.AX", "RIO": "RIO.AX", "TCLRY": "TLC.AX", "TLSYY": "TLS.AX", "WOWOY": "WOW.AX",
    "ABEV": "ABEV3.SA", "ITUB": "ITUB4.SA", "PBR": "PETR4.SA", "VALE": "VALE3.SA", "XP": "XP",
    "AC": "AC.TO", "BMO": "BMO.TO", "ENB": "ENB.TO", "SHOP": "SHOP.TO", "TD": "TD.TO",
    "BABA": "9988.HK", "BIDU": "9888.HK", "JD": "9618.HK", "NIO": "9866.HK", "PDD": "PDD", "XPEV": "9868.HK",
    "ORAN": "ORA.PA", "SAN": "SAN.PA", "AIQUY": "AI.PA",
    "SAP": "SAP.DE", "VWAGY": "VOW3.DE", "BMWYY": "BMW.DE", "DB": "DBK.DE",
    "ARM": "ARM.L", "AZN": "AZN.L", "BP": "BP.L", "SHEL": "SHEL.L", "UL": "ULVR.L",
    "SONY": "6758.T", "TM": "7203.T", "HMC": "7267.T", "NTDOY": "7974.T",
    "TSM": "2330.TW", "UMC": "2303.TW", "ASX": "3711.TW", "AUO": "2409.TW", "CHT": "2412.TW",
}


def get_tracked_tickers():
    tickers = set(ADR_COUNTRY_MAP.keys())
    tickers.update(ticker for ticker in ADR_ORIGINAL_MAP.values() if ticker)
    return sorted(tickers)
