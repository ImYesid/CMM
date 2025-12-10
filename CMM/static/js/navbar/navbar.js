document.addEventListener("DOMContentLoaded", function () {
    // MODAL ENCUESTA
  let EncuestaFormURL = "";
  // Cargar el formulario cuando se abre el modal
  $('#modalEncuesta').on('show.bs.modal', function (event) {
    const trigger = $(event.relatedTarget);
    const EncuestaFormURL = trigger.data('url');  // ← captura la URL definida en el HTML
    const notificacionId = trigger.data('id');

    // Marcar notificación como leída vía AJAX
    $.post(`/ordenes/${notificacionId}/`, function (data) {
        if (data.success) {
            // Cambiar estilos en el DOM
            trigger.find('.notify')
                   .removeClass('bg-light-warning text-warning')
                   .addClass('bg-light-secondary text-muted');
            trigger.find('.msg-title')
                   .removeClass('text-dark')
                   .addClass('text-muted');
        }
    });

    // Cargar formulario de encuesta
    $('#modalEncuestaBody').html(`
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2">Cargando formulario...</p>
        </div>
    `);

    $.get(EncuestaFormURL, function (data) {
      $('#modalEncuestaBody').html(data);
    });
  });

  //Lanzar SUBMIT del FORM
  $(document).on('click', '#submitAdd', function () {
    const form = document.getElementById('EncuestaForm');
    if (form.checkValidity()) {
      $('#EncuestaForm').submit();
    } else {
      form.reportValidity();  // muestra los errores nativos del navegador
    }
  });

  // Enviar el formulario via AJAX
  $(document).on('submit', '#EncuestaForm', function (e) {
    e.preventDefault();
    $.post(EncuestaFormURL, $(this).serialize(), function (data) {
      if (data.success) {
        $('#modalEncuesta').modal('hide');
        // refrescar contador de notificaciones
        location.reload();
      } else {
        $('#modalEncuestaBody').html(data.form_html);
      }
    });
  })

  // MODAL NOTIFICACIONES
  $('#modalNotificacion').on('show.bs.modal', function () {
    
  });
})

$(document).ready(function () {
    (function () {
        'use strict';
        var forms = document.querySelectorAll('.needs-validation');
        Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    })();

});
