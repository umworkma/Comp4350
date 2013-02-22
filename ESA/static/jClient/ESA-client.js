// display an alert box
function display_alert(alertType, htmlMsg) {
    type = 'alert alert-' + alertType;
    msg = '';

    switch (alertType) {
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

};

// create json object and send it to server
function createJsonObject() {
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
                display_alert('success', data.result);

            } else {
                display_alert('block', data.result);

            }
        }
    },

    // ajax post request
    $.post($SCRIPT_ROOT + '/_submit_org_form', JSON.stringify(data), success, "json");

    return false;

}