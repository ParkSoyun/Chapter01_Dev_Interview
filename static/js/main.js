function check_user() {
    let password = $('#inputPassword').val()
    $.ajax({
        type: "POST",
        url: "/check-userinfo",
        data: {password_give: password},
        success: function (response) {
            let msg = response["msg"];
            let user = response["user"];
            if (msg == "success") {
                alert("확인완료")
                get_userinfo(user);
            } else {
                alert("비밀번호가 틀렸습니다.")
                $('#inputPassword').val("");
            }
        }
    });
}

function get_userinfo(user){
    $.ajax({
        type: "POST",
        url: "/userinfo",
        data: {name_give: user[0]["name"], email_give: user[0]["email"]},
        success: function (response) {
            console.log(response);
        }
    });
}

function sign_up() {
    let username = $("#inputUserName").val()
    let email = $("#inputEmail").val()
    let password = $("#inputPassword").val()
    let password2 = $("#inputCheckPassword").val()

    if (username == "") {
        $("#help-email").text("이름을 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#inputUserName").focus()
        return;
    }

    if(!email.includes('@')) {
        $("#help-email").text("email 형식으로 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#inputEmail").focus()
        return;
    }

    if (password == "") {
        $("#help-password").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#inputPassword").focus()
        return;
    } else if (!is_password(password)) {
        $("#help-password").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe").addClass("is-danger")
        $("#inputPassword").focus()
        return;
    } else {
        $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success")
    }
    if (password2 == "") {
        $("#help-password").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#inputCheckPassword").focus()
        return;
    } else if (password2 != password) {
        $("#help-password").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe").addClass("is-danger")
        $("#inputCheckPassword").focus()
        return;
    } else {
        $("#help-password").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success")
    }
    $.ajax({
        type: "POST",
        url: "/signup",
        data: {
            username_give: username,
            email_give : email,
            password_give: password
        },
        success: function (response) {
            alert("회원가입을 축하드립니다!")
            window.location.replace("/signin")
        }
    });
}

function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

function sign_in() {
    let email = $("#inputEmail").val()
    let password = $("#inputPassword").val()

    if (email == "") {
        $("#help-email-password-login").text("이메일을 입력해주세요.")
        $("#inputEmail").focus()
        return;
    }

    if (password == "") {
        $("#help-email-password-login").text("비밀번호를 입력해주세요.")
        $("#inputPassword").focus()
        return;
    }
    $.ajax({
        type: "POST",
        url: "/signin",
        data: {
            email_give: email,
            password_give: password
        },
        success: function (response) {
            console.log(response['result'])
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/question'});
                console.log($.cookie('mytoken', response['token'], {path: '/question'}))
                //window.location.replace("/question")
            } else {
                alert(response['msg'])
            }
        }
    });
}
