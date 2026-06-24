# 🎮 Trollus - Proyecto de Vibecoding

El proyecto consiste en el desarrollo de un videojuego de plataformas 2D estilo "Level Devil" utilizando Python y Pygame, con el objetivo de aplicar técnicas de vibecoding y prompt engineering, se utilizó inteligencia artificial (principalmente a través de Cursor y Claude) como asistente de programación para generar código, iterar sobre funcionalidades y corregir errores, el resultado es un juego funcional con dos niveles, trampas interactivas y una mecánica centrada en la "troleada" al jugador.

---

## 📝 EVIDENCIA DE VIBECODING (PROMPTS)

### PROMPT 1

**Qué se pidió:**
> "Quiero crear un juego de plataformas 2D en Python con Pygame. El estilo es como 'Level Devil': un juego troll, donde la dificultad no está en la habilidad, sino en los trucos y trampas del nivel. Necesito un esqueleto básico con un jugador que pueda moverse a la izquierda y derecha, saltar, y una plataforma simple. Tiene que tener una ventana de juego y un loop principal."

**Ajuste realizado:**
Se necesitaba una base funcional para empezar a construir el juego, con físicas básicas como la gravedad, colisiones y controles responsivos. La IA generó el código base con la clase `Jugador` y el bucle principal, lo que me permitió tener un prototipo jugable.

---

### PROMPT 2

**Qué se pidió:**
> "El juego base funciona. Ahora quiero añadir mi primera trampa al estilo Level Devil. Quiero que en el nivel 1, cuando el jugador llegue a la puerta de salida, el suelo se desvanezca y el jugador caiga a un pozo. El jugador debe reaparecer al inicio del nivel cuando muere."

**Ajuste realizado:**
La primera versión de la trampa no se activaba correctamente ya que la detección de colisión era imprecisa. Se ajustó la lógica para que la trampa se active cuando el jugador está sobre ella y se agregó una animación de derrumbe con partículas para mejorar la experiencia visual.

---

### PROMPT 3

**Qué se pidió:**
> "Hagamos el nivel 2 pero diferente. Quiero que el personaje empiece con un hoyo en el mapa y que el hoyo se mueva hacia él cuando avance, como una troleada."

**Ajuste realizado:**
El hoyo inicialmente era demasiado simple y no generaba la "troleada" deseada. Se refinó el concepto para tener dos hoyos: uno falso (visible, que se mueve rápido) y uno verdadero (camuflado con el suelo).

---

## 🔄 ITERACIÓN Y MEJORA

En esta etapa pedí que me hiciera una animación ya que en el prototipo no se tenía eso, entonces creé un prompt para que me hiciera una animación tipo derrumbe con partículas.

**Prompt de mejora:**
> "Quiero que el derrumbe del suelo tenga una animación visual: que el suelo se agriete, se oscurezca y se hunda lentamente. También quiero partículas de tierra cayendo para que se vea más realista."

**Impacto:**
La animación transformó una trampa simple en un evento visualmente impactante, ya que el jugador ahora ve cómo el suelo se agrieta y se desmorona antes de caer, lo que aumenta esa sensación de troleada característica del juego.

---

## 🧪 VALIDACIÓN DEL RESULTADO

### a. ¿Cómo se probó el código?

El juego se probó manualmente ejecutando múltiples partidas en ambos niveles. Se verificó:

- ✅ Los movimientos y salto del jugador responden correctamente.
- ✅ La trampa del Nivel 1 se activa y el jugador reinicia al caer.
- ✅ El hoyo falso del Nivel 2 se mueve rápido y el hoyo verdadero está camuflado.
- ✅ La puerta cambia de nivel y muestra el mensaje de "FELICIDADES" al completar el Nivel 2.
- ✅ El reinicio con la tecla `R` funciona correctamente.

### b. Error identificado y solución

**Error:** El jugador no se caía en el hoyo del Nivel 2. Inicialmente, el jugador podía caminar sobre el hoyo sin caer porque el suelo no se eliminaba correctamente.

**Solución:** Se dividió el suelo en dos partes (izquierda y derecha) y se recortaron dinámicamente según la posición del hoyo. Esto eliminó el suelo donde estaba el hoyo, forzando al jugador a caer al pisarlo.

---

## 📚 REFLEXIÓN FINAL

### a. ¿Qué aprendí usando IA para programar?

Aprendí a estructurar mejor mis peticiones y a iterar sobre el código generado en lugar de esperar una solución perfecta desde el principio. La IA es una excelente herramienta para generar prototipos rápidos, pero el verdadero valor está en saber refinar y ajustar el código para que cumpla con los requisitos específicos del proyecto.

### b. Ventajas y límites del vibecoding

**Ventajas:**
- Desarrollar una idea de juego funcional en pocas horas.
- Explorar diferentes mecánicas sin invertir mucho tiempo.

**Límites:**
- A veces el código generado necesita muchos ajustes.
- En algunos casos, no comprendo completamente el código generado.

### c. Partes del código que comprendo y necesito reforzar

**Comprendo bien:**
- La estructura de los niveles y la transición entre ellos.
- La detección de colisiones básicas.
- La lógica del jugador (movimiento, salto, gravedad).

**Necesito reforzar:**
- La implementación de sistemas más complejos como partículas o efectos visuales avanzados.
- La optimización de gráficos con Pygame.

---

## 🎮 Controles del juego

| Tecla | Acción |
|-------|--------|
| `A` / `←` | Mover a la izquierda |
| `D` / `→` | Mover a la derecha |
| `Espacio` / `↑` / `W` | Saltar |
| `R` | Reiniciar nivel |
| `1` | Ir al Nivel 1 |
| `2` | Ir al Nivel 2 |
| `Esc` | Salir del juego |

---

## 📦 Cómo ejecutar el juego

```bash
# 1. Clonar el repositorio
git clone https://github.com/Stevecup123/trollus-game.git

# 2. Entrar a la carpeta
cd trollus-game

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el juego
python main.py
