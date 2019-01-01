function removeNewMember(num) {
    $('#new_profile_member_' + num).parent().remove()
}

function addNewMemberRow() {
    if (typeof addNewMemberRow.count == 'undefined')
        addNewMemberRow.count = 1;
    addNewMemberRow.count++;
    let num = addNewMemberRow.count;

    $('<div class="member_list_row">')
        .appendTo('#member_list')
        .append('<input type="text" id="new_profile_member_' + num + '" required>')
        .append('<span onclick="removeNewMember(' + num + ')">&#x2716;</span>')
}
