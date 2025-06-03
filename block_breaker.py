import pygame
import sys
import json
import random

# ============ Konfigurasi Awal ============
pygame.init()
WIDTH, HEIGHT = 900, 600  # ukuran layar diubah agar lebih lega
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker Edukasi")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 100)
FPS = 60
clock = pygame.time.Clock()

# ============ Kelas Paddle ============
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, self.width, self.height)
        self.speed = 7

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# ============ Kelas Ball ============
class Ball:
    def __init__(self):
        self.radius = 10
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, self.radius * 2, self.radius * 2)
        self.speed_x = 5
        self.speed_y = -5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.circle(screen, RED, self.rect.center, self.radius)

# ============ Kelas Block ============
class Block:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 60, 20)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# ============ Fungsi: Tampilkan Input Box ============
def input_box(prompt):
    font = pygame.font.SysFont(None, 28)
    input_text = ''
    while True:
        screen.fill(BLACK)
        box_rect = pygame.Rect(100, 150, 600, 200)
        pygame.draw.rect(screen, (30, 30, 30), box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)

        prompt_surface = font.render(prompt, True, WHITE)
        screen.blit(prompt_surface, (box_rect.x + 10, box_rect.y + 10))

        input_surface = font.render(input_text, True, GREEN)
        screen.blit(input_surface, (box_rect.x + 10, box_rect.y + 60))

        info = font.render("Ketik jawaban dan tekan [ENTER]", True, (200, 200, 200))
        screen.blit(info, (box_rect.x + 10, box_rect.y + box_rect.height - 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

# ============ Fungsi: Tampilkan Penjelasan ============
def show_multiline_box(message):
    font = pygame.font.SysFont(None, 28)
    words = message.split()
    lines = []
    line = ''

    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < 580:
            line = test_line
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)

    while True:
        screen.fill(BLACK)
        box_rect = pygame.Rect(100, 150, 600, 200)
        pygame.draw.rect(screen, (40, 40, 40), box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)

        for i, l in enumerate(lines):
            text_surface = font.render(l.strip(), True, WHITE)
            screen.blit(text_surface, (box_rect.x + 10, box_rect.y + 10 + i * 30))

        info = font.render("Tekan [ENTER] untuk melanjutkan...", True, (180, 180, 180))
        screen.blit(info, (box_rect.x + 10, box_rect.y + box_rect.height - 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# ============ Fungsi: Load Soal dari JSON ============
def load_questions():
    with open('blockgame/questions.json', 'r') as f:
        return json.load(f)

# ============ Fungsi: Tampilkan Satu Soal ============
def ask_question(questions, category="general"):
    pool = [q for q in questions if q['category'] == category]
    if not pool:
        return True
    q = random.choice(pool)
    answer = input_box(q['question'])
    if answer.strip().lower() == str(q['answer']).strip().lower():
        return True
    else:
        explanation = q.get('explanation', 'Tidak ada penjelasan.')
        show_multiline_box(f"Jawaban salah!\n{explanation}")
        return False

# ============ Fungsi: Layar Game Over dengan Pilihan Restart/Quit ============
def game_over_screen(score):
    font_title = pygame.font.SysFont(None, 50, bold=True)
    font_option = pygame.font.SysFont(None, 36)
    font_option_sel = pygame.font.SysFont(None, 40, bold=True)

    options = ["Restart", "Quit"]
    selected = 0  # indeks pilihan

    while True:
        screen.fill(BLACK)

        title_surf = font_title.render("Permainan Selesai!", True, (255, 100, 100))
        score_surf = font_option.render(f"Skor Akhir: {score}", True, WHITE)

        screen.blit(title_surf, ((WIDTH - title_surf.get_width()) // 2, HEIGHT // 4))
        screen.blit(score_surf, ((WIDTH - score_surf.get_width()) // 2, HEIGHT // 4 + 60))

        for i, option in enumerate(options):
            if i == selected:
                option_surf = font_option_sel.render(option, True, (255, 215, 0))
            else:
                option_surf = font_option.render(option, True, WHITE)
            x = (WIDTH - option_surf.get_width()) // 2
            y = HEIGHT // 2 + i * 50
            screen.blit(option_surf, (x, y))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected == 0

# ============ Fungsi Utama Game ============
def main():
    paddle = Paddle()
    ball = Ball()
    questions = load_questions()
    score = 0
    lives = 3  # jumlah nyawa

    blocks = []
    colors = [GREEN, RED, BLUE, YELLOW]

    for row in range(4):
        for col in range(10):
            color = random.choice(colors)
            x = 60 + col * 65
            y = 50 + row * 30
            blocks.append(Block(x, y, color))

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        ball.move()

        # Pantul bola ke paddle
        if ball.rect.colliderect(paddle.rect):
            ball.speed_y *= -1

        # Pantul bola ke blok dan hapus blok tanpa soal
        hit_block = None
        for block in blocks:
            if ball.rect.colliderect(block.rect):
                hit_block = block
                break

        if hit_block:
            ball.speed_y *= -1
            blocks.remove(hit_block)
            score += 10

        # Saat bola jatuh ke bawah
        if ball.rect.top > HEIGHT:
            # Tampilkan soal kategori "general"
            if ask_question(questions, 'general'):
                # Jawab benar: reset bola di tengah & lanjut main
                ball.rect.center = (WIDTH // 2, HEIGHT // 2)
                ball.speed_y = -5
            else:
                lives -= 1
                if lives <= 0:
                    running = False
                else:
                    # Reset posisi bola dan lanjut main
                    ball.rect.center = (WIDTH // 2, HEIGHT // 2)
                    ball.speed_y = -5

        # Gambar objek
        paddle.draw()
        ball.draw()
        for block in blocks:
            block.draw()

        # Tampilkan skor di kiri atas
        font = pygame.font.SysFont(None, 28)
        score_text = font.render(f"Skor: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Tampilkan label "Nyawa:" dan lingkaran nyawa di kanan atas
        lives_text = font.render("Nyawa:", True, WHITE)
        lives_text_pos = (WIDTH - 145, 10)
        screen.blit(lives_text, lives_text_pos)
        for i in range(lives):
            x = WIDTH - 60 + i * 22
            y = 20
            pygame.draw.circle(screen, RED, (x, y), ball.radius)
            pygame.draw.circle(screen, WHITE, (x, y), ball.radius, 2)  # border putih

        pygame.display.flip()

    # Game over, tampilkan layar akhir
    if game_over_screen(score):
        main()
    else:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
