Feature: Login Screen

Scenario: 
    First launch app should appear on login page
    then check for empty username and password
    
Given I launch the app
Then I should be on Login Screen

When I click on login with "" and ""
Then alert box message "Input required" and "Please enter username and/or"
When I touch the alert view button marked "Ok"
