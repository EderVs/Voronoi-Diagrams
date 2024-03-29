var site_name_index = 0;
var site_x_index = 1;
var site_y_index = 2;
var site_w_index = 3;
var session = Date.now().toString();
var csrftoken = "";
var max_sites = 100;

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

function get_site_div(site_id, values) {
    return `<div class="site col" id="site_` + site_id + `">
    <div class="row">
        <input type="text" class="site_name" placeholder="Name" name="site`+ site_id + `_name" value=` + (values.name != null ? values.name : `""`) + ` required maxlength="4">
        <button type="button" id="remove_site_`+ site_id + `" onclick="remove_site(` + site_id + `)">Remove Site</button>
    </div>
    <div class="row">
        <input type="number" step="any" class="site_x" placeholder="Site x" name="site`+ site_id + `_x" value=` + (values.x != null ? values.x : `""`) + ` required>
        <input type="number" step="any" class="site_y" placeholder="Site y" name="site`+ site_id + `_y" value=` + (values.y != null ? values.y : `""`) + ` required>
        <input type="number" step="any" class="site_w" placeholder="Site weight" name="site`+ site_id + `_w" value=` + (values.w != null ? values.w : `""`) + ` style="display:none">
    </div>
    </div>`
}

function get_weighted_site_div(site_id, values) {
    return `<div class="site col" id="site_` + site_id + `">
    <div class="row">
        <input type="text" class="site_name" placeholder="Name" name="site`+ site_id + `_name" value=` + (values.name != null ? values.name : `""`) + ` required maxlength="4">
        <button type="button" id="remove_site_`+ site_id + `" onclick="remove_site(` + site_id + `)">Remove Site</button>
    </div>
    <div class="row">
        <input type="number" step="any" class="site_x" placeholder="Site x" name="site`+ site_id + `_x" value=` + (values.x != null ? values.x : `""`) + ` required>
        <input type="number" step="any" class="site_y" placeholder="Site y" name="site`+ site_id + `_y" value=` + (values.y != null ? values.y : `""`) + ` required>
        <input type="number" step="any" class="site_w" placeholder="Site weight" name="site`+ site_id + `_w" value=` + (values.w != null ? values.w : `""`) + ` required>
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

function add_site(values) {
    console.log($('#num_sites').val());
    if ($('#num_sites').val() >= max_sites) {
        return;
    }
    var actual_site = $('#actual_sites').attr("value");
    $('#num_sites').attr("value", parseInt($('#num_sites').attr("value")) + 1);
    $('#actual_sites').attr("value", parseInt($('#actual_sites').attr("value")) + 1);
    evaluate_start_buttons();
    if ($('input[name=vd_type]:checked', '#vd_form').val() == 'vd') {
        $('#sites').append(get_site_div(actual_site, values));
    } else {
        $('#sites').append(get_weighted_site_div(actual_site, values));
    }
}

function add_site_event() {
    add_site({})
}

$('#add_site').click(add_site_event);
$('#random_sites').click(random_sites);

function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function random_sites() {
    console.log("hello")
    $('#sites').html("");
    $('#num_sites').attr("value", 0);
    $('#actual_sites').attr("value", 0);
    var min_x = parseInt($('#limit_x0').val());
    min_x = (min_x != null ? min_x : -100);
    var max_x = parseInt($('#limit_x1').val());
    max_x = (max_x != null ? max_x : 100);
    var min_y = parseInt($('#limit_y0').val());
    min_y = (min_y != null ? min_y : -100);
    var max_y = parseInt($('#limit_y1').val());
    max_y = (max_y != null ? max_y : 100);
    var min_w = 0;
    var max_w = 20;
    for (let i = 0; i < parseInt($('#num_random_sites').val()); i++) {
        var values = { x: getRndInteger(min_x, max_x), y: getRndInteger(min_y, max_y), w: getRndInteger(min_w, max_w), name: (i + 1).toString() };
        add_site(values);
    }
}

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

async function write_plot(resp) {
    $('#plot').html(resp);
}

$('#plot-vd').click(function () {
    data = getFormData(vd_form);
    data["sites"] = get_sites();
    $('#loading').html(loading_content());
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
                    write_plot(resp).then(() => {
                        $('#loading').html("")
                        // Step buttons.
                        $('#next-step').attr('disabled', 'disabled');
                        $('#next-step-responsive').attr('disabled', 'disabled');
                        $('#prev-step').attr('disabled', 'disabled');
                        $('#prev-step-responsive').attr('disabled', 'disabled');
                        $('#download-ggb').removeAttr('disabled');
                        $('#download-ggb-responsive').removeAttr('disabled');
                        // Actual Event
                        $('#actual_event').html("");
                        // Queue
                        $('#qqueue').html("");
                        // LList
                        $('#llist').html("");
                    });
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
    $('#loading').html(loading_content());
    $.ajax({
        type: 'GET',
        url: '/steps/first/',
        dataType: 'html',
        data: { body: JSON.stringify(data), session: session },
        success: function (resp) {
            write_plot(resp).then(() => {
                $('#loading').html("")
                get_info()
            });
        },
        error: function (resp) {
            $('#loading').html("")
            console.log(resp);
        }
    });
})

function next_step() {
    $('#loading').html(loading_content());
    $.ajax({
        type: 'GET',
        url: '/steps/next/',
        dataType: 'html',
        data: { session: session },
        success: function (resp) {
            write_plot(resp).then(() => {
                $('#loading').html("")
                get_info()
            });
        },
        error: function (resp) {
            $('#loading').html("")
            console.log(resp);
        }
    });
}

$('#next-step').click(next_step)

$('#next-step-responsive').click(next_step)

function prev_step() {
    $('#loading').html(loading_content());
    $.ajax({
        type: 'GET',
        url: '/steps/prev/',
        dataType: 'html',
        data: { session: session },
        success: function (resp) {
            write_plot(resp).then(() => {
                $('#loading').html("")
                get_info()
            });
        },
        error: function (resp) {
            $('#loading').html("")
            console.log(resp);
        }
    });
}

$('#prev-step').click(prev_step)
$('#prev-step-responsive').click(prev_step)

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
    var boundary_div = "";
    if (boundary.active) {
        boundary_div = "<div class='LBoundary active-boundary'>";
    } else if (boundary.is_to_be_deleted) {
        boundary_div = "<div class='LBoundary intersection'>";
    } else {
        boundary_div = "<div class='LBoundary'>";
    }
    if (boundary.is_null) {
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

function get_region_div(region) {
    var region_div = "'>";
    if (region.active) {
        region_div = "<div class='LRegion active-region'>";
    } else if (region.is_to_be_deleted) {
        region_div = "<div class='LRegion intersection'>";
    } else {
        region_div = "<div class='LRegion'>";
    }

    region_div += "R(" + region.site.name + ")";
    region_div += "</div>";
    return region_div;
}

function loading_content() {
    return `<span>↓</span>
        <span style="--delay: 0.1s">↓</span>
        <span style="--delay: 0.3s">↓</span>
        <span style="--delay: 0.4s">↓</span>
        <span style="--delay: 0.5s">↓</span>
    `
}

function get_info() {
    $('#qqueue').html(loading_content())
    $('#llist').html(loading_content())
    $('#actual_event').html(loading_content())
    $.ajax({
        type: 'GET',
        url: '/steps/info/',
        dataType: 'json',
        data: { session: session },
        success: function (resp) {
            console.log(resp);
            $('#qqueue').html("");
            $('#qqueue-responsive').html("");
            $('#llist').html("");
            $('#actual_event').html("");
            $('#actual_event-responsive').html("");

            // L List
            console.log(resp)
            if (resp.l_structure.length > 0) {
                left_boundary = { is_null: true, active: false }
                resp.l_structure[0].left = left_boundary
                $('#llist').append(get_boundary_div(resp.l_structure[0].left));
            }
            for (let i = 0; i < resp.l_structure.length; i++) {
                var region = resp.l_structure[i]
                if (region.right == null) {
                    right_boundary = { is_null: true, active: false }
                    region.right = right_boundary
                }
                $('#llist').append(get_region_div(region));
                $('#llist').append(get_boundary_div(region.right));
            }

            // Q Queue
            for (let i = 0; i < resp.q_structure.length; i++) {
                var event = resp.q_structure[i]
                var event_div = "<div class='event'>" + event.event_str + "</div>"
                $('#qqueue').append(event_div);
                $('#qqueue-responsive').append(event_div);
            }

            // Actual Event
            if (resp.actual_event) {
                var actual_event = resp.actual_event
                var actual_event_div = "<div class='event'>" + actual_event.event_str + "</div>"
                $('#actual_event').html(actual_event_div);
                $('#actual_event-responsive').html(actual_event_div);
            }

            // Steps
            if (resp.is_next_step || !resp.is_diagram) {
                $('#next-step').removeAttr('disabled');
                $('#next-step-responsive').removeAttr('disabled');
                $('#download-ggb').attr('disabled', 'disabled');
                $('#download-ggb-responsive').attr('disabled', 'disabled');
            } else {
                $('#next-step').attr('disabled', 'disabled');
                $('#next-step-responsive').attr('disabled', 'disabled');
                $('#download-ggb').removeAttr('disabled');
                $('#download-ggb-responsive').removeAttr('disabled');
            }
            if (resp.is_prev_step) {
                $('#prev-step').removeAttr('disabled');
                $('#prev-step-responsive').removeAttr('disabled');
            } else {
                $('#prev-step').attr('disabled', 'disabled');
                $('#prev-step-responsive').attr('disabled', 'disabled');
            }
        },
        error: function (resp) {
            console.log(resp);
        }
    });
}

$('#prev-step').attr('disabled', 'disabled');
$('#next-step').attr('disabled', 'disabled');
$('#prev-step-responsive').attr('disabled', 'disabled');
$('#next-step-responsive').attr('disabled', 'disabled');
$('#download-ggb').attr('disabled', 'disabled');
$('#download-ggb-responsive').attr('disabled', 'disabled');
evaluate_start_buttons();
add_site_event();

$(document).ready(function () {
    $('#sidebarOpen').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
    $('#sidebarOpen-responsive').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
    $('#left').on('click', function () {
        if ($('#sidebar').hasClass('active')) {
            $('#sidebar').toggleClass('active');
        }
    });
    $('#step_info').on('click', function () {
        if ($('#sidebar').hasClass('active')) {
            $('#sidebar').toggleClass('active');
        }
    });
    $('#llist_container').on('click', function () {
        if ($('#sidebar').hasClass('active')) {
            $('#sidebar').toggleClass('active');
        }
    });
    $('#sidebar').toggleClass('active');
});

function download_gpp() {
    var a = document.createElement("a");
    a.href = '/geogebra/gpp/?session=' + session;
    a.setAttribute("download", "voronoi_diagram.ggb");
    a.click();
}

$('#download-ggb').click(download_gpp)
$('#download-ggb-responsive').click(download_gpp)