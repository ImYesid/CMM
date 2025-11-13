document.addEventListener("DOMContentLoaded", function () {
    function actualizarNotificaciones() {
        let alertCount = document.querySelector("#notificaciones-count");
        if (!alertCount) return;

        let url = alertCount.getAttribute("data-url");  // Obtener la URL desde el HTML

        fetch(url)
            .then(response => response.json())
            .then(data => {
                let count = data.count;

                if (count > 0) {
                    alertCount.textContent = count;
                    alertCount.style.display = "inline-block";
                } else {
                    alertCount.style.display = "none";
                }
            })
            .catch(error => console.error("Error al obtener las notificaciones:", error));
    }

    // Llamar la función cada 10 segundos
    setInterval(actualizarNotificaciones, 10000);
});