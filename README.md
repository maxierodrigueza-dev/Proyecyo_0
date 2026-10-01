# Proyecto 0

Herramienta en Python para procesar y analizar observaciones meteorológicas del Servicio Meteorológico Nacional (SMN).

## Funciones Principales

*   **Cantidad de ciudades leídas:** Calcula el total de registros procesados.
*   **Temperaturas extremas:** Identifica la ciudad con la temperatura máxima y mínima.
*   **Top N ciudades:** Función genérica para ordenar ciudades de mayor a menor según cualquier campo (temperatura, viento, etc.).
*   **Vientos extremos:** Determina las velocidades de viento máxima y mínima.
*   **Separador de viento:** Convierte cadenas como "Norte 3" en tuplas (dirección, velocidad) y maneja el caso de "Calma".
*   **Reporte de faltantes:** Genera un diccionario agrupando por campo las ciudades que contienen datos nulos (None).

## Enlaces de Interés

* [Sitio oficial del SMN - Descarga de datos](https://www.google.com/search?q=https://www.smn.gob.ar/descarga-de-datos&utm_source=gemini)
*  **Ejemplo de ejecución en terminal:**Aviso: Se ignoraron 96 líneas por formato inválido.

--- Resumen Meteorológico ---
Cantidad total de ciudades leídas: 121
Ciudades con toda la información: 25

Top 5 ciudades más cálidas:
- Rivadavia: 28.0°C
- Orán: 27.4°C
- Pcia. Roque Saenz Peña: 26.7°C
- Tartagal: 26.4°C
- Resistencia: 26.3°C

Top 5 ciudades más frias:
- Base Belgrano II: -28.6°C
- Base San Martín: -24.8°C
- Base Orcadas: -24.3°C
- Base Marambio: -15.5°C
- Base Esperanza: -9.5°C

Top 5 ciudades más ventosas:
- Mount Pleasant Airport (Islas Malvinas): 42.0
- Perito Moreno: 38.0
- San Julián: 37.0
- Río Gallegos: 37.0
- Comodoro Rivadavia: 33.0

Top 5 ciudades menos ventosas:
- Base Carlini: 0.0
- Bolívar: 0.0
- Cipolletti: 0.0
- Gobernador Gregores: 0.0
- Mar del Plata: 0.0

Horarios reportados:
09:00, 10:00, 11:00, 12:00, 13:00, 15:00

Información faltante:
Ciudades sin toda la información: 96
Sensación térmica (°C): ['Azul', 'Bahía Blanca', 'Benito Juárez', 'Bolívar', 'Campo de Mayo', 'Coron
el Suarez', 'Dolores', 'El Palomar', 'Ezeiza', 'Junín', 'La Plata', 'Las Flores', 'Mar del Plata', '
Mariano Moreno', 'Merlo', 'Morón', 'Nueve de Julio', 'Olavarría', 'Pehuajó', 'Pigué', 'Punta Indio B
.A.', 'San Fernando', 'Tandil', 'Trenque Lauquen', 'Tres Arroyos', 'Villa Gesell', 'Aeroparque Bueno
s Aires', 'Buenos Aires', 'Catamarca', 'Tinogasta', 'Puerto Madryn', 'Trelew', 'Córdoba', 'Córdoba O
bservatorio', 'Esc. Aviación Militar', 'Laboulaye', 'Marcos Juárez', 'Pilar Obs.', 'Río Cuarto', 'Vi
lla Dolores', 'Villa María Del Río Seco', 'Corrientes', 'Ituzaingó', 'Mercedes', 'Monte Caseros', 'P
aso De Los Libres', 'Concordia', 'Gualeguaychú', 'Paraná', 'Formosa', 'La Quiaca', 'Jujuy', 'Jujuy U
niversidad Nacional', 'General Pico', 'Victorica', 'Santa Rosa', 'Chamical', 'Chepes', 'Chilecito',
'La Rioja', 'Malargue', 'Mendoza', 'Mendoza Observatorio', 'San Martín (Mza)', 'San Rafael', 'Uspall
ata', 'Bernardo De Irigoyen', 'Iguazú', 'Oberá', 'Posadas', 'Neuquén', 'Cipolletti', 'El Bolsón', 'M
aquinchao', 'Río Colorado', 'Viedma', 'Metán', 'Salta', 'Jachal', 'San Juan', 'San Luis', 'Santa Ros
a del Conlara', 'Villa Reynolds', 'Gobernador Gregores', 'Ceres', 'Rafaela', 'Reconquista', 'Rosario
', 'Santa Fe', 'Sunchales', 'Venado Tuerto', 'Termas de Rio Hondo', 'Santiago del Estero', 'Tucumán'
, 'Base Esperanza', 'Base Carlini']


