function myFunction() {            
    var button = document.getElementById("busqueda_normal");
    if (button.disabled === true) {
        button.disabled = false;
    } else {
        button.disabled = true;
    }

    var button = document.getElementById("busqueda_fecha");
    if (button.disabled === true) {
        button.disabled = false;
    } else {
        button.disabled = true;
    }

    var x = document.getElementById("normal");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }

    var x = document.getElementById("fecha");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
        document.getElementById('inputDesde').value = "";
        document.getElementById('inputHasta').value = "";

    }
}

//----------------------------------    CALENDARIO     ----------------------------------------------------

jQuery.extend( jQuery.fn.pickadate.defaults, {
    monthsFull: [ 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre' ],
    monthsShort: [ 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic' ],
    weekdaysFull: [ 'Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado' ],
    weekdaysShort: [ ' dom', ' lun', ' mar', ' mié', ' jue', ' vie', ' sáb' ],
    today: 'Fecha de Hoy',
    clear: 'Deshacer',
    close: 'Aceptar',
    firstDay: 1,
    format: 'dddd d !de mmmm !de yyyy',
    formatSubmit: 'yyyy/mm/dd'
});

jQuery.extend( jQuery.fn.pickatime.defaults, {
    clear: 'Borrar'
});



// Get the elements
var from_input = $('#startingDate').pickadate(), from_picker = from_input.pickadate('picker')
 
var to_input = $('#endingDate').pickadate(), to_picker = to_input.pickadate('picker')

// Check if there’s a “from” or “to” date to start with and if so, set their appropriate properties.
if (from_picker.get('value')) {
    to_picker.set('min', from_picker.get('select'))
}
if (to_picker.get('value')) {
    from_picker.set('max', to_picker.get('select'))
}

// Apply event listeners in case of setting new “from” / “to” limits to have them update on the other end. If ‘clear’ button is pressed, reset the value.
from_picker.on('set', function (event) {
if (event.select) {
    to_picker.set('min', from_picker.get('select'))
} else if ('clear' in event) {
    to_picker.set('min', false)
}
})
to_picker.on('set', function (event) {
if (event.select) {
    from_picker.set('max', to_picker.get('select'))
} else if ('clear' in event) {
    from_picker.set('max', false)
}
})



document.getElementById('startingDate').addEventListener('click', () => {
        document.getElementById('bottom').scrollIntoView();
});
document.getElementById('endingDate').addEventListener('click', () => {
        document.getElementById('bottom').scrollIntoView();
});
//--------------------------------------------------------------------------------------------------------------------
