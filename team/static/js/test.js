/**
 * Created by cwh on 16-6-4.
 */
function loadValidCode(id) {
    $.ajax({
            url: "http://110.64.69.66:8081/team/valid_code",
            // url: "http://127.0.0.1:8000/team/valid_code",
            processData: false,
            xhrFields: {withCredentials: true}
        }).always(function (data) {
                console.log('test');
                $(id).attr('src', "data:image/gif;base64," + data);
            }
        );

}

$(document).ready(function () {
    $('#check').click(function () {
        loadValidCode('#check');
    });
    $('#check2').click(function () {
        loadValidCode('#check2');
    });
    loadValidCode('#check');
    loadValidCode('#check2');
    $('#reg_btn').click(function () {
        $.ajax({
            type: "post",
            url: "http://110.64.69.66:8081/team/register/",
            dataType: "json",
            data: {
                "mail": $('#r_mail').val(),
                "pwd": $('#r_pwd').val(),
                "inv": $('#r_inv').val(),
                "code": $('#r_code').val()
            },
            xhrFields: {withCredentials: true},
            headers: {
                "Access-Control-Allow-Origin":"*"
            }

        }).always(function (data) {
            console.log(data);
        });

    })
});