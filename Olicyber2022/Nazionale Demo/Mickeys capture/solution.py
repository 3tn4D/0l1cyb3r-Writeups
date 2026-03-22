import pyshark
import json
import pygame
import sys

# flag{posso_catturar3_anche_pacchett1_U5b!}

# PS: la parte di pygame l'ha fatta Claude :)

# --- Estrai i delta dalla cattura ---
cap = pyshark.FileCapture("./capture.pcapng")
deltas = []

for packet in cap:
    if "DATA" in str(packet.layers):
        data = str(packet.data._all_fields)
        if "usbhid.data" in data:
            data = json.loads(data.replace("'", '"'))["usbhid.data"]
            bytes_ = data.split(":")
            dx = int(bytes_[1], 16)
            dy = int(bytes_[2], 16)
            if dx > 127: dx -= 256
            if dy > 127: dy -= 256
            deltas.append((dx, dy))

cap.close()

# --- Costruisci tutti i punti assoluti ---
points = []
x, y = 0, 0
for dx, dy in deltas:
    x += dx
    y += dy
    points.append((x, y))

# --- Pygame ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse replay")
clock = pygame.time.Clock()

# Calcola bounds del percorso per centrare
if points:
    min_x = min(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)
    path_w = max_x - min_x
    path_h = max_y - min_y
else:
    min_x = min_y = 0
    path_w = path_h = 0

PADDING = 100
CANVAS_W = max(path_w + PADDING * 2, WIDTH)
CANVAS_H = max(path_h + PADDING * 2, HEIGHT)

# Offset per centrare il percorso sul canvas
offset_x = -min_x + PADDING
offset_y = -min_y + PADDING

# Canvas grande su cui disegnare tutto
canvas = pygame.Surface((CANVAS_W, CANVAS_H))
canvas.fill((0, 0, 0))

# Stato
i = 0
animating = True
done = False

# Camera (angolo in alto a sinistra del canvas visibile)
cam_x, cam_y = 0, 0
SCROLL_SPEED = 20
dragging = False
drag_start = (0, 0)
cam_start = (0, 0)

cx, cy = offset_x, offset_y  # posizione corrente sul canvas

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                # Restart animazione
                canvas.fill((0, 0, 0))
                i = 0
                animating = True
                done = False
                cx, cy = offset_x, offset_y

        # Scroll con rotella
        if event.type == pygame.MOUSEWHEEL:
            cam_y -= event.y * SCROLL_SPEED
            cam_x -= event.x * SCROLL_SPEED

        # Drag con tasto sinistro (solo quando finita animazione)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and done:
            dragging = True
            drag_start = pygame.mouse.get_pos()
            cam_start = (cam_x, cam_y)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
        if event.type == pygame.MOUSEMOTION and dragging:
            mx, my = pygame.mouse.get_pos()
            cam_x = cam_start[0] - (mx - drag_start[0])
            cam_y = cam_start[1] - (my - drag_start[1])

    # Clampa camera ai bordi del canvas
    cam_x = max(0, min(cam_x, CANVAS_W - WIDTH))
    cam_y = max(0, min(cam_y, CANVAS_H - HEIGHT))

    # Animazione
    if animating and i < len(points):
        px, py = points[i]
        nx, ny = px + offset_x, py + offset_y
        pygame.draw.line(canvas, (0, 255, 0), (int(cx), int(cy)), (int(nx), int(ny)), 2)
        cx, cy = nx, ny

        # Segui il cursore con la camera durante l'animazione
        cam_x = max(0, min(cx - WIDTH // 2, CANVAS_W - WIDTH))
        cam_y = max(0, min(cy - HEIGHT // 2, CANVAS_H - HEIGHT))

        i += 1
        if i >= len(points):
            animating = False
            done = True

    # Disegna punto corrente
    if not done:
        pygame.draw.circle(canvas, (255, 255, 255), (int(cx), int(cy)), 4)

    # Renderizza porzione visibile del canvas
    screen.blit(canvas, (0, 0), (cam_x, cam_y, WIDTH, HEIGHT))

    # UI
    font = pygame.font.SysFont(None, 24)
    if done:
        msg = "Fine — Scorri con rotella/drag | R = ricomincia | ESC = esci"
    else:
        msg = f"Replay... {i}/{len(points)}"
    label = font.render(msg, True, (180, 180, 180))
    screen.blit(label, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()