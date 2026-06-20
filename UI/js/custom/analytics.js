// Chart instances
let revenueTrendChart = null;
let monthlyRevenueChart = null;
let topProductsChart = null;
let revenueByProductChart = null;

$(function() {
    loadDashboardAnalytics();
    
    // Set default dates (last 30 days)
    let today = new Date();
    let thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000));
    
    $('#endDate').val(formatDateForInput(today));
    $('#startDate').val(formatDateForInput(thirtyDaysAgo));
});

// =============== LOAD ALL DASHBOARD DATA ===============
function loadDashboardAnalytics() {
    console.log("Loading dashboard analytics...");
    loadDashboardStats();
    loadRevenueTrends();
    loadMonthlyRevenue();
    loadTopSellingProducts();
    loadRevenueByProduct();
    loadTopCustomers();
    loadInventoryOverview();
}

// =============== DASHBOARD STATS ===============
function loadDashboardStats() {
    $.ajax({
        url: dashboardStatsApiUrl,
        type: 'GET',
        success: function(data) {
            console.log("Dashboard stats loaded:", data);
            $('#totalRevenue').text('₨' + formatNumber(data.total_revenue));
            $('#totalOrders').text(data.total_orders);
            $('#avgOrderValue').text('₨' + formatNumber(data.average_order_value));
            $('#productsInStock').text(data.products_in_stock);
            $('#lowStockCount').text(data.low_stock_count);
        },
        error: function(error) {
            console.log("Error loading dashboard stats:", error);
            alert('Error loading statistics');
        }
    });
}

// =============== REVENUE TRENDS ===============
function loadRevenueTrends() {
    let startDate = $('#startDate').val();
    let endDate = $('#endDate').val();
    
    console.log("Loading revenue trends from", startDate, "to", endDate);
    
    $.ajax({
        url: revenueTrendsApiUrl,
        type: 'GET',
        data: {
            start_date: startDate || null,
            end_date: endDate || null
        },
        success: function(data) {
            console.log("Revenue trends loaded:", data);
            if (data.length > 0) {
                displayRevenueTrendChart(data);
            } else {
                console.log("No revenue trend data");
            }
        },
        error: function(error) {
            console.log("Error loading revenue trends:", error);
        }
    });
}

function displayRevenueTrendChart(data) {
    let labels = data.map(item => item.date);
    let revenues = data.map(item => item.revenue);
    
    let ctx = document.getElementById('revenueTrendChart').getContext('2d');
    
    if (revenueTrendChart) {
        revenueTrendChart.destroy();
    }
    
    revenueTrendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Daily Revenue',
                data: revenues,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 5,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: { size: 12, weight: 'bold' }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₨' + formatNumber(value);
                        }
                    }
                }
            }
        }
    });
}

// =============== MONTHLY REVENUE ===============
function loadMonthlyRevenue() {
    $.ajax({
        url: monthlyRevenueApiUrl,
        type: 'GET',
        success: function(data) {
            console.log("Monthly revenue loaded:", data);
            if (data.length > 0) {
                displayMonthlyRevenueChart(data);
            }
        },
        error: function(error) {
            console.log("Error loading monthly revenue:", error);
        }
    });
}

function displayMonthlyRevenueChart(data) {
    let labels = data.map(item => item.month);
    let revenues = data.map(item => item.revenue);
    
    let ctx = document.getElementById('monthlyRevenueChart').getContext('2d');
    
    if (monthlyRevenueChart) {
        monthlyRevenueChart.destroy();
    }
    
    monthlyRevenueChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Monthly Revenue',
                data: revenues,
                backgroundColor: [
                    '#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe',
                    '#43e97b', '#fa709a', '#fee140', '#30cfd0', '#330867',
                    '#667eea', '#764ba2'
                ],
                borderRadius: 5,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: { size: 12, weight: 'bold' }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₨' + formatNumber(value);
                        }
                    }
                }
            }
        }
    });
}

// =============== TOP SELLING PRODUCTS ===============
function loadTopSellingProducts() {
    let startDate = $('#startDate').val();
    let endDate = $('#endDate').val();
    
    $.ajax({
        url: topProductsApiUrl,
        type: 'GET',
        data: {
            start_date: startDate || null,
            end_date: endDate || null,
            limit: 10
        },
        success: function(data) {
            console.log("Top products loaded:", data);
            if (data.length > 0) {
                displayTopProductsChart(data);
            }
        },
        error: function(error) {
            console.log("Error loading top products:", error);
        }
    });
}

function displayTopProductsChart(data) {
    let labels = data.map(item => item.product_name);
    let quantities = data.map(item => item.total_quantity);
    
    let ctx = document.getElementById('topProductsChart').getContext('2d');
    
    if (topProductsChart) {
        topProductsChart.destroy();
    }
    
    topProductsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Quantity Sold',
                data: quantities,
                backgroundColor: '#667eea',
                borderColor: '#764ba2',
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return parseInt(value);
                        }
                    }
                }
            }
        }
    });
}

// =============== REVENUE BY PRODUCT ===============
function loadRevenueByProduct() {
    let startDate = $('#startDate').val();
    let endDate = $('#endDate').val();
    
    $.ajax({
        url: revenueByProductApiUrl,
        type: 'GET',
        data: {
            start_date: startDate || null,
            end_date: endDate || null,
            limit: 10
        },
        success: function(data) {
            console.log("Revenue by product loaded:", data);
            if (data.length > 0) {
                displayRevenueByProductChart(data);
            }
        },
        error: function(error) {
            console.log("Error loading revenue by product:", error);
        }
    });
}

function displayRevenueByProductChart(data) {
    let labels = data.map(item => item.product_name);
    let revenues = data.map(item => item.total_revenue);
    
    let colors = [
        '#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe',
        '#43e97b', '#fa709a', '#fee140', '#30cfd0', '#330867'
    ];
    
    let ctx = document.getElementById('revenueByProductChart').getContext('2d');
    
    if (revenueByProductChart) {
        revenueByProductChart.destroy();
    }
    
    revenueByProductChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: revenues,
                backgroundColor: colors,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 10 },
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '₨' + formatNumber(context.parsed);
                        }
                    }
                }
            }
        }
    });
}

// =============== TOP CUSTOMERS ===============
function loadTopCustomers() {
    let startDate = $('#startDate').val();
    let endDate = $('#endDate').val();
    
    console.log("Loading top customers...");
    console.log("Start Date:", startDate, "End Date:", endDate);
    
    $.ajax({
        url: customerStatsApiUrl,
        type: 'GET',
        data: {
            start_date: startDate && startDate.trim() ? startDate : '',
            end_date: endDate && endDate.trim() ? endDate : ''
        },
        success: function(data) {
            console.log("Top customers loaded:", data);
            displayTopCustomers(data);
        },
        error: function(error) {
            console.log("Error loading top customers:", error);
            $('#topCustomersTable').html('<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> Error loading customers. Please try again.</div>');
        }
    });
}

function displayTopCustomers(customers) {
    console.log("Displaying customers count:", customers.length);
    
    if (!customers || customers.length === 0) {
        $('#topCustomersTable').html('<div class="alert alert-info"><i class="fas fa-info-circle"></i> No customer data found for selected date range</div>');
        return;
    }
    
    let tableHtml = `
        <table class="table table-striped table-hover">
            <thead class="table-light">
                <tr>
                    <th>Customer Name</th>
                    <th>Total Orders</th>
                    <th>Total Spent</th>
                    <th>Avg Order Value</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    customers.forEach(function(customer, index) {
        let totalSpent = customer.total_spent ? parseFloat(customer.total_spent) : 0;
        let avgSpent = customer.avg_spent ? parseFloat(customer.avg_spent) : 0;
        let orderCount = customer.order_count ? parseInt(customer.order_count) : 0;
        
        tableHtml += `
            <tr>
                <td><strong>${customer.customer_name || 'Unknown'}</strong></td>
                <td><span class="badge bg-primary">${orderCount}</span></td>
                <td>₨${formatNumber(totalSpent)}</td>
                <td>₨${formatNumber(avgSpent)}</td>
            </tr>
        `;
    });
    
    tableHtml += `
            </tbody>
        </table>
    `;
    
    $('#topCustomersTable').html(tableHtml);
    console.log("Customers table displayed successfully");
}
// =============== INVENTORY OVERVIEW ===============
function loadInventoryOverview() {
    $.ajax({
        url: inventoryOverviewApiUrl,
        type: 'GET',
        success: function(data) {
            console.log("Inventory overview loaded:", data);
            $('#invTotalProducts').text(data.total_products);
            $('#invInStock').text(data.in_stock);
            $('#invLowStock').text(data.low_stock);
            $('#invOutOfStock').text(data.out_of_stock);
            $('#stockValue').text('₨' + formatNumber(data.total_stock_value));
        },
        error: function(error) {
            console.log("Error loading inventory overview:", error);
        }
    });
}

// =============== DATE FILTER ===============
function applyDateFilter() {
    console.log("Applying date filter...");
    loadDashboardAnalytics();
    alert('Analytics updated for selected date range!');
}

function resetDateFilter() {
    console.log("Resetting date filter...");
    let today = new Date();
    let thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000));
    
    $('#endDate').val(formatDateForInput(today));
    $('#startDate').val(formatDateForInput(thirtyDaysAgo));
    
    loadDashboardAnalytics();
}

// =============== UTILITY FUNCTIONS ===============
function formatNumber(num) {
    if (!num) return '0.00';
    return (Math.round(num * 100) / 100).toFixed(2);
}

function formatDateForInput(date) {
    let year = date.getFullYear();
    let month = String(date.getMonth() + 1).padStart(2, '0');
    let day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function logout() {
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = "login.html";
}
