
$(document).ready(function () {
    if ($.fn.DataTable.isDataTable("#example2")) {
        $("#example2").DataTable().destroy();
    }

    var table = $('#example2').DataTable({
        lengthChange: false,
        dom: 'Bfrtip',  // Necesario para mostrar los botones
        buttons: ['excel', 'pdf', 'print'],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
        },
        initComplete: function () {
            console.log("Traducción cargada correctamente.");
        }
    });

    table.buttons().container()
        .appendTo('#example2_wrapper .col-md-6:eq(0)');
});

$(document).ready(function () {
    if ($.fn.DataTable.isDataTable("#informe")) {
        $("#informe").DataTable().destroy();
    }

    var table = $('#informe').DataTable({
        responsive: true,
        lengthChange: false,
        dom: 'Bfrtip',  // Necesario para mostrar los botones
        buttons: ['excel', 'pdf', 'print', 'colvis'],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
        },
        initComplete: function () {
            console.log("Traducción cargada correctamente.");
        },
        colReorder: true,  // habilita la reordenación de columnas
        colVis: {
            buttonText: 'Mostrar/Ocultar Columnas', // Botón para mostrar/ocultar columnas
            restore: 'Restaurar columnas',
            showAll: 'Mostrar todo',
            hideAll: 'Ocultar todo'
        },
        rowGroup: {
            dataSrc: 'rollo_numero'  // Agrupamos por el campo "rollo_numero"
        },
        columnDefs: [
            {
                targets: [1, 2, 3, 4, 5, 6, 7, 8, 9],  // Definir qué columnas no se deben ordenar (si aplica)
                orderable: true
            }
        ]
    });

    // Función para filtrar rango de fecha (columna Fecha = índice 1)
    $.fn.dataTable.ext.search.push(function (settings, data) {
        var min = $('#filter-fecha-desde').val();
        var max = $('#filter-fecha-hasta').val();
        var fecha = data[1]; // formato "dd/mm/YYYY"

        if (min) {
            var desde = new Date(min);
            var partes = fecha.split('/');
            var fc = new Date(partes[2], partes[1] - 1, partes[0]);
            if (fc < desde) return false;
        }
        if (max) {
            var hasta = new Date(max);
            var partes = fecha.split('/');
            var fc = new Date(partes[2], partes[1] - 1, partes[0]);
            if (fc > hasta) return false;
        }
        return true;
    });

    // Función genérica para filtrar por columna exacta
    function applySelectFilter(selectId, columnIndex) {
        $('#' + selectId).on('change', function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            table.column(columnIndex)
                .search(val ? '^' + val + '$' : '', true, false)
                .draw();
        });
    }

    // Asocia cada filtro
    $('#filter-fecha-desde, #filter-fecha-hasta').on('change', function () {
        table.draw();
    });
    applySelectFilter('filter-rollo', 2);  // Filtro para "Rollo Nº"
    applySelectFilter('filter-tela', 3);   // Filtro para "Tela"
    applySelectFilter('filter-color', 4);  // Filtro para "Color"

    table.buttons().container()
        .appendTo('#informe_wrapper .col-md-6:eq(0)');

    function updateResumen() {
        // Filtrar solo filas visibles según búsqueda/filtros
        var data = table.rows({ search: 'applied' }).data();

        var totalCortes = data.length;
        var totalMetros = 0;
        var totalCapas = 0;

        // Recorremos cada fila visible
        data.each(function (row) {
            var metrosText = row[5] || '';  // Obtén el valor de la celda que contiene el texto
            console.log('Original metrosText:', metrosText);  // Verifica qué valor estás obteniendo

            // Reemplazar la coma por punto para asegurarse de que el valor se pueda interpretar correctamente
            var metrosTextFormatted = metrosText.replace(',', '.');  // Reemplazar coma por punto
            console.log('Formatted metrosText:', metrosTextFormatted);  // Verifica el valor después del reemplazo

            var metrosNum = parseFloat(metrosTextFormatted.replace(/[^\d\.]/g, '')) || 0;  // Limpia el texto y convierte a número
            console.log('Parsed metrosNum:', metrosNum);  // Verifica el número convertido

            // Si el valor está en centímetros, lo convertimos a metros
            if (metrosText.includes('cm')) {
                metrosNum = metrosNum / 100;  // Convertir de cm a metros
                console.log('After conversion to meters:', metrosNum);  // Verifica la conversión
            }

            // Suma el total de metros
            totalMetros += metrosNum;

            // row[8] => Capas, debe ser un entero
            var capasNum = parseInt(row[8], 10) || 0;
            totalCapas += capasNum;
        });

        // Actualizamos el DOM
        $('#card-total-cortes').text(totalCortes);
        $('#card-total-metros').text(totalMetros.toFixed(2) + ' m');
        $('#card-total-capas').text(totalCapas);
    }

    // Llamar inicialmente y cada vez que la tabla se redibuja
    updateResumen();
    table.on('draw', updateResumen);
});


$(document).ready(function () {
    if ($.fn.DataTable.isDataTable("#productos")) {
        $("#productos").DataTable().destroy();
    }

    var table = $('#productos').DataTable({
        lengthChange: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'copy',
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function (data, row, column, node) {
                            if (column === 5) { // Columna de tallas
                                return $(node).text().replace(/\s+/g, ' ').trim();
                            }
                            if (column === 6) { // Columna de colores
                                return $(node).find('.color-circle').map(function () {
                                    return $(this).attr('data-color');
                                }).get().join(', ');
                            }
                            return data;
                        }
                    }
                }
            },
            {
                extend: 'excel',
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function (data, row, column, node) {
                            if (column === 5) { // Columna de tallas
                                return $(node).text().replace(/\s+/g, ' ').trim();
                            }
                            if (column === 6) { // Columna de colores
                                return $(node).find('.color-circle').map(function () {
                                    return $(this).attr('data-color');
                                }).get().join(', ');
                            }
                            return data;
                        }
                    }
                }
            },
            {
                extend: 'pdf',
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function (data, row, column, node) {
                            if (column === 5) { // Columna de tallas
                                return $(node).text().replace(/\s+/g, ' ').trim();
                            }
                            if (column === 6) { // Columna de colores
                                return $(node).find('.color-circle').map(function () {
                                    return $(this).attr('data-color');
                                }).get().join(', ');
                            }
                            return data;
                        }
                    }
                }
            },
            {
                extend: 'print',
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function (data, row, column, node) {
                            if (column === 5) { // Columna de tallas
                                return $(node).text().replace(/\s+/g, ' ').trim();
                            }
                            if (column === 6) { // Columna de colores
                                return $(node).find('.color-circle').map(function () {
                                    return $(this).attr('data-color');
                                }).get().join(', ');
                            }
                            return data;
                        }
                    }
                }
            }
        ],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
        },
        columnDefs: [
            {
                targets: 5, // Columna de tallas
                orderable: true,
                searchable: true,
                render: function (data, type, row) {
                    return data.replace(/\s+/g, ' ').trim();
                }
            },
            {
                targets: 6, // Columna de colores
                orderable: true,
                searchable: true,
                render: function (data, type, row, meta) {
                    if (type === 'filter' || type === 'sort') {
                        var tempDiv = document.createElement("div");
                        tempDiv.innerHTML = data;
                        return Array.from(tempDiv.querySelectorAll(".color-circle")).map(span => span.getAttribute("data-color")).join(', ');
                    }
                    return data;
                }
            }
        ],
        initComplete: function () {
            console.log("Traducción cargada correctamente.");
        }
    });

    table.buttons().container()
        .appendTo('#productos_wrapper .col-md-6:eq(0)');
});