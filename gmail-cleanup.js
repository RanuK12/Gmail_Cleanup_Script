/**
 * Gmail Cleanup Script
 * 
 * Este script automatiza la limpieza de correos electrónicos en Gmail según criterios
 * personalizables para mantener tu bandeja de entrada organizada.
 * 
 * Autor: RanuK12
 * Licencia: MIT
 */

// Configuración principal
const BATCH_LIMIT = 100; // Límite de procesamiento por lote

/**
 * Función principal que inicia el proceso de limpieza.
 */
function cleanup() {
  // Configuración de las consultas de búsqueda
  const queryArray = [
    "category:promotions in:inbox AND -in:starred older_than:"
  ];
  
  // Configuración de períodos para cada consulta
  // index: corresponde a la posición en queryArray
  // type: unidad de tiempo (year, month, day)
  // value: cantidad de unidades
  const delayInfo = [
    {index: 0, type: "year", value: 1}
  ];
  
  // Procesa cada consulta configurada
  for (let i = 0; i < queryArray.length; i++) {
    let isQueryValid = false;
    let finalQuery = queryArray[i];
    
    // Construye la consulta final con el período correspondiente
    for (let j = 0; j < delayInfo.length; j++) {
      if (delayInfo[j].index == i) {
        finalQuery += delayInfo[j].value;
        
        switch(delayInfo[j].type) {
          case "year":
          case "month":
          case "day":
            finalQuery += delayInfo[j].type.charAt(0);
            isQueryValid = true;
            break;
          default:
            isQueryValid = false;
            Logger.log("Tipo de período no válido");
        }
      }
    }
    
    // Ejecuta limpieza si la consulta es válida
    if (isQueryValid) {
      Logger.log("Ejecutando limpieza con consulta: " + finalQuery);
      messageCleanup(finalQuery, BATCH_LIMIT);
    }
  }
}

/**
 * Elimina los mensajes que coinciden con la consulta especificada.
 * 
 * @param {string} query - Consulta de búsqueda en formato Gmail
 * @param {number} batchSize - Tamaño del lote para procesar
 */
function messageCleanup(query, batchSize) {
  let threads;
  let processedCount = 0;
  
  Logger.log("Iniciando limpieza con consulta: " + query);
  
  do {
    // Busca hilos que coincidan con la consulta
    threads = GmailApp.search(query, 0, batchSize);
    
    if (threads.length > 0) {
      // Mueve los hilos encontrados a la papelera
      GmailApp.moveThreadsToTrash(threads);
      
      // Actualiza contadores y registro
      processedCount += threads.length;
      Logger.log("Procesados " + threads.length + " hilos. Total: " + processedCount);
      
      // Pausa para evitar exceder cuotas de API
      Utilities.sleep(1000);
    }
  } while (threads.length > 0);
  
  Logger.log("Limpieza completada. Total eliminado: " + processedCount + " hilos.");
}

/**
 * Función para ejecutar el script manualmente desde el editor.
 */
function runCleanup() {
  cleanup();
}
