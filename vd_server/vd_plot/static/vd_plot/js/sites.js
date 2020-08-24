function get_site_div(site_id) {
    return `<div class="site" id="site_` + site_id + `">
    <input type="text" placeholder="Name" name="site`+ site_id + `_name">
    <input type="text" placeholder="Site x" name="site`+ site_id + `_x" required>
    <input type="text" placeholder="Site y" name="site`+ site_id + `_y" required>
    <button type="button" id="remove_site_`+ site_id + `" onclick="remove_site(` + site_id + `)">Remove Site</button>
    </div>`
}
function get_weighted_site_div(site_id) {
    return `<div class="site" id="site_` + site_id + `">
    <input type="text" placeholder="Name" name="site`+ site_id + `_name">
    <input type="text" placeholder="Site x" name="site`+ site_id + `_x" required>
    <input type="text" placeholder="Site y" name="site`+ site_id + `_y" required>
    <input type="text" placeholder="Site weight" name="site`+ site_id + `_w" required>
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

function remove_site(site_id) {
    $('#site_' + site_id).remove()
    $('#num_sites').attr("value", parseInt($('#num_sites').attr("value")) - 1)
}