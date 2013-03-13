Then(/^I should be on Login Screen$/) do
    check_element_exists "view view:'UILabel' marked:'Welcome to ESA Service'"

    check_element_exists "view view:'UILabel' marked:'Username'"
    check_element_exists "view view:'UITextField' marked:'acc_username'"
    check_element_exists "view view:'UITextFieldLabel' marked:'username'"

    check_element_exists "view view:'UILabel' marked:'Password'"
    check_element_exists "view view:'UITextField' marked:'acc_password'"
    check_element_exists "view view:'UITextFieldLabel' marked:'password'"

    check_element_exists "view view:'UIRoundedRectButton' marked:'Login'"
    check_element_exists "view view:'UIButtonLabel' marked:'Login'"

    check_element_exists "view view:'UILabel' marked:'Need an account?'"
    check_element_exists "view view:'UIRoundedRectButton' marked:'Signup'"
    check_element_exists "view view:'UIButtonLabel' marked:'Signup'"

end


When(/^I click on login with "(.*?)" and "(.*?)"$/) do |username, password|
    text_field_username = "view:'UITextField' marked:'acc_username'"
    text_field_password = "view:'UITextField' marked:'acc_password'"

    check_element_exists text_field_username
    touch text_field_username
    frankly_map( text_field_username, 'setText:', username)
    frankly_map( text_field_username, 'endEditing:', true)

    check_element_exists text_field_password
    touch text_field_password
    frankly_map( text_field_password, 'setText:', password)
    frankly_map( text_field_password, 'endEditing:', true)

    touch "view:'UIRoundedRectButton' marked:'Login'"

end


Then(/^alert box message "(.*?)" and "(.*?)"$/) do |title, message|
    # check_element_exists( "alertView view marked:'#{message}'" )

    check_element_exists "view view:'UILabel' marked:'#{title}'"
    check_element_exists "view view:'UILabel' marked:'#{message}'"

end

When(/^I touch the alert view button marked "(.*?)"$/) do |mark|
    touch( "alertView button marked:'#{mark}'" )
    # touch "view:'UIAlertButton' marked:'ok'"
    # touch "button marked:'ok'"
    # alertView button marked:'ok'
    # touch "alertView button marked:'Ok'"
    
end
