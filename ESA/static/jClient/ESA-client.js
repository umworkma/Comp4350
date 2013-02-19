// create json object and send it to server
function createJsonObject() {
    data = {
        orgname:  $('input[name="orgname"]').val(),
        desc:     $('#desc').val(),
        pwd:      $('input[name="pwd"]').val(),
        phone:    $('input[name="phone"]').val(),
        address:  $('input[name="address"]').val(),
        city:     $('input[name="city"]').val(),
        province: $('input[name="province"]').val(),
        postal:   $('input[name="postal"]').val(),
        email:    $('input[name="email"]').val()
    },

    success = function(data) {
        // get a value which sent back from server
        alert("successfully submitted"
                +"\n ***** Your Info *****"
                +"\n user name: " + data.orgname
                +"\n description: " + data.desc
                +"\n password: " + data.pwd
                +"\n phone: " + data.phone
                +"\n address: " + data.address
                +"\n city: " + data.city
                +"\n province: " + data.province
                +"\n postal: " + data.postal
                +"\n email: " + data.email);

    },

    // ajax post request
    $.post($SCRIPT_ROOT + '/_submit_org_form', data, success, "json");

    return false;
    
}
