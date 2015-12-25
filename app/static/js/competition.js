// 获取学院和专业  并且赋值到表单
function get_acachemy_major(id_aca, id_maj, aca_hi, maj_hi) {
    $.getJSON('/department/_get', function(data) {
        var opt = "";
        var id_acachemy = "";
        opt += "<option value=\"\" disabled selected>==选择学院==</option>";
        for(var i=0; i<data.departments.length; i++) {
            if(data.departments[i].acachemy_id != 0) {
                opt += "<option value=\""  + data.departments[i].id + "\">" + data.departments[i].acachemy.acachemy_name + "</option>";
            }
        }
        $(id_aca).html(opt);
        opt = "<option value=\"\" disabled selected>==选择专业==</option>";
        $(id_maj).html(opt);

        $(id_aca).change(function() {
            var id = 0;
            id = $(this).val();
            id = id - 1;
            var opt = "";
            for(var i=0; i<data.departments[id].majors.length; i++) {
                opt += "<option value=\"" + data.departments[id].majors[i].major_id + "\">" + data.departments[id].majors[i].major_name + "</option>";
            }
            id_major = data.departments[id].majors[0].major_id;
            $(aca_hi).val(id+1);
            $(maj_hi).val(id_major);
            $(id_maj).html(opt);
        })
        $(id_maj).change(function() {
            $(maj_hi).val($(this).val());
        })
    })
}


get_acachemy_major("#acachemy", "#major", "#acachemy_hi", "#major_hi");

// 老师部分获取单位信息
$.getJSON('/department/_get', function(data) {
    var opt = "";
    var id_acachemy = "";
    opt += "<option value=\"\" disabled selected>==选择单位==</option>";
    for(var i=0; i<data.departments.length; i++) {
        if(data.departments[i].acachemy_id != 0) {
            opt += "<option value=\""  + data.departments[i].id + "\">" + data.departments[i].acachemy.acachemy_name + "</option>";
        }
    }
    $("#teacher_acachemy").html(opt);
    $("#teacher_acachemy").change(function () {
        var id = $(this).val();
        id = id -1;
        opt = "";
        for(var i=0; i<data.departments[id].teachers.length; i++) {
            opt += "<option value=\"" + data.departments[id].teachers[i].teacher_id + "\">";
        }
        $("#teacher").html(opt);
    })
})


// 监听老师信息的选择
function immediately(){
    var element = document.getElementById("teacher_id");
    if("\v"=="v") {
        element.onpropertychange = webChange;
    }else{
        element.addEventListener("input",webChange,false);
    }
    function webChange() {
        var student_id = element.value;
        if (student_id.length >= 5){
            $.getJSON('/competition/_get_teacher', {id: student_id}, function (data) {
                document.getElementById("teacher_name").value=data.teacher_name;
            })
        }
    }
}
immediately();


$(function() {
    $("#student_info").click(function () {
        $.ajax({
            url: '/add_student',
            type: 'POST',
            data: $('#student_form').serialize(),
            success: window.location.reload()
        });
    })
})

$(function() {
    $("#teacher_info").click(function () {
        $.ajax({
            url: '/add_teacher',
            type: 'POST',
            data: $('#teacher_form').serialize(),
            success: window.location.reload()
        });
    })
})

var competition_id = document.getElementById("competition_id").value;
function delTeacher() {
    var teacher_id = event.target.getAttribute('data');
    $.ajax({
        url: '/competition/_del_teacher',
        data: {
            id: competition_id,
            teacher_id: teacher_id
        },
        success: window.location.reload()
    })
}

function delStudent() {
    var student_id = event.target.getAttribute('data');
    $.ajax({
        url: '/competition/_del_student',
        data: {
            id: competition_id,
            student_id: student_id
        },
        success: window.location.reload()
    })
}

function editStudent() {
    var student_id = event.target.getAttribute('data_id');
    var student_name = event.target.getAttribute('data_name');
    var grade = event.target.getAttribute('data_grade');
    var acachemy_id = event.target.getAttribute('data_acachemy');
    var major_id = event.target.getAttribute('data_major');
    document.getElementById("edit_student_id").value = student_id;
    document.getElementById('edit_student_name').value = student_name;
    document.getElementById('edit_student_grade').value = grade;
    $.getJSON('/competition/_get_grade', function(data) {
        console.log(data.grades[1].grade);
        var opt = "";
        opt += "<option value=\"\" disabled selected>" + grade + "</option>";
        for(var i=0;i<data.grades.length;i++) {
            opt += "<option value=\""  + data.grades[i].id + "\">" + data.grades[i].grade + "</option>";
        }
        $("#edit_student_grade").html(opt);
    })
    get_acachemy_major("#edit_student_acachemy", "#edit_student_major", "#edit_student_acachemy_hi", "#edit_student_major_hi");
}
