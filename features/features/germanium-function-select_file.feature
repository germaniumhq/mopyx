Feature: Support uploading files in Germanium

  Scenario: Uploading a file should work.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/select_file.html'
    When I upload a file using the form from the page
    Then the file is uploaded successfully
