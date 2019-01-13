function changeExchangeRateSucceed() {
    location.reload()
}

function changeExchangeRateFail(res, status, error) {
    alert(status + error + JSON.stringify(res));
}

function summarize() {
    let data = {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        note: $('#note').val().trim()
    };

    $('[id^="exchange_rate_"]').each(
        function (i) {
            if (isNaN(parseInt(this.value)))
                alert("Invalid exchange rate num " + (i + 1));
            else
                data[this.id.substring(14)] = this.value;
        }
    );

    $.ajax({
        url: '/edit_exchange_rate/',
        type: 'POST',
        dataType: 'json',
        data: data,
        success: changeExchangeRateSucceed,
        error: changeExchangeRateFail
    });
}

function selectMember(id, nameTag) {
    // highlight label
    $('.debtor-label').removeClass('selected');
    $(nameTag).addClass('selected');

    // show member summarize
    $('#no-data-note').hide();
    $('[class^="summarize-member-"]').hide();
    $('.summarize-member-' + id).show();
}
