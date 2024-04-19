import pandas as pd
import re
from datetime import datetime

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