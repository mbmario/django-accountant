$(document).ready(function() {

    $(".selectpicker").change(function() {

        console.log("CHANGE REGISTERED");
        event.preventDefault();

        // get the selected category name, i.e. "food"
        var cat = $(this).find('option:selected').text();
        // get the line item name, i.e. "Totino's pizza"
        var li = $(this).closest('.row').children().first().text().trim();
        var id = $(this).data('id');
        console.log("CAT: " + cat + " LI: " + li + " id: " + id);

        // send an ajax post request, telling it to assign li's category field to cat
        $.ajax({
            url : '/assign_cat_to_li',
            type : 'POST',
            data : { 'li' : li, 'cat' : cat, 'id' : id},
            success: function () {
                // update text of parent to cat
                console.log('INSIDE AJAX success on assigning ' + li + ' to ' + cat);
//                $(this).parent().children().removeAttr("selected")
//                $(this).attr("selected", "selected")
//                $(this).attr("value", cat)
            }
        });
    });
});