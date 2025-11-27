function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
let smartwizard = document.getElementById("smartwizard");
let dataId = smartwizard.getAttribute("data-id");

//DINAMICA DEL SMARTWIZARD
const Preventivo ="Preventivo";
const Predictivo = "Predictivo";
const Correctivo = "Correctivo";
const Inspeccion = "Inspeccion";

var steps = [Preventivo, Predictivo, Correctivo, Inspeccion];
var step = steps.indexOf(dataId);
if (step === -1) {
    step = 0;
}

//Visualizacion dinamica de div dentro del Smartwizard
function Div_dynamic(aux_temporal, accion) {
    let stepNow = $("#smartwizard").smartWizard("getStepIndex"); // Obtiene el paso actual
    let Add = document.getElementById(`Add${aux_temporal}`);
    let View = document.getElementById(`View${aux_temporal}`);
    let submitAdd = document.getElementById(`submitAdd${aux_temporal}`);
    let submitEdit = document.getElementById(`submitEdit${aux_temporal}`);

    const btnMostrar = document.getElementById(`btnMostrar${aux_temporal}`)
    btnMostrar.textContent = btnMostrar.textContent === "Añadir" ? "Consultar" : "Añadir";

    //REGISTRAR
    if (View.style.display === "block" && Add.style.display === "none"){

        document.getElementById(`Title${aux_temporal}`).textContent = `${accion} Plan ${aux_temporal}`;

        Add.style.opacity = "0";
        Add.style.display = "block";

        View.style.opacity = "1";
        View.style.display = "none";
        
        setTimeout(() => {
            Add.style.opacity = "1";
            Add.style.transition = "opacity 0.5s ease-in-out";

            View.style.opacity = "0";
            View.style.transition = "opacity 0.5s ease-in-out";
        }, 100);

        changeTabID(aux)
        
        $("#smartwizard").smartWizard("reset"); // Resetea el wizard
        $("#smartwizard").smartWizard("goToStep", stepNow); // Vuelve al paso guardado
        return true;
    
    //CONSULTAR
    }else{
        
        document.getElementById(`Title${aux_temporal}`).textContent = `Lista de Plan ${aux_temporal}`;

        View.style.opacity = "0";
        View.style.display = "block";

        Add.style.opacity = "1";
        Add.style.display = "none";

        setTimeout(() => {
            View.style.opacity = "1";
            View.style.transition = "opacity 0.5s ease-in-out";

            Add.style.opacity = "0";
            Add.style.transition = "opacity 0.5s ease-in-out";
        }, 100);

        changeTabID(aux)

        $('#smartwizard').smartWizard("reset");
        $("#smartwizard").smartWizard("goToStep", stepNow); // Vuelve al paso guardado
        return true;
    }
};

//DETONANTE DE VIEWS "Agregar/Add" CON EL FORM
function ViewAdd(form, aux, submit) {
    
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // ¡PREVENIR EL ENVÍO NORMAL DEL FORMULARIO!

        const addUrl = submit.getAttribute('data-add-url');
        if (!addUrl) {
            console.error("URL no definida en el botón.");
            return;
        }
        // Obtener los datos del formulario
        const formData = new FormData(form);
        fetch(addUrl, {
            method: 'POST',
            body: formData,
            headers: {
                "X-CSRFToken": getCSRFToken() 
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Error en la solicitud al servidor.");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                Swal.fire("Agregado", data.message, "success")
                    .then(()=> {
                        window.location.href = `/planes/${aux}/`;
                    });
            } else {
                Swal.fire("Error", data.message, "error");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
        });
    });
}

//DETONANTE DE VIEWS "edit"
function ViewField(id) {
    const aux = window.location.hash.replace("#", "");
    const form = document.getElementById(`Form${aux}`);

    fetch(`/planes/editar/${id}/`)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Datos recibidos:", data.data);

            Object.keys(data.data).forEach(field => {
                let input = form.querySelector(`[name="${field}"]`);
                if (input) {
                    input.value = data.data[field];
                } else {
                    console.warn(`Campo '${field}' no encontrado en el formulario ${aux}.`);
                }
            });
        } else {
            console.error("Error al obtener los datos.");
        }
    })
    .catch(error => console.error("Error en la solicitud AJAX:", error));
}


//DETONANTE DE VIEWS "Editar/Edit" CON EL FORM
function ViewEdit(form, id) {
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const editUrl = `/planes/editar/${id}/`;  // ← URL corregida
        const formData = new FormData(form);

        fetch(editUrl, {
            method: 'POST',
            body: formData,
            headers: {
                "X-CSRFToken": getCSRFToken() 
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Error en la solicitud al servidor.");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                Swal.fire("Actualizado", data.message, "success")
                    .then(() => window.location.href = `/planes/${aux}/`);
            } else {
                Swal.fire("Error", data.message, "error");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
        });
    });
}


// Limpiar todos los campos del formulario
function CleanField(form) {
    form.querySelectorAll("input, textarea").forEach(field => {
        field.value = "";
    });
};

//Cambio de Paso en el SmartWizard dinamico
function changeTabID(aux_temporal) {
    let nuevaURL = new URL(window.location.href);
    nuevaURL.pathname = `/agregar/${aux_temporal}/`;
    window.history.pushState(null, "", nuevaURL.toString());
}

//VISUALIZACION DINAMICA DE SUBMIT EN EL FORM (Agregar/Editar)
function submitAdd(aux){
    let Add = document.getElementById(`submitAdd${aux}`);
    let Edit = document.getElementById(`submitEdit${aux}`);

    Add.style.opacity = "0";
    Add.style.display = "block";
    Edit.style.opacity = "1";
    Edit.style.display = "none";

    setTimeout(() => {
        Add.style.opacity = "1";
        Add.style.transition = "opacity 0.5s ease-in-out";

        Edit.style.opacity = "0";
        Edit.style.transition = "opacity 0.5s ease-in-out";
    }, 100);
}

function submitEdit(aux){
    let Add = document.getElementById(`submitAdd${aux}`);
    let Edit = document.getElementById(`submitEdit${aux}`);

    Edit.style.opacity = "0";
    Edit.style.display = "block";
    Add.style.opacity = "1";
    Add.style.display = "none";

    setTimeout(() => {
        Edit.style.opacity = "1";
        Edit.style.transition = "opacity 0.5s ease-in-out";

        Add.style.opacity = "0";
        Add.style.transition = "opacity 0.5s ease-in-out";
    }, 100);
}
 
//FUNCIONES CRUD
document.addEventListener("DOMContentLoaded", function () {

    ///PLAN PREVENTIVO
    document.getElementById("btnMostrarPreventivo").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash // Captura el ID del paso smartwizard
            aux = aux.replace("#", "") // Elimina el símbolo "#"
            changeTabID(aux)

            //REGISTRAR FORM
            const form = document.getElementById(`Form${aux}`)
            const submit = document.getElementById(`submitAdd${aux}`)
            
            submitAdd(aux)
            Div_dynamic(aux, "Registrar ")
            CleanField(form)
            ViewAdd(form, aux, submit)
        }
    });

    document.querySelectorAll(".editar-Preventivo").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash // Captura el ID del paso smartwizard
            aux = aux.replace("#", "") // Elimina el símbolo "#"
            changeTabID(aux)

            //EDITAR
            const id = this.getAttribute("data-id")
            const form = document.getElementById(`Form${aux}`)
            
            submitEdit(aux)
            Div_dynamic(aux, "Editar ")
            ViewField(id)
            ViewEdit(form, id)

        });
    });

    ///PLAN PREDICTIVO
    document.getElementById("btnMostrarPredictivo").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash // Captura el ID del paso smartwizard
            aux = aux.replace("#", "") // Elimina el símbolo "#"
            changeTabID(aux)

            //REGISTRAR FORM
            const form = document.getElementById(`Form${aux}`)
            const submit = document.getElementById(`submitAdd${aux}`)
            CleanField(form)
            submitAdd(aux)
            Div_dynamic(aux, "Registrar ")
            ViewAdd(form, aux, submit)
        }
    });

    document.querySelectorAll(".editar-Predictivo").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash // Captura el ID del paso smartwizard
            aux = aux.replace("#", "") // Elimina el símbolo "#"
            changeTabID(aux)

            //EDITAR
            const id = this.getAttribute("data-id")
            const form = document.getElementById(`Form${aux}`)
            
            submitEdit(aux)
            Div_dynamic(aux, "Editar ")
            ViewField(id)
            ViewEdit(form, id)

        });
    });

    ///PLAN PREDICTIVO
    document.getElementById("btnMostrarCorrectivo").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash // Captura el ID del paso smartwizard
            aux = aux.replace("#", "") // Elimina el símbolo "#"
            changeTabID(aux)

            //REGISTRAR FORM
            const form = document.getElementById(`Form${aux}`)
            const submit = document.getElementById(`submitAdd${aux}`)
            CleanField(form)
            submitAdd(aux)
            Div_dynamic(aux, "Registrar ")
            ViewAdd(form, aux, submit)
        }
    });

    document.querySelectorAll(".editar-Correctivo").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash // Captura el ID del paso smartwizard
            aux = aux.replace("#", "") // Elimina el símbolo "#"
            changeTabID(aux)

            //EDITAR
            const id = this.getAttribute("data-id")
            const form = document.getElementById(`Form${aux}`)
            
            submitEdit(aux)
            Div_dynamic(aux, "Editar ")
            ViewField(id)
            ViewEdit(form, id)

        });
    });

    ///PLAN INSPECCION
    document.getElementById("btnMostrarInspeccion").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash // Captura el ID del paso smartwizard
            aux = aux.replace("#", "") // Elimina el símbolo "#"
            changeTabID(aux)

            //REGISTRAR FORM
            const form = document.getElementById(`Form${aux}`)
            const submit = document.getElementById(`submitAdd${aux}`)
            CleanField(form)
            submitAdd(aux)
            Div_dynamic(aux, "Registrar ")
            ViewAdd(form, aux, submit)
        }
    });

    document.querySelectorAll(".editar-Inspeccion").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash // Captura el ID del paso smartwizard
            aux = aux.replace("#", "") // Elimina el símbolo "#"
            changeTabID(aux)

            //EDITAR
            const id = this.getAttribute("data-id")
            const form = document.getElementById(`Form${aux}`)
            
            submitEdit(aux)
            Div_dynamic(aux, "Editar ")
            ViewField(id)
            ViewEdit(form, id)

        });
    });

});


//smartwizard
$(document).ready(function () {
    // Step show event
    $("#smartwizard").on("showStep", function (stepPosition) {
        $("#prev-btn").removeClass('disabled');
        $("#next-btn").removeClass('disabled');
        if (stepPosition === 'first') {
            $("#prev-btn").addClass('disabled');
        } else if (stepPosition === 'last') {
            $("#next-btn").addClass('disabled');
        } else {
            $("#prev-btn").removeClass('disabled');
            $("#next-btn").removeClass('disabled');
        }
        
    });
    // Smart Wizard
    $('#smartwizard').smartWizard({
        selected: step,
        theme: 'dots',
        transition: {
            animation: 'none', // none/fade/slide-horizontal/slide-vertical/slide-swing
        },
        toolbarSettings: {
            toolbarPosition: 'both',
        },
        anchorSettings: {
            enableAllAnchors: true // pasos sin restricciones
        }
    });
    
    $("#prev-btn").on("click", function () {
        // Navigate previous
        $('#smartwizard').smartWizard("prev");
        return true;
        
    });
    $("#next-btn").on("click", function () {
        // Navigate next
        $('#smartwizard').smartWizard("next");
        return true;
    });
});