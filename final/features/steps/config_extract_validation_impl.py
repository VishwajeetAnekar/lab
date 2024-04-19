import pandas as pd
import re

def white_space_validation(csv_df):
    csv_df= pd.read_csv(csv_df)
    result_data = []

    for col in csv_df.columns:
        for idx, value in csv_df[col].items():
            if isinstance(value, str) and re.search(r'^\s|\s$|\s{2,}', value):
                result_data.append({
                    "PHARMACY_TRANSACTION_ID": csv_df.loc[idx, 'PHARMACY_TRANSACTION_ID'],
                    "Column Name": col,
                    "Value": value,
                    "Status": "Fail",
                    "Comments": "Whitespace found"
                })

    result_df = pd.DataFrame(result_data, columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Value', 'Status', 'Comments'])

    if not result_df.empty and "Fail" in result_df["Status"].values:
        return result_df, "Some values have unnecessary white space or are missing"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Value', 'Status', 'Comments']), "All transactions passed"


def duplicate_keys_validation(csv_file):
    df = pd.read_csv(csv_file)
    column_names = df.columns.tolist()
    duplicates = {}
    result_data = []

    for col in column_names:
        base_col = col.split('.')[0].lower()
        if base_col in duplicates:
            duplicates[base_col].append(col)
        else:
            duplicates[base_col] = [col]

    for col in column_names:
        base_col = col.split('.')[0].lower()
        if len(duplicates[base_col]) > 1:
            result_data.append({
                "Column Name": col,
                "Status": "Fail",
                "Details": f"Duplicate Column found"
            })
        else:
            result_data.append({
                "Column Name": col,
                "Status": "Pass",
                "Details": "Unique Column"
            })

    result_df = pd.DataFrame(result_data)

    if result_df['Status'].eq('Pass').all():
        validation_result = "Success: No duplicate columns found"
    else:
        validation_result = result_df[result_df['Status'] == 'Fail'].to_string(
            index=False)

    return result_df, validation_result

def required_fields_validation(config_df, csv_df):
    config_df = pd.read_csv(config_df)
    csv_df = pd.read_csv(csv_df)
    required_columns = config_df[config_df['Requirement'].isin(
        ['Y', 'C'])]['Field Name'].tolist()
    validation_results = []

    for field_name in required_columns:
        requirement = config_df.loc[config_df['Field Name'] == field_name, 'Requirement'].iloc[0]
        
        if field_name in csv_df.columns:
            for idx, value in csv_df[field_name].items():
                txn_id = csv_df.at[idx, 'PHARMACY_TRANSACTION_ID']

                if pd.isna(value):
                    validation_results.append({
                        'PHARMACY_TRANSACTION_ID': txn_id,
                        'Column Name': field_name,
                        'Required Field (Y/N)': requirement,
                        'Value': 'Missing',
                        'Status': 'Fail',
                        'Details': f"{field_name} is a required field and is missing value."
                    })
                elif requirement == 'C' and value == 'C':
                    validation_results.append({
                        'PHARMACY_TRANSACTION_ID': txn_id,
                        'Column Name': field_name,
                        'Required Field (Y/N)': requirement,
                        'Value': value,
                        'Status': 'Fail',
                        'Details': f"{field_name} is a conditional field and has an invalid value: {value}."
                    })
        else:
            validation_results.append({
                'PHARMACY_TRANSACTION_ID': '',
                'Column Name': field_name,
                'Required Field (Y/N)': requirement,
                'Value': 'NA',
                'Status': 'Fail',
                'Details': f"{field_name} is a required field but does not exist in the CSV file."
            })

    result_df = pd.DataFrame(validation_results, columns=[
        'PHARMACY_TRANSACTION_ID', 'Column Name', 'Required Field (Y/N)', 'Value', 'Status', 'Details'])

    if not result_df.empty:
        return result_df, "Some required fields are missing or have invalid values"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Required Field (Y/N)', 'Value', 'Status', 'Details']), "All transactions passed"


def expected_value_validation(config_file, csv_file):
    config_df = pd.read_csv(config_file)
    csv_df = pd.read_csv(csv_file)
    
    expected_fields = config_df[config_df['Expected Value/s (comma separated)'].notna()]
    
    validation_results = []
    
    for idx, row in expected_fields.iterrows():
        field_name = row['Field Name']
        requirement = row['Requirement']
        expected_values = [val.strip() for val in row['Expected Value/s (comma separated)'].split(',')]
        
        if field_name in csv_df.columns:
            for idx, value in csv_df[field_name].items():
                txn_id = csv_df.at[idx, 'PHARMACY_TRANSACTION_ID']

                if pd.isna(value) or value == '':
                    if requirement in ['Y', 'C']:
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Column Name': field_name,
                            'Requirement': requirement,
                            'Value': 'Missing',
                            'Status': 'Fail',
                            'Comments': f"{field_name} is a required field and is missing value."
                        })
               
                    continue
                
                if str(value) not in expected_values:
                    validation_results.append({
                        'PHARMACY_TRANSACTION_ID': txn_id,
                        'Column Name': field_name,
                        'Requirement': requirement,
                        'Value': value,
                        'Status': 'Fail',
                        'Comments': f"{field_name} has an unexpected value: {value}. Expected values are {', '.join(expected_values)}."
                    })
                
        else:
            validation_results.append({
                'PHARMACY_TRANSACTION_ID': '',
                'Column Name': field_name,
                'Requirement': requirement,
                'Value': 'NA',
                'Status': 'Fail',
                'Comments': f"{field_name} is a required field but does not exist in the CSV file."
            })

    result_df = pd.DataFrame(validation_results, columns=[
        'PHARMACY_TRANSACTION_ID', 'Column Name', 'Requirement', 'Value', 'Status', 'Comments'])

    if not result_df.empty:
        return result_df, "Some fields have unexpected values or are missing"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Requirement', 'Value', 'Status', 'Comments']), "All transactions passed"


def field_name_validation(config_file, csv_file):
    config_df = pd.read_csv(config_file)
    csv_df = pd.read_csv(csv_file)

    expected_field_data = config_df[['Field Name', 'Requirement']].values.tolist()
    actual_field_names = csv_df.columns.tolist()

    result_data = []

    for expected_field, requirement in expected_field_data:
        if expected_field in actual_field_names:
            result_data.append({
                'Config Column': expected_field,
                'CSV Column': expected_field,
                'Requirement': requirement,
                'Status': 'Pass',
                'Comments': f"Field name '{expected_field}' is present in the CSV file."
            })
        elif expected_field.lower() in [col.lower() for col in actual_field_names]:
            actual_field = [col for col in actual_field_names if col.lower() == expected_field.lower()][0]
            result_data.append({
                'Config Column': expected_field,
                'CSV Column': actual_field,
                'Requirement': requirement,
                'Status': 'Pass',
                'Comments': f"Field name '{expected_field}' is present in the CSV file with different case: '{actual_field}'."
            })
        else:
            if requirement in ['Y', 'C']:
                result_data.append({
                    'Config Column': expected_field,
                    'CSV Column': '',
                    'Requirement': requirement,
                    'Status': 'Fail',
                    'Comments': f"Required field '{expected_field}' is missing in the CSV file."
                })
            else:
                result_data.append({
                    'Config Column': expected_field,
                    'CSV Column': '',
                    'Requirement': requirement,
                    'Status': 'Pass',
                    'Comments': f"Non-required field '{expected_field}' is not present in the CSV file, but it's okay."
                })

    result_df = pd.DataFrame(result_data, columns=['Config Column', 'CSV Column', 'Requirement', 'Status', 'Comments'])

    if result_df['Status'].eq('Fail').any():
        return result_df, "Some expected field names are missing or case-sensitive matching failed"
    else:
        return pd.DataFrame(columns=['Config Column', 'CSV Column', 'Requirement', 'Status', 'Comments']), "All expected field names are present in the CSV file"
