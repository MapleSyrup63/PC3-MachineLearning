from naoqi import ALProxy
import cv2
import numpy as np
from skimage.feature import hog
import joblib
import time

# IP y puerto del robot NAO fisico
# IP = "192.168.108.90" 
# PROXY = 9559

# IP y puerto del robot NAO virtual
IP = "127.0.0.1"
PROXY = 50355
camera = ALProxy("ALVideoDevice", IP, PROXY)
tts = ALProxy("ALTextToSpeech", IP, PROXY)

# Configuracion para idioma espanol
try:
    tts.setLanguage("Spanish")
    print("Idioma configurado a espanol")
except:
    print("No se pudo cambiar el idioma, usando idioma por defecto")

# Cargar modelo
try:
    clf = joblib.load("modelo.pkl")
    print("Modelo cargado exitosamente")
    print("Tipo de modelo:", type(clf))
except Exception as e:
    print("Error cargando modelo:", e)
    exit()

# Capturar imagen
resolution = 2  # 640x480 (kVGA)
colorSpace = 11  # RGB
fps = 10

# Extraer features
def extract_features(img):
    img = cv2.resize(img, (128, 128))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = hog(gray, orientations=9, pixels_per_cell=(8, 8),
                   cells_per_block=(2, 2), block_norm='L2-Hys', visualize=False)
    return features

def capturar_y_predecir():
    try:
        nameId = camera.subscribeCamera("python_client", 0, resolution, colorSpace, fps)
        print("Usando subscribeCamera con camara 0")
    except:
        try:
            nameId = camera.subscribe("python_client", resolution, colorSpace, fps)
            print("Usando subscribe con parametros")
        except:
            try:
                nameId = camera.subscribeCameras("python_client", [0], [resolution], [colorSpace], [fps])
                print("Usando subscribeCameras")
            except:
                nameId = camera.subscribe("python_client")
                print("Usando subscribe basico")
                
    image = camera.getImageRemote(nameId)
    camera.unsubscribe(nameId)

    width = image[0]
    height = image[1]
    print("Imagen capturada: {}x{} pixels".format(width, height))
    
    array = image[6]
    img = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))

    feat = extract_features(img)
    pred = clf.predict([feat])[0]
    
    return pred

# Ejecutar durante 2 minutos (120 segundos), capturando cada 10 segundos
duracion_total = 120  # 2 minutos
intervalo = 10        # 10 segundos
iteraciones = duracion_total // intervalo  # 12 iteraciones

print("Iniciando deteccion de objetos por 2 minutos...")
print("Capturando imagen cada {} segundos".format(intervalo))

for i in range(iteraciones):
    print("\n--- Captura {} de {} ---".format(i + 1, iteraciones))
    
    try:
        pred = capturar_y_predecir()
        
        if pred is not None:
            resultado = "Creo que estas mostrando un " + str(pred)
            print("Prediccion: {}".format(pred))
            print("Diciendo: {}".format(resultado))
            tts.say(resultado)
        else:
            print("Error: prediccion es None")
            tts.say("No pude identificar el objeto")
            
    except Exception as e:
        print("Error en captura {}: {}".format(i + 1, e))
        tts.say("Error al procesar la imagen")
    
    if i < iteraciones - 1:
        print("Esperando {} segundos...".format(intervalo))
        time.sleep(intervalo)

print("\nDeteccion completada. Programa terminado.")
