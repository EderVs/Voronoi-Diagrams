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

$(function () {
    $('#add_site').click(function () {
        if ($('input[name=vd_type]:checked', '#vd_form').val() == 'vd') {
            $('#sites').append(get_site_div($('#actual_sites').attr("value")))
        } else {
            $('#sites').append(get_weighted_site_div($('#actual_sites').attr("value")))
        }
        $('#num_sites').attr("value", parseInt($('#num_sites').attr("value")) + 1)
        $('#actual_sites').attr("value", parseInt($('#actual_sites').attr("value")) + 1)
    });
});

$('input[name=vd_type]', '#vd_form').click(function () {
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
});

function remove_site(site_id) {
    $('#site_' + site_id).remove()
    $('#num_sites').attr("value", parseInt($('#num_sites').attr("value")) - 1)
}

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

    sendData();
});

function sendData() {
    data = getFormData(vd_form);
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
    data["sites"] = sites;
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
        }
    });
}