import cv2
import mediapipe as mp
import numpy as np
import random

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

class JuegoDeFiguras:
    def __init__(self):
        self.ventana = "Atrapa La Figura Divertida"
        self.estado_juego = "menu"
        self.captura = cv2.VideoCapture(0)
        self.figuras_cayendo = []
        self.velocidad_figura = 5
        self.puntuacion = 0
        self.opciones_menu = ["Iniciar Juego", "Salir"]
        self.opcion_seleccionada_indice = 0
        self.fuente = cv2.FONT_HERSHEY_SIMPLEX
        self.escala_fuente = 1
        self.color_fuente = (255, 255, 255)
        self.grosor_fuente = 2
        self.altura_item_menu = 40

        cv2.namedWindow(self.ventana)
        self.configurar_interacciones_menu()

    def configurar_interacciones_menu(self):
        cv2.setMouseCallback(self.ventana, self.callback_raton)

    def callback_raton(self, evento, x, y, banderas, param):
        if self.estado_juego == "menu":
            if evento == cv2.EVENT_MOUSEMOVE:
                for i, opcion in enumerate(self.opciones_menu):
                    y_inicio_texto = (self.captura.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2) + (i * self.altura_item_menu) - (len(self.opciones_menu) * self.altura_item_menu // 2)
                    y_fin_texto = y_inicio_texto + self.altura_item_menu
                    if y_inicio_texto < y < y_fin_texto:
                        self.opcion_seleccionada_indice = i
                        break
                else:
                    self.opcion_seleccionada_indice = -1
            elif evento == cv2.EVENT_LBUTTONDOWN:
                if self.opcion_seleccionada_indice == 0:
                    self.iniciar_juego()
                elif self.opcion_seleccionada_indice == 1:
                    self.salir_programa()

    def iniciar_juego(self):
        self.restablecer_estado_juego()
        self.estado_juego = "jugando"
        self.figuras_cayendo = []
        self.puntuacion = 0

    def restablecer_estado_juego(self):
        self.figuras_cayendo = []
        self.velocidad_figura = 5
        self.puntuacion = 0

    def estado_fin_del_juego(self):
        self.estado_juego = "game_over"

    def salir_programa(self):
        self.captura.release()
        cv2.destroyAllWindows()

    def dibujar_menu(self, frame):
        altura, ancho, _ = frame.shape
        centro_x, centro_y = ancho // 2, altura // 2

        for i, opcion in enumerate(self.opciones_menu):
            texto_x = centro_x - (len(opcion) * self.escala_fuente * 8)
            texto_y = centro_y + (i * self.altura_item_menu) - (len(self.opciones_menu) * self.altura_item_menu // 2)
            color = (0, 255, 0) if i == self.opcion_seleccionada_indice else self.color_fuente
            cv2.putText(frame, opcion, (texto_x, texto_y), self.fuente, self.escala_fuente, color, self.grosor_fuente)

        cv2.putText(frame, "Atrapa La Figura Divertida", (10, 30), self.fuente, 1, (255, 255, 255), 2)

    def dibujar_fin_del_juego(self, frame):
        altura, ancho, _ = frame.shape
        centro_x, centro_y = ancho // 2, altura // 2
        cv2.putText(frame, "¡Fin del Juego!", (centro_x - 120, centro_y - 20), self.fuente, 2, (0, 0, 255), 3)
        cv2.putText(frame, f"Puntuacion Final: {self.puntuacion}", (centro_x - 150, centro_y + 30), self.fuente, 1, (0, 0, 255), 3)
        
        btn_reiniciar_x = centro_x - 100
        btn_reiniciar_y = centro_y + 80
        btn_ancho = 200
        btn_alto = 40
        cv2.rectangle(frame, (btn_reiniciar_x, btn_reiniciar_y), (btn_reiniciar_x + btn_ancho, btn_reiniciar_y + btn_alto), (0, 255, 0), -1)
        cv2.putText(frame, "Jugar de Nuevo", (btn_reiniciar_x + 20, btn_reiniciar_y + 25), self.fuente, 0.7, (0, 0, 0), 2)

        btn_salir_x = centro_x - 100
        btn_salir_y = centro_y + 140
        cv2.rectangle(frame, (btn_salir_x, btn_salir_y), (btn_salir_x + btn_ancho, btn_salir_y + btn_alto), (255, 0, 0), -1)
        cv2.putText(frame, "Salir", (btn_salir_x + 70, btn_salir_y + 25), self.fuente, 0.7, (0, 0, 0), 2)

    def manejar_clic_boton_fin_juego(self, x, y):
        if self.estado_juego == "game_over":
            altura, ancho, _ = self.captura.read()[1].shape
            centro_x, centro_y = ancho // 2, altura // 2
            
            btn_reiniciar_x = centro_x - 100
            btn_reiniciar_y = centro_y + 80
            btn_ancho = 200
            btn_alto = 40
            if btn_reiniciar_x < x < btn_reiniciar_x + btn_ancho and btn_reiniciar_y < y < btn_reiniciar_y + btn_alto:
                self.iniciar_juego()
                return

            btn_salir_x = centro_x - 100
            btn_salir_y = centro_y + 140
            if btn_salir_x < x < btn_salir_x + btn_ancho and btn_salir_y < y < btn_salir_y + btn_alto:
                self.salir_programa()
                return
    
    def callback_raton_fin_juego(self, evento, x, y, banderas, param):
        if evento == cv2.EVENT_LBUTTONDOWN:
            self.manejar_clic_boton_fin_juego(x, y)


    def ejecutar(self):
        with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as manos, \
             mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as detector_rostro:
            
            while True:
                exito, imagen = self.captura.read()
                if not exito:
                    break

                imagen = cv2.flip(imagen, 1)
                imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
                
                resultados_manos = manos.process(imagen_rgb)
                resultados_rostro = detector_rostro.process(imagen_rgb)
                
                imagen_bgr = cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2BGR)

                if self.estado_juego == "menu":
                    self.dibujar_menu(imagen_bgr)
                    cv2.setMouseCallback(self.ventana, self.callback_raton)
                    
                elif self.estado_juego == "jugando":
                    if resultados_manos.multi_hand_landmarks:
                        for puntos_mano in resultados_manos.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(imagen_bgr, puntos_mano, mp_hands.HAND_CONNECTIONS)

                            punta_dedo_x = int(puntos_mano.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * imagen_bgr.shape[1])
                            punta_dedo_y = int(puntos_mano.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * imagen_bgr.shape[0])

                            cv2.circle(imagen_bgr, (punta_dedo_x, punta_dedo_y), 10, (0, 255, 0), -1)

                            for i in range(len(self.figuras_cayendo) - 1, -1, -1):
                                fig_x, fig_y, fig_tamano = self.figuras_cayendo[i]
                                if fig_y + fig_tamano // 2 > punta_dedo_y > fig_y - fig_tamano // 2 and \
                                   fig_x - fig_tamano // 2 < punta_dedo_x < fig_x + fig_tamano // 2:
                                    self.figuras_cayendo.pop(i)
                                    self.puntuacion += 1

                    if random.randint(1, 40) == 1:
                        tamano_figura = random.randint(30, 60)
                        fig_x = random.randint(tamano_figura // 2, imagen_bgr.shape[1] - tamano_figura // 2)
                        fig_y = 0
                        self.figuras_cayendo.append((fig_x, fig_y, tamano_figura))

                    for i in range(len(self.figuras_cayendo) - 1, -1, -1):
                        fig_x, fig_y, fig_tamano = self.figuras_cayendo[i]
                        fig_y += self.velocidad_figura
                        cv2.circle(imagen_bgr, (fig_x, fig_y), fig_tamano // 2, (0, 0, 255), -1)
                        self.figuras_cayendo[i] = (fig_x, fig_y, fig_tamano)

                        if fig_y > imagen_bgr.shape[0]:
                            self.figuras_cayendo.pop(i)
                            self.estado_fin_del_juego()

                    cv2.putText(imagen_bgr, f"Puntuacion: {self.puntuacion}", (10, 30), self.fuente, 1, (255, 255, 255), 3)
                    
                    if resultados_rostro.multi_face_landmarks:
                        for face_landmarks in resultados_rostro.multi_face_landmarks:
                            mp_drawing.draw_landmarks(
                                image=imagen_bgr,
                                landmark_list=face_landmarks,
                                connections=mp_face_mesh.FACEMESH_TESSELATION,
                                landmark_drawing_spec=None,
                                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1))

                elif self.estado_juego == "game_over":
                    self.dibujar_fin_del_juego(imagen_bgr)
                    cv2.setMouseCallback(self.ventana, self.callback_raton_fin_juego)

                cv2.imshow(self.ventana, imagen_bgr)

                if self.estado_juego == "menu":
                    if cv2.waitKey(1) & 0xFF == 27:
                        self.salir_programa()
                elif self.estado_juego == "jugando":
                    if cv2.waitKey(1) & 0xFF == 27:
                        self.estado_juego = "menu"


if __name__ == "__main__":
    juego = JuegoDeFiguras()
    juego.ejecutar()
