document.addEventListener("DOMContentLoaded", function () {
    // MODAL ENCUESTA
  let EncuestaFormURL = "";
  // Cargar el formulario cuando se abre el modal
  $('#modalEncuesta').on('show.bs.modal', function (event) {
    const trigger = $(event.relatedTarget);
    EncuestaFormURL = trigger.data('url');  // ← captura la URL definida en el HTML
    $('#modalEncuestaBody').html(`
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-2">Cargando formulario...</p>
            </div>
        `);

    $.get(User_feedbackFormURL, function (data) {
      $('#modalEncuestaBody').html(data);
    });
  });

  //Lanzar SUBMIT del FORM
  $(document).on('click', '#submitAdd', function () {
    const form = document.getElementById('User_feedbackForm');
    if (form.checkValidity()) {
      $('#User_feedbackForm').submit();
    } else {
      form.reportValidity();  // muestra los errores nativos del navegador
    }
  });

  // Enviar el formulario via AJAX
  $(document).on('submit', '#User_feedbackForm', function (e) {
    e.preventDefault();
    $.post(User_feedbackFormURL, $(this).serialize(), function (data) {
      if (data.success) {
        let nuevaOpcion = new Option(data.numero_factura, data.id, true, true);
        $('#id_factura').append(nuevaOpcion).trigger('change');
        $('#modalEncuesta').modal('hide');
      } else {
        $('#modalEncuestaBody').html(data.form_html);
      }
    });
  })
})

