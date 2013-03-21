

function ESA() {
    // POST ajax call to send json object to server
    this.ajaxJSON = function(url, data, success) {
        $.ajax({
            type: 'POST',
            url: url,
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            success: success,

        });
    }
	
    // display an alert box
    this.display_alert = function (type, htmlMsg) {
		if(htmlMsg == "EmpTrue")
		{
			$("#employee-reg-response").empty();
			$("#employee-reg-response").append("<p>Successfully Registered !!</p>");
			$("#employee-reg-response").append("<p>Click <b><a href='/'>here</a></b> to continue.</p>");
		}
		else
		{
			type = 'alert alert-' + type;
			msg = '';
			switch (type) {
				case 'block':
					msg = '<strong>Warning:</strong>';
					break;
				case 'error':
					msg = '<strong>Error:</strong>';
					break;
				case 'success':
					msg = '<strong>Success:</strong>';
					break;
				case 'info':
					msg = '<strong>Note:</strong>';
					break;
				default:
					type = 'alert alert-block';
					msg = '<strong>Warning!</strong>';

			}
			msg +=  htmlMsg;

			// alert-block, alert-error, alert-success, alert-info
			// are the 4 difference type of alert block.
			alert = $('<div>');
			alert.attr('class', type);

			// Adding the close button to close the alert box
			button = $('<button>', {
				'type':'button',
				'class': 'close',
				'data-dismiss': 'alert',
				text: '&times;'
			});
			// display the &times; html extended characters
			button.html(button.text());

			// adding close button and message to alert box
			alert.append(button);
			alert.append(msg);

			// adding the alert box into the message area
			$('.msg_area').append(alert);
			
			// set timeout to dismiss alert message
			window.setTimeout(function() {
				alert.alert('close')
			}, 2000);
		}
    };

};
// Active the singleton of ESA in Global object
ESA = new ESA();


// Check for valid organization name as the user types.
function checkForDuplicateEmployeeUserName() {
    url = '/_check_dup_employee_user_name'
	userName = $('input[name="username"]').val(),
	data = { 'username': userName },
	success = function(data) {
		if(typeof data.result != 'undefined' ) {
			if(data.result == 'True') {
				updateIsValidEmployeeUserNameMsg(true);
			} else {
				updateIsValidEmployeeUserNameMsg(false);
			}
		}
    },
	ESA.ajaxJSON(url, data, success);
    return false;
}

// Check for valid organization name as the user types.
function checkForDuplicateOrgName() {
	url = '/_check_dup_org_name',
    orgName = $('input[name="org_name"]').val(),
	data = { 'org_name': orgName },
	success = function(data) {
		if(typeof data.result != 'undefined' ) {
			if(data.result == 'True') {
				updateIsValidOrgNameMsg(true);
			} else {
				updateIsValidOrgNameMsg(false);
			}
		}
    },


    ESA.ajaxJSON(url, data, success);
    return false;
}


// Display an alert if the organization name is a duplicate.
function updateIsValidEmployeeUserNameMsg(isActive) {
    type = 'alert alert-error';
    msg = 'This user name already exists. Please choose a different name.';
    alert = $('<div>');
    alert.attr('class', type);

    // Adding the close button to close the alert box
    button = $('<button>', {
        'type':'button',
        'class': 'close',
        'data-dismiss': 'alert',
        text: '&times;'
    });
    // display the &times; html extended characters
    button.html(button.text());

    // adding close button and message to alert box
    alert.append(button);
    alert.append(msg);

    // adding the alert box into the message area
    if(isActive){
        $('.alert_isValidEmployeeUserName').append(alert);
    } else {
        $('.alert_isValidEmployeeUserName').children().remove()
		//alert.alert('close');
		//$('.alert_isValidOrgName').innerHTML = '';
	}
};


// Display an alert if the organization name is a duplicate.
function updateIsValidOrgNameMsg(isActive) {
    type = 'alert alert-error';
    msg = 'This name already exists. Please choose a different name.';
    alert = $('<div>');
    alert.attr('class', type);

    // Adding the close button to close the alert box
    button = $('<button>', {
        'type':'button',
        'class': 'close',
        'data-dismiss': 'alert',
        text: '&times;'
    });
    // display the &times; html extended characters
    button.html(button.text());

    // adding close button and message to alert box
    alert.append(button);
    alert.append(msg);

    // adding the alert box into the message area
    if(isActive){
    	$('.alert_isValidOrgName').append(alert);
	} else {
		$('.alert_isValidOrgName').children().remove()
		//alert.alert('close');
		//$('.alert_isValidOrgName').innerHTML = '';
	}
};

// create json object and send it to server
function createJsonObjectForOrganization() {
    url = '/_submit_org_form',

    data = {
        org_name: $('input[name="org_name"]').val(),
        org_desc: $('#org_desc').val(),
        Entity:   {
        	entity_type: 1,
        	addresses: [
        		{
					address1: 	$('input[name="address1"]').val(),
        			address2: 	$('input[name="address2"]').val(),
        			address3: 	$('input[name="address3"]').val(),
        			city:     	$('input[name="city"]').val(),
        			province: 	$('input[name="province"]').val(),
        			country:	$('input[name="country"]').val(),
        			postalcode:	$('input[name="postalcode"]').val(),
        			isprimary:	"True"
				}
			],
			contacts: [
				{
					type: 		1,
        			value:    	$('input[name="phone"]').val(),
        			isprimary:	"True"
				},
				{
					type:		2,
					value:		$('input[name="email"]').val(),
					isprimary:	"False"
				}
			]
		}
    },


    success = function(data) {
        // check for server return data.result
        if(typeof data.result != 'undefined' ) {
            // display the 2 type of alert box base of the result
            if(data.result == 'True') {
                ESA.display_alert('success', data.result);

            } else {
                ESA.display_alert('block', data.result);

            }
        }
    },

    ESA.ajaxJSON(url, data, success);

    return false;

}

// create json object and send it to server
function createJsonObjectForEmployee() {

	url = '/_submit_employee_form',
    data = {
		username: $('input[name="username"]').val(),
		password: $('input[name="pwd1"]').val(),
        firstname: $('input[name="firstname"]').val(),
        lastname: $('input[name="lastname"]').val(),
        Entity:   {
        	entity_type: 1,
        	addresses: [
        		{
					address1: 	$('input[name="address1"]').val(),
        			address2: 	$('input[name="address2"]').val(),
        			address3: 	$('input[name="address3"]').val(),
        			city:     	$('input[name="city"]').val(),
        			province: 	$('input[name="province"]').val(),
        			country:	$('input[name="country"]').val(),
        			postalcode:	$('input[name="postalcode"]').val(),
        			isprimary:	"True"
				}
			],
			contacts: [
				{
					type: 		1,
        			value:    	$('input[name="phone"]').val(),
        			isprimary:	"True"
				},
				{
					type:		2,
					value:		$('input[name="email"]').val(),
					isprimary:	"False"
				}
			]
		}
    },
    
    success = function(data) {
        // check for server return data.result
        if(typeof data.result != 'undefined' ) {
            // display the 2 type of alert box base of the result
            if(data.result == 'EmpTrue') {
                ESA.display_alert('success', data.result);

            } else {
                ESA.display_alert('block', data.result);

            }
        }
    },

    // ajax post request
	ESA.ajaxJSON(url, data, success);

    return false;

}

function eventOnSubmit() {

    url = '/organization/'+ org_id + '/events',
    data = {
        name: $('input[name="event_name"]').val(),
        description: $('input[name="event_desc"]').val(),
        startdate: $('input[name="event_start"]').val(),
        enddate: $('input[name="event_end"]').val(),
        organizationFK: org_id
    },
    
    success = function(data) {
        // check for server return data.result
        if(typeof data.result != 'undefined' ) {
            // display the 2 type of alert box base of the result
            if(data.result == 'EmpTrue') {
                ESA.display_alert('success', data.result);

            } else {
                ESA.display_alert('block', data.result);

            }
        }
    },

    // ajax post request
    ESA.ajaxJSON(url, data, success);

    return false;

}

function join_org(button, org_id) {
    url = '/_member',

    data = {
        org_id: org_id
    },

    //what needs to happen client-side on success (response)
    success = function(data) {
        // check for server return data.result
        if(typeof data.result != 'undefined' ) {
            // display the 2 type of alert box base of the result
            if(data.result == 'True') {
                ESA.display_alert('success', data.result);
                setTimeout(function() { $(button).button('complete'); }, 500);
                setTimeout(function() { $(button).attr('disabled', 'disabled').addClass('disabled'); }, 1000);
            } else {
                ESA.display_alert('block', data.result);
                $(button).button('reset')
            }
        }
    },

    //disable button
    $(button).button('loading')

    ESA.ajaxJSON(url, data, success);

    return false;
}   




// active carousel when DOM is fully loaded
$(document).ready(function() {
    $('.carousel').carousel({  interval: 3000
    });
});
