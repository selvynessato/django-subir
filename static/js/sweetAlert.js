function mostrarMensaje() {
    Swal.fire({
        position: 'top-center',
        icon: 'success',
        title: 'Tu compra se ha añadido al carrito',
        showConfirmButton: false,
        timer: 2000
    });
}