import os
import cv2
import numpy as np
from sklearn.svm import SVC
from skimage.feature import hog
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def extract_features(img):
    img = cv2.resize(img, (128, 128))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = hog(gray, orientations=9, pixels_per_cell=(8, 8),
                   cells_per_block=(2, 2), block_norm='L2-Hys', visualize=False)
    return features

def load_dataset(dataset_path):
    X = []
    y = []
    for label in os.listdir(dataset_path):
        folder = os.path.join(dataset_path, label)
        if not os.path.isdir(folder):
            continue
        for img_file in os.listdir(folder):
            img_path = os.path.join(folder, img_file)
            img = cv2.imread(img_path)
            if img is not None:
                feat = extract_features(img)
                X.append(feat)
                y.append(label.decode('utf-8') if isinstance(label, str) else label)
    return np.array(X), np.array(y)

# Rutas
TRAIN_PATH = "imagenet_all_rounder/train/"
VAL_PATH = "imagenet_all_rounder/val/"

# Carga de datos
X_train, y_train = load_dataset(TRAIN_PATH)
X_val, y_val = load_dataset(VAL_PATH)

# Creacion y entrenamiento de modelo
clf = SVC(kernel='linear', probability=True)
clf.fit(X_train, y_train)

# Guardado del modelo
joblib.dump(clf, "modelo.pkl", compress=3, protocol=2)

# Evaluacion
y_pred = clf.predict(X_val)

print("Evaluacion del Modelo en Validacion")
print("Accuracy:")
print(accuracy_score(y_val, y_pred))
print("Reporte de Clasificacion:")
print(classification_report(y_val, y_pred))
print("Matriz de Confusion:")
print(confusion_matrix(y_val, y_pred))