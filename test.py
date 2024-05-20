import os
import pandas as pd
from prettytable import PrettyTable
from datetime import datetime


def read_csv_files(folder_path):
    config_file_path = None
    extract_file_path = None

    for file_name in os.listdir(folder_path):
        if file_name.startswith("config") and file_name.endswith(".csv"):
            config_file_path = os.path.join(folder_path, file_name)
        elif file_name.endswith(".csv"):
            extract_file_path = os.path.join(folder_path, file_name)

    if not config_file_path or not extract_file_path:
        raise FileNotFoundError(
            "Either config file or extract file is missing in the folder.")

    return config_file_path, extract_file_path

def validate_required_fields(config_file, extract_file):
    config_df = pd.read_csv(config_file)
    extract_df = pd.read_csv(extract_file)

    primary_key_field = config_df.loc[
        config_df['Field Name'].str.contains(
            'PHARMACY_TRANSACTION_ID', case=False, na=False),
        'Field Name'
    ].values[0]

    required_fields = config_df.loc[config_df['Requirement']
                                    == 'Y', 'Field Name'].tolist()

    missing_data = []

    for field in required_fields:
        if field not in extract_df.columns:
            sample_primary_keys = extract_df[primary_key_field].head(
                5).tolist()
            missing_data.append({
                "Column": field,
                "Error": "Column not found in extract file",
                "Missing Primary Keys": sample_primary_keys
            })
        else:
            missing_values = extract_df[field].isna(
            ) | extract_df[field].astype(str).str.strip().eq('')
            if missing_values.any():
                missing_primary_keys = extract_df.loc[missing_values, primary_key_field].tolist(
                )
                missing_data.append({
                    "Column": field,
                    "Error": "Missing values found in column",
                    "Missing Primary Keys": missing_primary_keys
                })

    table = PrettyTable()
    table.field_names = ["Column", "Error", "Missing Primary Keys"]
    for row in missing_data:
        table.add_row([row["Column"], row["Error"], ', '.join(
            map(str, row["Missing Primary Keys"]))])
    print(table)

    save_to_csv = input(
        "Do you want to save the validation results to a CSV file? (yes/no): ").lower()
    if save_to_csv == "yes":
        df = pd.DataFrame(missing_data)
        df.to_csv('required_validations.csv', index=False)
        print("Validation results saved to required_validations.csv")


def column_name_match(config_file, extract_file):
    config_df = pd.read_csv(config_file)
    extract_df = pd.read_csv(extract_file)

    config_columns = set(config_df['Field Name'].tolist())
    extract_columns = set(extract_df.columns.tolist())

    total_config_count = len(config_columns)
    total_extract_count = len(extract_columns)

    if config_columns == extract_columns:
        print("Column names match exactly between config and extract files.")
    else:
        missing_in_extract = config_columns - extract_columns
        missing_in_config = extract_columns - config_columns

        print("Column names do not match between config and extract files:")
        table = PrettyTable()
        table.field_names = ["Total Count in Config",
                             "Count in Extract", "Missing in Config", "Missing in Extract"]
        table.add_row([total_config_count, total_extract_count, ", ".join(
            missing_in_config), ", ".join(missing_in_extract)])
        print(table)

        save_to_csv = input(
            "Do you want to save the comparison results to a CSV file? (yes/no): ").lower()
        if save_to_csv == "yes":
            comparison_results = {
                "Total Count in Config": [total_config_count],
                "Count in Extract": [total_extract_count],
                "Missing in Config": [", ".join(missing_in_config)],
                "Missing in Extract": [", ".join(missing_in_extract)]
            }
            df = pd.DataFrame(comparison_results)
            df.to_csv('column_comparison_results.csv', index=False)
            print("Comparison results saved to column_comparison_results.csv")


def validate_expected_values(config_file, extract_file):
    config_df = pd.read_csv(config_file)
    extract_df = pd.read_csv(extract_file)

    expected_value_fields = config_df.loc[config_df['Expected Value/s (comma separated)'].notna(
    ), 'Field Name'].tolist()

    validation_results = []

    for field in extract_df.columns:
        if field in expected_value_fields:
            expected_values = config_df.loc[config_df['Field Name'] ==
                                            field, 'Expected Value/s (comma separated)'].iloc[0].split(',')
            for index, row in extract_df.iterrows():
                if pd.notna(row[field]) and row[field] not in expected_values:
                    validation_results.append({
                        "Column Name": field,
                        "Expected values from config": ', '.join(expected_values),
                        "Actual value in extract": row[field],
                        "PHARMACY_TRANSACTION_ID": row['PHARMACY_TRANSACTION_ID']
                    })

    if validation_results:
        fail_table = PrettyTable()
        fail_table.field_names = ["Column Name", "Expected values from config",
                                  "Actual value in extract", "PHARMACY_TRANSACTION_ID"]
        for row in validation_results:
            fail_table.add_row([row["Column Name"], row["Expected values from config"],
                               row["Actual value in extract"], row["PHARMACY_TRANSACTION_ID"]])

        print(fail_table)

        save_to_csv = input(
            "Do you want to save the validation results to a CSV file? (yes/no): ").lower()
        if save_to_csv == "yes":
            df = pd.DataFrame(validation_results)
            df.to_csv('expected_value_validations.csv', index=False)
            print("Validation results saved to expected_value_validations.csv")
    else:
        print('All expected values are present in the extract file.')


def validate_patient_age(extract_file):

    
    extract_df = pd.read_csv(extract_file)
    
    validation_results = []

    for index, row in extract_df.iterrows():
        birth_year = row['PATIENT_YEAR_OF_BIRTH']
        if pd.notna(birth_year):
            try:
                birth_year = int(birth_year)
                current_year = datetime.now().year
                age = current_year - birth_year
                if age > 89:
                    validation_results.append({
                        "PATIENT_YEAR_OF_BIRTH": birth_year,
                        "Age": age,
                        "PHARMACY_TRANSACTION_ID": row['PHARMACY_TRANSACTION_ID']
                    })
            except ValueError:
                # Handle non-integer birth year values
                pass

    if validation_results:
        fail_table = PrettyTable()
        fail_table.field_names = ["PATIENT_YEAR_OF_BIRTH", "Age", "PHARMACY_TRANSACTION_ID"]
        for row in validation_results:
            fail_table.add_row([row["PATIENT_YEAR_OF_BIRTH"], row["Age"], row["PHARMACY_TRANSACTION_ID"]])

        print(fail_table)
        
        save_to_csv = input("Do you want to save the validation results to a CSV file? (yes/no): ").lower()
        if save_to_csv == "yes":
            df = pd.DataFrame(validation_results)
            df.to_csv('age_validation_failures.csv', index=False)
            print("Validation results saved to age_validation_failures.csv")
    else:
        print('All patient ages are within acceptable range.')

def validate_zip_code(extract_file):
    
    extract_df = pd.read_csv(extract_file)
    
    validation_results = []

    allowed_zip_codes = [36, 59, 102, 203, 205, 369, 556, 692, 821, 823, 878, 879, 884, 893]

    for index, row in extract_df.iterrows():
        zip_code = row['PATIENT_ZIP_CODE']
        if pd.notna(zip_code):
            try:
                zip_code = int(zip_code)
                if zip_code not in allowed_zip_codes:
                    validation_results.append({
                        "PATIENT_ZIP_CODE": zip_code,
                        "PHARMACY_TRANSACTION_ID": row['PHARMACY_TRANSACTION_ID']
                    })
            except ValueError:
                # Handle non-integer zip codes
                validation_results.append({
                    "PATIENT_ZIP_CODE": zip_code,
                    "PHARMACY_TRANSACTION_ID": row['PHARMACY_TRANSACTION_ID']
                })

    if validation_results:
        fail_table = PrettyTable()
        fail_table.field_names = ["PATIENT_ZIP_CODE", "PHARMACY_TRANSACTION_ID"]
        for row in validation_results:
            fail_table.add_row([row["PATIENT_ZIP_CODE"], row["PHARMACY_TRANSACTION_ID"]])

        print(fail_table)
        
        save_to_csv = input("Do you want to save the validation results to a CSV file? (yes/no): ").lower()
        if save_to_csv == "yes":
            df = pd.DataFrame(validation_results)
            df.to_csv('zip_code_validation_failures.csv', index=False)
            print("Validation results saved to zip_code_validation_failures.csv")
    else:
        print('All patient zip codes are within the allowed range.')

def count_field_names(config_file, extract_file):    
    config_df = pd.read_csv(config_file)
    extract_df = pd.read_csv(extract_file)
    config_count = len(config_df['Field Name'])
    extract_count = len(extract_df.columns)
    status = "Pass" if config_count == extract_count else "Fail"
    table = PrettyTable()
    table.field_names = ["Status", "Count in Config", "Count in Extract"]
    table.add_row([status, config_count, extract_count])
    print(table)

if __name__ == "__main__":
    folder_path = 'Files'
    config_file_path, extract_file_path = read_csv_files(folder_path)
    validate_required_fields(config_file_path, extract_file_path)
    column_name_match(config_file_path, extract_file_path)
    validate_expected_values(config_file_path, extract_file_path)
    validate_patient_age(extract_file_path)
    validate_zip_code(extract_file_path)
    count_field_names(config_file_path, extract_file_path)

# if __name__ == "__main__":
#     folder_path = 'Files'
#     config_file_path, extract_file_path = read_csv_files(folder_path)
    
#     while True:
#         print("\nMenu:")
#         print("1. Validate required fields")
#         print("2. Match column names")
#         print("3. Validate expected values")
#         print("4. Validate patient age")
#         print("5. Validate zip code")
#         print("6. Count field names")
#         print("7. Exit")
        
#         choice = input("\nEnter your choice (1-7): ")
        
#         if choice == '1':
#             validate_required_fields(config_file_path, extract_file_path)
#         elif choice == '2':
#             column_name_match(config_file_path, extract_file_path)
#         elif choice == '3':
#             validate_expected_values(config_file_path, extract_file_path)
#         elif choice == '4':
#             validate_patient_age(extract_file_path)
#         elif choice == '5':
#             validate_zip_code(extract_file_path)
#         elif choice == '6':
#             count_field_names(config_file_path, extract_file_path)
#         elif choice == '7':
#             print("Exiting program.")
#             break
#         else:
#             print("Invalid choice. Please enter a number from 1 to 7.")




def validate_date(value, date_format):
    try:
        if pd.notna(value):
            datetime.strptime(str(int(value)), date_format)
        return True
    except ValueError:
        return False

def validate_varchar(value, max_length):
    return len(str(value)) <= max_length

def validate_data_types_and_formats(config_file, extract_file):
    config_df = pd.read_csv(config_file)
    extract_df = pd.read_csv(extract_file)

    date_fields = config_df[(config_df['Data Type'].str.startswith('DATE')) & (config_df['Field Format'].notna())]
    varchar_fields = config_df[(config_df['Data Type'].str.startswith('VARCHAR')) & (config_df['Field Format'].isna())]

    validation_errors = []

    # Validate DATE fields
    for _, row in date_fields.iterrows():
        field_name = row['Field Name']
        date_format = row['Field Format']
        if field_name in extract_df.columns:
            for index, extract_row in extract_df.iterrows():
                if not validate_date(extract_row[field_name], date_format):
                    validation_errors.append({
                        "Field Name": field_name,
                        "Expected Format": date_format,
                        "Actual Value": extract_row[field_name],
                        "PHARMACY_TRANSACTION_ID": extract_row['PHARMACY_TRANSACTION_ID'],
                        "Error": "Invalid Date Format"
                    })

    # Validate VARCHAR fields
    for _, row in varchar_fields.iterrows():
        field_name = row['Field Name']
        max_length = int(row['Data Type'].split('(')[1].split(')')[0])
        if field_name in extract_df.columns:
            for index, extract_row in extract_df.iterrows():
                if not validate_varchar(extract_row[field_name], max_length):
                    validation_errors.append({
                        "Field Name": field_name,
                        "Expected Format": f'VARCHAR({max_length})',
                        "Actual Value": extract_row[field_name],
                        "PHARMACY_TRANSACTION_ID": extract_row['PHARMACY_TRANSACTION_ID'],
                        "Error": "Exceeds Max Length"
                    })

    # Display results
    if validation_errors:
        error_table = PrettyTable()
        error_table.field_names = ["Field Name", "Expected Format", "Actual Value", "PHARMACY_TRANSACTION_ID", "Error"]
        for error in validation_errors:
            error_table.add_row([error["Field Name"], error["Expected Format"], error["Actual Value"], error["PHARMACY_TRANSACTION_ID"], error["Error"]])
        print(error_table)

        save_to_csv = input("Do you want to save the validation results to a CSV file? (yes/no): ").lower()
        if save_to_csv == "yes":
            df = pd.DataFrame(validation_errors)
            df.to_csv('data_type_validation_results.csv', index=False)
            print("Validation results saved to data_type_validation_results.csv")
    else:
        print('All data types and formats are correct in the extract file.')
