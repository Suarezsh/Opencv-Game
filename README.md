# Atrapa las Figuras Divertidas: Un Juego Interactivo con OpenCV

## Descripción General

"Atrapa las Figuras Divertidas" es un juego desarrollado en Python utilizando la biblioteca OpenCV para la detección de movimiento a través de la cámara web. El objetivo principal del jugador es atrapar figuras que caen en la pantalla utilizando el movimiento de su mano (específicamente, el dedo índice). El juego incorpora un sistema de niveles progresivos, puntuación, registro de jugadores con persistencia de datos mediante SQLite, y adaptaciones para la accesibilidad.

Este proyecto se inspira en la jugabilidad clásica de "atrapa-objetos" pero con una interfaz moderna y tecnología de visión artificial, ofreciendo una experiencia interactiva y divertida.

## Características Principales

*   **Control por Gestos:** Utiliza la detección de manos de MediaPipe y OpenCV para seguir el movimiento del dedo índice del jugador, permitiendo interactuar con el juego sin necesidad de periféricos.
*   **Jugabilidad Intuitiva:** El objetivo es atrapar figuras que caen, moviendo la mano para dirigirlas.
*   **Sistema de Niveles Progresivo:** A medida que el jugador atrapa figuras, la dificultad aumenta (velocidad de las figuras, tasa de aparición). El nivel se basa en la "Racha Total" de figuras atrapadas a lo largo del tiempo.
*   **Gestión de Jugadores y Progreso:**
    *   **Registro de Jugador:** Al iniciar, se solicita el nombre del jugador.
    *   **Base de Datos SQLite:** Guarda el progreso de cada jugador, incluyendo:
        *   **Nombre del Jugador.**
        *   **Nivel Máximo Alcanzado.**
        *   **PRIME (Mejor Puntuación Individual):** La puntuación más alta lograda en una sola partida.
        *   **Racha Total:** La suma acumulada de todas las figuras atrapadas por el jugador.
    *   **Persistencia de Datos:** El progreso se guarda automáticamente y se carga al iniciar el juego.
    *   **Opción de Reiniciar Progreso:** Permite borrar todos los datos de todos los jugadores y empezar de cero.
*   **Interfaz de Usuario:**
    *   **Menú Principal:** Con opciones para "Iniciar Juego", "Reiniciar Progreso" y "Salir", navegable por ratón o teclado (aunque la versión actual se centra en el ratón).
    *   **Pantalla de Entrada de Nombre:** Interfaz estilo "Plants vs. Zombies" para ingresar el nombre del jugador.
    *   **Pantalla de Juego:** Muestra el Nivel, Puntos (de la ronda actual), Racha (total acumulada) y PRIME (mejor puntuación individual).
    *   **Pantalla "Game Over":** Muestra estadísticas de la partida y opciones para "Jugar de Nuevo", "HOME" (volver al menú) o "Salir".
*   **Adaptabilidad a Dificultades:** Diseñado con la accesibilidad en mente (ver sección específica).
*   **Imágenes de Figuras Personalizables:** Soporta el uso de imágenes PNG de figuras (originalmente Pokémon) que caen, permitiendo una fácil personalización del aspecto visual.

## Adaptación para Personas con Dificultades

Este juego ha sido concebido con la accesibilidad como un pilar fundamental, buscando ofrecer una experiencia inclusiva. Se han considerado las siguientes áreas y posibles adaptaciones para personas con diversas condiciones:

### 1. Dificultades de Movilidad y Coordinación Motora

*   **Control por Cámara:** La principal interacción se basa en el movimiento general de la mano, no en movimientos finos y precisos. Esto es beneficioso para personas que pueden tener dificultades con la motricidad fina, el control de un ratón o un teclado complejo.
*   **Objetivo Amplio:** Las figuras que caen son de un tamaño considerable, y la colisión se detecta en un área relativamente amplia (círculo alrededor de la punta del dedo índice), reduciendo la necesidad de apuntar con alta precisión.
*   **Niveles de Dificultad Progresiva:** El juego aumenta gradualmente la velocidad y la frecuencia de las figuras, permitiendo al jugador adaptarse a su propio ritmo. La racha de figuras atrapadas determina el nivel, dando una sensación de progresión a largo plazo.
*   **Sin Controles de Teclado Obligatorios:** Aunque se implementó la navegación por teclado, la interacción principal es por gestos, y las opciones de menú/game over son manejables con ratón, lo que reduce la dependencia de la destreza manual fina.

### 2. Dificultades Visuales

*   **Contraste de Color:** Se utilizan colores de alto contraste para los elementos importantes:
    *   Figuras que caen (rojas).
    *   Dedo índice detectado (verde).
    *   Conexiones de mano (verde).
    *   Texto del menú y estado del juego (blanco o verde/rojo para selección/mensajes).
*   **Indicadores Visuales Claros:** El punto de interacción del dedo índice se marca con un círculo grande y brillante. Las figuras son formas circulares o imágenes claras.
*   **Tamaño Ajustable de Ventana:** La ventana de OpenCV se puede redimensionar (hasta un límite de 1280x720 por defecto), permitiendo al usuario ajustar el tamaño de visualización según su comodidad.
*   **Escalabilidad de Fuentes:** Aunque no implementado explícitamente como una opción, el uso de `cv2.FONT_HERSHEY_SIMPLEX` y escalas de fuente manejables permite ajustar el tamaño del texto si fuera necesario modificar el código.
*   **Paleta de Colores:** Los colores de los elementos del juego (figuras rojas, dedo verde, texto blanco) son seleccionados para maximizar la visibilidad.

### 3. Dificultades Cognitivas o de Atención

*   **Jugabilidad Simple y Repetitiva:** El objetivo principal es fácil de entender: atrapar figuras. La mecánica no requiere memorización compleja ni multitarea avanzada.
*   **Retroalimentación Inmediata:** Cada figura atrapada otorga puntos y aumenta la racha, proporcionando una recompensa inmediata y clara.
*   **Estados del Juego Definidos:** El juego tiene estados claros (Menú, Jugando, Game Over, Entrada de Nombre) que ayudan al jugador a orientarse.
*   **Tiempo de Reacción Flexible:** Aunque hay un elemento de tiempo, la velocidad de las figuras aumenta gradualmente. El juego no penaliza de forma severa por perder una figura (simplemente no se suman puntos y la racha puede romperse si el juego finaliza por no atrapar suficientes).

### 4. Consideraciones Adicionales para Accesibilidad

*   **Sin Dependencia de Sonido:** El juego no requiere audio para funcionar. Toda la información crítica se presenta visualmente.
*   **Entrada de Nombre Sencilla:** La solicitud de nombre se realiza por consola, evitando la complejidad de interfaces gráficas adicionales para esta función básica.

**Nota:** Para usuarios con dificultades severas en la detección de manos (por ejemplo, debido a movimientos muy limitados), sería necesario considerar métodos de entrada alternativos o ajustes en los parámetros de detección de MediaPipe, lo cual escapa a la complejidad de este script pero es un área de mejora para el futuro.

## Tecnologías Utilizadas

*   **Python:** Lenguaje de programación principal.
*   **OpenCV (`cv2`):** Para captura de video, procesamiento de imágenes, detección de gestos y dibujo en pantalla.
*   **MediaPipe:** Para la detección de manos y puntos de referencia faciales.
*   **NumPy:** Para operaciones numéricas y manipulación de arrays (imágenes).
*   **Random:** Para la generación aleatoria de figuras y sus posiciones.
*   **Time:** Para medir el tiempo (ej. para el cursor parpadeante).
*   **OS:** Para interactuar con el sistema de archivos (cargar imágenes).
*   **SQLite3:** Para la gestión de la base de datos de jugadores y progreso.

## Requisitos del Sistema

*   **Sistema Operativo:** Compatible con Windows, macOS, Linux.
*   **Hardware:** Cámara web funcional.
*   **Software:**
    *   Python 3.7+
    *   OpenCV (instalar con `pip install opencv-python`)
    *   MediaPipe (instalar con `pip install mediapipe`)
    *   NumPy (instalar con `pip install numpy`)

## Instalación

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/Suarezsh/Opencv-Game
    cd Opencv-Game
    ```
2.  **Crear Carpeta de Imágenes:**
    Crea una carpeta llamada `img` en el directorio raíz del proyecto (`Opencv-Game/`).
3.  **Agregar Imágenes:**
    Coloca las imágenes de las figuras (ej. `img1.png`, `img2.png`, ..., `img6.png`) dentro de la carpeta `img/`. Asegúrate de que sean archivos `.png` con fondo transparente.
4.  **Instalar Dependencias:**
    Abre tu terminal en el directorio del proyecto y ejecuta:
    ```bash
    pip install opencv-python mediapipe numpy
    ```
    *(NumPy y OpenCV suelen instalarse automáticamente con Mediapipe, pero es buena práctica asegurarlas).*

## Cómo Jugar

1.  **Ejecutar el Script:**
    Abre tu terminal en el directorio del proyecto y ejecuta:
    ```bash
    python tu_script_game.py 
    ```
    *(Reemplaza `tu_script_game.py` con el nombre real de tu archivo Python).*
2.  **Ingresar Nombre:**
    Se te pedirá que ingreses un nombre de jugador en la consola. Una vez ingresado, se abrirá la ventana del juego.
3.  **Menú Principal:**
    *   Utiliza el ratón o las flechas del teclado para navegar entre "Iniciar Juego", "Reiniciar Progreso" y "Salir".
    *   Presiona `ENTER` para seleccionar una opción.
4.  **Jugando:**
    *   El juego se mostrará en la ventana de OpenCV.
    *   Sigue las figuras que caen y trata de atraparlas moviendo tu mano frente a la cámara. El dedo índice se marcará con un círculo verde.
    *   Los "Puntos" son los de la ronda actual.
    *   La "Racha" es el total de figuras atrapadas acumuladas.
    *   El "Nivel" aumenta según la "Racha".
    *   El "PRIME" muestra tu mejor puntuación individual histórica.
5.  **Game Over:**
    *   Cuando no logras atrapar suficientes figuras, la partida termina.
    *   Verás tus estadísticas de la ronda y tu progreso general.
    *   Puedes seleccionar:
        *   **Jugar de Nuevo:** Para empezar una nueva ronda.
        *   **HOME:** Para regresar al menú principal.
        *   **Salir:** Para cerrar el juego.
6.  **Salir del Juego:**
    *   Puedes presionar la tecla `ESC` en cualquier momento para volver al menú principal (si estás jugando) o para salir del juego (si estás en el menú o en "Game Over").
    *   Cerrar la ventana de OpenCV también saldrá del juego.

## Contribuciones y Mejoras

*   **Personalización de Figuras:** Reemplaza las imágenes en la carpeta `./img` con tus propios PNG para cambiar la apariencia de las figuras.
*   **Nuevos Gestos:** Podría implementarse la detección de otros gestos para controles adicionales.
*   **Modo de Dificultad:** Añadir opciones de dificultad (fácil, medio, difícil) que ajusten la velocidad, la racha necesaria por nivel, etc.
*   **Efectos de Sonido:** Incorporar efectos de sonido para capturas, niveles y game over.
*   **Interfaz Gráfica Completa:** Migrar la interfaz del menú y la entrada de nombre a una biblioteca GUI más robusta (como Tkinter o PyQt) para una mejor experiencia de usuario.
*   **Optimización de Detección:** Ajustar parámetros de MediaPipe para mejorar la precisión o el rendimiento en diferentes cámaras o condiciones de iluminación.
<img width="1601" height="896" alt="image" src="https://github.com/user-attachments/assets/71bb2653-0059-418a-b82b-22e182da2538" />
<img width="1047" height="897" alt="image" src="https://github.com/user-attachments/assets/d74077e5-7319-401d-acbe-70eaf3585386" />


