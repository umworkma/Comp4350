function PrivilegePortal() {
    // take response data and draw table of members in DOM
    this.getOrganizationSuccessFn = function(response) {
        target_area = $('#pp_org_member');
        target_area.empty();

        // incoming data object
        if( typeof response != 'undefined' && typeof response.People != 'undefined') {
            // table
            member_table = $('<table>').addClass('table table-striped table-hover');
            member_table.attr('id', "pp_org_member_table");

            // table caption
            member_table_caption = $('<caption>');
            member_table_caption.text('List of user');
            member_table.append(member_table_caption);

            // table header
            member_table_head = $('<thead>');
            member_table_head_row = $('<tr>');
            member_table_head_row.html('<td>First Name</td><td>Last Name</td>')
            member_table_head.append(member_table_head_row);
            member_table.append(member_table_head);

            // table body with members info
            member_table_body = $('<tbody>');
            for(i = 0; i < response.People.length; i++) {
                member_table_body_row = $('<tr>');
                member_table_body_row.attr('id', 'pp_org_member_id_'+response.People[i].emp_entityfk);

                member_table_body_row.html('<td>' + response.People[i].firstname + 
                    '</td><td>' + response.People[i].lastname + '</td>');

                member_table_body.append(member_table_body_row);
            }
            member_table.append(member_table_body);

            // append table into pp_org_member div box
            target_area.append(member_table);

        } else {
            target_area.append('<p>Response did not contain any member</p>');
            console.debug("Response did not contain any member");
        }


    };

    // ajax GET caller, send org id to server when success call getOrganizationSuccessFn to make table
    this.getOrganization = function(id) {
        url = '/privilege/'+id;
        data = {};
        success = this.getOrganizationSuccessFn;

        ESA.ajaxGetJSON(url, data, success, this);

    };

    // click event handler when organization been select in Privilege Portal, 
    // then use getOrganization to send ajax to server for a list of member in org.
    this.chooseOrganization = function(link) {
        pp_org_header = /pp_org_id_/;
        org_id = $(link).attr('id');

        if(org_id == 'undefined') {
            console.debug("PrivilegePortal: link did not contain id attr!");

        } else {
            // console.debug(org_id);
            org_id = org_id.replace(pp_org_header, "");
            // console.debug(org_id);
            this.getOrganization(org_id);

        };
    };// end of chooseOrganization

    scope = this;
}; // end of PrivilegePortal