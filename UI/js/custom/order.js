var productPrices = {};
var productOptionsHtml = '<option value="">--Select--</option>';

function appendProductRow() {
    var row = $(".product-box").html();
    $(".product-box-extra").append(row);
    var lastRow = $(".product-box-extra .product-item").last();
    lastRow.find(".remove-row").removeClass('hideit');
    lastRow.find(".product-price").val('0.0');
    lastRow.find(".product-qty").val('1');
    lastRow.find(".product-total").val('0.0');
    lastRow.find("select").empty().html(productOptionsHtml);
}

$(function () {
    $.get(productListApiUrl, function (response) {
        productPrices = {};
        if (response) {
            productOptionsHtml = '<option value="">--Select--</option>';
            $.each(response, function (index, product) {
                productOptionsHtml += '<option value="' + product.product_id + '">' + product.name + '</option>';
                productPrices[product.product_id] = product.price_per_unit;
            });
            $(".product-box").find("select").empty().html(productOptionsHtml);
            appendProductRow();
        }
    });
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

$("#saveOrder").on("click", function () {
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
        url: orderSaveApiUrl,
        data: {
            'data': JSON.stringify(requestPayload)
        }
    }).done(function () {
        window.location.href = 'index.html';
    }).fail(function () {
        alert("Failed to save order. Make sure the backend server is running on port 5000.");
    });
});
