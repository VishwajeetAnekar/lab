import pandas as pd

def datatype_validation(config_file, csv_file):
    config_df = pd.read_csv(config_file)
    csv_df = pd.read_csv(csv_file)
    validation_results = []

    for idx, row in config_df.iterrows():
        field_name = row['Field Name']
        datatype = row['Data Type']
        requirement = row['Requirement']

        if 'DATE' in datatype:
            if field_name in csv_df.columns:
                for idx, value in csv_df[field_name].items():
                    txn_id = csv_df.at[idx, 'PHARMACY_TRANSACTION_ID']
                    if not validate_date(value, requirement):
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Field Name': field_name,
                            'Status': 'Fail',
                            'Details': f"{field_name} has invalid date format: {value}"
                        })
            elif requirement != 'N':
                validation_results.append({
                    'PHARMACY_TRANSACTION_ID': '',
                    'Field Name': field_name,
                    'Status': 'Fail',
                    'Details': f"{field_name} is required but missing in the CSV file"
                })

        elif 'VARCHAR' in datatype:
            if field_name in csv_df.columns:
                for idx, value in csv_df[field_name].items():
                    txn_id = csv_df.at[idx, 'PHARMACY_TRANSACTION_ID']
                    if not validate_varchar(value, requirement):
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Field Name': field_name,
                            'Status': 'Fail',
                            'Details': f"{field_name} has more than 256 characters: {value}"
                        })
            elif requirement != 'N':
                validation_results.append({
                    'PHARMACY_TRANSACTION_ID': '',
                    'Field Name': field_name,
                    'Status': 'Fail',
                    'Details': f"{field_name} is required but missing in the CSV file"
                })

        elif 'DOUBLE' in datatype:
            if field_name in csv_df.columns:
                for idx, value in csv_df[field_name].items():
                    txn_id = csv_df.at[idx, 'PHARMACY_TRANSACTION_ID']
                    if not validate_double(value, requirement):
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Field Name': field_name,
                            'Status': 'Fail',
                            'Details': f"{field_name} is not a valid number: {value}"
                        })
            elif requirement != 'N':
                validation_results.append({
                    'PHARMACY_TRANSACTION_ID': '',
                    'Field Name': field_name,
                    'Status': 'Fail',
                    'Details': f"{field_name} is required but missing in the CSV file"
                })

        elif 'NUMBER' in datatype:
            if field_name in csv_df.columns:
                for idx, value in csv_df[field_name].items():
                    txn_id = csv_df.at[idx, 'PHARMACY_TRANSACTION_ID']
                    if not validate_number(value, requirement):
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Field Name': field_name,
                            'Status': 'Fail',
                            'Details': f"{field_name} is not a valid number: {value}"
                        })
            elif requirement != 'N':
                validation_results.append({
                    'PHARMACY_TRANSACTION_ID': '',
                    'Field Name': field_name,
                    'Status': 'Fail',
                    'Details': f"{field_name} is required but missing in the CSV file"
                })

    result_df = pd.DataFrame(validation_results, columns=['PHARMACY_TRANSACTION_ID', 'Field Name', 'Status', 'Details'])
    return result_df
