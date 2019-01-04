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
    let allLabel = $('#select_all_debtors').toggleClass('selected');
    let selected = allLabel.hasClass('selected');
    let labels = $('#new-payment .debtor-label');
    if (selected)
        labels.addClass('selected');
    else
        labels.removeClass('selected');
    let count = labels.length - 1;
    deselectAll.count = selected ? count : 0;
    deselectAll.countMax = count;
}

function deselectAll(obj) {
    if (deselectAll.countMax === undefined) {
        deselectAll.count = 0;
        deselectAll.countMax = $('#new-payment .debtor-label').length - 1;
    }
    let label = $(obj);
    label.toggleClass('selected');
    if (label.hasClass('selected'))
        deselectAll.count++;
    else
        deselectAll.count--;
    if (deselectAll.count === deselectAll.countMax)
        $('#select_all_debtors').addClass('selected');
    else
        $('#select_all_debtors').removeClass('selected');
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
        this.exchange_fees = data.exchange_fees;

        this.fields = [
            'id', 'date_time', 'content', 'lender',
            'debtors', 'total', 'currency', 'exchange_fees'
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

        // validate exchange_fees
        let exchange_fee = evalArithmetic(this.exchange_fees);
        if (isNaN(exchange_fee))
            this.addError('exchange_fees', 'Invalid arithmetic expression');
        else
            this.exchange_fees = exchange_fee;

        // validate currency
        if (this.currency === null)
            this.addError('currency', 'A currency must be selected');
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

function clearNewPaymentFields() {
    $('#payment_date').val('');
    $('#payment_content').val('');
    $('#payment_lender').val('');
    $('#new-payment .debtor-label').removeClass('selected');
    deselectAll.count = 0;
    $('#payment_total').val('');
    $('#payment_currency').val('');
    $('#payment_exchange_fees').val('');
}

function addNewPaymentSucceed() {
    location.reload();
}

function addNewPaymentFail(res, status, error) {
    alert(status + error + JSON.stringify(res));
}

function getNewPaymentData() {
    let debtors = [];
    $('.debtor-label.selected').children().each(function () {
        debtors.push(this.value.trim())
    });
    return {
        date_time: $('#payment_date').val().replace('T', ' '),
        content: $('#payment_content').val().trim(),
        lender: $('#payment_lender').val(),
        total: $('#payment_total').val().trim(),
        currency: $('#payment_currency').val(),
        exchange_fees: $('#payment_exchange_fees').val().trim(),
        debtors: debtors
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
