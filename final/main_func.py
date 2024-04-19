import pandas as pd
import re
import os
from datetime import datetime


def column_count_validation(csv1, csv2):
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    
    col_count_df1 = df1.shape[1]
    col_count_df2 = df2.shape[1]
    
    if col_count_df1 != col_count_df2:
        error_message = f"Number of columns are not equal. ({col_count_df1}) and ({col_count_df2})"
        status = "Fail"
    else:
        success_message = "Both files have the same number of columns"
        status = "Pass"
        error_message = None
        
    file_name1 = os.path.basename(csv1)
    file_name2 = os.path.basename(csv2)

    result_df = pd.DataFrame({"Feature": 'Column Count',
                              file_name1: [col_count_df1],
                              file_name2: [col_count_df2],
                              "Status": [status],
                              "Result": [error_message if status == 'Fail' else success_message]})

    return result_df, error_message if status == 'Fail' else success_message


def unique_value_validation(csv1,csv2):
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)

    unique_ids_df1 = df1['PHARMACY_TRANSACTION_ID'].value_counts()
    repeated_ids_df1 = unique_ids_df1[unique_ids_df1 > 1].index.tolist()

    result_rows = []

    for transaction_id in df1['PHARMACY_TRANSACTION_ID'].unique():
        if transaction_id in repeated_ids_df1:
            result_rows.append({
                'PHARMACY_TRANSACTION_ID': transaction_id,
                'Status': 'Fail',
                'Details': 'Common Value found'
            })
        else:
            result_rows.append({
                'PHARMACY_TRANSACTION_ID': transaction_id,
                'Status': 'Pass',
                'Details': 'Unique value'
            })

    result_df = pd.DataFrame(result_rows, columns=[
                             'PHARMACY_TRANSACTION_ID', 'Status', 'Details'])

    if any(row['Status'] == 'Fail' for row in result_rows):
        return result_df, "Error: Repeated values found in File 1"
    else:
        return result_df, "Success: No repeated values found in File 1"

def row_count_validation(csv_file, csv_file2):
    df1 = pd.read_csv(csv_file)
    df2 = pd.read_csv(csv_file2)

    row_count_df1 = df1.shape[0]
    row_count_df2 = df2.shape[0]

    file_name1 = os.path.basename(csv_file)
    file_name2 = os.path.basename(csv_file2)
    if row_count_df1 != row_count_df2:
        error_message = f"Number of rows are not equal. ({row_count_df1}) and ({row_count_df2})"
        status = "Fail"
    else:
        success_message = "Both files have the same number of rows"
        status = "Pass"
        error_message = None

    result_df = pd.DataFrame({"Feature": 'Row Count Validation',
                              file_name1: [row_count_df1],
                              file_name2: [row_count_df2],
                              "Status": [status],
                              "Result": [error_message if status == 'Fail' else success_message]})

    return result_df, error_message if status == 'Fail' else success_message


def column_name_match(csv_file, csv_file2):
    df1 = pd.read_csv(csv_file)
    df2 = pd.read_csv(csv_file2)
    file_name1 = os.path.basename(csv_file)
    file_name2 = os.path.basename(csv_file2)
    result_data = []

    for col1 in df1.columns:
        if col1 in df2.columns:
            status = "Pass"
            result_message = "Column names match"
        else:
            status = "Fail"
            result_message = "Column names do not match"

        result_data.append({
            file_name1: col1,
            file_name2: col1 if status == "Pass" else None,
            "Status": status,
            "Result": result_message
        })

    for col2 in df2.columns:
        if col2 not in df1.columns:
            result_data.append({
                file_name1: None,
                file_name2: col2,
                "Status": "Fail",
                "Result": "Column names do not match"
            })

    result_df = pd.DataFrame(result_data, columns=[
                             file_name1, file_name2, "Status", "Result"])

    if result_df['Status'].eq('Pass').all():
        return "Success: Column names match", result_df
    else:
        return "Error: Column names do not match", result_df

def required_fields_validation(config_df, csv_df):
    config_df = pd.read_csv(config_df)
    csv_df = pd.read_csv(csv_df)
    required_columns = config_df[config_df['Requirement'].isin(
        ['Y', 'C'])]['Field Name'].tolist()
    validation_results = []

    for field_name in required_columns:
        is_required = config_df.loc[config_df['Field Name']
                                    == field_name, 'Requirement'].iloc[0] == 'Y'

        if field_name in csv_df.columns:
            for idx, value in csv_df[field_name].items():
                txn_id = csv_df.at[idx, 'PHARMACY_TRANSACTION_ID']

                if pd.isna(value):
                    validation_results.append({
                        'PHARMACY_TRANSACTION_ID': txn_id,
                        'Column Name': field_name,
                        'Required Field (Y/N)': 'Y' if is_required else 'C',
                        'Value': 'Missing',
                        'Status': 'Fail',
                        'Details': f"{field_name} is a required field and is missing value."
                    })
                elif not is_required and value == 'C':
                    validation_results.append({
                        'PHARMACY_TRANSACTION_ID': txn_id,
                        'Column Name': field_name,
                        'Required Field (Y/N)': 'C',
                        'Value': value,
                        'Status': 'Fail',
                        'Details': f"{field_name} is a conditional field and has an invalid value: {value}."
                    })
        else:
            validation_results.append({
                'PHARMACY_TRANSACTION_ID': '',
                'Column Name': field_name,
                'Required Field (Y/N)': 'Y' if is_required else 'C',
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

    

def white_space_validation(config_df, csv_df):
    config_df = pd.read_csv(config_df)
    csv_df = pd.read_csv(csv_df)
    result_data = []

    for col in csv_df.columns:
        if col not in config_df['Field Name'].values:
            continue

        requirement = config_df.loc[config_df['Field Name'] == col, 'Requirement'].iloc[0]

        for idx, value in csv_df[col].items():
            if pd.isna(value):
                if requirement in ['Y', 'C']:
                    result_data.append({
                        "PHARMACY_TRANSACTION_ID": csv_df.loc[idx, 'PHARMACY_TRANSACTION_ID'],
                        "Column Name": col,
                        "Requirement": requirement,
                        "Value": 'Missing',
                        "Status": "Fail",
                        "Details": f"{col} is a required field and is missing value."
                    })
                continue

            if isinstance(value, str) and re.search(r'^\s|\s$|\s{2,}', value):
                result_data.append({
                    "PHARMACY_TRANSACTION_ID": csv_df.loc[idx, 'PHARMACY_TRANSACTION_ID'],
                    "Column Name": col,
                    "Requirement": requirement,
                    "Value": value,
                    "Status": "Fail",
                    "Details": "Whitespace found"
                })


    result_df = pd.DataFrame(result_data, columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Requirement', 'Value', 'Status', 'Details'])

    if not result_df.empty and "Fail" in result_df["Status"].values:
        return result_df, "Some values have unnecessary white space or are missing"
    else:
        return pd.DataFrame(columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Requirement', 'Value', 'Status', 'Details']), "All transactions passed"


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



def maximum_length_validation(config_df, csv_df):
    config_file = pd.read_csv(config_df)
    csv_file = pd.read_csv(csv_df)
    result_data = []

    for _, row in config_file.iterrows():
        col_name = row['Field Name']
        dtype = row['Data Type']
        requirement = row['Requirement']

        if col_name not in csv_file.columns:
            result_data.append(
                ("", col_name, requirement, dtype, "", "Fail", f"Column '{col_name}' not found in the CSV file"))
            continue

        col_values = csv_file[col_name].astype(str)

        for idx, value in col_values.items():
            txn_id = csv_file.at[idx, 'PHARMACY_TRANSACTION_ID']

            if pd.isna(value) or value.lower() == 'nan':
                if requirement in ['Y', 'C']:
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, 'Missing', "Fail", f"{col_name} is a required field and is missing value."))
                continue

            if not value.strip():
                if requirement == 'Y':
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, 'Empty', "Fail", f"{col_name} is a required field and has an empty value."))
                elif requirement == 'C':
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, 'Empty', "Fail", f"{col_name} is a conditional field and has an empty value."))
                continue

            if re.match(r'DATE\(\d+\)', dtype):
                length = int(re.search(r'\((\d+)\)', dtype).group(1))
                value = value.replace('.0', '')

                if length == 8:
                    if len(value) != length or not re.match(r'^\d+$', value):
                        result_data.append(
                            (txn_id, col_name, requirement, dtype, value, "Fail", "Invalid date format"))
                        continue

                    try:
                        datetime.strptime(value, '%Y%m%d')
                    except ValueError:
                        result_data.append(
                            (txn_id, col_name, requirement, dtype, value, "Fail", "Invalid date format"))
                        continue

                elif length == 14:
                    try:
                        datetime.strptime(value, '%Y%m%d %H:%M:%S')
                    except ValueError:
                        result_data.append(
                            (txn_id, col_name, requirement, dtype, value, "Fail", "Invalid date format"))
                        continue

            elif re.match(r'DATETIME\(\d+\)', dtype):
                length = int(re.search(r'DATETIME\((\d+)\)', dtype).group(1))
                value_str = str(value).strip().replace('.0', '')

                if len(value_str) != length:
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, value_str, "Fail", "Invalid datetime format"))
                    continue

            elif dtype.startswith('DOUBLE'):
                if not re.match(r'^-?\d+(\.\d+)?$', value):
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, value, "Fail", "Invalid double format"))
                    continue

            # if dtype.startswith('DOUBLE'):
            #     match = re.match(r'^DOUBLE\((\d+)-(\d+)\)$', dtype)
            #     if match:
            #         lower_bound, upper_bound = map(int, match.groups())
            #         if not re.match(r'^-?\d{1,%d}(\.\d{1,%d})?$' % (upper_bound, upper_bound), value):
            #             result_data.append(
            #                 (txn_id, col_name, requirement, dtype, value, "Fail", "Invalid double format"))
            #     else:
            #         if not re.match(r'^-?\d+(\.\d+)?$', value):
            #             result_data.append(
            #                 (txn_id, col_name, requirement, dtype, value, "Fail", "Invalid double format"))
                
                
            elif dtype.startswith('NUMBER'):
                match = re.match(r'^NUMBER\((\d+)-(\d+)\)$', dtype)
                if match:
                    min_len, max_len = map(int, match.groups())
                    if not re.match(r'^\d{%d,%d}$' % (min_len, max_len), value):
                        result_data.append(
                            (txn_id, col_name, requirement, dtype, value, "Fail", "Invalid numbformat"))
                else:
                    if not re.match(r'^\d+$', value):
                        result_data.append(
                            (txn_id, col_name, requirement, dtype, value, "Fail", "Invalid numbformat"))
                                    
            elif dtype.startswith('VARCHAR'):
                            match = re.match(r'^VARCHAR\((\d+)-(\d+)\)$', dtype)
                            if match:
                                min_len, max_len = map(int, match.groups())
                                if not min_len <= len(value) <= max_len:
                                    result_data.append(
                                        (txn_id, col_name, requirement, dtype, value, "Fail", "Value length does not match the specified range"))
                            else:
                                length = int(re.search(r'\((\d+)\)', dtype).group(1))
                                if len(value) > length:
                                    result_data.append(
                                        (txn_id, col_name, requirement, dtype, value, "Fail", "Exceeded length limit"))

            elif dtype.startswith('TIMESTAMP'):
                try:
                    datetime.strptime(value, '%Y%m%d %H:%M:%S')
                except ValueError:
                    result_data.append(
                        (txn_id, col_name, requirement, dtype, value, "Fail", "Invalid timestamp format"))
                    continue
            else:
                result_data.append(
                    (txn_id, col_name, requirement, dtype, value, "Fail", f"Unsupported data type '{dtype}'"))

    validation_result_df = pd.DataFrame(result_data, columns=[
                                        "PHARMACY_TRANSACTION_ID", "Column Name", "Requirement", "Data Type", "Value", "Status", "Details"])

    if validation_result_df['Status'].eq('Fail').any():
        return "Some test cases failed. Please check the output for more details", validation_result_df
    else:
        return "All test cases passed successfully", validation_result_df


