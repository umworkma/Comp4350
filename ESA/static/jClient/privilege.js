function PrivilegePortal() {
    this.org_id;

    // Active Accordion for member privilege 
    this.activeAccordion = function() {
        $( "#pp_accordion" ).accordion({
            collapsible: true,
            heightStyle: "content"

        });
    };

    // Active Draggable Permission item
    this.activeDragPermission = function() {
        num_permission = $('#pp_permission_list table tbody tr').size();

        for(i=0; i<num_permission; i++) {
            permission_id = '#' + $('#pp_permission_list table tr')[i].id;

            $(permission_id).draggable({
                helper: "clone",
                revert: "invalid"

            });
        }
    };

    // Active Member Drappable for privilege assignment and drop handle function
    this.activeMemberDrappable = function() {
        $('#pp_org_member div#pp_accordion').children().each(function(){
            $(this).droppable({
                drop: function(event, ui) {

                    console.debug(this.id);
                    console.debug(ui.draggable.context.id);

                    if(/pp_org_member_privilege_\d/.test(this.id))
                        member_id = this.id.replace(/pp_org_member_privilege_/, '');

                    else if(/pp_org_member_\d/.test(this.id))
                        member_id = this.id.replace(/pp_org_member_/, '');

                    if(/pp_privilege_id_\d/.test(ui.draggable.context.id))
                        privilege_id = ui.draggable.context.id.replace(/pp_privilege_id_/, '');

                    if(typeof member_id != 'undefined' && typeof privilege_id != 'undefined') {
                        console.debug('Member: ' + member_id + '\tPrivilege id: ' + privilege_id);
                        ESA.privilege.setMemberPrivilege(member_id, privilege_id);

                    } else {
                        console.debug('PrivilegePortal: privilege id or member id is not found from html id');

                    }
                }
            });
        })
    };

    //
    // Get member in an Organization
    //
    // take response data and draw accordion of members and member's privilege in DOM
    this.getOrganizationSuccessFn = function(response) {
        target_area = $('#pp_org_member');
        target_area.empty();

        // incoming data object
        if( typeof response != 'undefined' && typeof response.People != 'undefined' &&
            typeof response.Organization != 'undefined') {
            ESA.privilege.org_id = response.Organization.org_entityfk;

            org_title = $('<h3>');
            org_title.text(response.Organization.org_name);
            target_area.append(org_title);

            member_div = $('<div>');
            member_div.attr('id', 'pp_accordion');

            for(i = 0; i < response.People.length; i++) {
                member_div_row = $('<h3>');
                member_div_row.attr('id', 'pp_org_member_' + response.People[i].emp_entityfk);
                member_div_row.text( response.People[i].firstname + ' ' + response.People[i].lastname);

                member_div_row_div = $('<div>');
                member_div_row_div.attr('id', 'pp_org_member_privilege_' + response.People[i].emp_entityfk);
                member_div_row_div.text('This user has no privileges.');

                member_div.append(member_div_row);
                member_div.append(member_div_row_div);

                // get this user privileges
                ESA.privilege.getMemberPrivilege(response.People[i].emp_entityfk);


            }

            target_area.append(member_div);
            // activate accordion
            ESA.privilege.activeAccordion();
            ESA.privilege.activeDragPermission();
            ESA.privilege.activeMemberDrappable();

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
    // take response data and draw table of member's privileges in DOM
    this.getMemberPrivilegeSuccessFn = function(response) {
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
            member_privilege_caption.text('Available Privileges');
            member_privilege_table.append(member_privilege_caption);

            // table header
            member_privilege_head = $('<thead>');
            member_privilege_head_row = $('<tr>');
            member_privilege_head_row.html('<td>Privilege List</td><td></td>')
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
            data={};
            success = this.getMemberPrivilegeSuccessFn;

            ESA.ajaxGetJSON(url, data, success);

        } else {
            console.debug("PrivilegePortal: organization id has not been defined!");

        }
    };


    //
    // Assign Privilege to member
    //
    // set member privilege success function. On server response success, will call getMemberPrivilege
    // to rebuild member privilege table else display server error.
    this.setMemberPrivilegeSuccessFn = function(response) {
        if( typeof response != 'undefined' && typeof response.success != 'undefined' &&
            response.success == 'true') {
            console.debug('Assign Privilege success');
            if(/\/privilege\/\d\/\d/.test(this.url)) {
                member_id = this.url.replace(/\/privilege\/\d\//,'');
                ESA.privilege.getMemberPrivilege(member_id);
            }


        } else {
            console.debug('Fail to assign privilege');
            if(typeof response.success != 'undefined' && typeof response.msg != 'undefined')
                ESA.display_alert('error', response.msg);
            else 
                ESA.display_alert('error', 'Fail to assign privilege');

        }
    };


    // ajax POST caller, send person id, privilege id and org_id to server
    this.setMemberPrivilege = function(person_id, privilege_id) {
        if(this.org_id != 'undefined') {
            url = '/privilege/'+this.org_id+'/'+person_id;
            data = {'privilege_id': privilege_id};
            success = this.setMemberPrivilegeSuccessFn;

            ESA.ajaxJSON(url, data, success);

        } else {
            console.debug("PrivilegePortal: organization id has not been defined!");

        }
    };

}; // end of PrivilegePortal