import pycountry

countries_list = ['Argentina', 'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Belgium', 'Bermuda', 'Bosnia-Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Canada', 'Cayman Islands', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Ecuador', 'Egypt', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Malaysia', 'Malta', 'Mauritius', 'Mexico', 'Mongolia', 'Montenegro', 'Morocco', 'Namibia', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palestinian Territory', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saudi Arabia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Taiwan', 'Tanzania', 'Thailand', 'Tunisia', 'Türkiye', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Venezuela', 'Vietnam', 'Zimbabwe']

manual_map = {
    'Bosnia-Herzegovina': 'BA',
    'Russia': 'RU',
    'South Korea': 'KR',
    'Türkiye': 'TR',
    'United Arab Emirates': 'AE',
    'United Kingdom': 'GB',
    'United States': 'US',
    'Vietnam': 'VN',
    'Palestinian Territory': 'PS',
    'Taiwan': 'TW',
    'Hong Kong': 'HK',
    'Macau': 'MO'
}

def get_flag_emoji(country_name):
    if country_name in manual_map:
        code = manual_map[country_name]
    else:
        try:
            # Check exact match
            country = pycountry.countries.get(name=country_name)
            if not country:
                country = pycountry.countries.search_fuzzy(country_name)[0]
            code = country.alpha_2
        except Exception:
            return ""
    
    return chr(ord(code[0]) + 127397) + chr(ord(code[1]) + 127397)

flags_dict = {}
for c in countries_list:
    flags_dict[c] = f"{get_flag_emoji(c)} {c}"

print("FLAGS_MAP = {")
for k, v in flags_dict.items():
    print(f'    "{k}": "{v}",')
print("}")
