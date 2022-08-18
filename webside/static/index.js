function select_discipline() {
    if (document.getElementById("tipo_prueba").value == "Velocidad")
    {
         document.getElementById("Velocidad").style.display = "block"
         document.getElementById("Vallas").style.display = "none"
         document.getElementById("FondoMedioFondo").style.display = "none"
         document.getElementById("Lanzamientos").style.display = "none"
         document.getElementById("Saltos").style.display = "none"
    }
    else if (document.getElementById("tipo_prueba").value == "Vallas")
    {
         document.getElementById("Velocidad").style.display = "none"
         document.getElementById("Vallas").style.display = "block"
         document.getElementById("FondoMedioFondo").style.display = "none"
         document.getElementById("Lanzamientos").style.display = "none"
         document.getElementById("Saltos").style.display = "none"
    }
    else if (document.getElementById("tipo_prueba").value == "Fondo / Medio Fondo")
    {
         document.getElementById("Velocidad").style.display = "none"
         document.getElementById("Vallas").style.display = "none"
         document.getElementById("FondoMedioFondo").style.display = "block"
         document.getElementById("Lanzamientos").style.display = "none"
         document.getElementById("Saltos").style.display = "none"
    }  
    else if (document.getElementById("tipo_prueba").value == "Lanzamientos")
    {
         document.getElementById("Velocidad").style.display = "none"
         document.getElementById("Vallas").style.display = "none"
         document.getElementById("FondoMedioFondo").style.display = "none"
         document.getElementById("Lanzamientos").style.display = "block"
         document.getElementById("Saltos").style.display = "none"
    }   
    else if (document.getElementById("tipo_prueba").value == "Saltos")
    {
         document.getElementById("Velocidad").style.display = "none"
         document.getElementById("Vallas").style.display = "none"
         document.getElementById("FondoMedioFondo").style.display = "none"
         document.getElementById("Lanzamientos").style.display = "none"
         document.getElementById("Saltos").style.display = "block"
    }      
 }


