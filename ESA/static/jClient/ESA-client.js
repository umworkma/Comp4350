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
        			irprimary:	"True"
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
		console.log(data);
        // get a value which sent back from server
        /*alert("successfully submitted"
                +"\n ***** Your Info *****"
                +"\n user name: " + data.org_name
                +"\n description: " + data.org_desc
                +"\n password: " + data.pwd
                +"\n phone: " + data.phone
                +"\n address: " + data.address1
                +"\n city: " + data.city
                +"\n province: " + data.province
                +"\n postal: " + data.postalcode
                +"\n email: " + data.email);*/

    },

    // ajax post request
    $.post($SCRIPT_ROOT + '/_submit_org_form', JSON.stringify(data), success, "json");

    return false;

}
