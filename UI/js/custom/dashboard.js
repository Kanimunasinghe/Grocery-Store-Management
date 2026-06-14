function loadAllOrders() {
    $.get(orderListApiUrl, function (response) {
        displayOrders(response);
    }).fail(function () {
        $('#ordersTable tbody').empty().html(
            '<tr><td colspan="5" class="text-center text-danger">' +
            'Could not load orders. Make sure the backend server is running on port 5000.</td></tr>'
        );
    });
}

function displayOrders(response) {
    var table = '';
    var totalCost = 0;

    if (!response || response.length === 0) {
        table = '<tr><td colspan="5" class="text-center">No orders found.</td></tr>';
    } else {
        $.each(response, function (index, order) {
            var orderTotal = parseFloat(order.total) || 0;
            totalCost += orderTotal;
            table += '<tr>' +
                '<td>' + order.datetime + '</td>' +
                '<td>' + order.order_id + '</td>' +
                '<td>' + order.customer_name + '</td>' +
                '<td>Rs.' + orderTotal.toFixed(2) + '</td>' +
                '<td><a href="edit-order.html?order_id=' + order.order_id + '" class="btn btn-xs btn-info">Edit</a></td></tr>';
        });
        table += '<tr><td colspan="4" style="text-align: end"><b>Total</b></td><td><b>Rs.' +
            totalCost.toFixed(2) + '</b></td></tr>';
    }

    $('#ordersTable tbody').empty().html(table);
}

$(function () {
    // Load all orders on page load
    loadAllOrders();

    // Search button click
    $("#searchBtn").on("click", function() {
        var customerName = $("#searchCustomerName").val();
        var orderId = $("#searchOrderId").val();
        var startDate = $("#searchStartDate").val();
        var endDate = $("#searchEndDate").val();

        // Build URL with parameters
        var url = orderSearchAdvancedApiUrl + '?';
        var params = [];
        
        if (customerName) {
            params.push('customer_name=' + encodeURIComponent(customerName));
        }
        if (orderId) {
            params.push('order_id=' + encodeURIComponent(orderId));
        }
        if (startDate) {
            params.push('start_date=' + encodeURIComponent(startDate));
        }
        if (endDate) {
            params.push('end_date=' + encodeURIComponent(endDate));
        }

        if (params.length === 0) {
            alert("Please enter at least one search criteria");
            return;
        }

        url += params.join('&');

        $.get(url, function(response) {
            displayOrders(response);
        }).fail(function() {
            $('#ordersTable tbody').empty().html(
                '<tr><td colspan="5" class="text-center text-danger">' +
                'Error searching orders. Please try again.</td></tr>'
            );
        });
    });

    // Reset button click
    $("#resetBtn").on("click", function() {
        $("#searchCustomerName").val('');
        $("#searchOrderId").val('');
        $("#searchStartDate").val('');
        $("#searchEndDate").val('');
        loadAllOrders();
    });

    // Allow search on Enter key press in search fields
    $("#searchCustomerName, #searchOrderId, #searchStartDate, #searchEndDate").on("keypress", function(e) {
        if (e.which == 13) { // Enter key
            $("#searchBtn").click();
            return false;
        }
    });
});