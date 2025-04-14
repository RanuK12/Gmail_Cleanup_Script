# Gmail Cleanup Script

Un script simple pero efectivo para Google Apps Script que te ayuda a mantener tu bandeja de entrada de Gmail limpia y organizada, eliminando automáticamente los correos electrónicos no deseados según criterios personalizables.

## Características

- Elimina correos electrónicos automáticamente basándose en consultas de búsqueda de Gmail
- Configurable para diferentes categorías, etiquetas y criterios de tiempo
- Respeta los correos destacados (con estrella)
- Procesamiento por lotes para manejar grandes volúmenes de correo
- Registro detallado de las operaciones realizadas

## ¿Cómo funciona?

Por defecto, el script está configurado para eliminar:
- Correos en la categoría "Promociones"
- Que están en la bandeja de entrada
- Que NO están destacados con estrella
- Que son más antiguos de 1 año

## Instalación

1. Abre [Google Apps Script](https://script.google.com/)
2. Crea un nuevo proyecto
3. Copia y pega el código del archivo `gmail-cleanup.js`
4. Guarda el proyecto con un nombre descriptivo (por ejemplo, "Gmail Cleanup")

## Uso

### Ejecución manual

1. Abre tu proyecto de Google Apps Script
2. Selecciona la función `runCleanup` en el menú desplegable
3. Haz clic en el botón de reproducción (▶️) para ejecutar el script
4. La primera vez, necesitarás autorizar el script para acceder a tu Gmail

### Ejecución automática (programada)

1. En tu proyecto de Google Apps Script, haz clic en el icono del reloj en la barra lateral (⏰)
2. Haz clic en "Agregar disparador"
3. Configura el disparador:
   - Selecciona la función `cleanup`
   - Elige la fuente de eventos como "Basado en tiempo"
   - Selecciona la frecuencia deseada (diaria, semanal, etc.)
   - Configura la hora específica para la ejecución
4. Guarda el disparador

## Personalización

### Modificar criterios de búsqueda

Edita el array `queryArray` para incluir tus propias consultas de búsqueda. Google Apps Script utiliza la misma sintaxis de búsqueda que Gmail.

Ejemplos de consultas útiles:

```javascript
const queryArray = [
  "category:promotions in:inbox AND -in:starred older_than:",  // Promociones antiguas
  "category:social in:inbox AND -in:starred older_than:",      // Social antiguo
  "label:newsletter older_than:",                              // Newsletters antiguos
  "from:example.com AND -in:starred older_than:",              // Correos antiguos de un dominio específico
];
```

### Modificar períodos de tiempo

Edita el array `delayInfo` para cambiar el período de tiempo para cada consulta:

```javascript
const delayInfo = [
  {index: 0, type: "year", value: 1},   // 1 año para la consulta en posición 0
  {index: 1, type: "month", value: 6},  // 6 meses para la consulta en posición 1
  {index: 2, type: "day", value: 30},   // 30 días para la consulta en posición 2
  {index: 3, type: "month", value: 3}   // 3 meses para la consulta en posición 3
];
```

## Precauciones

- **Prueba primero**: Antes de programar ejecuciones automáticas, ejecuta el script manualmente para verificar que funciona como esperas.
- **Respaldos**: Considera hacer una copia de seguridad de correos importantes.
- **Papelera**: Los correos se mueven a la papelera, no se eliminan permanentemente de inmediato.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

## Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de abrir un issue o enviar un pull request.
