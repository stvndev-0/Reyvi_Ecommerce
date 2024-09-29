function volver(){
    window.history.back();
}

// Funcion para mostrar mensaje
function showMessages(messages){
    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = '';  // Limpiar cualquier mensaje anterior
    
    // Añadir cada mensaje recibido al contenedor
    messages.forEach(message => {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-warning alert-dismissible fade show';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        messagesContainer.appendChild(alertDiv);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var message = localStorage.getItem('message');
    
    if (message) {
        // Mostrar el mensaje
        showMessages(JSON.parse(message));
        
        // Eliminar el mensaje del localStorage
        localStorage.removeItem('message');
    }
});

// Cart
const button_add = document.getElementById('add-cart')
const button_update = document.getElementById('update-cart')
const button_delete = document.getElementById('product-removed')

if (button_add) {
    button_add.addEventListener('click', function(){
        fetch(addCartUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                product_id: document.getElementById('add-cart').value,
                product_qty: document.getElementById('qty-cart').value,
                action: 'post'
            })
        })
        .then(response => response.json())
        .then(data => {
            showMessages(data.messages)
            document.getElementById('cart_quantity').textContent = data.qty;
        })
        .catch(error => console.error('Error al añadir el producto al carrito:', error));
    });
}

if (button_update) {
    button_update.addEventListener('click', function(){
        var quantities = {};
    
        // Recorre todos los inputs de cantidad en la tabla
        document.querySelectorAll('.product-quantity').forEach(function(input) {
            var productId = input.getAttribute('data-index');
            var quantity = input.value;
            quantities[productId] = quantity;
        });
        
        // Enviar las cantidades actualizadas al servidor mediante fetch
        fetch('update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                action: 'post',
                quantities: quantities
            })
        })
        .then(response => response.json())
        .then(data => {
            showMessages(data.messages);
            // Actualizar los totales después de la actualización
            for (var productId in data.updated_totals) {
                document.getElementById('total-' + productId).innerText = '$' + data.updated_totals[productId];
            }
            // Actualizar el total del carrito
            document.getElementById('cart-total').innerText = '$' + data.new_cart_total;
        })
        .catch(error => console.error('Error al actualizar el carrito:', error));
    });
}

if (button_delete){
    button_delete.addEventListener('click', function(e) { 
        const productid = e.target.dataset.index;

        fetch('delete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Asegúrate de que la cabecera CSRF es necesaria según tu configuración
            },
            body: JSON.stringify({
                product_id: productid,
                action: 'post'
            })
        })
        .then(response => response.json())
        .then(data => {
            showMessages(data.messages);
        })
        .catch(error => console.error('Error al eliminar el producto del carrito:', error));
    });
}
