from behave import *
import os
import features.steps.config_extract_validation_impl as main_func

@given('a CSV file "{csv_file}"')
def step_given_csv_file(context, csv_file):
    context.data_file = csv_file
    

@when(u'I validate for whitespace')
def step_impl(context):
    context.validation_result_df, context.validation_result = main_func.white_space_validation(context.data_file)
    context.validation_result_df.to_csv(
        'Results/WhiteSpace_validation_result.csv', index=False)

@then(u'the validation should be successful')
def step_impl(context):
    if "Some values have unnecessary white space" in context.validation_result:
        assert False, "White space validation failed: Some values has unnecessary white space"
    else:
        assert True, "White space validation passed"


@when(u'I validate for duplicate keys')
def step_impl(context):
    context.validation_result_df, context.validation_result = main_func.duplicate_keys_validation(
        context.data_file)
    
    result_file_name = f'Results/duplicate_{os.path.basename(context.data_file).replace(".csv", "")}.csv'
    context.validation_result_df.to_csv(result_file_name, index=False)

@then(u'no duplicate rows or columns should be found')
def step_impl(context):
    if context.validation_result == "Success: No duplicate columns found":
        validation_result = "Success"
    else:
        validation_result = "Error"

    assert validation_result == "Success", "Validation failed"

@given('a configuration file "{config_file}"')
def step_given_config_file(context, config_file):
    context.config_file = config_file

@when('I validate the required fields')
def step_validate_required_fields(context):
    context.validation_result_df, context.validation_result = main_func.required_fields_validation(
        context.config_file, context.data_file)
    context.validation_result_df.to_csv(
        'Results/Required_fields_validation_result.csv', index=False)

@then('all required fields should have values')
def step_verify_required_fields(context):
    if "Some required fields are missing" in context.validation_result:
        assert False, "Required fields validation failed: Some required fields are missing"
    else:
        assert True, "Required fields validation passed"

@when(u'I validate the expected values')
def step_impl(context):
    context.validation_result_df, context.validation_summary = main_func.expected_value_validation(
        context.config_file, context.data_file)
    context.validation_result_df.to_csv('Results/expected_value_validation_result.csv', index=False)

@then(u'the values in each field should match the expected values as per the configuration')
def step_impl(context):
    assert context.validation_summary == "Some fields have unexpected values or are missing", "Validation failed"

@when(u'I validate the field names')
def step_impl(context):
    context.validation_result_df, context.validation_summary = main_func.field_name_validation(
        context.config_file, context.data_file)
    context.validation_result_df.to_csv('Results/field_name_validation_result.csv', index=False)

@then(u'the field names should match the configuration')
def step_impl(context):
    assert context.validation_summary == "Some column names do not match the expected field names", "Validation failed"
