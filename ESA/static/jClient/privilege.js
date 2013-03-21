function PrivilegePortal() {
    this.org_id;

    // Active Accordion for member privilege 
    this.activeAccordion = function() {
        $( "#pp_accordion" ).accordion({
            collapsible: true,
            heightStyle: "content"

        });
    };

    // take response data and draw accordion of members and member's permission in DOM
    this.getOrganizationSuccessFn = function(response) {
        target_area = $('#pp_org_member');
        target_area.empty();

        // incoming data object
        if( typeof response != 'undefined' && typeof response.People != 'undefined' &&
            typeof response.Organization != 'undefined') {
            ESA.privilege.org_id = response.Organization.org_entityfk;

            member_div = $('<div>');
            member_div.attr('id', 'pp_accordion');

            for(i = 0; i < response.People.length; i++) {
                member_div_row = $('<h3>');
                member_div_row.attr('id', 'pp_org_member_' + response.People[i].emp_entityfk);
                member_div_row.text( response.People[i].firstname + ' ' + response.People[i].lastname);

                member_div_row_div = $('<div>');
                member_div_row_div.attr('id', 'pp_org_member_privilege_' + response.People[i].emp_entityfk);
                member_div_row_div.text('This user has no privilege.');

                member_div.append(member_div_row);
                member_div.append(member_div_row_div);

                // get this user permissions
                ESA.privilege.getMemberPrivilege(response.People[i].emp_entityfk);

            }

            target_area.append(member_div);
            // activate accordion
            ESA.privilege.activeAccordion();

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

        ESA.ajaxGetJSON(url, data, success);

    };

    // click event handler when organization been select in Privilege Portal, 
    // then use getOrganization to send ajax to server for a list of member in org.
    this.chooseOrganization = function(link) {
        pp_org_header = /pp_org_id_/;
        org_id = $(link).attr('id');

        if(org_id == 'undefined') {
            console.debug("PrivilegePortal: link did not contain id attr!");

        } else {
            org_id = org_id.replace(pp_org_header, "");
            this.getOrganization(org_id);

        };
    };// end of chooseOrganization


    //
    // Show Member Privilege 
    // 
    // take response data and draw table of member's permission in DOM
    this.getMemberPrivilegeSuccessFn = function(response) {
        console.debug(response);

        // incoming data object
        if( typeof response != 'undefined' && typeof response.PersonPrivileges != 'undefined' && 
            typeof response.emp_entityfk != 'undefined' && 
            typeof response.org_entityfk != 'undefined') {
            target_area = $('#pp_org_member_privilege_' + response.emp_entityfk);
            target_area.empty();

            // table
            member_privilege_table = $('<table>').addClass('table table-striped table-hover');
            member_privilege_table.attr('id', 'pp_member_privilege_table_' + response.emp_entityfk);

            // table caption
            member_privilege_caption = $('<caption>');
            member_privilege_caption.text('Available Permission');
            member_privilege_table.append(member_privilege_caption);

            // table header
            member_privilege_head = $('<thead>');
            member_privilege_head_row = $('<tr>');
            member_privilege_head_row.html('<td>Permission</td><td></td>')
            member_privilege_head.append(member_privilege_head_row);
            member_privilege_table.append(member_privilege_head);

            for(i = 0; i < response.PersonPrivileges.length; i++) {
                member_privilege_table_body_row = $('<tr>');

                member_privilege_table_body_row_cell_privilege = $('<td>');
                member_privilege_table_body_row_cell_privilege.text(response.PersonPrivileges[i].privilege);
                member_privilege_table_body_row.append(member_privilege_table_body_row_cell_privilege);

                member_privilege_table_body_row_cell_delete = $('<td>');
                member_privilege_table_body_row_cell_delete_button = $('<button>');
                member_privilege_table_body_row_cell_delete_button.attr('class', 'btn btn-danger disabled');
                member_privilege_table_body_row_cell_delete_button.text('remove');
                member_privilege_table_body_row_cell_delete.append(member_privilege_table_body_row_cell_delete_button);
                member_privilege_table_body_row.append(member_privilege_table_body_row_cell_delete);

                member_privilege_table.append(member_privilege_table_body_row);

            }

            target_area.append(member_privilege_table);
            // activate accordion
            ESA.privilege.activeAccordion();


        } else {
            console.debug("Response did not contain any member");

        }
    };


    // ajax GET caller, send person id to server when success call 
    this.getMemberPrivilege = function(id) {
        if(this.org_id != 'undefined') {
            url = '/privilege/'+this.org_id+'/'+id;
            // data = {'person_id': id};
            data={};
            success = this.getMemberPrivilegeSuccessFn;

            ESA.ajaxGetJSON(url, data, success);
            // $('#pp_org_member_id_4').popover('show');

        } else {
            console.debug("PrivilegePortal: organization id has not been defined!");

        }
    };
}; // end of PrivilegePortal