# Flood Among Us — Itch.io Prototype (UNSC Immersive HTML)

Versión: prototipo HTML con estética UNSC/Halo — listo para subir a itch.io.

## Contenido
- `index.html` — interfaz principal con intro y juego.
- `style.css` — estilos (fuente Orbitron desde Google Fonts).
- `script.js` — lógica del juego, generación de casos, audio handlers.
- `/assets/sounds/` — sonidos de ejemplo (puedes reemplazarlos por efectos libres de mejor calidad).

## Cómo probar localmente
1. Descarga o copia la carpeta `flood_among_us_itch/` en tu máquina.
2. Abre `index.html` en un navegador moderno (Chrome/Edge/Firefox). Si el audio no se reproduce automáticamente, pulsa el botón *Activar audio*.
3. Presiona cualquier tecla para salir del boot-screen y acceder al menú.

## Cómo subir a itch.io
1. Empaqueta la carpeta `flood_among_us_itch/` en un archivo `.zip` (asegúrate de mantener la estructura de archivos).
2. En itch.io, crea un nuevo proyecto y selecciona tipo *HTML* si deseas que se ejecute en navegador. Sube el archivo `.zip` y configura la resolución si quieres.
3. Verifica que los archivos de audio estén incluidos en la subida (itch.io permite reproducir audio desde la carpeta assets).

## Notas de licencia de assets
Los archivos de audio incluidos son bucles y tonos generados como placeholders. Te recomiendo reemplazarlos por efectos libres (por ejemplo en freesound.org con licencia Creative Commons 0/BY) si vas a publicar el juego públicamente.

## Posibles mejoras
- Añadir animaciones SVG más complejas para el logo emblema militar.
- Implementar salvado de partidas y desbloqueo de finales.
- Añadir efectos visuales y sprites para personajes/armas.
- Portar a React/Tailwind para interfaz más rica (puedo hacerlo cuando quieras).

---
Desarrollado como prototipo por tu asistente.