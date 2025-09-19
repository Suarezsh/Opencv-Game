# 🌟 Atrapa las Figuras Divertidas 🌟

¡Bienvenido a **Atrapa las Figuras Divertidas**! Un juego de destreza e interacción visual desarrollado con la potencia de **OpenCV** y **MediaPipe**. ¡Pon a prueba tu velocidad y precisión con un simple gesto de tu mano!

---

## ✨ ¿Qué es este juego?

"Atrapa las Figuras Divertidas" transforma tu cámara web en un controlador de juego. Utilizando **OpenCV** para capturar y procesar el video en tiempo real, y **MediaPipe** para detectar con precisión tus manos y dedos, el juego te desafía a atrapar figuras que caen en la pantalla. ¡Tu dedo índice es tu única herramienta!

Este proyecto combina la tecnología de visión artificial con mecánicas de juego clásicas, todo ello envuelto en una experiencia fluida y accesible.

---

## 🚀 Características Principales

*   **Control de Gestos Revolucionario:** Olvídate del ratón y el teclado para jugar. Mueve tu mano y tu dedo índice será tu puntero. ¡La tecnología al servicio de la diversión!
*   **Jugabilidad Adictiva:** ¡Atrapa tantas figuras como puedas! Observa cómo la velocidad y la dificultad aumentan, poniendo a prueba tus reflejos.
*   **Sistema de Niveles y Racha:** Supera niveles basándote en tu **Racha Total** (figuras atrapadas acumulativamente) y compite por la **PRIME** (tu mejor puntuación individual).
*   **Gestión de Jugadores Inteligente:**
    *   **Registro Personalizado:** Cada jugador tiene su propio perfil.
    *   **Base de Datos Persistente (SQLite):** Tu progreso (Nivel, PRIME, Racha Total) se guarda de forma segura. ¡Tu avance nunca se pierde!
    *   **Reiniciar Progreso:** ¿Quieres empezar de nuevo? Borra todos los datos y vuelve a ser un novato.
*   **Interfaz de Usuario Dinámica:**
    *   **Menú Principal Atractivo:** Navega con el ratón o el teclado para iniciar el juego, gestionar tu progreso o salir.
    *   **Entrada de Nombre Estilo Clásico:** Un campo de texto claro y animado para ingresar tu nombre de jugador.
    *   **Pantallas de Juego Claras:** Información esencial (Nivel, Puntos, Racha, PRIME) siempre visible.
    *   **Pantalla "Game Over":** Muestra tus estadísticas de ronda y te da opciones claras para continuar o salir.
*   **Accesibilidad Integral:** Diseñado pensando en todos. Movilidad, visión y capacidades cognitivas consideradas para una experiencia inclusiva. (Ver sección dedicada a accesibilidad).

---

## 🏆 Adaptación y Accesibilidad

Hemos puesto especial cuidado en hacer este juego accesible para una amplia gama de usuarios, incluyendo aquellos con diversas necesidades:

### 🤝 **Movilidad y Coordinación Motora**

*   **Interacción Natural:** El control principal es el movimiento de la mano, que no requiere la motricidad fina del ratón o el teclado.
*   **Área de Captura Amplia:** Las figuras y el punto de interacción del dedo índice son generosos, minimizando la frustración por la falta de precisión extrema.
*   **Dificultad Progresiva y Adaptativa:** Los niveles aumentan gradualmente, permitiendo a cada jugador adaptarse a su propio ritmo.

### 💡 **Dificultades Visuales**

*   **Alto Contraste:** Uso de colores vivos y contrastantes para figuras, puntos de interacción y texto, asegurando una excelente visibilidad.
*   **Indicadores Claros:** El dedo detectado se resalta con un círculo brillante. Las figuras tienen formas distintivas.
*   **Ventana Redimensionable:** Adapta el tamaño de la ventana de juego a tu preferencia.

### 🧠 **Dificultades Cognitivas o de Atención**

*   **Jugabilidad Sencilla:** El objetivo es claro y fácil de aprender: atrapar figuras.
*   **Retroalimentación Inmediata:** Capturar una figura recompensa al instante con puntos y aumento de racha.
*   **Estados Definidos:** El juego se mueve a través de estados bien delimitados (Menú, Jugando, Game Over, Entrada de Nombre) para mantener la claridad.

---

## 🛠️ Tecnologías Utilizadas

*   **Python:** El lenguaje de programación central.
*   **OpenCV (`cv2`):** Para el núcleo de la visión artificial, captura de video y dibujo en pantalla.
*   **MediaPipe:** La herramienta estrella para la detección de manos precisa y en tiempo real.
*   **NumPy:** Para el manejo eficiente de datos de imagen y cálculos.
*   **Random:** Para añadir aleatoriedad y sorpresas.
*   **Time:** Para sincronización de elementos visuales como el cursor.
*   **OS:** Para la gestión de archivos y rutas.
*   **SQLite3:** La base de datos ligera y robusta para guardar el progreso de los jugadores.

---

## 🚀 Cómo Empezar

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/Suarezsh/Opencv-Game
    cd Opencv-Game
    ```
2.  **Instalar Dependencias:**
    Asegúrate de tener Python instalado. Luego, en la terminal, dentro del directorio del proyecto:
    ```bash
    pip install opencv-python mediapipe numpy
    ```
3.  **Ejecutar el Juego:**
    Inicia la aplicación con:
    ```bash
    python app.py
    ```
    *(Si el archivo principal es `app.py`)*

---

## 🎮 Cómo Jugar

1.  **Bienvenida e Ingreso de Nombre:** Al iniciar, se te pedirá tu nombre en la consola.
2.  **Menú Principal:**
    *   Usa el **ratón** para moverte entre las opciones: **"Iniciar Juego"**, **"Reiniciar Progreso"**, **"Salir"**.
    *   Haz clic con el ratón o presiona **ENTER** para seleccionar.
3.  **Jugando:**
    *   Observa las figuras caer en la ventana de OpenCV.
    *   **Mueve tu mano** frente a la cámara. El dedo índice (marcado con un círculo verde) es tu objetivo.
    *   **Atrapa las figuras** moviendo tu dedo índice sobre ellas.
    *   Verás en pantalla:
        *   **Nivel:** Progresa con tu **Racha**.
        *   **Racha:** La cantidad total de figuras atrapadas.
        *   **Puntos:** Tu puntuación en la ronda actual.
        *   **PRIME:** Tu mejor puntuación individual histórica.
4.  **Pantalla "Game Over":**
    *   Cuando pierdes, verás tus estadísticas.
    *   Selecciona con el **ratón** o **ENTER**:
        *   **Jugar de Nuevo:** Para empezar otra partida.
        *   **HOME:** Para volver al menú principal.
        *   **Salir:** Para cerrar el juego.
5.  **Salir del Juego:**
    *   Presiona la tecla **ESC** en cualquier momento para volver al menú (si estás jugando) o para salir del juego (si estás en menú o "Game Over").
    *   Cerrar la ventana de OpenCV también finalizará el juego.

---

## 💡 Contribuciones y Mejoras Futuras

¡Tu creatividad es el límite! Aquí hay algunas ideas para llevar este juego al siguiente nivel:

*   **Personalización de Figuras:** ¡Agrega tus propias imágenes en la carpeta `img` para darle un toque único!
*   **Más Gestos:** Implementa la detección de otros gestos para acciones especiales.
*   **Modos de Dificultad:** Permite a los jugadores elegir entre "Fácil", "Normal", "Difícil".
*   **Efectos de Sonido:** ¡Dale vida al juego con sonidos para capturas, niveles y game over!
*   **Interfaz Gráfica Completa:** Integra el menú principal y la entrada de nombre usando bibliotecas como Tkinter o PyQt para una experiencia más pulida.
*   **Optimización de Detección:** Experimenta con los parámetros de MediaPipe para mejorar el rendimiento.
*   **Power-ups:** Introduce elementos especiales que den bonificaciones temporales (ej. ralentizar figuras, imán).

---




<img width="1601" height="896" alt="image" src="https://github.com/user-attachments/assets/71bb2653-0059-418a-b82b-22e182da2538" />
<img width="1047" height="897" alt="image" src="https://github.com/user-attachments/assets/d74077e5-7319-401d-acbe-70eaf3585386" />


