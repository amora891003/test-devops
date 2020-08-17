import numpy as np
from cv2 import cv2
from PIL import Image

# --- Paso 1
# --- Función para recortar distintas partes de una imagen

image = cv2.imread('./inputs/recorte2_0.jpg') # --- Busca la imagen en la ruta definida
#----Coordenadas para imagen 1
#[x1,y1]
#      -------
#      -     -
#      -     -
#      -------
#             [x2,y2]

# coordenadas [x1,y1]
point1 = [[615,432]]
# coordenadas [x2,y2]
point2 = [[1891,697]]

#----Coordenadas para imagen 2
point3 = [[618,12]]
point4 = [[1165,188]]

#----Coordenadas para imagen 3
point5 = [[1013,162]]
point6 = [[1882,252]]

#----Coordenadas para imagen 4
point7 = [[1326,606]]
point8 = [[1893,777]]

#----Coordenadas para imagen 5
point9 = [[1735,2]]
point10 = [[1893,780]]

#----Coordenadas para imagen 6
point11 = [[2,760]]
point12 = [[612,784]]

#----Coordenadas para imagen 7
point13 = [[4,3]]
point14 = [[17,354]]


# --- Arreglo de coordenadas para obtener los 3 recortes de la misma imagen, es necesario agregar dos veces una misma coordenada para que sean tomados correctamente.
points = np.array([[point1,point1, point2],[point3,point3, point4],[point5,point5, point6],[point7,point7, point8],[point9,point9, point10],[point11,point11, point12],[point13,point13, point14]],dtype=np.float32)

# --- Ciclo para recorrer el arreglo de coordenadas y recortar las 7 imagenes
for i, c in enumerate(points):
       x, y, w, h = cv2.boundingRect(c)
       crop = image[y: y+h, x: x+w]
       cv2.imshow('recorte_{}.jpg'.format(i), crop)
       cv2.imwrite("./outputSignature/" + 'recorte_{}.jpg'.format(i), crop)
cv2.waitKey(0)
cv2.destroyAllWindows()

# --- Paso 2 
# --- Concatenar modificando el tamaño de las imagenes

im0 = Image.open('./outputSignature/recorte_0.jpg')
im1 = Image.open('./outputSignature/recorte_1.jpg')
im2 = Image.open('./outputSignature/recorte_2.jpg')
im3 = Image.open('./outputSignature/recorte_3.jpg')
# --- Recorte horizontal
im4 = Image.open('./outputSignature/recorte_4.jpg')
# --- Imagen para dejar espacio vertical
espacioh = Image.open('./outputSignature/recorte_5.jpg')
# --- Imagen para dejar espacio horizontal
espaciov = Image.open('./outputSignature/recorte_6.jpg')

# --- Función para concatenar verticalmente 
def get_concat_v_resize(im1, im2, resample=Image.BICUBIC, resize_big_image=True):
   if im1.width == im2.width:
       _im1 = im1
       _im2 = im2
   elif (((im1.width > im2.width) and resize_big_image) or
         ((im1.width < im2.width) and not resize_big_image)):
       _im1 = im1.resize(
           (im2.width, int(im1.height * im2.width / im1.width)), resample=resample)
       _im2 = im2
   else:
       _im1 = im1
       _im2 = im2.resize(
           (im1.width, int(im2.height * im1.width / im2.width)), resample=resample)
   dst = Image.new('RGB', (_im1.width, _im1.height + _im2.height))
   dst.paste(_im1, (0, 0))
   dst.paste(_im2, (0, _im1.height))
   return dst

# --- Función para concatenar horizontalmente
def get_concat_h_resize(im1, im2, resample=Image.BICUBIC, resize_big_image=True):
    if im1.height == im2.height:
        _im1 = im1
        _im2 = im2
    elif (((im1.height > im2.height) and resize_big_image) or
          ((im1.height < im2.height) and not resize_big_image)):
        _im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((int(im2.width * im1.height / im2.height), im1.height), resample=resample)
    dst = Image.new('RGB', (_im1.width + _im2.width, _im1.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (_im1.width, 0))
    return dst

# --- Agregar espacio en blanco entre las imagenes verticales
get_concat_v_resize(im0, espacioh, resize_big_image=False).save('./outputSignature/concat0.jpg')

get_concat_v_resize(im1, espacioh, resize_big_image=False).save('./outputSignature/concat1.jpg')

get_concat_v_resize(im2, espacioh, resize_big_image=False).save('./outputSignature/concat2.jpg')

get_concat_v_resize(im3, espacioh, resize_big_image=False).save('./outputSignature/concat3.jpg')

# --- Agregar espacio en blanco a la imagen horizontal
get_concat_h_resize(espaciov,im4, resize_big_image=False).save('./outputSignature/concat4.jpg')

# --- Concatenar imagenes verticalmente
im5 = Image.open('./outputSignature/concat0.jpg')
im6 = Image.open('./outputSignature/concat1.jpg')
get_concat_v_resize(im5, im6, resize_big_image=False).save('./outputSignature/concat5.jpg')

im7 = Image.open('./outputSignature/concat5.jpg')
im8 = Image.open('./outputSignature/concat2.jpg')

get_concat_v_resize(im7, im8, resize_big_image=False).save('./outputSignature/concat7.jpg')

im9 = Image.open('./outputSignature/concat7.jpg')
im10 = Image.open('./outputSignature/concat3.jpg')
get_concat_v_resize(im9, im10, resize_big_image=False).save('./outputSignature/concat8.jpg')

# --- Concatenar imagen horizontal
im11 = Image.open('./outputSignature/concat8.jpg')
im12 = Image.open('./outputSignature/concat4.jpg')
get_concat_h_resize(im11, im12, resize_big_image=False).save('./outputSignature/firmas4_0.jpg')



# --- Paso 3
# --- Busca la imagen que se concatenó en la ultima ruta definida
image = cv2.imread("./outputSignature/firmas4_0.jpg")

# --- Reliza un ajuste de tamaño a la imegen ---
image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

result = image.copy()

#--- Convierte la imagen a escala de grises para usarlo en un umbral binario ---
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# --- Ejectua una acción para obtener una imagen con un umbral binario invertido ---
retval, thresh_gray = cv2.threshold(
    gray, 0, 255, type=cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

cv2.imshow('sign_thresh_gray', thresh_gray) # --- Muestra la imagen ---

# --- Se realiza una expansión horizontal y vertical para juntar una misma firma que se encuentra separada por trazos ---
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))
threshed = cv2.morphologyEx(thresh_gray, cv2.MORPH_CLOSE, rect_kernel)
cv2.imshow('threshed', threshed) # --- Muestra la imagen ---
cv2.waitKey()

#--- Busca todos los contornos y áreas externos de la imagen binaria ( threshed ) ---
contours = cv2.findContours(threshed, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

# --- Cicla todas los contornos y áreas encontrados en la imagen ---
# --- Posterior con una función obtendremos una imagen por cada firma encontrada. ---
for i, cnt in enumerate(contours):
    # -- Dibuja un rectángulo aproximado alrededor de la imagen binaria
    x, y, w, h = cv2.boundingRect(cnt)
    # -- Obtine los valores para poder dibujar un contrno por sin angulos interiores mayores a 180 grados.
    # -- Cada que localiza un punto final en el trazo de la firma lo detecta como un extremo del contorno 
    hull = cv2.convexHull(cnt)
    cv2.drawContours(image, [hull], -1, (0, 0, 255), 1) # -- Dibuja el contorno convexHull con un color rojo, con el fin de representarlo en una venta.
    # cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
    if cv2.contourArea(cnt) > 500: # --- Validación para detectar el área dentro de un contorno, esto es para no recuperar cosas pequeñas en la imagen
        # --- Recupera una región rectangular tomando como referencias los contornos de convexHull y guardar esa región como una imagen
        roi = image[y:y + h, x: x + w]
        cv2.imshow('Imagen_{}.jpg'.format(i), roi) # --- Muestra la imagen ---
        cv2.imwrite("./outputSignature/" + 'Signature_{}.jpg'.format(i), roi) # --- Guarda la imagen ---
        cv2.waitKey()

cv2.imshow('convex hull', image) # --- Muestra la imagen de convex hull ---
cv2.imshow('convex Draw', result) # --- Muestra la imagen de rectangle ---
cv2.waitKey()
