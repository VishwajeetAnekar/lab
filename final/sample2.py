import pandas as pd
import re

def validate_date(value, format_str):
    formats = {
        'DATE': ['%Y%m%d'],
        'DATETIME': ['%Y%m%d%H%M%S', '%Y%m%d %H:%M:%S', '%Y-%m-%d %H:%M:%S'],
        'TIMESTAMP': ['%Y%m%d%H%M%S']
    }
    for fmt in formats.get(format_str.upper(), []):
        try:
            pd.to_datetime(str(value), format=fmt)
            return True
        except:
            continue
    return False

def validate_varchar(value, length):
    return isinstance(value, str) and len(value) <= length

def validate_number(value):
    return isinstance(value, (int, float))

def validate_double(value):
    return isinstance(value, (int, float))

import pandas as pd
import re

def data_type_validation(config_file, data_file):
    config_df = pd.read_csv(config_file)
    data_df = pd.read_csv(data_file)
    
    validation_results = []
    
    for idx, row in data_df.iterrows():
        txn_id = row['PHARMACY_TRANSACTION_ID']
        
        for col in data_df.columns:
            field_info = config_df[config_df['Field Name'] == col]
            
            if not field_info.empty:
                data_type = field_info.iloc[0]['Data Type']
                
                if data_type.startswith("VARCHAR"):
                    max_length = int(re.search(r'\((.*?)\)', data_type).group(1))
                    value = str(row[col])
                    
                    if len(value) > max_length:
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Column Name': col,
                            'Data Type': 'VARCHAR',
                            'Status': 'Fail',
                            'Details': f"Value '{value}' in column '{col}' exceeds maximum length of {max_length} characters."
                        })
                    else:
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Column Name': col,
                            'Data Type': 'VARCHAR',
                            'Status': 'Pass',
                            'Details': None
                        })
                        
                elif data_type in ["DATE", "DATETIME", "TIMESTAMP"]:
                    format_info = field_info.iloc[0]['Field Format']
                    value = str(row[col])
                    
                    if len(value) != len(format_info):
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Column Name': col,
                            'Data Type': data_type,
                            'Status': 'Fail',
                            'Details': f"Value '{value}' in column '{col}' does not match the expected format '{format_info}'."
                        })
                    else:
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Column Name': col,
                            'Data Type': data_type,
                            'Status': 'Pass',
                            'Details': None
                        })
                        
                elif data_type in ["NUMBER", "DOUBLE"]:
                    value = str(row[col])
                    
                    try:
                        float(value)
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Column Name': col,
                            'Data Type': data_type,
                            'Status': 'Pass',
                            'Details': None
                        })
                    except ValueError:
                        validation_results.append({
                            'PHARMACY_TRANSACTION_ID': txn_id,
                            'Column Name': col,
                            'Data Type': data_type,
                            'Status': 'Fail',
                            'Details': f"Value '{value}' in column '{col}' is not a valid {data_type}."
                        })

    result_df = pd.DataFrame(validation_results, columns=['PHARMACY_TRANSACTION_ID', 'Column Name', 'Data Type', 'Status', 'Details'])




    if result_df['Status'].eq('Fail').any():
        return result_df, "Some data type validations failed"
    else:
        return pd.DataFrame(columns=['Config Column', 'CSV Value', 'Requirement', 'Status', 'Comments']), "All data type validations passed"

config_file = 'config.csv'
csv_file = 'data.csv'
result_df, message = data_type_validation(config_file, csv_file)
print(result_df)
result_df.to_csv('data_type_validation_result.csv', index=False)
