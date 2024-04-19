import pandas as pd
import os

def read_csv_files(csv_file1, csv_file2):
    try:
        df1 = pd.read_csv(csv_file1)
        df2 = pd.read_csv(csv_file2)
        return df1, df2
    except FileNotFoundError as e:
        return f"Error: {e}", None
    except pd.errors.ParserError as e:
        return f"Error reading CSV files: {e}", None
    except Exception as e:
        return f"An unexpected error occurred: {e}", None

def column_count_validation(csv_file1, csv_file2):
    df1, df2 = read_csv_files(csv_file1, csv_file2)

    col_count_df1 = df1.shape[1]
    col_count_df2 = df2.shape[1]

    file_name1 = os.path.basename(csv_file1)
    file_name2 = os.path.basename(csv_file2)

    if col_count_df1 != col_count_df2:
        status = "Fail"
        message = "Number of columns are not equal."
    else:
        status = "Pass"
        message = "Both files have the same number of columns."

    result_df = pd.DataFrame({
        "Feature": 'Column Count',
        file_name1: [col_count_df1],
        file_name2: [col_count_df2],
        "Status": [status],
        "Result": [message]
    })

    return result_df, message

def unique_value_validation(csv_file1, csv_file2):
    df1, df2 = read_csv_files(csv_file1, csv_file2)

    file_name1 = os.path.basename(csv_file1)
    file_name2 = os.path.basename(csv_file2)

    unique_ids_df1 = df1['PHARMACY_TRANSACTION_ID'].value_counts()
    repeated_ids_df1 = unique_ids_df1[unique_ids_df1 > 1].index.tolist()

    unique_ids_df2 = df2['PHARMACY_TRANSACTION_ID'].value_counts()
    repeated_ids_df2 = unique_ids_df2[unique_ids_df2 > 1].index.tolist()

    result_rows = []
    for transaction_id in df1['PHARMACY_TRANSACTION_ID'].unique():
        if transaction_id in repeated_ids_df1:
            result_rows.append({
                'PHARMACY_TRANSACTION_ID': transaction_id,
                'File': file_name1,
                'Status': 'Fail',
                'Comments': 'Duplicate value found in File 1'
            })
        else:
            result_rows.append({
                'PHARMACY_TRANSACTION_ID': transaction_id,
                'File': file_name1,
                'Status': 'Pass',
                'Comments': 'Unique value in File 1'
            })

    for transaction_id in df2['PHARMACY_TRANSACTION_ID'].unique():
        if transaction_id in repeated_ids_df2:
            result_rows.append({
                'PHARMACY_TRANSACTION_ID': transaction_id,
                'File': file_name2,
                'Status': 'Fail',
                'Comments': 'Duplicate value found in File 2'
            })
        else:
            result_rows.append({
                'PHARMACY_TRANSACTION_ID': transaction_id,
                'File': file_name2,
                'Status': 'Pass',
                'Comments': 'Unique value in File 2'
            })

    result_df = pd.DataFrame(result_rows, columns=[
                             'PHARMACY_TRANSACTION_ID', 'File', 'Status', 'Comments'])

    common_ids = set(df1['PHARMACY_TRANSACTION_ID']).intersection(
        set(df2['PHARMACY_TRANSACTION_ID']))

    common_rows = []
    for transaction_id in common_ids:
        common_rows.append({
            'PHARMACY_TRANSACTION_ID': transaction_id,
            'File': 'Both',
            'Status': 'Fail',
            'Comments': 'Common value found in both files'
        })

    common_df = pd.DataFrame(common_rows, columns=[
                             'PHARMACY_TRANSACTION_ID', 'File', 'Status', 'Comments'])

    final_df = pd.concat([result_df, common_df], ignore_index=True)

    message = "Error: Common values found between File 1 and File 2" if common_ids else "Success: No common values found between File 1 and File 2"

    return final_df, message

def row_count_validation(csv_file1, csv_file2):
    df1, df2 = read_csv_files(csv_file1, csv_file2)

    row_count_df1 = df1.shape[0]
    row_count_df2 = df2.shape[0]

    file_name1 = os.path.basename(csv_file1)
    file_name2 = os.path.basename(csv_file2)

    if row_count_df1 != row_count_df2:
        status = "Fail"
        message = "Number of rows are not equal"
    else:
        status = "Pass"
        message = "Both files have the same number of rows."

    result_df = pd.DataFrame({
        "Feature": 'Row Count',
        file_name1: [row_count_df1],
        file_name2: [row_count_df2],
        "Status": [status],
        "Result": [message]
    })

    return result_df, message

def column_name_match(csv_file1, csv_file2):
    df1, df2 = read_csv_files(csv_file1, csv_file2)

    file_name1 = os.path.basename(csv_file1)
    file_name2 = os.path.basename(csv_file2)

    cols1 = [col.lower() for col in df1.columns.tolist()]
    cols2 = [col.lower() for col in df2.columns.tolist()]

    result_data = []

    for col1 in df1.columns:
        col1_lower = col1.lower()
        if col1_lower in cols2:
            status = "Pass"
            col2 = df2.columns[cols2.index(col1_lower)]
            result_message = "Column names match"
        else:
            status = "Fail"
            col2 = None
            result_message = "Column names do not match"

        result_data.append({
            file_name1: col1,
            file_name2: col2,
            "Status": status,
            "Result": result_message
        })

    for col2 in df2.columns:
        col2_lower = col2.lower()
        if col2_lower not in cols1:
            result_data.append({
                file_name1: None,
                file_name2: col2,
                "Status": "Fail",
                "Result": "Column names do not match"
            })

    result_df = pd.DataFrame(result_data, columns=[
                             file_name1, file_name2, "Status", "Result"])

    message = "Success: Column names match" if result_df['Status'].eq('Pass').all() else "Error: Column names do not match"

    return result_df, message
