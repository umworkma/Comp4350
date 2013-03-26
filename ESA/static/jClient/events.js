function EventsPortal() {
    this.org_id;

    // Active Accordion for member privilege 
    this.activeAccordion = function(id) {
        if(typeof id == 'undefined') {
            $( "#ep_accordion" ).accordion({
                collapsible: true,
                heightStyle: "content"

            });
        } else {
            $( "#"+id ).accordion({
                collapsible: true,
                heightStyle: "content"

            });
        }
    };

    // Active Draggable Member item
    this.activeDragMember = function() {
        num_permission = $('#ep_org_table_member tbody tr').size();

        for(i=0; i<num_permission; i++) {
            permission_id = '#' + $('#ep_org_table_member tbody tr')[i].id;

            $(permission_id).draggable({
                helper: "clone",
                revert: "invalid"

            });
        }
    };

    // Active Shift Drappable for shift assignment and drop handle function
    this.activeShiftDrappable = function() {
        $('#ep_org_events div#ep_accordion').children().each(function(){
            if (/ep_org_events_detail_\d{0,9}/.test(this.id)) {
                $(this).children().each(function() {

                    if (/ep_accordion_\d{0,9}/.test(this.id)) {
                        $(this).children().each(function() {

                            $(this).droppable({
                                drop: function(event, ui) {
                                    if(/ep_org_events_detail_\d{0,9}_shift_\d{0,9}/.test(this.id)) {
                                        shift_id = this.id.replace(/ep_org_events_detail_\d{0,9}_shift_/, '');
                                        event_id = this.id.replace(/ep_org_events_detail_/, '');
                                        event_id = event_id.replace(/_shift_\d{0,9}/, '');

                                    } else if(/ep_org_events_\d{0,9}_shift_\d{0,9}/.test(this.id)) {
                                        shift_id = this.id.replace(/ep_org_events_\d{0,9}_shift_/, '');
                                        event_id = this.id.replace(/ep_org_events_/, '');
                                        event_id = event_id.replace(/_shift_\d{0,9}/, '');
                                    }

                                    if(/ep_org_table_member_\d{0,9}/.test(ui.draggable.context.id))
                                        member_id = ui.draggable.context.id.replace(/ep_org_table_member_/, '');

                                    if(typeof shift_id != 'undefined' && typeof event_id != 'undefined' && typeof member_id != 'undefined') {
                                        ESA.events.assignMemberToShift(member_id, event_id, shift_id);

                                    } else {
                                        console.debug('PrivilegePortal: privilege id or member id is not found from html id');

                                    }
                                }
                            }); // if droppable
                        })
                    } // if /ep_accordion_\d/
                })
            } // if /ep_org_events_detail_\d/
        })
    };

    //
    // Get events in an Organization
    //
    // take response data and draw accordion of event and org's events in DOM
    this.getOrganizationSuccessFn = function(response) {
        target_area = $('#ep_org_events');
        target_area.empty();

        // incoming data object
        if( typeof response != 'undefined' && typeof response.Events != 'undefined' &&
            typeof response.Organization != 'undefined') {
            ESA.events.org_id = response.Organization.org_entityfk;

            org_title = $('<h3>');
            org_title.text(response.Organization.org_name);
            target_area.append(org_title);

            if(response.Events != 'None') {

                events_div = $('<div>');
                events_div.attr('id', 'ep_accordion');

                    for(i = 0; i < response.Events.length; i++) {
                        events_div_row = $('<h3>');
                        events_div_row.attr('id', 'ep_org_events_' + response.Events[i].event_pk);
                        events_div_row.text( response.Events[i].event_name + ' - ' + response.Events[i].event_desc);

                        events_div_row_div = $('<div>');
                        events_div_row_div.attr('id', 'ep_org_events_detail_' + response.Events[i].event_pk);
                        events_div_row_div.text('This event has no shifts.');

                        events_div.append(events_div_row);
                        events_div.append(events_div_row_div);

                        // get this event shift
                        ESA.events.getEventShift(response.Events[i].event_pk);

                    }
                
                target_area.append(events_div);
                ESA.events.getMemberInOrganization();
                // activate accordion
                ESA.events.activeAccordion();
            }else {
                target_area.append($('<p>').text(response.Organization.org_name + ' has no event.'));

            }
        } else {
            target_area.append('<p>Response did not contain any member</p>');
            console.debug("Response did not contain any member");

        }
    };

    // ajax GET caller, send org id to server when success call getOrganizationSuccessFn to make table
    this.getOrganization = function(id) {
        url = '/organization/'+id+'/events';
        data = {};
        success = this.getOrganizationSuccessFn;

        ESA.ajaxGetJSON(url, data, success);

    };

    // click event handler when organization been select in Privilege Portal, 
    // then use getOrganization to send ajax to server for a list of member in org.
    this.chooseOrganization = function(link) {
        ep_org_header = /ep_org_id_/;
        org_id = $(link).attr('id');

        if(org_id == 'undefined') {
            console.debug("Events: link did not contain id attr!");

        } else {
            org_id = org_id.replace(ep_org_header, "");
            this.getOrganization(org_id);

        };
    };// end of chooseOrganization


    //
    // Show Event Shift
    // 
    // take response data and draw event's shift in DOM
    this.getEventShiftSuccessFn = function(response) {

        // incoming data object
        if( typeof response != 'undefined' && typeof response.Shifts != 'undefined' && 
            typeof response.event_id != 'undefined') {
            target_area = $('#ep_org_events_detail_'+response.event_id);
            target_area.empty();

            org_title = $('<h3>');
            org_title.text('Shifts');
            target_area.append(org_title);

            events_div = $('<div>');
            events_div.attr('id', 'ep_accordion_'+response.event_id);

            for(i = 0; i < response.Shifts.length; i++) {
                events_div_row = $('<h3>');
                events_div_row.attr('id', 'ep_org_events_'+ response.event_id + '_shift_' + response.Shifts[i].shift_pk);
                events_div_row.text(response.Shifts[i].shift_start + ' - ' + response.Shifts[i].shift_end);

                events_div_row_div = $('<div>');
                events_div_row_div.attr('id', 'ep_org_events_detail_'+ response.event_id + '_shift_' + response.Shifts[i].shift_pk);
                events_div_row_div.text('This shift has no workers.');

                events_div.append(events_div_row);
                events_div.append(events_div_row_div);

                // get this event shift workers
                ESA.events.getEventShiftWorker(response.event_id, response.Shifts[i].shift_pk);

            }

            target_area.append(events_div);
            // activate accordion
            ESA.events.activeAccordion(events_div.attr('id'));
            ESA.events.activeShiftDrappable();


        } else {
            console.debug("Response did not contain any event's shift data");

        }
    };


    // ajax GET caller, send person id to server when success call 
    this.getEventShift = function(id) {
        if(this.org_id != 'undefined') {
            url = '/organization/'+this.org_id+'/events/'+id+'';
            data={};
            success = this.getEventShiftSuccessFn;

            ESA.ajaxGetJSON(url, data, success);

        } else {
            console.debug("Events: organization id has not been defined!");

        }
    };

    //
    // Get member in an Organization
    //
    // take response data and draw accordion of members and member's privilege in DOM
    this.getMemberInOrganizationSuccessFn = function(response) {
        target_area = $('#ep_org_member_list');
        target_area.empty();

        // incoming data object
        if( typeof response != 'undefined' && typeof response.People != 'undefined' &&
            typeof response.Organization != 'undefined') {
            // table
            org_member_table = $('<table>').addClass('table table-striped table-hover');
            org_member_table.attr('id', 'ep_org_table_member');

            // table caption
            org_member_caption = $('<caption>');
            org_member_caption.text('Available Members');
            org_member_table.append(org_member_caption);

            // table header
            org_member_head = $('<thead>');
            org_member_head_row = $('<tr>');
            org_member_head_row.html('<td>Name</td>')
            org_member_head.append(org_member_head_row);
            org_member_table.append(org_member_head);

            org_member_table_body = $('<tbody>');

            if(response.People != 'None') {
                for(i = 0; i < response.People.length; i++) {
                    org_member_table_body_row = $('<tr>');
                    org_member_table_body_row.addClass('info')
                    org_member_table_body_row.attr('id', 'ep_org_table_member_'+response.People[i].emp_entityfk)

                    org_member_table_body_row_cell = $('<td>');
                    org_member_table_body_row_cell.text(response.People[i].firstname + " "+ response.People[i].lastname);
                    org_member_table_body_row.append(org_member_table_body_row_cell);

                    org_member_table_body.append(org_member_table_body_row);

                }
            } else {
                org_member_table_body_row = $('<tr>');
                org_member_table_body_row_cell = $('<td>');
                org_member_table_body_row_cell.text('No member in organization.');
                org_member_table_body_row.append(org_member_table_body_row_cell);

                org_member_table_body.append(org_member_table_body_row);

            }

            org_member_table.append(org_member_table_body);

            target_area.append(org_member_table);
            ESA.events.activeDragMember();

        } else {
            target_area.append('<p>Response did not contain any member</p>');
            console.debug("Response did not contain any member");

        }
    };

    // ajax GET caller, send org id to server when success call getMemberInOrganization to make table
    this.getMemberInOrganization = function() {
        if(this.org_id != 'undefined') {
            url = '/organization/'+this.org_id+'/members';
            data = {};
            success = this.getMemberInOrganizationSuccessFn;

            ESA.ajaxGetJSON(url, data, success);
        } else {
            console.debug("Events: organization id has not been defined!");

        }
    };


    //
    // Show Shift worker 
    // 
    // take response data and draw table of member's privileges in DOM
    this.getEventShiftWorkerSuccessFn = function(response) {
        // incoming data object
        if( typeof response != 'undefined' && typeof response.Workers != 'undefined' && 
            typeof response.event_id != 'undefined' && typeof response.shift_id != 'undefined') {
            target_area = $('#ep_org_events_detail_' + response.event_id + '_shift_' + response.shift_id);
            target_area.empty();

            // table
            event_shift_worker_table = $('<table>').addClass('table table-striped table-hover');
            event_shift_worker_table.attr('id', 'ep_org_table_event_'+response.event_id+'_shift_' + response.shift_id);

            // table caption
            event_shift_worker_caption = $('<caption>');
            event_shift_worker_caption.text('Current Workers');
            event_shift_worker_table.append(event_shift_worker_caption);

            // table header
            event_shift_worker_head = $('<thead>');
            event_shift_worker_head_row = $('<tr>');
            event_shift_worker_head_row.html('<td>Name</td><td></td>')
            event_shift_worker_head.append(event_shift_worker_head_row);
            event_shift_worker_table.append(event_shift_worker_head);

            if(response.Workers != 'None') {
                for(i = 0; i < response.Workers.length; i++) {
                    event_shift_worker_table_body_row = $('<tr>');

                    event_shift_worker_table_body_row_cell_privilege = $('<td>');
                    event_shift_worker_table_body_row_cell_privilege.text(response.Workers[i].firstname + " "+ response.Workers[i].lastname);
                    event_shift_worker_table_body_row.append(event_shift_worker_table_body_row_cell_privilege);

                    event_shift_worker_table_body_row_cell_delete = $('<td>');
                    event_shift_worker_table_body_row_cell_delete_button = $('<button>');
                    event_shift_worker_table_body_row_cell_delete_button.attr('class', 'btn btn-danger');
                    event_shift_worker_table_body_row_cell_delete_button.attr('onclick', 'ESA.events.removeMemberFromShift('+response.Workers[i].emp_entityfk+', '+response.event_id+', '+response.shift_id+')');
                    event_shift_worker_table_body_row_cell_delete_button.text('remove');
                    event_shift_worker_table_body_row_cell_delete.append(event_shift_worker_table_body_row_cell_delete_button);
                    event_shift_worker_table_body_row.append(event_shift_worker_table_body_row_cell_delete);

                    event_shift_worker_table.append(event_shift_worker_table_body_row);
                }
            } else {
                event_shift_worker_table_body_row = $('<tr>');
                event_shift_worker_table_body_row_cell_privilege = $('<td>');
                event_shift_worker_table_body_row_cell_privilege.text('This shift has no workers.');
                event_shift_worker_table_body_row.append(event_shift_worker_table_body_row_cell_privilege);

                event_shift_worker_table.append(event_shift_worker_table_body_row);

            }

            target_area.append(event_shift_worker_table);

            ESA.events.activeShiftDrappable();



        } else {
            console.debug("Response did not contain any member");

        }
    };


    // ajax GET caller, send shift id to server when success call 
    this.getEventShiftWorker = function(event_id, shift_id) {
        if(this.org_id != 'undefined') {
            url = '/organization/'+this.org_id+'/events/'+event_id+'/shifts/'+shift_id;
            data={};
            success = this.getEventShiftWorkerSuccessFn;

            ESA.ajaxGetJSON(url, data, success);

        } else {
            console.debug("Events: organization id has not been defined!");

        }
    };


    //
    // Assign Shift to member
    //
    // set shift to member when return success from server
    this.assignMemberToShiftSuccessFn = function(response) {
        if( typeof response != 'undefined' && typeof response.success != 'undefined' &&
            response.success == 'true') {
            if(/\/organization\/\d{0,9}\/events\/\d{0,9}\/shifts\/\d{0,9}/.test(this.url)) {
                shift_id = this.url.replace(/\/organization\/\d{0,9}\/events\/\d{0,9}\/shifts\//,'');
                event_id = this.url.replace(/\/organization\/\d{0,9}\/events\//,'');
                event_id = event_id.replace(/\/shifts\/\d{0,9}/,'');

                if(typeof shift_id != 'undefined' && typeof event_id != 'undefined')
                    ESA.events.getEventShiftWorker(event_id, shift_id);

            }
        } else {
            if(typeof response.success != 'undefined' && typeof response.msg != 'undefined')
                ESA.display_alert('error', response.msg);
            else 
                ESA.display_alert('error', 'Fail to assign privilege');

        }
    };


    // ajax POST caller, send member_id, event_id, shift_id to assign shift to server
    this.assignMemberToShift = function(member_id, event_id, shift_id) {
        if(this.org_id != 'undefined') {
            url = '/organization/'+this.org_id+'/events/'+ event_id +'/shifts/' + shift_id;
            data = {'person_id': member_id};
            success = this.assignMemberToShiftSuccessFn;

            ESA.ajaxJSON(url, data, success);

        } else {
            console.debug("Events: organization id has not been defined!");

        }
    };


    //
    // remove member from shift
    //
    // remove member from shift success handler function when request return true
    this.removeMemberFromShiftSuccessFn = function(response) {
        if( typeof response != 'undefined' && typeof response.success != 'undefined' &&
            response.success == 'true') {


            if(/\/organization\/\d{0,9}\/events\/\d{0,9}\/shifts\/\d{0,9}\/\d{0,9}/.test(this.url)) {
                shift_id = this.url.replace(/\/organization\/\d{0,9}\/events\/\d{0,9}\/shifts\//,'');
                shift_id = shift_id.replace(/\/\d{0,9}/, '');
                event_id = this.url.replace(/\/organization\/\d{0,9}\/events\//,'');
                event_id = event_id.replace(/\/shifts\/\d{0,9}\/\d{0,9}/,'');

                if(typeof shift_id != 'undefined' && typeof event_id != 'undefined')
                    ESA.events.getEventShiftWorker(event_id, shift_id);

            }
        } else {
            console.debug('Fail to assign privilege');
            if(typeof response.success != 'undefined' && typeof response.msg != 'undefined')
                ESA.display_alert('error', response.msg);
            else 
                ESA.display_alert('error', 'Fail to remove privilege');

        }
    };


    // ajax POST caller, send person id, privilege id and org_id to server
    this.removeMemberFromShift = function(member_id, event_id, shift_id) {
        if(this.org_id != 'undefined') {
            url = '/organization/'+this.org_id+'/events/'+event_id+'/shifts/'+shift_id+'/'+member_id;
            data = {};
            success = this.removeMemberFromShiftSuccessFn;

            ESA.ajaxDeleteJSON(url, data, success);

        } else {
            console.debug("PrivilegePortal: organization id has not been defined!");

        }
    };

}; // end of end of EventsPortal