import pygame
from pygame import Vector2
import math

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
LINE_LENGTH = 2
LINE_THICKNESS = 1

ORIGIN_X, ORIGIN_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
TARGET_ANGLE = math.pi / 2


def rotate_point(point, pivot, theta):
    s, c = math.sin(theta), math.cos(theta)
    x, y = point - pivot
    return Vector2(
        pivot.x + c * x - s * y,
        pivot.y + s * x + c * y
    )

def world_to_screen(point, camera_pos, zoom):
    return (point - camera_pos) * zoom + Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Dragon Curve Fractal')
    clock = pygame.time.Clock()

    running = True
    animating = False
    angle_progress = 0.0

    origin = Vector2(ORIGIN_X, ORIGIN_Y)
    vector = Vector2(ORIGIN_X + LINE_LENGTH, ORIGIN_Y)

    all_vectors = [origin, vector]
    reversed_copy = []
    pivot = vector

    zoom = 1.0
    camera_pos = Vector2(ORIGIN_X, ORIGIN_Y)  # world center
    dragging = False
    drag_start = Vector2(0, 0)
    camera_start = Vector2(0, 0)

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not animating:
                    pivot = all_vectors[-1]
                    reversed_copy = list(reversed(all_vectors[:-1]))
                    animating = True
                    angle_progress = 0.0
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom *= 1.1  # zoom in
                elif event.y < 0:
                    zoom /= 1.1  # zoom out
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                dragging = True
                drag_start = Vector2(pygame.mouse.get_pos())
                camera_start = camera_pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_now = Vector2(pygame.mouse.get_pos())
                delta = (drag_start - mouse_now) / zoom
                camera_pos = camera_start + delta

        screen.fill((0, 0, 0))

        if animating:
            angle_progress += 5 * dt
            if angle_progress >= TARGET_ANGLE:
                angle_progress = TARGET_ANGLE
                animating = False
                new_vectors = all_vectors[:]
                for v in reversed_copy:
                    new_vectors.append(rotate_point(v, pivot, TARGET_ANGLE))
                all_vectors = new_vectors
            else:
                rotated_part = [rotate_point(v, pivot, angle_progress) for v in reversed_copy]
                pygame.draw.lines(screen, (255, 100, 100), False,
                                  [world_to_screen(p, camera_pos, zoom) for p in [pivot] + rotated_part], 2)

        screen_vectors = [world_to_screen(p, camera_pos, zoom) for p in all_vectors]
        pygame.draw.lines(screen, (255, 255, 255), False, screen_vectors, 2)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()