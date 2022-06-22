// $(document).ready(function () {
//     show_question();
// });

function show_question() {
    $.ajax({
        type: "GET",
        url: "/question",
        data: {},
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
        data: {email: 'test@test.test', question_num: questionNum, answer: my_answer},
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
                                                        </tr>
                                                    </thead>
                                                    <tbody id="table">`

                $('#main-box').append(prev_button)
                $('#main-box').append(question_card1)

                for(let i=0; i<answer_list.length; i++) {
                    let answer_comment = answer_list[i]['answer']
                    let user_email = answer_list[i]['user_email']

                    let answer_table = ``

                    if(user_email === 'test@test.test') {
                        answer_table = `<tr>
                                            <th class="answer-comment col-md-8">${answer_comment}</th>
                                            <td class="my-td" id="edit_answer">
                                                <button onclick="edit_answer()" type="button" class="btn btn-light">수정</button>
                                            </td>
                                            <td class="my-td">🤍</td>
                                        </tr>`
                    } else {
                        answer_table = `<tr>
                                            <th class="answer-comment col-md-8">${answer_comment}</th>
                                            <td class="my-td"></td>
                                            <td class="my-td">🤍</td>
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

function edit_answer() {

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

