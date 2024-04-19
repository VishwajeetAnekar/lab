from behave import *
import compare_extracts_validation_impl as main_func

@given('I have the CSV file "{csv_file}"')
def step_given_csv_file(context, csv_file):
    context.csv_file = csv_file

@given('I have another CSV file "{csv_file2}"')
def step_given_another_csv_file(context, csv_file2):
    context.csv_file2 = csv_file2


#Column Count Validation    
@when('I perform a comparison of the CSV files')
def step_perform_comparison(context):
    context.validation_result_df, context.validation_result = main_func.column_count_validation(
        context.csv_file, context.csv_file2)
    context.validation_result_df.to_csv('Results/Compare/Column_Count.csv', index=False)
    
@then('the number of columns should be identical')
def step_verify_column_count(context):
    assert context.validation_result == "Both files have the same number of columns.", f"Error: {context.validation_result}"

#Unique Value Validation
@when('I compare the CSV files for unique values')
def step_compare_unique_values(context):
    context.validation_result_df, context.validation_result = main_func.unique_value_validation(
        context.csv_file, context.csv_file2)
    context.validation_result_df.to_csv('Results/Compare/Unique_Value.csv', index=False)

@then('the number of unique values should be the same')
def step_verify_unique_values(context):
    if context.validation_result.startswith("Success"):
        assert True, "No repeated values found in either file"
    else:
        assert False, f"Error: {context.validation_result}"

#Row Count Validation
@when(u'I perform a comparison of the CSV files for rows')
def step_impl(context):
    context.validation_result_df, context.validation_result = main_func.row_count_validation(
        context.csv_file, context.csv_file2)
    context.validation_result_df.to_csv('Results/Compare/Row_Count.csv', index=False)

@then(u'the number of rows should be identical')
def step_impl(context):
    assert context.validation_result.startswith("Both files"), f"Error: {context.validation_result}"

#Column Name Validation
@when(u'I perform a comparison of the CSV files for column names')
def step_impl(context):
    context.validation_result_df, context.validation_message = main_func.column_name_match(
        context.csv_file, context.csv_file2)
    context.validation_result_df.to_csv('Results/Compare/Column_Name.csv', index=False)

@then(u'the column names should match')
def step_impl(context):
    expected_message = "Success: Column names match"
    assert context.validation_message == expected_message, f"Expected message: {expected_message}, Actual message: {context.validation_message}"
