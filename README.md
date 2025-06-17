# Objetivos

Nuestro principal objetivo consiste en desarrollar un sistema funcional de clasificación de objetos mediante visión por computadora, basado en aprendizaje automático supervisado, que permita al robot humanoide NAO V6 reconocer imágenes y comunicar lo que observa.
A partir de este objetivo nos planteamos metas a cumplir, como objetivos específicos establecidos para el éxito del aprendizaje de nuestro robot para clasificar objetos correctamente:
* Diseñar y entrenar un modelo de clasificación de imágenes utilizando el algoritmo LinearSVC y características HOG.
* Construir una base de datos de imágenes etiquetadas con diferentes clases de objetos (por ejemplo: perro, silla, avión, tren).
* Implementar un módulo de preprocesamiento de imágenes que convierta imágenes en vectores de características mediante Histogram of Oriented Gradients (HOG).
* Integrar el modelo entrenado con el robot NAO V6 mediante Python 2.7 y la interfaz ALProxy de NAOqi para el control de voz y movimiento.
* Simular y demostrar una secuencia en la cual NAO observa distintas imágenes y verbaliza correctamente la clase reconocida.
* Evaluar las posibilidades de escalabilidad del sistema para incorporar más clases, modelos más complejos, o inferencia remota en el futuro.

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

# Instrucciones

- Se debe tener configurado el entorno de Python 2.7.16 con el SDK NAOqi para poder acceder al robot NAO y a sus configuraciones y herramientas.
- El dataset de imágenes se encuentra en el repositorio en la carpeta "imagenet_all_rounder", y están particionadas en "train" y "val", y luego en cada una las imágenes están organizadas en carpetas con los nombres de sus clases.
- En caso se quiera añadir más clases e imágenes, bastará con crear las carpetas con los nombres de las clases tanto en "train" como en "val", y ahí alojar las imágenes que se requieran.
- El modelo ya entrenado se encuentra disponible en este mismo repositorio, y se llama "modelo.pkl".
- En caso se quiera generar nuevamente el modelo, bastará con ejecutar el archivo Python "generacion_de_modelo.py".
- Una vez con ello, se deberá acceder al archivo "ejecucion.py" mediante algún IDE o editor de código.
- Ya dentro del archivo, las variables IP y PROXY deberán variar dependiendo del robot NAO que se planee manejar.
- Si es un robot virtual, deberemos acceder al software "Choregraphe" para conocer el puerto necesario.
- Si es un robot físico, deberemos conectarnos a este primero mediante su red WiFi, y posteriormente registrar su IP y puerto en el software "Choregraphe".
- Los valores correspondientes los guardaremos en el archivo "ejecucion.py" (actualmente está configurado con los parámetros necesarios para el robot virtual).
- Con todo lo anterior ya configurado, bastará con ejecutar el archivo "ejecucion.py" para poder iniciar el programa (que se nutre del modelo creado).
- Al hacer uso del robot físico, se deberá acercar un objeto o imagen correspondiente a la cámara del NAO cada 10 segundos en un lapso de 2 minutos, para que pueda tomar las capturas.
- Por consola y mediante los altavoces del robot se mencionará la respuesta de la predicción que haga a partir de la captura.
- Pasados los 2 minutos, el programa finalizará.

# Vídeo de la solución

Link del vídeo: [Video](https://www.youtube.com/watch?v=zUt82hoqFAs)
