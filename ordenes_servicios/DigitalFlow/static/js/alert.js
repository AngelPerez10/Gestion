
document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const form = this.closest('.delete-form');
            Swal.fire({
                title: '¿Estás seguro?',
                text: '¡No podrás revertir esto!',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Envía el formulario
                    fetch(form.action, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        body: new FormData(form)
                    })
                        .then(response => {
                            if (response.ok) {
                                Swal.fire({
                                    icon: 'success',
                                    title: 'Orden eliminada',
                                    text: 'La orden fue eliminada exitosamente.',
                                    timer: 3000,
                                    showConfirmButton: false
                                }).then(() => {
                                    location.reload(); // Recarga la página para reflejar los cambios
                                });
                            } else {
                                Swal.fire({
                                    icon: 'error',
                                    title: 'Error',
                                    text: 'Ocurrió un error al intentar eliminar la orden.',
                                    showConfirmButton: true
                                });
                            }
                        })
                        .catch(error => {
                            Swal.fire({
                                icon: 'error',
                                title: 'Error',
                                text: 'Ocurrió un error inesperado.',
                                showConfirmButton: true
                            });
                        });
                }
            });
        });
    });
});

