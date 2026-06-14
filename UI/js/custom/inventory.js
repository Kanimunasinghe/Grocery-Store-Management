$(function() {
    loadAllInventory();
    loadLowStockItems();
});

// =============== LOAD ALL INVENTORY ===============
function loadAllInventory() {
    $.ajax({
        url: inventoryListApiUrl,
        type: 'GET',
        success: function(data) {
            displayInventory(data);
        },
        error: function(error) {
            console.log("Error loading inventory:", error);
            $('#inventoryTableContainer').html('<div class="alert alert-danger">Error loading inventory</div>');
        }
    });
}

function displayInventory(inventories) {
    if (inventories.length === 0) {
        $('#inventoryTableContainer').html('<div class="alert alert-info">No inventory found</div>');
        return;
    }

    let tableHtml = `
        <table class="table table-striped table-hover">
            <thead class="table-light">
                <tr>
                    <th>Product ID</th>
                    <th>Product Name</th>
                    <th>Unit</th>
                    <th>Qty On Hand</th>
                    <th>Reorder Level</th>
                    <th>Status</th>
                    <th>Last Updated</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
    `;

    inventories.forEach(function(item) {
        let statusBadge = item.status === 'Low Stock' 
            ? `<span class="badge badge-low"><i class="fas fa-exclamation-triangle"></i> ${item.status}</span>`
            : `<span class="badge badge-good"><i class="fas fa-check"></i> ${item.status}</span>`;

        let rowClass = item.status === 'Low Stock' ? 'low-stock-row' : '';

        tableHtml += `
            <tr class="${rowClass}">
                <td><strong>${item.product_id}</strong></td>
                <td>${item.product_name}</td>
                <td>${item.uom_name}</td>
                <td>
                    <strong>${item.quantity_on_hand}</strong>
                </td>
                <td>${item.reorder_level}</td>
                <td>${statusBadge}</td>
                <td><small>${item.last_updated.substring(0, 19)}</small></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="openAdjustModal(${item.product_id}, '${item.product_name}', ${item.quantity_on_hand})" title="Adjust Stock">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-secondary" onclick="openReorderModal(${item.product_id}, '${item.product_name}', ${item.reorder_level}, ${item.reorder_quantity})" title="Reorder Settings">
                        <i class="fas fa-cog"></i>
                    </button>
                </td>
            </tr>
        `;
    });

    tableHtml += `
            </tbody>
        </table>
    `;

    $('#inventoryTableContainer').html(tableHtml);
}

// =============== SEARCH INVENTORY ===============
function searchInventory() {
    let searchProductName = $('#searchProductName').val().trim();
    let searchProductId = $('#searchProductId').val().trim();

    if (!searchProductName && !searchProductId) {
        alert('Please enter product name or ID');
        return;
    }

    let searchType = searchProductId ? 'product_id' : 'product_name';
    let searchValue = searchProductId || searchProductName;

    $.ajax({
        url: searchInventoryApiUrl,
        type: 'GET',
        data: {
            search_type: searchType,
            search_value: searchValue
        },
        success: function(data) {
            displayInventory(data);
        },
        error: function(error) {
            console.log("Error searching inventory:", error);
            alert('Error searching inventory');
        }
    });
}

function resetInventorySearch() {
    $('#searchProductName').val('');
    $('#searchProductId').val('');
    loadAllInventory();
}

// =============== ADJUST STOCK ===============
function openAdjustModal(productId, productName, currentQty) {
    $('#adjustProductId').val(productId);
    $('#adjustProductName').val(productName);
    $('#adjustCurrentQty').val(currentQty);
    $('#adjustmentQty').val('');
    $('#adjustmentNotes').val('');
    
    let adjustModal = new bootstrap.Modal(document.getElementById('adjustStockModal'));
    adjustModal.show();
}

function saveAdjustment() {
    let productId = $('#adjustProductId').val();
    let adjustmentQty = parseFloat($('#adjustmentQty').val());
    let notes = $('#adjustmentNotes').val().trim();

    if (!adjustmentQty || adjustmentQty === 0) {
        alert('Please enter adjustment quantity');
        return;
    }

    let data = {
        product_id: parseInt(productId),
        adjustment_quantity: adjustmentQty,
        notes: notes || 'Manual adjustment'
    };

    $.ajax({
        url: adjustStockApiUrl,
        type: 'POST',
        data: {
            data: JSON.stringify(data)
        },
        success: function(response) {
            alert('Stock adjusted successfully!');
            bootstrap.Modal.getInstance(document.getElementById('adjustStockModal')).hide();
            loadAllInventory();
            loadLowStockItems();
        },
        error: function(error) {
            console.log("Error adjusting stock:", error);
            alert('Error adjusting stock');
        }
    });
}

// =============== REORDER LEVELS ===============
function openReorderModal(productId, productName, reorderLevel, reorderQty) {
    $('#reorderProductId').val(productId);
    $('#reorderProductName').val(productName);
    $('#reorderLevel').val(reorderLevel);
    $('#reorderQuantity').val(reorderQty);
    
    let reorderModal = new bootstrap.Modal(document.getElementById('reorderLevelsModal'));
    reorderModal.show();
}

function saveReorderLevels() {
    let productId = $('#reorderProductId').val();
    let reorderLevel = parseInt($('#reorderLevel').val());
    let reorderQty = parseInt($('#reorderQuantity').val());

    if (!reorderLevel || !reorderQty) {
        alert('Please fill all fields');
        return;
    }

    let data = {
        product_id: parseInt(productId),
        reorder_level: reorderLevel,
        reorder_quantity: reorderQty
    };

    $.ajax({
        url: updateReorderLevelsApiUrl,
        type: 'POST',
        data: {
            data: JSON.stringify(data)
        },
        success: function(response) {
            alert('Reorder levels updated successfully!');
            bootstrap.Modal.getInstance(document.getElementById('reorderLevelsModal')).hide();
            loadAllInventory();
        },
        error: function(error) {
            console.log("Error updating reorder levels:", error);
            alert('Error updating reorder levels');
        }
    });
}

// =============== LOW STOCK ITEMS ===============
function loadLowStockItems() {
    $.ajax({
        url: lowStockApiUrl,
        type: 'GET',
        success: function(data) {
            displayLowStockItems(data);
        },
        error: function(error) {
            console.log("Error loading low stock items:", error);
            $('#lowStockTableContainer').html('<div class="alert alert-danger">Error loading low stock items</div>');
        }
    });
}

function displayLowStockItems(items) {
    if (items.length === 0) {
        $('#lowStockTableContainer').html('<div class="alert alert-success"><i class="fas fa-check-circle"></i> All products are well stocked!</div>');
        return;
    }

    let tableHtml = `
        <div class="alert alert-warning mb-3">
            <i class="fas fa-exclamation-triangle"></i> <strong>${items.length}</strong> product(s) below reorder level
        </div>
        <table class="table table-striped">
            <thead class="table-danger">
                <tr>
                    <th>Product ID</th>
                    <th>Product Name</th>
                    <th>Unit</th>
                    <th>Current Stock</th>
                    <th>Reorder Level</th>
                    <th>Shortage</th>
                    <th>Suggested Order Qty</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
    `;

    items.forEach(function(item) {
        tableHtml += `
            <tr class="table-danger">
                <td><strong>${item.product_id}</strong></td>
                <td><strong>${item.product_name}</strong></td>
                <td>${item.uom_name}</td>
                <td><strong style="color: red;">${item.quantity_on_hand}</strong></td>
                <td>${item.reorder_level}</td>
                <td><strong>${item.shortage}</strong></td>
                <td>${item.reorder_quantity}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="openAdjustModal(${item.product_id}, '${item.product_name}', ${item.quantity_on_hand})">
                        <i class="fas fa-plus"></i> Add Stock
                    </button>
                </td>
            </tr>
        `;
    });

    tableHtml += `
            </tbody>
        </table>
    `;

    $('#lowStockTableContainer').html(tableHtml);
}

// =============== STOCK TRANSACTIONS ===============
function loadTransactions() {
    let transactionType = $('#transactionTypeFilter').val();

    $.ajax({
        url: stockTransactionsApiUrl,
        type: 'GET',
        data: {
            transaction_type: transactionType || null
        },
        success: function(data) {
            displayTransactions(data);
        },
        error: function(error) {
            console.log("Error loading transactions:", error);
            $('#transactionsTableContainer').html('<div class="alert alert-danger">Error loading transactions</div>');
        }
    });
}

function displayTransactions(transactions) {
    if (transactions.length === 0) {
        $('#transactionsTableContainer').html('<div class="alert alert-info">No transactions found</div>');
        return;
    }

    let tableHtml = `
        <table class="table table-striped table-sm">
            <thead class="table-light">
                <tr>
                    <th>Date/Time</th>
                    <th>Product</th>
                    <th>Type</th>
                    <th>Quantity</th>
                    <th>Reference</th>
                    <th>Notes</th>
                </tr>
            </thead>
            <tbody>
    `;

    transactions.forEach(function(txn) {
        let typeIcon = '';
        let typeBadgeClass = '';

        if (txn.transaction_type === 'order') {
            typeIcon = '<i class="fas fa-shopping-cart"></i>';
            typeBadgeClass = 'bg-danger';
        } else if (txn.transaction_type === 'purchase') {
            typeIcon = '<i class="fas fa-cart-plus"></i>';
            typeBadgeClass = 'bg-success';
        } else if (txn.transaction_type === 'adjustment') {
            typeIcon = '<i class="fas fa-edit"></i>';
            typeBadgeClass = 'bg-warning';
        } else if (txn.transaction_type === 'return') {
            typeIcon = '<i class="fas fa-undo"></i>';
            typeBadgeClass = 'bg-info';
        }

        let qtyColor = txn.quantity < 0 ? 'red' : 'green';
        let refText = txn.reference_id ? `#${txn.reference_id}` : '-';

        tableHtml += `
            <tr>
                <td><small>${txn.created_at.substring(0, 19)}</small></td>
                <td>${txn.product_name}</td>
                <td><span class="badge ${typeBadgeClass}">${typeIcon} ${txn.transaction_type}</span></td>
                <td><strong style="color: ${qtyColor};">${txn.quantity}</strong></td>
                <td>${refText}</td>
                <td><small>${txn.notes || '-'}</small></td>
            </tr>
        `;
    });

    tableHtml += `
            </tbody>
        </table>
    `;

    $('#transactionsTableContainer').html(tableHtml);
}

// Load transactions on page load
$(document).ready(function() {
    loadTransactions();
});
