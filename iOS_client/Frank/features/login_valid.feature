Feature: Login Screen

Scenario: 
    First launch app should appear on login page
    then check for fixture username(user0) and password

Given I launch the app
Then I should be on Login Screen

When I click on login with "user0" and "password0"
Then alert box message "Login Success!" and "Hi Chris!"
When I touch the alert view button marked "Ok"
