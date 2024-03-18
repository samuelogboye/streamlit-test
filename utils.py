sector_attributes = {
    'A': 'Agriculture,forestry and fishing',
    'B': 'Mining and quarrying',
    'C': 'Manufacturing',
    'D': 'Electricity, gas, steam',
    'E': 'Water supply, sewerage',
    'F': 'Construction',
    'G': 'Wholesale and retail trade',
    'H': 'Transportation',
    'I': 'Accommodation and food service activities',
    'J': 'Information and communication',
    'K': 'Financial and insurance',
    'L': 'Real estate',
    'M': 'Knowledge-based services',
    'N': 'Travel agent, cleaning',
    'O': 'Public administration, defence and comp. social',
    'P': 'Education',
    'Q': 'Human health and social work',
    'R': 'Arts, entertainment, recreation activities',
    'S': 'Other service activities',
    'T': 'Private households with hired help; households’ production of goods and services for their own use'
}

def get_company_codes(c_name):
        return [code for code, name in sector_attributes.items() if name == c_name][0]


