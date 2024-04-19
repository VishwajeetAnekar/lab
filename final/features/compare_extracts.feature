Feature: Compare Extracts Validation

  Scenario Outline: Validate Column Count
    Given I have the CSV file "<csv_file>"
    And I have another CSV file "<csv_file2>"
    When I perform a comparison of the CSV files
    Then the number of columns should be identical

  Examples:
    | csv_file                         | csv_file2                        |
    | D:\final\CSV files\Extracts\extract.csv | D:\final\CSV files\Extracts\extract-old.csv |

  Scenario Outline: Validate Row Count
    Given I have the CSV file "<csv_file>"
    And I have another CSV file "<csv_file2>"
    When I perform a comparison of the CSV files for rows
    Then the number of rows should be identical

  Examples:
    | csv_file                         | csv_file2                        |
    | D:\final\CSV files\Extracts\extract.csv | D:\final\CSV files\Extracts\extract-old.csv |

  Scenario Outline: Validate Column Names
    Given I have the CSV file "<csv_file>"
    And I have another CSV file "<csv_file2>"
    When I perform a comparison of the CSV files for column names
    Then the column names should match

  Examples:
    | csv_file                         | csv_file2                        |
    | D:\final\CSV files\Extracts\extract.csv | D:\final\CSV files\Extracts\extract-old.csv |

  Scenario Outline: Validate Unique Values
    Given I have the CSV file "<csv_file>"
    And I have another CSV file "<csv_file2>"
    When I compare the CSV files for unique values
    Then the number of unique values should be the same

  Examples:
    | csv_file                         | csv_file2                        |
    | D:\final\CSV files\Extracts\extract.csv | D:\final\CSV files\Extracts\extract-old.csv |