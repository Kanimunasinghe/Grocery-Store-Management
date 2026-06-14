var productPrices = {};
var productOptionsHtml = '<option value="">--Select--</option>';
var currentOrderId = null;

function getQueryParam(param) {
    var urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function appendProductRow(product_id, quantity, price) {
    var row = $(".product-box").html();
    $(".product-box-extra").append(row);
    var lastRow = $(".product-box-extra .product-item").last();
    lastRow.find(".remove-row").removeClass('hideit');
    lastRow.find(".product-price").val(price);
    lastRow.find(".product-qty").val(quantity);
    lastRow.find("select").empty().html(productOptionsHtml);
    
    // Select the product
    if (product_id) {
        lastRow.find(".cart-product").val(product_id);
    }
}

function loadOrderData() {
    currentOrderId = getQueryParam('order_id');
    
    if (!currentOrderId) {
        alert('Order ID not found');
        window.location.href = 'index.html';
        return;
    }

    // Load products list
    $.get(productListApiUrl, function (response) {
        productPrices = {};
        if (response) {
            productOptionsHtml = '<option value="">--Select--</option>';
            $.each(response, function (index, product) {
                productOptionsHtml += '<option value="' + product.product_id + '">' + product.name + '</option>';
                productPrices[product.product_id] = product.price_per_unit;
            });
            
            // Load order data
            $.get(orderGetByIdApiUrl + '/' + currentOrderId, function (orderData) {
                if (orderData) {
                    // Fill customer name
                    $("#customerName").val(orderData.customer_name);
                    
                    // Clear existing rows
                    $(".product-box-extra").empty();
                    
                    // Populate order details
                    $.each(orderData.order_details, function (index, detail) {
                        appendProductRow(detail.product_id, detail.quantity, detail.price_per_unit);
                    });
                    
                    calculateValue();
                } else {
                    alert('Order not found');
                    window.location.href = 'index.html';
                }
            }).fail(function () {
                alert('Failed to load order data. Make sure the backend server is running on port 5000.');
                window.location.href = 'index.html';
            });
        }
    });
}

$(function () {
    loadOrderData();
});

$("#addMoreButton").click(function () {
    appendProductRow();
});

$(document).on("click", ".remove-row", function () {
    if ($(".product-box-extra .product-item").length === 1) {
        alert("At least one product is required.");
        return;
    }
    $(this).closest('.product-item').remove();
    calculateValue();
});

$(document).on("change", ".cart-product", function () {
    var product_id = $(this).val();
    var price = productPrices[product_id] || 0;
    $(this).closest('.product-item').find('.product-price').val(price);
    calculateValue();
});

$(document).on("change", ".product-qty", function () {
    calculateValue();
});

$("#updateOrder").on("click", function () {
    calculateValue();

    var formData = $("form").serializeArray();
    var requestPayload = {
        customer_name: null,
        total: null,
        order_details: []
    };

    for (var i = 0; i < formData.length; ++i) {
        var element = formData[i];
        var lastElement = null;

        switch (element.name) {
            case 'customerName':
                requestPayload.customer_name = element.value.trim();
                break;
            case 'product_grand_total':
                requestPayload.total = element.value;
                break;
            case 'product':
                if (element.value) {
                    requestPayload.order_details.push({
                        product_id: element.value,
                        quantity: null,
                        total: null
                    });
                }
                break;
            case 'qty':
                lastElement = requestPayload.order_details[requestPayload.order_details.length - 1];
                if (lastElement) {
                    lastElement.quantity = element.value;
                }
                break;
            case 'item_total':
                lastElement = requestPayload.order_details[requestPayload.order_details.length - 1];
                if (lastElement) {
                    lastElement.total_price = element.value;
                }
                break;
        }
    }

    if (!requestPayload.customer_name) {
        alert("Please enter a customer name.");
        return;
    }
    if (requestPayload.order_details.length === 0) {
        alert("Please add at least one product.");
        return;
    }

    requestPayload.grand_total = $("#product_grand_total").val();
    console.log("grand_total:", requestPayload.grand_total);
    console.log("full payload:", JSON.stringify(requestPayload));

    $.ajax({
        method: "POST",
        url: orderUpdateApiUrl + '/' + currentOrderId,
        data: {
            'data': JSON.stringify(requestPayload)
        }
    }).done(function () {
        alert("Order updated successfully!");
        window.location.href = 'index.html';
    }).fail(function () {
        alert("Failed to update order. Make sure the backend server is running on port 5000.");
    });
});