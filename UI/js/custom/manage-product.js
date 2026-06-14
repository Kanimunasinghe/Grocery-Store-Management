var productModal = $("#productModal");

function loadAllProducts() {
    $.get(productListApiUrl, function (response) {
        displayProducts(response);
    });
}

function displayProducts(response) {
    if(response) {
        var table = '';
        $.each(response, function(index, products) {
            table += '<tr data-id="'+ products.product_id +'" data-name="'+ products.name +'" data-unit="'+ products.uom_id +'" data-price="'+ products.price_per_unit +'">' +
                '<td>'+ products.name +'</td>'+
                '<td>'+ products.uom_name +'</td>'+
                '<td>'+ products.price_per_unit +'</td>'+
                '<td><span class="btn btn-xs btn-danger delete-product">Delete</span></td></tr>';
        });
        $("table").find('tbody').empty().html(table);
    }
}

$(function () {
    // Load all products on page load
    loadAllProducts();

    // Load UOM list for search filter
    $.get(uomListApiUrl, function (response) {
        if(response) {
            var options = '<option value="">--Select Unit--</option>';
            $.each(response, function(index, uom) {
                options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
            });
            $("#searchUomId").empty().html(options);
        }
    });

    // Search button click
    $("#searchBtn").on("click", function() {
        var productName = $("#searchProductName").val();
        var productId = $("#searchProductId").val();
        var uomId = $("#searchUomId").val();
        var minPrice = $("#searchMinPrice").val();
        var maxPrice = $("#searchMaxPrice").val();

        // Build URL with parameters
        var url = productSearchAdvancedApiUrl + '?';
        var params = [];
        
        if (productName) {
            params.push('product_name=' + encodeURIComponent(productName));
        }
        if (productId) {
            params.push('product_id=' + encodeURIComponent(productId));
        }
        if (uomId) {
            params.push('uom_id=' + encodeURIComponent(uomId));
        }
        if (minPrice) {
            params.push('min_price=' + encodeURIComponent(minPrice));
        }
        if (maxPrice) {
            params.push('max_price=' + encodeURIComponent(maxPrice));
        }

        if (params.length === 0) {
            alert("Please enter at least one search criteria");
            return;
        }

        url += params.join('&');

        $.get(url, function(response) {
            displayProducts(response);
        }).fail(function() {
            $("table").find('tbody').empty().html(
                '<tr><td colspan="4" class="text-center text-danger">Error searching products. Please try again.</td></tr>'
            );
        });
    });

    // Reset button click
    $("#resetBtn").on("click", function() {
        $("#searchProductName").val('');
        $("#searchProductId").val('');
        $("#searchUomId").val('');
        $("#searchMinPrice").val('');
        $("#searchMaxPrice").val('');
        loadAllProducts();
    });

    // Allow search on Enter key press in search fields
    $("#searchProductName, #searchProductId, #searchMinPrice, #searchMaxPrice").on("keypress", function(e) {
        if (e.which == 13) { // Enter key
            $("#searchBtn").click();
            return false;
        }
    });
});

// Save Product
     $("#saveProduct").on("click", function () {
        // If we found id value in form then update product detail
        var data = $("#productForm").serializeArray();
        var requestPayload = {
            product_name: null,
            uom_id: null,
            price_per_unit: null
        };
        for (var i=0;i<data.length;++i) {
            var element = data[i];
            switch(element.name) {
                case 'name':
                    requestPayload.product_name = element.value;
                    break;
                case 'uoms':
                    requestPayload.uom_id = element.value;
                    break;
                case 'price':
                    requestPayload.price_per_unit = element.value;
                    break;
            }
        }
        callApi("POST", productSaveApiUrl, {
            'data': JSON.stringify(requestPayload)
        });
    });

    $(document).on("click", ".delete-product", function (){
        var tr = $(this).closest('tr');
        var data = {
            product_id : tr.data('id')
        };
        var isDelete = confirm("Are you sure to delete "+ tr.data('name') +" item?");
        if (isDelete) {
            callApi("POST", productDeleteApiUrl, data);
        }
    });

    productModal.on('hide.bs.modal', function(){
        $("#id").val('0');
        $("#name, #unit, #price").val('');
        productModal.find('.modal-title').text('Add New Product');
    });

    productModal.on('show.bs.modal', function(){
        //JSON data by API call
        $.get(uomListApiUrl, function (response) {
            if(response) {
                var options = '<option value="">--Select--</option>';
                $.each(response, function(index, uom) {
                    options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
                });
                $("#uoms").empty().html(options);
            }
        });
    });