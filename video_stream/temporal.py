        while True:
            leido, image = cap.read()
            if not leido:break
            #small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25) # Reduce el tamaño del frame para que sea más rápido el procesamiento
            elapsed_time = time.time() - start_time_fps
            frame_count += 1
            f_data_locations = face_recognition.face_locations(image) # Obtiene las coordenadas del rostro en la imagen
            if f_data_locations != []:                                # Si se detecta un rostro
                print("[PROCESO] Rostro detectado")
                face_names = []
                f_frame_codings = face_recognition.face_encodings(image,f_data_locations)        # Obtenemos las características del rostro encontrado
                for face_encoding, (top, right, bottom, left) in zip(f_frame_codings, f_data_locations):                                            # Comparamos el rostro encontrado con los rostros conocidos
                    matches = face_recognition.compare_faces(f_circulo_encodings, face_encoding)
                    print("Matches: ", matches)
                    if True in matches:                                                          # Si se reconoce el rostro
                        index = matches.index(True)
                        name = f_circulo_names[index]
                        face_names.append(name)
                    else:
                        name = "Desconocido"
                    cv2.rectangle(image, (left, top), (right, bottom), (0,255,0), 2)
                    cv2.rectangle(image, (left, bottom -10), (right, bottom), (0,255,0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(image, name, (left +3, bottom -3), font, 0.4, (255,255,255), 1)
            else:
                print("[ALERTA] No se detecto un rostro")
            if elapsed_time >= 1:
                    fps = frame_count / elapsed_time
                    frame_count = 0
                    start_time_fps = time.time()
            text = f"FPS: {fps}"
            cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)    
            cv2.imshow('Frame',image)
            if cv2.waitKey(1) 