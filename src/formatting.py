def format_naics():   
    '''Take naics categories and map streamlit labels to dataframe values.
    
    NOTE: the naics column in the original df is used to find the k in naics_categories. 
    The values were looked up from the NAICS database from 2022 data: 
    https://www.census.gov/naics/?input=99999002&year=2022
    Some values repeat, but is matches the database.''' 
    
    naics_categories = {
        "11" : "Agriculture, Forestry, Fishing and Hunting",
        "21" : "Mining, Quarrying, and Oil and Gas Extraction",
        '22' : "Utilities",
        '23' : "Construction",
        '31' : "Manufacturing",
        '32' : "Manufacturing",
        '33' : "Manufacturing",
        '42' : "Wholesale Trade",
        '44' : "Retail Trade",
        '45' : "Retail Trade",
        '48' : "Transportation and Warehousing",
        '49' : "Transportation and Warehousing",
        '51' : "Information",
        '52' : "Finance and Insurance",
        '53' : "Real Estate and Rental and Leasing",
        '54' : "Professional, Scientific, and Technical Services",
        '55' : "Management of Companies and Enterprises",
        '56' : "Administrative and Support and Waste Management and Remediation Services",
        '61' : "Educational Services",
        '62' : "Health Care and Social Assistance",
        '71' : "Arts, Entertainment, and Recreation",
        '72' : "Accommodation and Food Services",
        '81' : "Other Services (except Public Administration)",
        '92' : "Public Administration",
        '99' : "Unclassified Establishments"
    }
    naics_labels = {k : f'{k} - {v}' for k, v in naics_categories.items()}
    return naics_labels

def format_employee_sizes():
    employee_sizes = [
        '1 to 4',
        '5 to 9',
        '10 to 19',
        '20 to 49',
        '50 to 99',
        '100 to 249',
        '250 to 499',
        '500 to 999',
        '1000 to 4999'
    ]
    return employee_sizes

def format_telcom():
    '''Telcom values need to be ordered for slider so just manually creating this as a list.
    Values were created from original distinct telecom_expense column'''
    telcom_labels = [
        'Less than $2,000',
        '$2,000 to $5,000', 
        '$5,000 to $20,000',
        '$20,000 to $50,000',   
        '$50,000 to $100,000',
        '$50,000 to $100,000',
        '$100,000 to $250,000',
        'Over $250,000'                       
    ]
    return telcom_labels       