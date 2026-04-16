# fpl-pdf-service

Microservicio interno para la generación y aplanamiento automático de planes de vuelo impresos (Formulario OACI FPL).

## 🚀 Uso como Microservicio (HTTP API)

El servicio expone un único endpoint para recibir los datos del vuelo por POST y devuelve el archivo PDF de forma binaria.

1.  **Iniciar el servidor:** 
    Instala las dependencias y corre la aplicación Flask (recomendado usar Gunicorn para producción):
    ```bash
    pip install -r requirements.txt
    python app.py
    ```
    El servidor arrancará en `http://0.0.0.0:5000`.

2.  **Llamada a la API:**
    Envía una petición POST a `/api/fill-pdf` con el payload JSON. El servidor devolverá el archivo como adjunto (ej. `LVABC 15-04-2026.pdf`).

    **Ejemplo en JavaScript/Node:**
    ```javascript
    const response = await fetch("http://localhost:5000/api/fill-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(fplData) // Ver formato abajo
    });

    if (response.ok) {
        const blob = await response.blob();
        // Guardar o mostrar el PDF
    }
    ```

## 📦 Uso como Módulo Python (Integración en tu código)

Como el programa ahora es 100% modular, podrías mover la carpeta a tu proyecto backend existente y evitar llamar a una API HTTP externa. Solamente importás el módulo central de generación de PDF.

**Ejemplo en Python:**
```python
# Importar la función procesadora directamente
from fpl_service_folder.pdf_service import fill_pdf

# Diccionario con todo el payload (equivalente al JSON de abajo)
vuelo_data = {
    "aircraft_id": "LVILQ",
    "departure_aerodrome": "SAAP",
    "route": "DCT SAAR",
    # ... resto de las llaves
}

# Generar los bytes del PDF en crudo
pdf_bytes = fill_pdf(vuelo_data)

# Guardar en disco o manejar por cuenta tuya
with open(f"{vuelo_data['aircraft_id']}.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## 📄 Estructura de Datos (JSON Payload)

El servicio requiere un objeto JSON plano que contenga como llaves los campos del formulario. 
- Los **Textos/Números** se envían como `strings`.
- Las **Opciones Extras de Casilla 19** que se deben **TACHAR** se envían como booleanos o nulos. *(Recuerda, el valor False indica que debe aparecer tachado, no marcado).*
- La firma debe enviarse como una cadena Base64 (PNG con transparencia).

### Esquema de Referencia

```json
{
  "date": "16/04/2026",
  "aircraft_id": "LVILQ",
  "flight_rules": "V",
  "type_of_flight": "G",
  "number": "1",
  "type_of_aircraft": "C150",
  "wake_turbulence_cat": "L",
  "equipment": "S",
  "surveillance": "S",
  "departure_aerodrome": "SAAP",
  "departure_time": "1400",
  "cruising_speed": "N0110",
  "level": "A045",
  "route": "LOREM IPSUM DCT",
  "destination_aerodrome": "SAAR",
  "total_eet": "0130",
  "altn_aerodrome": "SAAV",
  "altn_aerodrome_2": "ZZZZ",
  "other_info": "RMK/ FLIGHT TEST",
  "endurance": "0400",
  "persons_on_board": "2",
  
  "dinghies_number": "1",
  "dinghies_capacity": "4",
  "dinghies_colour": "ORANGE",
  "aircraft_colour": "WHITE",
  "remarks": "PPA/12345678",
  "pilot_in_command": "LEHOUX ELIAN",
  "filed_by": "LEHOUX ELIAN",

  "signature_image": "data:image/png;base64,iVBORw0KGgoA...",

  "radio_uhf": false,
  "radio_vhf": false,
  "radio_elt": false,
  "survival_polar": false,
  "survival_desert": false,
  "survival_maritime": false,
  "survival_jungle": false,
  "jackets_light": false,
  "jackets_fluor": false,
  "jackets_uhf": false,
  "jackets_vhf": false,
  "dinghies_cover": false
}
```

> **Nota Automática de OACI:** No hace falta enviar las llaves maestras como `"survival_all"`, `"jackets_all"`, etc. El microservicio evaluará todos los "survival" (polar, jungle, etc.) y decidirá lógicamente si tacha automáticamente esa casilla.
