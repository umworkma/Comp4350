function EventsPortal() {
    // this.org_id;

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
            // activate accordion
            ESA.events.activeAccordion();
            // ESA.privilege.activeDragPermission();
            // ESA.privilege.activeMemberDrappable();

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
                events_div_row.text(response.Shifts[i].shift_location);

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
            // ESA.privilege.activeDragPermission();
            // ESA.privilege.activeMemberDrappable();


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
                    event_shift_worker_table_body_row_cell_delete_button.attr('class', 'btn btn-danger disabled');
                    // event_shift_worker_table_body_row_cell_delete_button.attr('onclick', 'ESA.privilege.removeMemberPrivilege('+response.emp_entityfk+', '+response.PersonPrivileges[i].privilege_pk+')');
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
            // activate accordion
            ESA.privilege.activeAccordion();


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




}; // end of EventsPortal