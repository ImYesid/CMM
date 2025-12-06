document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  fetch("/home/data/")
    .then(response => response.json())
    .then(data => {
      // METRICAS GENERALES
      document.querySelector("#valor_operarios").textContent = data.operarios_activos ?? 0;
      document.querySelector("#valor_activos").textContent = data.activos_operativos ?? 0;
      document.querySelector("#valor_incidencias").textContent = `${data.indice_incidencias ?? 0}%`;

      // GRAFICA OT POR TECNICO
      if (data.ot_estado_proceso && data.ot_por_tecnico) {
        const totalOT = data.ot_estado_proceso.reduce((acc, e) => acc + e.total, 0);
        document.querySelector("#valor_ot").textContent = totalOT;

        const tecnicos = data.ot_por_tecnico.map(e => e.username);
        const abiertas = data.ot_por_tecnico.map(e => e.abiertas);
        const enEjecucion = data.ot_por_tecnico.map(e => e.en_ejecucion);

        const ctx7 = document.getElementById('chart7');
        if (ctx7) {
          new Chart(ctx7.getContext('2d'), {
            type: 'bar',
            data: {
              labels: tecnicos,
              datasets: [
                {
                  label: 'Abiertas',
                  data: abiertas,
                  backgroundColor: '#ffc107',
                  borderRadius: 4
                },
                {
                  label: 'En Ejecución',
                  data: enEjecucion,
                  backgroundColor: '#28a745',
                  borderRadius: 4
                }
              ]
            },
            options: {
              indexAxis: 'y',
              maintainAspectRatio: false,
              categoryPercentage: 0.6,
              plugins: {
                legend: { position: 'bottom', display: true }
              },
              scales: {
                x: { beginAtZero: true, title: { display: true, text: 'Cantidad de OT' } },
                y: { beginAtZero: true, title: { display: true, text: 'Técnico Asignado' } }
              }
            }
          });
        }
      }

      // GRAFICA PLAN GESTIÓN
      if (data.plan_por_tipo) {
        const tipos = data.plan_por_tipo.map(e => e.plan_tipo);
        const totales = data.plan_por_tipo.map(e => e.total);

        // Actualizar badges
        data.plan_por_tipo.forEach(e => {
          const id = e.plan_tipo.toLowerCase();
          const badge = document.getElementById(id);
          if (badge) badge.textContent = e.total;
        });

        const ctx8 = document.getElementById('chart8');
        if (ctx8) {
          const g1 = ctx8.getContext('2d').createLinearGradient(0, 0, 0, 300);
          g1.addColorStop(0, '#005bea'); g1.addColorStop(1, '#00c6fb');
          const g2 = ctx8.getContext('2d').createLinearGradient(0, 0, 0, 300);
          g2.addColorStop(0, '#ff6a00'); g2.addColorStop(1, '#ee0979');
          const g3 = ctx8.getContext('2d').createLinearGradient(0, 0, 0, 300);
          g3.addColorStop(0, '#17ad37'); g3.addColorStop(1, '#98ec2d');
          const g4 = ctx8.getContext('2d').createLinearGradient(0, 0, 0, 300);
          g4.addColorStop(0, '#6c757d'); g4.addColorStop(1, '#adb5bd');

          new Chart(ctx8.getContext('2d'), {
            type: 'pie',
            data: {
              labels: tipos,
              datasets: [{
                data: totales,
                backgroundColor: [g1, g2, g3, g4],
                borderWidth: 1
              }]
            },
            options: {
              maintainAspectRatio: false,
              cutout: 90,
              plugins: { legend: { display: false } }
            }
          });
        }
      }

      // GRAFICA INDICADORES DE DESEMPEÑO
      if (data.indicadores) {
        const labels = data.indicadores.map(e => e.mes);
        const mtbf = data.indicadores.map(e => e.mtbf);
        const mttr = data.indicadores.map(e => e.mttr);
        const disponibilidad = data.indicadores.map(e => e.disponibilidad * 100); // porcentaje

        const ctx5 = document.getElementById('chart5');
        if (ctx5) {
          new Chart(ctx5.getContext('2d'), {
            type: 'line',
            data: {
              labels: labels,
              datasets: [
                {
                  label: 'MTBF (Horas)',
                  data: mtbf,
                  borderColor: '#5e72e4',
                  backgroundColor: 'rgba(94,114,228,0.2)',
                  borderWidth: 3,
                  tension: 0.4,
                  fill: true,
                  pointRadius: 3
                },
                {
                  label: 'MTTR (Horas)',
                  data: mttr,
                  borderColor: '#ffc107',
                  backgroundColor: 'rgba(255,193,7,0.2)',
                  borderWidth: 3,
                  tension: 0.4,
                  fill: true,
                  pointRadius: 3
                },
                {
                  label: 'Disponibilidad (%)',
                  data: disponibilidad,
                  borderColor: '#2dce89',
                  backgroundColor: 'rgba(45,206,137,0.2)',
                  borderWidth: 3,
                  tension: 0.4,
                  fill: true,
                  pointRadius: 3,
                  yAxisID: 'y2'
                }
              ]
            },
            options: {
              maintainAspectRatio: false,
              plugins: { legend: { display: true } },
              scales: {
                y: {
                  beginAtZero: true,
                  title: { display: true, text: 'Horas promedio' }
                },
                y2: {
                  position: 'right',
                  beginAtZero: true,
                  title: { display: true, text: 'Disponibilidad (%)' },
                  grid: { drawOnChartArea: false }
                },
                x: {
                  title: { display: true, text: 'Mes-Año' }
                }
              }
            }
          });
        }
      }
      // Actualizar los valores del último mes en los <h5>
      if (data.ultimo_mes) {
        document.getElementById("MTBF").textContent = data.ultimo_mes.mtbf ?? 0;
        document.getElementById("MTTR").textContent = data.ultimo_mes.mttr ?? 0;
        document.getElementById("Disponibilidad").textContent = `${(data.ultimo_mes.disponibilidad * 100).toFixed(2)}%`;
      }
    })
    .catch(err => console.error("Error cargando datos del dashboard:", err));
});