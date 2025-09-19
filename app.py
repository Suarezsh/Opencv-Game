import cv2
import mediapipe as mp
import numpy as np
import random
import time
import os
import sqlite3

class GameDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('game_progress.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                max_level INTEGER DEFAULT 1,
                prime_score INTEGER DEFAULT 0,
                total_figures_caught INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def save_player_progress(self, name, level, current_round_score, total_figures_caught_accumulated):
        try:
            self.cursor.execute('SELECT max_level, prime_score, total_figures_caught FROM players WHERE name = ?', (name,))
            player_data = self.cursor.fetchone()

            if player_data:
                current_max_level, current_prime_score, current_total_figures_accumulated = player_data
                
                new_prime_score = max(current_prime_score, current_round_score)
                
                self.cursor.execute('''
                    UPDATE players SET max_level = ?, prime_score = ?, total_figures_caught = ?
                    WHERE name = ?
                ''', (current_max_level, new_prime_score, total_figures_caught_accumulated, name))
            else:
                self.cursor.execute('''
                    INSERT INTO players (name, max_level, prime_score, total_figures_caught)
                    VALUES (?, ?, ?, ?)
                ''', (name, level, current_round_score, total_figures_caught_accumulated))
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving progress: {e}")

    def get_player_progress(self, name):
        self.cursor.execute('SELECT * FROM players WHERE name = ?', (name,))
        return self.cursor.fetchone()

    def reset_all_progress(self):
        self.cursor.execute('DELETE FROM players')
        self.conn.commit()

class GameFigures:
    def __init__(self):
        self.db = GameDatabase()
        self.player_name = None
        self.window_name = "Atrapa las Figuras Divertidas"
        self.game_state = "enter_name"
        self.capture = cv2.VideoCapture(0)
        
        if not self.capture.isOpened():
            print("Error: No se pudo abrir la cámara.")
            exit()

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        
        self._load_images()
        
        self.falling_figures = []
        self.figure_speed = 5
        self.current_round_score = 0 
        self.total_figures_caught = 0 
        self.current_level = 1
        self.high_score = 0 
        
        self.menu_options = ["Iniciar Juego", "Reiniciar Progreso", "Salir"]
        self.selected_option_index = 0
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_color = (255, 255, 255)
        self.font_thickness = 2
        
        self.name_input_text = ""
        self.cursor_visible = True
        self.cursor_timer = 0

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 1280, 720)

        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils

        self.setup_mouse_interactions()

    def setup_mouse_interactions(self):
        cv2.setMouseCallback(self.window_name, self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, param):
        if self.game_state == "menu":
            if event == cv2.EVENT_MOUSEMOVE:
                self._update_menu_hover(x, y)
            elif event == cv2.EVENT_LBUTTONDOWN:
                self._select_menu_option_mouse(x, y)
        elif self.game_state == "game_over":
            if event == cv2.EVENT_MOUSEMOVE:
                self._update_game_over_hover(x, y)
            elif event == cv2.EVENT_LBUTTONDOWN:
                self._select_game_over_option_mouse(x, y)

    def _update_menu_hover(self, x, y):
        height, width, _ = self.capture.read()[1].shape
        center_x, center_y = width // 2, height // 2

        for i, option in enumerate(self.menu_options):
            y_pos = center_y + (i * 60)
            text_size, _ = cv2.getTextSize(option, self.font, self.font_scale, self.font_thickness)
            option_width = text_size[0]
            
            if center_x - option_width // 2 < x < center_x + option_width // 2 and \
               y_pos - 20 < y < y_pos + 20:
                self.selected_option_index = i
                return
        self.selected_option_index = -1

    def _select_menu_option_mouse(self, x, y):
        height, width, _ = self.capture.read()[1].shape
        center_x, center_y = width // 2, height // 2

        for i, option in enumerate(self.menu_options):
            y_pos = center_y + (i * 60)
            text_size, _ = cv2.getTextSize(option, self.font, self.font_scale, self.font_thickness)
            option_width = text_size[0]
            
            if center_x - option_width // 2 < x < center_x + option_width // 2 and \
               y_pos - 20 < y < y_pos + 20:
                if i == 0:
                    self.start_game()
                elif i == 1:
                    self._reset_progress()
                elif i == 2:
                    self._exit_game()
                break

    def _update_game_over_hover(self, x, y):
        height, width, _ = self.capture.read()[1].shape
        center_x, center_y = width // 2, height // 2

        buttons = [
            {"text": "Jugar de Nuevo", "y_offset": 100},
            {"text": "HOME", "y_offset": 160},
            {"text": "Salir", "y_offset": 220}
        ]

        for i, btn in enumerate(buttons):
            btn_x = center_x - 100
            btn_y = center_y + btn["y_offset"]
            btn_width, btn_height = 200, 40

            if btn_x < x < btn_x + btn_width and btn_y < y < btn_y + btn_height:
                self.selected_option_index = i
                return
        self.selected_option_index = -1

    def _select_game_over_option_mouse(self, x, y):
        height, width, _ = self.capture.read()[1].shape
        center_x, center_y = width // 2, height // 2

        buttons = [
            {"text": "Jugar de Nuevo", "y_offset": 100, "action": self.start_game},
            {"text": "HOME", "y_offset": 160, "action": lambda: self.set_game_state("menu")},
            {"text": "Salir", "y_offset": 220, "action": self._exit_game}
        ]

        for i, btn in enumerate(buttons):
            btn_x = center_x - 100
            btn_y = center_y + btn["y_offset"]
            btn_width, btn_height = 200, 40

            if btn_x < x < btn_x + btn_width and btn_y < y < btn_y + btn_height:
                btn["action"]()
                return

    def _load_images(self):
        self.images = []
        img_dir = "./img"
        
        for i in range(1, 7):
            img_path = os.path.join(img_dir, f"img{i}.png")
            if os.path.exists(img_path):
                img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                if img is not None:
                    img = cv2.resize(img, (80, 80))
                    self.images.append(img)
            else:
                print(f"Advertencia: No se encontró la imagen {img_path}")
        
        if not self.images:
            print("Error: No se cargaron imágenes. Asegúrate de que la carpeta './img' contenga img1.png a img6.png.")
            exit()

    def run(self):
        with self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands, \
             self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
            
            while True:
                success, frame = self.capture.read()
                if not success:
                    print("Error: No se pudo leer el frame de la cámara.")
                    break

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                hand_results = hands.process(rgb_frame)
                face_results = face_mesh.process(rgb_frame)
                
                bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

                if self.game_state == "enter_name":
                    self._draw_name_input(bgr_frame)
                elif self.game_state == "menu":
                    self._draw_menu(bgr_frame)
                elif self.game_state == "playing":
                    self._handle_playing_state(bgr_frame, hand_results, face_results)
                elif self.game_state == "game_over":
                    self._handle_game_over(bgr_frame)

                cv2.imshow(self.window_name, bgr_frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if self.game_state == "enter_name":
                    if key == 13: # Enter
                        self.player_name = self.name_input_text if self.name_input_text else "Jugador"
                        player_data = self.db.get_player_progress(self.player_name)
                        if player_data:
                            self.current_level = player_data[2]
                            self.total_figures_caught = player_data[4] # Racha total acumulada
                            self.high_score = player_data[3] # Mejor puntuación individual (PRIME)
                        else: # Jugador nuevo o progreso reiniciado
                            self.current_level = 1
                            self.total_figures_caught = 0
                            self.high_score = 0
                        self.game_state = "menu"
                    elif key == 8: # Backspace
                        self.name_input_text = self.name_input_text[:-1]
                    elif key != 255: 
                        self.name_input_text += chr(key)
                
                if key == 27:  # ESC
                    if self.game_state == "playing":
                        self.game_state = "menu"
                    elif self.game_state == "menu":
                        self._exit_game()
                    elif self.game_state == "game_over":
                        self._exit_game()
                
                if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break
                
                if self.game_state == "enter_name":
                    self.cursor_timer += 1
                    if self.cursor_timer % 30 == 0:
                        self.cursor_visible = not self.cursor_visible

        self.capture.release()
        cv2.destroyAllWindows()

    def _draw_name_input(self, frame):
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2

        title_text = "Ingresa tu nombre"
        cv2.putText(frame, title_text, (center_x - 180, center_y - 50), 
                    self.font, 1.8, (0, 255, 0), 3)

        input_box_width = 400
        input_box_height = 50
        input_box_x = center_x - input_box_width // 2
        input_box_y = center_y

        cv2.rectangle(frame, (input_box_x, input_box_y), 
                      (input_box_x + input_box_width, input_box_y + input_box_height), 
                      (255, 255, 255), 2)

        text_to_display = self.name_input_text
        if self.cursor_visible:
            text_to_display += "|"
        
        cv2.putText(frame, text_to_display, (input_box_x + 10, input_box_y + 35), 
                    self.font, 1, (255, 255, 255), 2)
        
        instruction_text = "Usa el teclado. Presiona ENTER para continuar."
        cv2.putText(frame, instruction_text, (center_x - 250, height - 50), 
                    self.font, 0.7, (200, 200, 200), 1)

    def _draw_menu(self, frame):
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2

        welcome_text = f"Bienvenido, {self.player_name}!"
        cv2.putText(frame, welcome_text, (center_x - 200, 100), 
                    self.font, 1.5, (0, 255, 0), 3)

        for i, option in enumerate(self.menu_options):
            y_pos = center_y + (i * 60)
            color = (0, 255, 0) if i == self.selected_option_index else (255, 255, 255)
            
            text_size, _ = cv2.getTextSize(option, self.font, self.font_scale, self.font_thickness)
            text_x = center_x - text_size[0] // 2
            
            cv2.putText(frame, option, (text_x, y_pos), 
                        self.font, self.font_scale, color, self.font_thickness)
        
        cv2.putText(frame, "Usa el raton o flechas y ENTER", (center_x - 200, height - 50), 
                    self.font, 0.7, (200, 200, 200), 1)

    def _reset_progress(self):
        self.db.reset_all_progress()
        self.total_figures_caught = 0 
        self.current_level = 1
        self.score = 0 
        self.high_score = 0 
        self.player_name = None 
        print("Progreso reiniciado. Se pedirá nombre al iniciar.")
        self.game_state = "enter_name"

    def start_game(self):
        player_data = self.db.get_player_progress(self.player_name)
        if player_data:
            self.current_level = player_data[2]
            self.total_figures_caught = player_data[4] # Racha total acumulada
            self.high_score = player_data[3] # Mejor puntuación individual (PRIME)
        else: # Jugador nuevo o progreso reiniciado
            self.current_level = 1
            self.total_figures_caught = 0
            self.high_score = 0
        
        self.score = 0 # SIEMPRE reinicia el score de la ronda actual
        self.game_state = "playing"
        self.falling_figures = []
        self.figure_speed = 5
        print("Iniciando juego...")

    def _exit_game(self):
        self.capture.release()
        cv2.destroyAllWindows()
        exit()

    def _handle_playing_state(self, frame, hand_results, face_results):
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                self._process_hand_interaction(frame, hand_landmarks)

        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1))

        self._spawn_falling_figures(frame)
        self._update_falling_figures(frame)
        
        if self.total_figures_caught >= 30 * self.current_level:
            self.current_level += 1
            self.figure_speed += 2
            print(f"Nivel {self.current_level} alcanzado!")

        cv2.putText(frame, f"Nivel: {self.current_level}", (10, 30), 
                    self.font, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Racha: {self.total_figures_caught}", (10, 60), 
                    self.font, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Puntos: {self.score}", (10, 90), 
                    self.font, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"PRIME: {self.high_score}", (10, 120),
                    self.font, 1, (255, 255, 100), 2)

    def _spawn_falling_figures(self, frame):
        spawn_chance = max(10, 40 - (self.current_level - 1) * 2)
        if random.randint(1, spawn_chance) == 1:
            if not self.images: return
            img = random.choice(self.images)
            fig_x = random.randint(img.shape[1] // 2, frame.shape[1] - img.shape[1] // 2)
            self.falling_figures.append((fig_x, 0, img))

    def _update_falling_figures(self, frame):
        for i in range(len(self.falling_figures) - 1, -1, -1):
            fig_x, fig_y, img = self.falling_figures[i]
            fig_y += self.figure_speed
            self._overlay_image(frame, img, (fig_x - img.shape[1]//2, fig_y - img.shape[0]//2))
            self.falling_figures[i] = (fig_x, fig_y, img)
            
            if fig_y > frame.shape[0]:
                self.falling_figures.pop(i)
                self._handle_game_over_state()

    def _process_hand_interaction(self, frame, hand_landmarks):
        tip_index_landmark = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        tip_x = int(tip_index_landmark.x * frame.shape[1])
        tip_y = int(tip_index_landmark.y * frame.shape[0])
        
        cv2.circle(frame, (tip_x, tip_y), 10, (0, 255, 0), -1)

        for i in range(len(self.falling_figures) - 1, -1, -1):
            fig_x, fig_y, img = self.falling_figures[i]
            
            dist_sq = (tip_x - fig_x)**2 + (tip_y - fig_y)**2
            radius_sum = (img.shape[1] // 2) + 10
            
            if dist_sq < radius_sum**2:
                self.falling_figures.pop(i)
                self.score += 1
                self.total_figures_caught += 1
                self.db.save_player_progress(self.player_name, self.current_level, self.score, self.total_figures_caught)

    def _overlay_image(self, background, foreground, location):
        x, y = location
        bg_h, bg_w = background.shape[:2]
        fg_h, fg_w = foreground.shape[:2]
        
        start_x = max(x, 0)
        start_y = max(y, 0)
        end_x = min(x + fg_w, bg_w)
        end_y = min(y + fg_h, bg_h)
        
        bg_region = background[start_y:end_y, start_x:end_x]
        
        fg_x1 = start_x - x
        fg_y1 = start_y - y
        fg_x2 = fg_x1 + (end_x - start_x)
        fg_y2 = fg_y1 + (end_y - start_y)
        
        fg_slice = foreground[fg_y1:fg_y2, fg_x1:fg_x2]
        
        if fg_slice.shape[2] == 4: 
            alpha = fg_slice[:, :, 3] / 255.0
            alpha_inv = 1.0 - alpha
            fg_rgb = fg_slice[:, :, :3]
            bg_rgb = bg_region[:, :, :3]
            
            final_rgb = (alpha[:, :, np.newaxis] * fg_rgb + 
                         alpha_inv[:, :, np.newaxis] * bg_rgb)
            
            background[start_y:end_y, start_x:end_x, :3] = final_rgb
        else:
            background[start_y:end_y, start_x:end_x] = fg_slice

    def _handle_game_over_state(self):
        self.game_state = "game_over"
        self.db.save_player_progress(self.player_name, self.current_level, self.score, self.total_figures_caught)

    def _handle_game_over(self, frame):
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2

        buttons = [
            {"text": "Jugar de Nuevo", "y_offset": 100, "action": self.start_game},
            {"text": "HOME", "y_offset": 160, "action": lambda: self.set_game_state("menu")},
            {"text": "Salir", "y_offset": 220, "action": self._exit_game}
        ]

        cv2.putText(frame, "Fin del Juego", (center_x - 200, center_y - 150), 
                    self.font, 2, (0, 0, 255), 3)
        
        cv2.putText(frame, f"Puntos: {self.score}", 
                    (center_x - 150, center_y - 50), self.font, 1, (255, 255, 255), 2)
        
        cv2.putText(frame, f"Nivel: {self.current_level}", 
                    (center_x - 150, center_y), self.font, 1, (0, 255, 0), 2)
        
        cv2.putText(frame, f"Racha: {self.total_figures_caught}", 
                    (center_x - 170, center_y + 50), self.font, 1, (255, 255, 0), 2)
        
        if self.player_name: 
            player_data = self.db.get_player_progress(self.player_name)
            if player_data:
                prime_score_text = f"PRIME: {player_data[3]}"
                cv2.putText(frame, prime_score_text, (center_x - 170, center_y + 100), 
                            self.font, 1, (255, 255, 100), 2)

        for i, btn in enumerate(buttons):
            btn_x = center_x - 100
            btn_y = center_y + btn["y_offset"]
            btn_width, btn_height = 200, 40

            btn_color = (0, 255, 0) if i == self.selected_option_index else (100, 100, 100)
            
            cv2.rectangle(frame, (btn_x, btn_y), 
                          (btn_x + btn_width, btn_y + btn_height), 
                          btn_color, -1)
            
            text_size, _ = cv2.getTextSize(btn["text"], self.font, 0.7, 2)
            text_x = btn_x + (btn_width - text_size[0]) // 2
            text_y = btn_y + btn_height // 2 + text_size[1] // 2
            
            cv2.putText(frame, btn["text"], 
                        (text_x, text_y), 
                        self.font, 0.7, (0, 0, 0), 2)
        
        cv2.putText(frame, "Usa el raton o flechas y ENTER", 
                    (center_x - 200, height - 50), self.font, 0.7, (200, 200, 200), 1)

    def set_game_state(self, state):
        self.game_state = state

if __name__ == "__main__":
    game = GameFigures()
    game.run()
