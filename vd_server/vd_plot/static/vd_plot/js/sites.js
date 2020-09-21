var site_name_index = 0;
var site_x_index = 1;
var site_y_index = 2;
var site_w_index = 3;

function get_site_div(site_id) {
    return `<div class="site" id="site_` + site_id + `">
    <input type="text" class="site_name" placeholder="Name" name="site`+ site_id + `_name">
    <input type="number" step="any" class="site_x" placeholder="Site x" name="site`+ site_id + `_x" required>
    <input type="number" step="any" class="site_y" placeholder="Site y" name="site`+ site_id + `_y" required>
    <input type="number" step="any" class="site_w" placeholder="Site weight" name="site`+ site_id + `_w" value="" style="display:none">
    <button type="button" id="remove_site_`+ site_id + `" onclick="remove_site(` + site_id + `)">Remove Site</button>
    </div>`
}
function get_weighted_site_div(site_id) {
    return `<div class="site" id="site_` + site_id + `">
    <input type="text" class="site_name" placeholder="Name" name="site`+ site_id + `_name">
    <input type="number" step="any" class="site_x" placeholder="Site x" name="site`+ site_id + `_x" required>
    <input type="number" step="any" class="site_y" placeholder="Site y" name="site`+ site_id + `_y" required>
    <input type="number" step="any" class="site_w" placeholder="Site weight" name="site`+ site_id + `_w" required>
    <button type="button" id="remove_site_`+ site_id + `" onclick="remove_site(` + site_id + `)">Remove Site</button>
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
        type: 'GET',
        url: '/plot-vd/',
        dataType: 'html',
        data: { body: JSON.stringify(data) },
        success: function (resp) {
            $('#plot').html(resp);
            $('#loading').html("")
        },
        error: function (resp) {
            $('#loading').html("")
            console.log(resp);
        }
    });
})

$('#first-step').click(function () {
    data = getFormData(vd_form);
    data["sites"] = get_sites();
    $('#loading').html("LOADING");
    // TODO: Disable plot VD?
    $.ajax({
        type: 'GET',
        url: '/steps/first/',
        dataType: 'html',
        data: { body: JSON.stringify(data) },
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
    // TODO: Disable plot VD?
    $.ajax({
        type: 'GET',
        url: '/steps/next/',
        dataType: 'html',
        data: { body: JSON.stringify(data) },
        success: function (resp) {
            $('#plot').html(resp);
            $('#loading').html("")
            get_info()
            // TODO: Enable Next step.
        },
        error: function (resp) {
            $('#loading').html("")
            console.log(resp);
        }
    });
})

$('#prev-step').click(function () {
    $('#loading').html("LOADING");
    // TODO: Disable plot VD?
    $.ajax({
        type: 'GET',
        url: '/steps/prev/',
        dataType: 'html',
        data: { body: JSON.stringify(data) },
        success: function (resp) {
            $('#plot').html(resp);
            $('#loading').html("")
            get_info()
            // TODO: Enable Next step.
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
        var site_name = site_divs[i].children[site_name_index].value;
        var site_x = site_divs[i].children[site_x_index].value;
        var site_y = site_divs[i].children[site_y_index].value;
        if ($('input[name=vd_type]:checked', '#vd_form').val() == 'vd') {
            var site = [site_x, site_y, site_name];
        } else {
            var site_w = site_divs[i].children[site_w_index].value;
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
                var event_str = ""
                if (event.is_site) {
                    event_str = "S(" + event.name + ")<br>"
                } else {
                    event_str = "I(" + event.point.x.toString() + ", " + event.point.y.toString() + ")<br>"
                }
                $('#qqueue').append(event_str);
            }

            // Actual Event
            var actual_event = resp.actual_event
            var actual_event_str = ""
            if (actual_event != null && actual_event.is_site) {
                actual_event_str = "S(" + actual_event.name + ")<br>"
            } else if (actual_event != null) {
                actual_event_str = "I(" + actual_event.point.x.toString() + ", " + actual_event.point.y.toString() + ")<br>"
            }
            $('#actual_event').html(actual_event_str);

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