import pandas as pd
import re
from datetime import datetime

def validate_no_dashes(value, field_name):
    if '-' in str(value):
        return f"{field_name} contains dashes"
    return None

def validate_2_chars(value, field_name):
    if not re.match(r'^[a-zA-Z]{2}$', str(value)):
        return f"{field_name} does not match the 2 chars format."
    return None

def validate_3_digits(value, field_name):
    value_str = str(value).rstrip('.0')
    if not re.match(r'^\d{3}$', value_str):
        return f"{field_name} does not match the 3 digits format."
    return None

def validate_two_char_state(value, field_name):
    if not re.match(r'^[a-zA-Z]{2}$', str(value)):
        return f"{field_name} does not match the two character state code format."
    return None

def validate_YYYY(value, field_name):
    value_str = str(value).rstrip('.0')
    if not re.match(r'^\d{4}$', value_str):
        return f"{field_name} does not match the YYYY format."
    return None

def validate_YYYYMMDD(value, field_name):
    value_str = str(value).rstrip('.0')
    if not re.match(r'^\d{8}$', value_str):
        return f"{field_name} does not match the YYYYMMDD format."
    return None

def validate_YYYYMMDDHHMMSS(value, field_name):
    value_int = int(value)
    value_str = str(value_int).rstrip('.0')
    pattern = r'^\d{14}$'
    if not re.match(pattern, value_str):
        return f"{field_name} does not match the YYYYMMDDHHMMSS format."
    try:
        datetime.strptime(value_str, '%Y%m%d%H%M%S')
    except ValueError:
        return f"{field_name} is not a valid datetime."
    return None

def validate_YYYYMMDD_HHMMSS(value, field_name):
    pattern = r'^\d{8} \d{2}:\d{2}:\d{2}$'
    if not re.match(pattern, value):
        return f"{field_name} does not match the YYYYMMDD HH:MM:SS format."
    try:
        datetime.strptime(value, '%Y%m%d %H:%M:%S')
    except ValueError:
        return f"{field_name} is not a valid datetime."
    return None


def validate_field_format(value, field_name, field_format):
    if field_format == 'No dashes':
        return validate_no_dashes(value, field_name)
    elif field_format == '2 chars':
        return validate_2_chars(value, field_name)
    elif field_format == '3 digits':
        return validate_3_digits(value, field_name)
    elif field_format == 'Two character state code':
        return validate_two_char_state(value, field_name)
    elif field_format == 'YYYY':
        return validate_YYYY(value, field_name)
    elif field_format == 'YYYYMMDD':
        return validate_YYYYMMDD(value, field_name)
    elif field_format == 'YYYYMMDDHHMMSS':
        return validate_YYYYMMDDHHMMSS(value, field_name)
    elif field_format == 'YYYYMMDD HH:MM:SS':
        return validate_YYYYMMDD_HHMMSS(value, field_name)
    return None

def field_format_validation(config_file, csv_file):
    config_df = pd.read_csv(config_file)
    csv_df = pd.read_csv(csv_file)
    
    result_data = []

    for idx, row in config_df.iterrows():
        field_name = row['Field Name']
        field_format = row['Field Format']
        requirement = row['Requirement']
        
        if field_name in csv_df.columns:
            for idx, value in csv_df[field_name].items():
                if pd.isna(value):
                    if requirement == 'N':
                        continue
                    else:
                        validation_result = f"{field_name} is a required field and is missing value."
                else:
                    validation_result = validate_field_format(value, field_name, field_format)
                    
                if validation_result:
                    result_data.append({
                        'PHARMACY_TRANSACTION_ID': csv_df.loc[idx, 'PHARMACY_TRANSACTION_ID'],
                        'Column Name': field_name,
                        'Field Format': field_format,
                        'Requirement': requirement,
                        'Value': value,
                        'Status': 'Fail',
                        'Details': validation_result
                    })

    result_df = pd.DataFrame(result_data, columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Field Format', 'Requirement', 'Value', 'Status', 'Details'])

    if not result_df.empty:
        return result_df, "Some fields have invalid values or are missing"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Field Format', 'Requirement', 'Value', 'Status', 'Details']), "All transactions passed"

# Testing the function

config_file = 'config.csv'
csv_file = 'data.csv'
result_df, message = field_format_validation(config_file, csv_file)
print(result_df)
result_df.to_csv('field_format_validation_result.csv', index=False)
