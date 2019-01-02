// ------------------- CLOCK --------------------

/**
 * Make the clock in homepage click
 */
function startTime() {
    let now = new Date();

    let year = now.getFullYear();
    let month = (now.getMonth() + 1).fillZero();
    let day = now.getDate().fillZero();
    let dayInWeek = daysInWeekNamesS[now.getDay()];
    let hour = now.getHours().fillZero();
    let minute = now.getMinutes().fillZero();
    let second = now.getSeconds().fillZero();

    $("#clock").html(
        "<div>" + dayInWeek + " " + day + "/" + month + "/" + year + "</div>" +
        "<div>" + hour + ":" + minute + ":" + second + "</div>"
    );

    setTimeout(startTime, 1000)
}

function setNewPaymentDatetimeNow() {
    let d = new Date();
    let datetime = [d.getFullYear(), (d.getMonth() + 1).fillZero(), d.getDate().fillZero()].join('-')
        + ' ' + [d.getHours().fillZero(), d.getMinutes().fillZero()].join(':');

    // Fire fox
    let datetimeField = $('#payment_date');
    datetimeField.val(datetime);

    // Other browsers
    if (datetimeField.val() !== datetime)
        datetimeField.val(datetime.replace(' ', 'T'))
}

function selectAll() {
    let checked = $('#select_all_debtors').prop('checked');
    let count = $('[name="payment_debtor"]').prop('checked', checked).length;
    deselectAll.count = checked ? count : 0;
    deselectAll.countMax = count;
}

function deselectAll(checkbox) {
    if (deselectAll.countMax === undefined) {
        deselectAll.count = 0;
        deselectAll.countMax = $('[name="payment_debtor"]').length;
    }
    if (checkbox.checked)
        deselectAll.count++;
    else
        deselectAll.count--;
    $('#select_all_debtors').prop('checked', deselectAll.count === deselectAll.countMax);
}

class Payment {
    constructor(data) {
        this.id = data.id;
        this.date_time = data.date_time;
        this.content = data.content;
        this.lender = data.lender;
        this.debtors = data.debtors;
        this.total = data.total;
        this.currency = data.currency;
        this.exchange_fee = data.exchange_fee;

        this.fields = [
            'id', 'date_time', 'content', 'lender',
            'debtors', 'total', 'currency', 'exchange_fee'
        ];
        this.errors = {};
        this.clean()
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
        // validate date time
        if (isNaN(Date.parse(this.date_time)))
            this.addError('date_time', 'Invalid date time');

        // validate content
        if (this.content === '')
            this.addError('content', 'Content cannot be empty');

        // validate lender
        if (this.lender === null)
            this.addError('lender', 'Lender must be selected');

        // validate debtors
        if (this.debtors.length === 0)
            this.addError('debtors', 'Atleast one debtor must be selected');

        // validate total
        let total = evalArithmetic(this.total);
        if (isNaN(total))
            this.addError('total', 'Invalid arithmetic expression');
        else
            this.total = total;

        // validate exchange_fee
        let exchange_fee = evalArithmetic(this.exchange_fee);
        if (isNaN(exchange_fee))
            this.addError('exchange_fee', 'Invalid arithmetic expression');
        else
            this.exchange_fee = exchange_fee;

        // validate currency
        if (this.currency === null)
            this.addError('currency', 'A currency must be selected');
    }

    getSubmitData() {
        let object = {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        };
        for (let field in this.fields)
            object[field] = this[field];
        return object;
    }
}

function clearNewPaymentFields() {
    $('#payment_date').val('');
    $('#payment_content').val('');
    $('#payment_lender').val('');
    $('#select_all_debtors').prop('checked', false);
    $('[name="payment_debtor"]').prop('checked', false);
    deselectAll.count = 0;
    $('#payment_total').val('');
    $('#payment_currency').val('');
    $('#payment_exchange_fee').val('');
}

function addNewPaymentSucceed() {
    location.reload();
}

function addNewPaymentFail(res, status, error) {
    alert(res);
    alert(status);
    alert(error);
}

function getNewPaymentData() {
    let members = [];
    $('[name="payment_debtor"]:checked').each(function () {
            members.push(this.value.trim())
    });
    return {
        date_time: $('#payment_date').val(),
        content: $('#payment_content').val().trim(),
        lender: $('#payment_lender').val(),
        total: $('#payment_total').val().trim(),
        currency: $('#payment_currency').val(),
        exchange_fee: $('#payment_exchange_fee').val().trim(),
        members: members
    }
}

function submitNewPaymentForm() {
    let payment = new Payment(getNewPaymentData());

    if (payment.isValid()) {
        $.ajax({
            url: '/add/',
            type: 'POST',
            dataType: 'json',
            data: payment.getSubmitData(),
            success: addNewPaymentSucceed,
            error: addNewPaymentFail
        });
    } else {
        alert(JSON.stringify(payment.errors))
    }
}
