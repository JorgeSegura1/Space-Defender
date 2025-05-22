# Space Defender

**Space Defender** es un clon sencillo de “shoot ’em up” hecho con Python y Pygame.

## 📋 Requisitos
- Python 3.7+
- [Pygame](https://www.pygame.org/):  
  ```bash
  pip install pygame

🚀 Cómo jugar
Ejecuta python main.py.

En el menú, selecciona Jugar (con teclado o clic del ratón).

Mueve tu nave con ← →, dispara con Espacio.

Presiona P para pausar.

Gana 10 puntos por cada enemigo destruido.

Al llegar a 50 puntos subirás al nivel 2, a 100 puntos al 3, etc.

📂 Estructura de funciones
init_pygame(): inicializa la pantalla.

show_main_menu(): menú principal con teclado y ratón.

play_game(): bucle principal de juego, gestiona niveles, disparos y colisiones.

show_pause_menu(): pausa el juego hasta presionar P.

spawn_enemies(): crea n enemigos con velocidad creciente.

Clase Enemy: objeto sprite que baja desde arriba.