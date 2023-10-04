import cv2
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import threading
from django.shortcuts import render
import face_recognition
import os
import time

# global f_circulo_encodings, f_circulo_names
# f_circulo_encodings = []
# f_circulo_names = []

# circuloPath = os.path.dirname(os.path.abspath(__file__))
# circuloPath = circuloPath + '\\encodings.txt'
# circuloPath = circuloPath.replace("\\","/")

# with open(circuloPath, "r") as file:
#     for line in file.readlines():
#         # Separar el nombre y los encodings usando la coma como delimitador
#         parts = line.strip().split(",")
#         name = parts[0]
#         encoding_str = parts[1:]

#         # Convertir los encodings de strings a flotantes
#         encoding = [float(x) for x in encoding_str]

#         # Agregar el nombre y los encodings a las listas correspondientes
#         f_circulo_names.append(name)
#         f_circulo_encodings.append(encoding)


@gzip.gzip_page
def video_feed(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam),content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request,'videostream.html')


class VideoCamera(object):

    def __init__(self):
        # global f_circulo_encodings, f_circulo_names
        # self.f_circulo_encodings = f_circulo_encodings
        # self.f_circulo_names = f_circulo_names
        # print(self.f_circulo_names)
        # print(self.f_circulo_encodings)
        self.video = cv2.VideoCapture(0)
        
        print("hola")
        self.f_circulo_encodings = []
        self.f_circulo_names = []
        circuloPath = os.path.dirname(os.path.abspath(__file__))
        circuloPath = circuloPath + '\\encodings.txt'
        circuloPath = circuloPath.replace("\\","/")
        with open(circuloPath, "r") as file:
            for line in file.readlines():
                # Separar el nombre y los encodings usando la coma como delimitador
                parts = line.strip().split(",")
                name = parts[0]
                encoding_str = parts[1:]

                # Convertir los encodings de strings a flotantes
                encoding = [float(x) for x in encoding_str]

                # Agregar el nombre y los encodings a las listas correspondientes
                self.f_circulo_names.append(name)
                self.f_circulo_encodings.append(encoding)



        (self.grabbed,self.frame) = self.video.read()
        threading.Thread(target=self.update,args=()).start()
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        image = self.frame
        # print(self.f_circulo_names)
        
        f_data_locations = face_recognition.face_locations(image) # Obtiene las coordenadas del rostro en la imagen
        if f_data_locations != []:                                # Si se detecta un rostro
            print("[PROCESO] Rostro detectado")
            face_names = []
            f_frame_codings = face_recognition.face_encodings(image,f_data_locations)        # Obtenemos las características del rostro encontrado
            for face_encoding, (top, right, bottom, left) in zip(f_frame_codings, f_data_locations):                                            # Comparamos el rostro encontrado con los rostros conocidos
                matches = face_recognition.compare_faces(self.f_circulo_encodings, face_encoding)
                print("Matches: ", matches)
                if True in matches:                                                          # Si se reconoce el rostro
                    index = matches.index(True)
                    name = self.f_circulo_names[index]
                    face_names.append(name)
                else:
                    name = "Desconocido"
                cv2.rectangle(image, (left, top), (right, bottom), (0,255,0), 2)
                cv2.rectangle(image, (left, bottom -10), (right, bottom), (0,255,0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, name, (left +3, bottom -3), font, 0.4, (255,255,255), 1)
        else:
            print("[ALERTA] No se detecto un rostro")


        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def update(self):
        while True:
            (self.grabbed,self.frame) = self.video.read()
        

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') 
# import cv2
# from django.http import StreamingHttpResponse
# from django.views.decorators import gzip

# from django.shortcuts import render
# #import logger


# def videostream(request):
#     return render(request, 'videostream.html')

# class VideoCamera:
#     def __init__(self):
#         self.video = cv2.VideoCapture("http://192.168.0.250:8080/video")
#         print("algo esta prenido")
#         if(self.video.isOpened() == False):
#             print("Error opening video stream or file")

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         success, image = self.video.read()
#         # Dibuja un rectángulo en la imagen
#         cv2.rectangle(image, (100, 100), (300, 300), (0, 255, 0), 2)  # Cambia los valores según tus necesidades
#         _, buffer = cv2.imencode('.jpg', image)
#         #make a logger for checking if the function is called
#         print("get_frame")
#         return buffer.tobytes()

    


# video_camera = VideoCamera()

# @gzip.gzip_page
# def video_feed(request):
#     return StreamingHttpResponse(video_camera.get_frame(), content_type="multipart/x-mixed-replace;boundary=frame")
