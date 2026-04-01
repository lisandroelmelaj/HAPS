import cv2
import numpy as np
import os

def procesar_mision_haps():
    # 1. Configuración de archivos
    nombre_entrada = "entrada.png" 
    nombre_salida = "mendoza_termica_ref.jpg"

    if not os.path.exists(nombre_entrada):
        print(f"❌ ERROR: No encontré '{nombre_entrada}'.")
        return

    # 2. Leer imagen (método robusto para acentos)
    with open(nombre_entrada, "rb") as f:
        img = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        print("❌ ERROR: No se pudo decodificar la imagen.")
        return

    # 3. Resize a resolución FLIR Boson 640 (640x512) 
    # Usamos 512 de alto para no distorsionar el sensor de 12um [cite: 9]
    img_640 = cv2.resize(img, (640, 512), interpolation=cv2.INTER_AREA)

    # 4. Dibujar el OBJETO de REFERENCIA (40 metros = 6 píxeles)
    # Definimos los puntos del rectángulo
    top_left = (50, 50)
    bottom_right = (50 + 6, 50 + 6) # 6 píxeles de ancho y alto
    color_rojo = (0, 0, 255) 
    
    # Grosor -1 significa que el rectángulo está RELLENO
    cv2.rectangle(img_640, top_left, bottom_right, color_rojo, -1)
    
    # Etiqueta
    cv2.putText(img_640, "Ref. 40m (6px)", (45, 45), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, color_rojo, 1)

    # 5. Guardar
    cv2.imwrite(nombre_salida, img_640)
    print(f"✅ ÉXITO: Imagen generada como '{nombre_salida}'")
    print(f"ℹ️ Resolución final: 640x512 (Standard Boson VGA) ")

if __name__ == "__main__":
    procesar_mision_haps()