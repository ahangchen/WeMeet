var pwd_flag = false;
$('#pwd-conf').blur(function () {
    pwd_flag = false;
    var pwd = document.getElementById('pwd').value;
    var pwdconf = document.getElementById('pwd-conf').value;
    if (pwd.length >= 6) {
        if (pwd != pwdconf) {
            document.getElementById("conf-result").innerHTML = "两次输入的密码不同，请重新输入";
        }
        if (pwd == pwdconf && pwdconf != "") {
            $("#conf-result").css("color", "green");
            document.getElementById("conf-result").innerHTML = "两次输入的密码相同";
            pwd_flag = true; //此时密码符合要求
        }
        if (pwd == "" && pwdconf == "") {
            document.getElementById("con-result").innerHTML = "";
        }
    }
    if (pwd.length < 6) {
        document.getElementById("conf-result").innerHTML = "";
    }
});
$('#pwd').keyup(function () {
    document.getElementById("pwd-result").innerHTML = "";
});
$('#pwd').blur(function () {
    var pattern = /^\d+$/;
    var pwd = document.getElementById('pwd').value;
    var pwdconf = document.getElementById('pwd-conf').value;
    if (pwd.length > 0 && pwd.length < 6) {
        document.getElementById("pwd-result").innerHTML = "密码小于6个字符请重新输入";
    }
    if (pwd.length >= 6) {
        if (pattern.test(pwd)) {
            document.getElementById("pwd-result").innerHTML = "不能为纯数字";
        } else {
            document.getElementById("pwd-result").innerHTML = "密码符合要求";
        }
    }
    if (pwd == "" && pwdconf == "") {
        document.getElementById("conf-result").innerHTML = "";
    }
}); //密码判断；
$("#finish").click(function () {
    var account;//未获取
    var credential = document.getElementById("hash_id").innerHTML;
    var pwd = document.getElementById('pwd').value;
    var pwd_hash = hex_sha1("pwd");
    if (pwd_flag == true) {
        var data = {account: account, credential: credential, pwd: pwd_hash};
        $.ajax({
            type: 'POST',
            data: data,
            url: '../../data/find.json',
            dataType: 'json',
            success: function (data) {
                if (data.err == 0) {
                    $("#return_show").css("display", "none");
                    $("#success-show").css("display", "block");
                }
                if (data.err == -4) {
                    document.getElementById('result').innerHTML = "账号不存在";
                }
                if (data.err == -7) {
                    document.getElementById('result').innerHTML = "凭据错误";
                }
                if (data.err == -10) {
                    document.getElementById('result').innerHTML = "操作失败";
                }
                if (data.err == -1) {
                    document.getElementById('result').innerHTML = "请求方法错误";
                }
            }
        });
    }
})