var site_name_index = 0;
var site_x_index = 1;
var site_y_index = 2;
var site_w_index = 3;
var session = Date.now().toString();
var csrftoken = "";

window.addEventListener("load", function () {
    csrftoken = $('[name=csrfmiddlewaretoken]').attr("value");
});

window.addEventListener("beforeunload", function (e) {
    $.ajax({
        type: 'POST',
        url: '/steps/delete/',
        dataType: 'json',
        data: { session: session },
        headers: { 'X-CSRFToken': csrftoken }
    });
});

function get_site_div(site_id) {
    return `<div class="site col" id="site_` + site_id + `">
    <div class="row">
        <input type="text" class="site_name" placeholder="Name" name="site`+ site_id + `_name">
        <button type="button" id="remove_site_`+ site_id + `" onclick="remove_site(` + site_id + `)">Remove Site</button>
    </div>
    <div class="row">
        <input type="number" step="any" class="site_x" placeholder="Site x" name="site`+ site_id + `_x" required>
        <input type="number" step="any" class="site_y" placeholder="Site y" name="site`+ site_id + `_y" required>
        <input type="number" step="any" class="site_w" placeholder="Site weight" name="site`+ site_id + `_w" value="" style="display:none">
    </div>
    </div>`
}

function get_weighted_site_div(site_id) {
    return `<div class="site col" id="site_` + site_id + `">
    <div class="row">
        <input type="text" class="site_name" placeholder="Name" name="site`+ site_id + `_name">
        <button type="button" id="remove_site_`+ site_id + `" onclick="remove_site(` + site_id + `)">Remove Site</button>
    </div>
    <div class="row">
        <input type="number" step="any" class="site_x" placeholder="Site x" name="site`+ site_id + `_x" required>
        <input type="number" step="any" class="site_y" placeholder="Site y" name="site`+ site_id + `_y" required>
        <input type="number" step="any" class="site_w" placeholder="Site weight" name="site`+ site_id + `_w" value="">
    </div>
    </div>`
}

function evaluate_start_buttons() {
    if (parseInt($('#num_sites').attr("value")) >= 1) {
        $('#first-step').removeAttr('disabled');
        $('#plot-vd').removeAttr('disabled');
    } else {
        $('#first-step').attr('disabled', 'disabled');
        $('#plot-vd').attr('disabled', 'disabled');
    }
}

function add_site() {
    if ($('input[name=vd_type]:checked', '#vd_form').val() == 'vd') {
        $('#sites').append(get_site_div($('#actual_sites').attr("value")));
    } else {
        $('#sites').append(get_weighted_site_div($('#actual_sites').attr("value")));
    }
    $('#num_sites').attr("value", parseInt($('#num_sites').attr("value")) + 1);
    $('#actual_sites').attr("value", parseInt($('#actual_sites').attr("value")) + 1);
    evaluate_start_buttons();
}

$('#add_site').click(add_site);

function remove_site(site_id) {
    $('#site_' + site_id).remove()
    $('#num_sites').attr("value", parseInt($('#num_sites').attr("value")) - 1)
    evaluate_start_buttons();
}

function change_vd_type() {
    var all_input_w = $('input[class=site_w]', '#vd_form');
    if ($('input[name=vd_type]:checked', '#vd_form').val() == 'vd') {
        for (var i = 0; i < all_input_w.length; i++) {
            all_input_w[i].style.display = 'none';
            all_input_w[i].required = false;
        }
    } else {
        for (var i = 0; i < all_input_w.length; i++) {
            all_input_w[i].style = '';
            all_input_w[i].required = true;
        }
    }
}

$('input[name=vd_type]', '#vd_form').click(change_vd_type);

function getFormData(form) {
    var unindexed_array = form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

var vd_form = $('#vd_form')

vd_form.submit(function (event) {
    event.preventDefault();
});

$('#plot-vd').click(function () {
    data = getFormData(vd_form);
    data["sites"] = get_sites();
    $('#loading').html("LOADING");
    $.ajax({
        type: 'POST',
        url: '/steps/delete/',
        dataType: 'json',
        data: { session: session },
        headers: { 'X-CSRFToken': csrftoken },
        success: function (r) {
            $.ajax({
                type: 'GET',
                url: '/plot-vd/',
                dataType: 'html',
                data: { body: JSON.stringify(data), session: session },
                success: function (resp) {
                    console.log("yep");
                    $('#plot').html(resp);
                    $('#loading').html("")
                    // Step buttons.
                    $('#next-step').attr('disabled', 'disabled');
                    $('#prev-step').attr('disabled', 'disabled');
                    // Actual Event
                    $('#actual_event').html("");
                    // Queue
                    $('#qqueue').html("");
                    // LList
                    $('#llist').html("");
                },
                error: function (resp) {
                    console.log(resp);
                    $('#loading').html("")
                }
            });
        },
        error: function (resp) {
            console.log(resp);
            $('#loading').html("")
        }
    });
})

$('#first-step').click(function () {
    data = getFormData(vd_form);
    data["sites"] = get_sites();
    $('#loading').html("LOADING");
    $.ajax({
        type: 'GET',
        url: '/steps/first/',
        dataType: 'html',
        data: { body: JSON.stringify(data), session: session },
        success: function (resp) {
            $('#plot').html(resp);
            $('#loading').html("")
            get_info()
        },
        error: function (resp) {
            $('#loading').html("")
            console.log(resp);
        }
    });
})

$('#next-step').click(function () {
    $('#loading').html("LOADING");
    $.ajax({
        type: 'GET',
        url: '/steps/next/',
        dataType: 'html',
        data: { body: JSON.stringify(data), session: session },
        success: function (resp) {
            $('#plot').html(resp);
            $('#loading').html("")
            get_info()
        },
        error: function (resp) {
            $('#loading').html("")
            console.log(resp);
        }
    });
})

$('#prev-step').click(function () {
    $('#loading').html("LOADING");
    $.ajax({
        type: 'GET',
        url: '/steps/prev/',
        dataType: 'html',
        data: { body: JSON.stringify(data), session: session },
        success: function (resp) {
            $('#plot').html(resp);
            $('#loading').html("")
            get_info()
        },
        error: function (resp) {
            $('#loading').html("")
            console.log(resp);
        }
    });
})

function get_sites() {
    var site_divs = $('.site');
    var sites = [];
    for (var i = 0; i < site_divs.length; i++) {
        var site_name = $(site_divs.get(i)).find('input[class="site_name"]')[0].value;
        var site_x = $(site_divs.get(i)).find('input[class="site_x"]')[0].value;
        var site_y = $(site_divs.get(i)).find('input[class="site_y"]')[0].value;
        if ($('input[name=vd_type]:checked', '#vd_form').val() == 'vd') {
            var site = [site_x, site_y, site_name];
        } else {
            var site_w = $(site_divs.get(i)).find('input[class="site_w"]')[0].value;
            var site = [site_x, site_y, site_w, site_name];
        }
        sites.push(site);
    }
    return sites;
}

function get_boundary_div(boundary) {
    var boundary_div = "<div class='LBoundary' style='display: inline;'>";
    if (boundary == null) {
        boundary_div += "Null";
    } else {
        boundary_div += "B*"
        if (boundary.sign) {
            boundary_div += "+"
        } else {
            boundary_div += "-"
        }
        boundary_div += "(" + boundary.sites[0].name + ", " + boundary.sites[1].name + ")"
    }
    boundary_div += "</div>"
    return boundary_div
}

function get_info() {
    $('#qqueue').html("LOADING")
    $('#llist').html("LOADING")
    $('#actual_event').html("LOADING")
    $.ajax({
        type: 'GET',
        url: '/steps/info/',
        dataType: 'json',
        data: { session: session },
        success: function (resp) {
            $('#qqueue').html("");
            $('#llist').html("");
            $('#actual_event').html("");

            // L List
            console.log(resp)
            if (resp.l_list.length > 0) {
                $('#llist').append(get_boundary_div(resp.l_list[0].left));
            }
            for (let i = 0; i < resp.l_list.length; i++) {
                var region = resp.l_list[i]
                var region_div = "<div class='LRegion' style='display: inline;'>";
                region_div += "R(" + region.site.name + ")"
                region_div += "</div>";
                $('#llist').append(region_div);
                $('#llist').append(get_boundary_div(resp.l_list[i].right));
            }

            // Q Queue
            for (let i = 0; i < resp.q_queue.length; i++) {
                var event = resp.q_queue[i]
                var event_div = "<div class='event'>" + event.event_str + "</div>"
                $('#qqueue').append(event_div);
            }

            // Actual Event
            var actual_event = resp.actual_event
            var actual_event_div = "<div class='event'>" + actual_event.event_str + "</div>"
            $('#actual_event').html(actual_event_div);

            // Steps
            if (resp.is_next_step || !resp.is_diagram) {
                $('#next-step').removeAttr('disabled');
            } else {
                $('#next-step').attr('disabled', 'disabled');
            }
            if (resp.is_prev_step) {
                $('#prev-step').removeAttr('disabled');
            } else {
                $('#prev-step').attr('disabled', 'disabled');
            }
        },
        error: function (resp) {
            console.log(resp);
        }
    });
}

$('#prev-step').attr('disabled', 'disabled');
$('#next-step').attr('disabled', 'disabled');
evaluate_start_buttons();
add_site();

$(document).ready(function () {
    $('#sidebarOpen').on('click', function () {
        console.log("hello0");
        $('#sidebar').toggleClass('active');
    });
    $('#sidebarCollapse').on('click', function () {
        console.log("hello1");
        $('#sidebar').toggleClass('active');
    });
    $('#left').on('click', function () {
        if ($('#sidebar').hasClass('active')) {
            console.log("hello");
            $('#sidebar').toggleClass('active');
        }
    });

});