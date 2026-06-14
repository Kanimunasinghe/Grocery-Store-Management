// Define your api here
var productListApiUrl = 'http://127.0.0.1:5000/getProducts';
var uomListApiUrl = 'http://127.0.0.1:5000/getUOM';
var productSaveApiUrl = 'http://127.0.0.1:5000/insertProduct';
var productDeleteApiUrl = 'http://127.0.0.1:5000/deleteProducts';
var orderListApiUrl = 'http://127.0.0.1:5000/getAllOrders';
var orderSaveApiUrl = 'http://127.0.0.1:5000/insertOrder';
var orderGetByIdApiUrl = 'http://127.0.0.1:5000/getOrderById';
var orderUpdateApiUrl = 'http://127.0.0.1:5000/updateOrder';
var orderSearchApiUrl = 'http://127.0.0.1:5000/searchOrders';
var orderSearchAdvancedApiUrl = 'http://127.0.0.1:5000/searchOrdersAdvanced';
var productSearchApiUrl = 'http://127.0.0.1:5000/searchProducts';
var productSearchAdvancedApiUrl = 'http://127.0.0.1:5000/searchProductsAdvanced';
var signupApiUrl = 'http://127.0.0.1:5000/signup';
var signinApiUrl = 'http://127.0.0.1:5000/signin';
var logoutApiUrl = 'http://127.0.0.1:5000/logout';
var inventoryListApiUrl = 'http://127.0.0.1:5000/getInventory';
var lowStockApiUrl = 'http://127.0.0.1:5000/getLowStockItems';
var adjustStockApiUrl = 'http://127.0.0.1:5000/adjustStock';
var updateReorderLevelsApiUrl = 'http://127.0.0.1:5000/updateReorderLevels';
var stockTransactionsApiUrl = 'http://127.0.0.1:5000/getStockTransactions';
var searchInventoryApiUrl = 'http://127.0.0.1:5000/searchInventory';
var dashboardStatsApiUrl = 'http://127.0.0.1:5000/getDashboardStats';
var revenueTrendsApiUrl = 'http://127.0.0.1:5000/getRevenueTrends';
var topProductsApiUrl = 'http://127.0.0.1:5000/getTopProducts';
var revenueByProductApiUrl = 'http://127.0.0.1:5000/getRevenueByProduct';
var monthlyRevenueApiUrl = 'http://127.0.0.1:5000/getMonthlyRevenue';
var customerStatsApiUrl = 'http://127.0.0.1:5000/getCustomerStats';
var inventoryOverviewApiUrl = 'http://127.0.0.1:5000/getInventoryOverview';


// For product drop in order
var productsApiUrl = 'https://fakestoreapi.com/products';

function callApi(method, url, data) {
    $.ajax({
        method: method,
        url: url,
        data: data
    }).done(function( msg ) {
        window.location.reload();
    });
}

function calculateValue() {
    var total = 0;
    $(".product-item").each(function( index ) {
        var qty = parseFloat($(this).find('.product-qty').val()) || 0;
        var price = parseFloat($(this).find('.product-price').val()) || 0;
        var lineTotal = price * qty;
        $(this).find('.product-total').val(lineTotal.toFixed(2));
        total += lineTotal;
    });
    $("#product_grand_total").val(total.toFixed(2));
}

function orderParser(order) {
    return {
        id : order.id,
        date : order.employee_name,
        orderNo : order.employee_name,
        customerName : order.employee_name,
        cost : parseInt(order.employee_salary)
    }
}

function productParser(product) {
    return {
        id : product.id,
        name : product.employee_name,
        unit : product.employee_name,
        price : product.employee_name
    }
}

function productDropParser(product) {
    return {
        id : product.id,
        name : product.title
    }
}

//To enable bootstrap tooltip globally
// $(function () {
//     $('[data-toggle="tooltip"]').tooltip()
// });