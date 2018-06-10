//
$(function() {
    $('input.analyze').on('click', function() {
        console.log("analyze button fired");
        //event.preventDefault();

        var start = document.querySelector('#month_start').value // ex 2018-01
        var end = document.querySelector('#month_end').value

        start_date = new Date(start);
        end_date = new Date(end);

        if (start_date > end_date) {
            error = '<p class="error">2nd date must be after 1st</span>';
            $(this).after(error);
            return;
        }
        var url = "/analyze=" + start + ":" + end;
//        $.ajax({
//            url: "/analyze=" + start + ":" + end,
//            type: 'GET',
//            success: function() {
//                console.log("sent analyze start/end");
//            },
//            error: function() {
//                console.log("analyze message did not work");
//            }
//        });
        window.location.replace(url);


    });
});



// "all ok" button sends message to views/button_input to mark all recent=True li as recent=False
$(function() {
    $('input.ok').on('click', function() {
        console.log("all ok button fired");
        event.preventDefault();
        $.ajax({
            url: '/button_input',
            type: 'POST',
            data: {'action' : 'all ok', 'id' : '', value : ''},
            success: function() {
                console.log("sent all ok");
            },
            error: function() {
                console.log("all ok message did not work");
            }
        });
    });
});

// "delete" button sends message to views/button_input to mark all recent=True li as recent=False
$(function() {
    $('button.delete').on('click', function() {
        console.log("delete button fired");
        event.preventDefault();

        var type = $(this).data('type');
        var action = "delete " + type;
        var id = $(this).data('id');

        $.ajax({
            url: '/button_input',
            type: 'POST',
            data: {'action' : action, 'id' : id, value : ''},
            success: function() {
                console.log("sent");
            },
            error: function() {
                console.log("all ok message did not work");
            }
        });

        //remove the whole line
        $(this).closest(".row").remove();

    });
});

