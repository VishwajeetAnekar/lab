Feature: Extract Config validation

  Scenario Outline: Validate Whitespace
    Given a CSV file "<csv_file>"
    When I validate for whitespace
      Then the validation should be successful

  Examples:
    | csv_file                   | 
    | D:\final\CSV files\Extracts\extract.csv| 

  Scenario Outline: Validate Duplicate Keys
    Given a CSV file "<csv_file>"
    When I validate for duplicate keys
    Then no duplicate rows or columns should be found

  Examples:
    | csv_file                   | 
    | D:\final\CSV files\Extracts\extract.csv| 

  Scenario Outline: Validate Required Fields
    Given a configuration file "<config_file>"
    And a CSV file "<csv_file>"
    When I validate the required fields
    Then all required fields should have values

  Examples:
    | csv_file                     |config_file                                         |
    | D:\final\CSV files\Extracts\extract.csv | D:\final\CSV files\Configs\Config_SG_Status_csv.csv |
  
  Scenario Outline: Validate Expected Value
    Given a configuration file "<config_file>"
    And a CSV file "<csv_file>"
    When I validate the expected values
    Then the values in each field should match the expected values as per the configuration

  Examples:
    | csv_file                     |config_file                                         |
    | D:\final\CSV files\Extracts\extract.csv | D:\final\CSV files\Configs\Config_SG_Status_csv.csv |
  
  Scenario Outline: Validate Field Name
    Given a configuration file "<config_file>"
    And a CSV file "<csv_file>"
    When I validate the field names
    Then the field names should match the configuration

  Examples:
    | csv_file                     |config_file                                         |
    | D:\final\CSV files\Extracts\extract.csv | D:\final\CSV files\Configs\Config_SG_Status_csv.csv |

  Scenario Outline: Validate Maximum Field Length
    Given a configuration file "<config_file>"
    And a CSV file "<csv_file>"
    When I validate the maximum field length
    Then the length of each field should be within the specified limits

  Examples:
    | csv_file                     |config_file                                         |
    | D:\final\CSV files\Extracts\extract.csv | D:\final\CSV files\Configs\Config_SG_Status_csv.csv |

  #   Scenario Outline: Validate Field Format
#     Given a configuration file "<config_file>"
#     And a CSV file "<csv_file>"
#     When I validate the field format
#     Then the format of each field should be as per the configuration

#   Examples:
#     | csv_file                         | config_file                                         |
#     | D:\Full\CSV files\demo.csv | D:\final\CSV files\Configs\Config_SG_Status_csv.csv |

#   Scenario Outline: Validate Data Type
#     Given a configuration file "<config_file>"
#     And a CSV file "<csv_file>"
#     When I validate the data types
#     Then the data types of each field should be as per the configuration

#   Examples:
#     | csv_file                         | config_file                                         |
#     | D:\Full\CSV files\demo.csv | D:\final\CSV files\Configs\Config_SG_Status_csv.csv |

