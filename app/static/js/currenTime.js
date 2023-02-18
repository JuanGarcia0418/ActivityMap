// Obtener el elemento de entrada de tiempo
var inputTime = document.getElementById("date");

// Crear un objeto de fecha y establecer la hora actual
var now = new Date();
var hours = now.getHours().toString().padStart(2, "0");
var minutes = now.getMinutes().toString().padStart(2, "0");
var timeString = hours + ":" + minutes;

// Establecer el valor predeterminado del campo de entrada de tiempo
inputTime.value = timeString;