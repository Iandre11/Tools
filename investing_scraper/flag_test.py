def get_flag_emoji(country_name):
    # Testing logic without external package if possible, or using pycountry
    import pycountry
    try:
        # Check if country name works directly
        country = pycountry.countries.search_fuzzy(country_name)[0]
        code = country.alpha_2
        return chr(ord(code[0]) + 127397) + chr(ord(code[1]) + 127397)
    except Exception as e:
        return ""

print("Spain:", get_flag_emoji("Spain"))
print("United States:", get_flag_emoji("United States"))
print("Bosnia-Herzegovina:", get_flag_emoji("Bosnia-Herzegovina"))
