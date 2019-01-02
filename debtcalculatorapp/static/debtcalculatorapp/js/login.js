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

class User {
    constructor(data) {
        this.id = data.id;
        this.username = data.username;
        this.email = data.email;
        this.password1 = data.password1;
        this.password2 = data.password2;
        this.base_currency = data.base_currency;
        this.members = data.members;

        this.fields = [
            'id', 'username', 'email', 'password1',
            'password2', 'base_currency', 'members'
        ];
        this.errors = {};
        this.clean();
    }

    /**
     * Return an object with format:
     *      field1: ['error 1', 'error 2', ... ],
     *      field2: ['error 1', 'error 2', ... ],
     *      ...
     * @param field
     * @param errorMessage
     */
    addError(field, errorMessage) {
        if (this.errors[field] === undefined)
            this.errors[field] = [errorMessage];
        else
            this.errors[field].push(errorMessage);
    }

    /**
     * Whether the object data is valid
     * @returns {boolean}
     */
    isValid() {
        return isEmpty(this.errors);
    }

    clean() {
        const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{4,20}$/;
        const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

        // validate username
        if (this.username === '')
            this.addError('name', 'Name cannot be empty');

        // validate email
        if (!this.email.match(emailRegex))
            this.addError('email', 'Invalid email')

        // validate password
        if (this.password1 !== this.password2)
            this.addError('password2', 'Passwords do not match');
        if (!this.password1.match(passwordRegex))
            this.addError('password1', 'Password must be between 4 and 20 characters and must contains lowercase, uppercase and digit');

        // validate members
        for (let i = 0; i < this.members.length; i++) {
            if (this.members[i] === '') {
                this.addError('members', 'Member ' + i + ' \'s name can not be empty');
            }
        }
        if (hasDuplicate(this.members))
            this.addError('members', 'Duplicate member names')
    }

    getSubmitData() {
        let object = {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        };
        for (let i = 0; i < this.fields.length; i++)
            object[this.fields[i]] = this[this.fields[i]];
        return object;
    }
}

function getNewUserData() {
    let members = [];
    $('.member_list_row').each(function (i) {
        members.push($(this).find('input').val().trim());
    });
    return {
        username: $('#new_profile_username').val(),
        email: $('#new_profile_email').val(),
        password1: $('#new_profile_password1').val(),
        password2: $('#new_profile_password2').val(),
        base_currency: $('#new_profile_base_currency').val(),
        members: members
    }
}

function registerSucceed() {
    window.location.href = getUrlParameter('next', '/')
}

function registerFail(res, status, error) {
    alert(status + error + JSON.stringify(res));
}

function submitRegisterForm() {
    let user = new User(getNewUserData());

    if (user.isValid()) {
        $.ajax({
            url: '/register/',
            type: 'POST',
            dataType: 'json',
            data: user.getSubmitData(),
            success: registerSucceed,
            error: registerFail
        });
    } else {
        alert(JSON.stringify(user.errors))
    }

}
