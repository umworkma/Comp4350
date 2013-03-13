Feature: Login Screen

Scenario: 
    First launch app should appear on login page
    then check for username with invalid password

Given I launch the app
Then I should be on Login Screen

When I click on login with "user0" and "pass"
Then alert box message "Login Failed!" and "Please check user name and password"
When I touch the alert view button marked "Ok"
