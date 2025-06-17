# Arquitectura de Componentes de la implementación

### Arquitectura del Sistema

La arquitectura del sistema está diseñada bajo un enfoque modular que separa el proceso de entrenamiento del modelo del de ejecución en el robot NAO V6, permitiendo así optimizar el uso de recursos computacionales. El entrenamiento, que 
demanda procesamiento intensivo, se realiza en un entorno externo (PC o servidor), mientras que el robot se encarga únicamente de ejecutar inferencias ligeras y brindar una respuesta interactiva en tiempo real.

#### Flujo General
1. Entrenamiento del Modelo
Se realiza en un entorno de desarrollo local (PC) utilizando Python 2.7. En esta etapa:
- Se procesan las imágenes mediante el método HOG (Histogram of Oriented Gradients) para extraer características relevantes.
- Se entrena un modelo de clasificación con la biblioteca scikit-learn, utilizando LinearSVC.
- El modelo resultante se guarda como un archivo .pkl.

2. Ejecución en el Robot NAO
El archivo .pkl se transfiere al NAO, que usa el modelo ya entrenado para realizar predicciones en tiempo real a partir de nuevas imágenes capturadas por su cámara.
Las predicciones se comunican mediante el módulo de síntesis de voz.

#### Componentes del Sistema

- Robot NAO V6: Ejecuta el modelo y comunica verbalmente la predicción.
- Python 2.7 + NAOqi SDK: Entorno de desarrollo compatible con la arquitectura del NAO.
- scikit-learn (LinearSVC): Biblioteca usada para entrenar el modelo de clasificación.
- HOG (Histogram of Oriented Gradients): Método de extracción de características robusto frente a variaciones de iluminación y posición.
- ALTextToSpeech: Módulo del NAO para sintetizar voz y entregar resultados hablados al usuario.
