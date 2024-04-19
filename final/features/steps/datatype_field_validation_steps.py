from behave import *
import datatype_field_validation_impl as main_func


@when(u'I validate the maximum field length')
def step_impl(context):
    context.validation_result, context.validation_result_df = main_func.maximum_length_validation(
        context.config_file, context.data_file)
    context.validation_result_df.to_csv('Results/maximum_length_validation_result.csv', index=False)

@then(u'the length of each field should be within the specified limits')
def step_impl(context):
    assert context.validation_result == "Some values failed maximum length and data type validation", "Validation failed"