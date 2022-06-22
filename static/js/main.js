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

// $(document).ready(function () {
//     show_question();
// });

function show_question() {
    // let token = document.cookie.split('=')[1]

    $.ajax({
        type: "GET",
        url: "/question",
        data: {},
        // beforeSend: function (xhr) {
        //     xhr.setRequestHeader("Content-type","application/json");
        //     xhr.setRequestHeader("Authorization","JWT " + token);
        // },
        success: function (response) {
            $('#main-box').empty()

            let min_qn = response['min_qn']
            let max_qn = response['max_qn']

            let question_info = response['question_info']
            let question_num = question_info['num']
            let question = question_info['question']

            let prev_button = ``
            let next_button = ``

            if(question_num == min_qn) {
                prev_button = `<button onclick="prev_question(${question_num})" type="button" class="btn btn-secondary next-button" disabled><</button>`
            } else {
                prev_button = `<button onclick="prev_question(${question_num})" type="button" class="btn btn-secondary next-button"><</button>`
            }

            let question_card = `<div class="card text-center question-box">
                                    <div class="card-header question-num">
                                        <h2>Question ${question_num}</h2>
                                    </div>
                                    <div class="card-body">
                                        <h3 class="card-title question">${question}</h3>
                                        <div class="answer-box">
                                            <textarea class="form-control answer" id="answerTextarea" placeholder="답변을 작성해보세요." rows="5"></textarea>
                                            <button onclick="save_answer(${question_num})" type="button" class="btn btn-outline-dark">답변 등록</button>
                                        </div>
                                    </div>
                                 </div>`

            if(question_num == max_qn) {
                next_button = ` <button onclick="next_question(${question_num})" type="button" class="btn btn-secondary next-button" disabled>></button>`
            } else {
                next_button = ` <button onclick="next_question(${question_num})" type="button" class="btn btn-secondary next-button">></button>`
            }

            $('#main-box').append(prev_button)
            $('#main-box').append(question_card)
            $('#main-box').append(next_button)
        },
        error : function(request, status, error ) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });
}

function save_answer(questionNum) {
    let my_answer = $('#answerTextarea').val()

    $.ajax({
        type: "POST",
        url: "/answer",
        data: {question_num: questionNum, answer: my_answer},
        success: function (response) {
            alert(response["msg"])

            if(response["answer_list"] != undefined) {
                $('#main-box').empty()

                let question_info = response['question_info']
                let question_num = question_info['num']
                let question = question_info['question']
                let answer_list = response['answer_list']

                let prev_button = `<button onclick="prev_question(${question_num})" type="button" class="btn btn-secondary next-button"><</button>`

                let question_card1 = `<div class="card text-center question-box">
                                        <div class="card-header question-num">
                                            <h2>Question ${question_num}</h2>
                                        </div>
                                        <div class="card-body">
                                            <h3 class="card-title question">${question}</h3>
                                            <div class="col-9 answer-box">
                                                <table class="table table-hover">
                                                    <thead>
                                                        <tr>
                                                            <th></th>
                                                            <td></td>
                                                            <td></td>
                                                            <td></td>
                                                        </tr>
                                                    </thead>
                                                    <tbody id="table">`

                $('#main-box').append(prev_button)
                $('#main-box').append(question_card1)

                for(let i=0; i<answer_list.length; i++) {
                    let answer_comment = answer_list[i]['answer']
                    let like_count = answer_list[i]['like_count']

                    let answer_table = ``

                    if(i == 0) {
                        answer_table = `<tr>
                                            <th class="answer-comment col-md-8" id="myanswer">${answer_comment}</th>
                                            <td class="my-td" id="edit_answer">
                                                <button onclick="edit_answer(${question_num})" type="button" class="btn btn-light">수정</button>
                                            </td>
                                            <td class="my-td">🤍</td>
                                            <td class="my-td like-count">${like_count}</td>
                                        </tr>`
                    } else {
                        answer_table = `<tr>
                                            <th class="answer-comment col-md-8">${answer_comment}</th>
                                            <td class="my-td"></td>
                                            <td class="my-td">🤍</td>
                                            <td class="my-td like-count">${like_count}</td>
                                        </tr>`
                    }

                    $('#table').append(answer_table)
                }

                let question_card2 = `</tbody>
                                    </table>
                                </div>
                            </div>
                        </div>`

                let next_button = `<button onclick="next_question(${question_num})" type="button" class="btn btn-secondary next-button">></button>`

                $('#main-box').append(question_card2)
                $('#main-box').append(next_button)
            }
        }
    });
}

function edit_answer(question_num) {
    let answer_comment = $('#myanswer').text()

    $.ajax({
        type: "PUT",
        url: "/answer",
        data: {
            flag: 0,
            answer_comment: answer_comment
        },
        success: function (response) {
            $('#myanswer').empty()
            $('#edit_answer').empty()

            let answer = response['answer_comment']

            console.log(answer)

            let editbox = `<textarea class="form-control answer" id="answerTextarea" rows="5">${answer}</textarea>`
            let editbutton = `<button onclick="send_new_answer(${question_num})" type="button" class="btn btn-light">수정</button>`

            $('#myanswer').append(editbox)
            $('#edit_answer').append(editbutton)
        }
    });
}

function send_new_answer(question_num) {
    let new_answer = $('#answerTextarea').val()

    $.ajax({
        type: "PUT",
        url: "/answer",
        data: {
            flag: 1,
            question_num: question_num,
            new_answer: new_answer
        },
        success: function (response) {
            $('#myanswer').empty()
            $('#edit_answer').empty()

            let answer_info = response['answer_info']
            let answer = answer_info['answer']

            let editbox = `${answer}`
            let editbutton = `<button onclick="edit_answer(${question_num})" type="button" class="btn btn-light">수정</button>`

            $('#myanswer').append(editbox)
            $('#edit_answer').append(editbutton)
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
                $.cookie('mytoken', response['token'], {path: '/'});
                console.log($.cookie('mytoken', response['token'], {path: '/question'}))

                window.location.replace("/question")
                // window.location.replace("/")
            } else {
                alert(response['msg'])
            }
        }
    });
}

function prev_question(current_qn) {
    $.ajax({
        type: "GET",
        url: "/prevquestion",
        data: {email: "test@test.test", current_qn: current_qn},
        success: function (response) {
            $('#main-box').empty()

            let min_qn = response['min_qn']
            let max_qn = response['max_qn']

            let question_info = response['question_info']
            let question_num = question_info['num']
            let question = question_info['question']

            let prev_button = ``
            let next_button = ``

            if(question_num == min_qn) {
                prev_button = `<button onclick="prev_question(${question_num})" type="button" class="btn btn-secondary next-button" disabled><</button>`
            } else {
                prev_button = `<button onclick="prev_question(${question_num})" type="button" class="btn btn-secondary next-button"><</button>`
            }

            let question_card = `<div class="card text-center question-box">
                                    <div class="card-header question-num">
                                        <h2>Question ${question_num}</h2>
                                    </div>
                                    <div class="card-body">
                                        <h3 class="card-title question">${question}</h3>
                                        <div class="answer-box">
                                            <textarea class="form-control answer" id="answerTextarea" placeholder="답변을 작성해보세요." rows="5"></textarea>
                                            <button onclick="save_answer(${question_num})" type="button" class="btn btn-outline-dark">답변 등록</button>
                                        </div>
                                    </div>
                                 </div>`

            if(question_num == max_qn) {
                next_button = ` <button onclick="next_question(${question_num})" type="button" class="btn btn-secondary next-button" disabled>></button>`
            } else {
                next_button = ` <button onclick="next_question(${question_num})" type="button" class="btn btn-secondary next-button">></button>`
            }

            $('#main-box').append(prev_button)
            $('#main-box').append(question_card)
            $('#main-box').append(next_button)
        },
        error : function(request, status, error ) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });
}

function next_question(current_qn) {
    $.ajax({
        type: "GET",
        url: "/nextquestion",
        data: {email: "test@test.test", current_qn: current_qn},
        success: function (response) {
            $('#main-box').empty()

            let min_qn = response['min_qn']
            let max_qn = response['max_qn']

            let question_info = response['question_info']
            let question_num = question_info['num']
            let question = question_info['question']

            let prev_button = ``
            let next_button = ``

            if(question_num == min_qn) {
                prev_button = `<button onclick="prev_question(${question_num})" type="button" class="btn btn-secondary next-button" disabled><</button>`
            } else {
                prev_button = `<button onclick="prev_question(${question_num})" type="button" class="btn btn-secondary next-button"><</button>`
            }

            let question_card = `<div class="card text-center question-box">
                                    <div class="card-header question-num">
                                        <h2>Question ${question_num}</h2>
                                    </div>
                                    <div class="card-body">
                                        <h3 class="card-title question">${question}</h3>
                                        <div class="answer-box">
                                            <textarea class="form-control answer" id="answerTextarea" placeholder="답변을 작성해보세요." rows="5"></textarea>
                                            <button onclick="save_answer(${question_num})" type="button" class="btn btn-outline-dark">답변 등록</button>
                                        </div>
                                    </div>
                                 </div>`

            if(question_num == max_qn) {
                next_button = ` <button onclick="next_question(${question_num})" type="button" class="btn btn-secondary next-button" disabled>></button>`
            } else {
                next_button = ` <button onclick="next_question(${question_num})" type="button" class="btn btn-secondary next-button">></button>`
            }

            $('#main-box').append(prev_button)
            $('#main-box').append(question_card)
            $('#main-box').append(next_button)
        },
        error : function(request, status, error ) {
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });
}