function test_privilege_createMemberTable() {
    module("Test privilege createMemberTable");
    const target_area = '#pp_org_member';


    fn_privilege_createMemberTable_no_member_data = function() {
        // const target_area = '#pp_org_members';
        equal($(target_area).size(), 1);
        equal($(target_area + ' p:first').text(), 'Please select an organization to assign privileges');

        ESA.privilege.getOrganizationSuccessFn();

        equal($(target_area).size(), 1);
        notEqual($(target_area + ' p:first').text(), 'Please select an organization to assign privileges');
        equal($(target_area + ' p:first').text(), 'Response did not contain any member');

    };

    fn_privilege_createMemberTable_fake_member_data = function() {
        fake_members = {"Members":[
            {"emp_entityfk":3,"firstname":"Chris","lastname":"Workman"},
            {"emp_entityfk":4,"firstname":"Ryoji","lastname":"Betchaku"}
        ]};
        // const target_area = '#pp_org_members';
        equal($(target_area).size(), 1);
        equal($(target_area + ' p:first').text(), 'Please select an organization to assign privileges');

        ESA.privilege.getOrganizationSuccessFn(fake_members);

        equal($(target_area).size(), 1);
        notEqual($(target_area + ' p:first').text(), 'Please select an organization to assign privileges');
        equal($(target_area + ' p:first').text(), 'Response did not contain any member');

    };

    fn_privilege_createMemberTable_real_member_data = function() {
        const member_table = '#pp_org_member_table';
        members = {"People":[
            {"emp_entityfk":3,"firstname":"Chris","lastname":"Workman"},
            {"emp_entityfk":4,"firstname":"Ryoji","lastname":"Betchaku"}
        ]};

        equal($(target_area).size(), 1);
        equal($(target_area + ' p:first').text(), 'Please select an organization to assign privileges');

        ESA.privilege.getOrganizationSuccessFn(members);

        equal($(target_area).size(), 1);
        notEqual($(target_area + ' p:first').text(), 'Please select an organization to assign privileges');

        // Table
        equal($(target_area + ' table').size(), 1);
        ok($(target_area + ' table').hasClass('table'))
        ok($(target_area + ' table').hasClass('table-striped'))
        ok($(target_area + ' table').hasClass('table-hover'))
        equal($(target_area + ' table').attr('id'), 'pp_org_member_table')
        equal($(member_table).size(), 1);

        // Table Caption
        equal($(member_table + ' caption').size(), 1);
        equal($(member_table + ' caption').text(), 'List of user')

        // Table Header
        equal($(member_table + ' thead').size(), 1);
        equal($(member_table + ' thead tr').size(), 1);
        equal($(member_table + ' thead tr td').size(), 2);
        $(member_table + ' thead tr td').each(
            function() { ok($(this).text() == 'First Name' || $(this).text() == 'Last Name');}
            );

        // Table Body
        equal($(member_table + ' tbody').size(), 1);
        equal($(member_table + ' tbody tr').size(), 2);
        // each row
        $(member_table + ' tbody tr').each(
            function() {
                ok($(this).attr('id') == 'pp_org_member_id_' + members.People[0].emp_entityfk ||
                    $(this).attr('id') == 'pp_org_member_id_' + members.People[1].emp_entityfk);

                ok($(this).has('td'))
                equal($(this).find('td').size(), 2);

                // each data cell
                $(this).find('td').each(
                    function() {
                        ok($(this).text() == members.People[0].firstname ||
                           $(this).text() == members.People[0].lastname ||
                           $(this).text() == members.People[1].firstname ||
                           $(this).text() == members.People[1].lastname);
                    }
                ); // end of data cell
            }
        ); // end of table body
    };

    // asynchronous test test function
    test("No member data", fn_privilege_createMemberTable_no_member_data);
    test("Fake member data", fn_privilege_createMemberTable_fake_member_data);
    test("Real member table", fn_privilege_createMemberTable_real_member_data);

};

function test_ESA_privilege() {
    test_privilege_createMemberTable();
    
}