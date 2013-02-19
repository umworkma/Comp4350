// Javascript unit testing for ESA-Client.js

// Note: This unit testing code is only an example code.
function test_createJsonObject() {
    // Grouping create JSON unit test
    module("Create JSON Object test module");

    // create input box
    create_DOM_input = function(field_name, type, value) {
        // get qunit-fixture div box for insert
        div = document.getElementById("qunit-fixture");

        // create the input text box
        input=document.createElement("INPUT");
        
        // adding attributes to input element
        input.name = field_name;
        input.type = type;
        input.value = value;

        // adding input to div box
        div.appendChild(input);

    };
    

    // create textarea box
    create_DOM_textarea = function (field_name, rows, value) {
        // get qunit-fixture div box for insert
        div = document.getElementById("qunit-fixture");

        // create the textarea text box
        textarea=document.createElement("textarea");
        text=document.createTextNode(value);

        // adding attributes to textarea element
        textarea.appendChild(text);
        textarea.id = field_name;
        textarea.name = field_name;
        textarea.rows = rows;

        // adding textarea to div box
        div.appendChild(textarea);

    };


    // Unit testing
    // basic unit testing assertion methods
    fn_createJsonObject_return = function() {
        ok(!createJsonObject());
        equal(createJsonObject(), false);
        notEqual(createJsonObject(), true);

    };


    // asynchronous unit testing assertion methods
    fn_ajaxAssert = function() {
        expect(1) //expect(4) // number of assertions to be expect
        setTimeout(function() {
            equal(createJsonObject(), false);
            // fn_createJsonObject_return();
            start();

        }, 1000);
    };


    // create HTML objects then call asynchronous test function
    test_createJsonObject_DOM = function(orgName, desc, pwd, phone, address, city, province, postal, email) {
        // Creating DOM objects
        create_DOM_input("orgname", "text", orgName);
        create_DOM_textarea("desc", 3, desc);
        create_DOM_input("pwd", "password", pwd);
        create_DOM_input("phone", "text", phone);
        create_DOM_input("address", "text", address);
        create_DOM_input("city", "password", city);
        create_DOM_input("province", "text", province);
        create_DOM_input("postal", "text", postal);
        create_DOM_input("email", "text", email);

        // asynchronous test test function
        asyncTest("Asynchronous Test", fn_ajaxAssert)
        
    };

    // Basic unit testing function call
    // test("Test createJsonObject return", fn_createJsonObject_return);
    
    // Asynchronous unit testing call with DOM object creation. 
    test_createJsonObject_DOM("Group 1", "SE2 Group 1", "password", "012-345-6789", "123 Neat Street", "Coolsville", "Manitoba", "Q1W 2E3", "awesomeco@awesomeco.ca");

};


window.onload = function() {
    test_createJsonObject();

};


