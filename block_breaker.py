import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker Edukasi Typing")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 100)
FPS = 60
clock = pygame.time.Clock()

class Paddle:
    def __init__(self):
        self.width = 125
        self.height = 15
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - 40, self.width, self.height)
        self.speed = 9

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.radius = 10
        self.reset_position()
        self.speed_x = 5
        self.speed_y = -5

    def reset_position(self, paddle=None):
        if paddle:
            self.rect = pygame.Rect(paddle.rect.centerx - self.radius, paddle.rect.top - self.radius * 2,
                                    self.radius * 2, self.radius * 2)
        else:
            self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, self.radius * 2, self.radius * 2)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.circle(screen, RED, self.rect.center, self.radius)

class Block:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 60, 20)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

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
        box_rect = pygame.Rect(100, 150, 700, 200)
        pygame.draw.rect(screen, (40, 40, 40), box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)

        total_text_height = len(lines) * 30
        start_y = box_rect.y + (box_rect.height - total_text_height) // 2

        for i, l in enumerate(lines):
            text_surface = font.render(l.strip(), True, WHITE)
            text_width = text_surface.get_width()
            text_x = box_rect.x + (box_rect.width - text_width) // 2
            text_y = start_y + i * 30
            screen.blit(text_surface, (text_x, text_y))

        info = font.render("Tekan [ENTER] untuk melanjutkan...", True, (180, 180, 180))
        info_x = box_rect.x + (box_rect.width - info.get_width()) // 2
        screen.blit(info, (info_x, box_rect.y + box_rect.height - 30))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def show_colored_level_message(level):
    font = pygame.font.SysFont(None, 28)
    message_start = "Selamat! Kamu naik ke Level "
    level_text = str(level)
    message_end = "!"

    while True:
        screen.fill(BLACK)
        box_rect = pygame.Rect(100, 150, 700, 200)
        pygame.draw.rect(screen, (40, 40, 40), box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)

        start_surface = font.render(message_start, True, WHITE)
        level_surface = font.render(level_text, True, YELLOW)
        end_surface = font.render(message_end, True, WHITE)

        total_width = start_surface.get_width() + level_surface.get_width() + end_surface.get_width()
        start_x = box_rect.x + (box_rect.width - total_width) // 2
        y = box_rect.y + (box_rect.height - 30) // 2

        screen.blit(start_surface, (start_x, y))
        screen.blit(level_surface, (start_x + start_surface.get_width(), y))
        screen.blit(end_surface, (start_x + start_surface.get_width() + level_surface.get_width(), y))

        info = font.render("Tekan [ENTER] untuk melanjutkan...", True, (180, 180, 180))
        screen.blit(info, (box_rect.x + (box_rect.width - info.get_width()) // 2, box_rect.y + box_rect.height - 30))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def typing_challenge(word, time_limit=35):
    font = pygame.font.SysFont(None, 32)
    input_text = ''
    start_time = pygame.time.get_ticks()
    current_time_limit = time_limit

    max_width = 700
    start_x = 100
    start_y = 160
    line_spacing = 30

    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for w in words:
            test_line = current_line + (w + " ")
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = w + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    prompt_lines = wrap_text(word, font, max_width)

    while True:
        screen.fill(BLACK)
        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed > current_time_limit:
            return False, False

        # Render dan tampilkan prompt (soal) per baris
        for i, line in enumerate(prompt_lines):
            rendered_line = font.render(line, True, WHITE)
            screen.blit(rendered_line, (start_x, start_y + i * line_spacing))

        # Bungkus jawaban yang diketik agar tidak terpotong lebar
        input_lines = wrap_text(input_text, font, max_width)
        # Tampilkan semua baris jawaban di bawah prompt
        answer_start_y = start_y + len(prompt_lines) * line_spacing + 10
        for i, line in enumerate(input_lines):
            rendered_line = font.render(line, True, GREEN)
            screen.blit(rendered_line, (start_x, answer_start_y + i * line_spacing))

        # Tampilkan timer di bawah jawaban yang diketik
        timer_y = answer_start_y + len(input_lines) * line_spacing + 10
        timer = font.render(f"Sisa Waktu: {int(current_time_limit - elapsed)} detik", True, YELLOW)
        screen.blit(timer, (start_x, timer_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text.strip().lower() == word.lower(), True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    char = event.unicode
                    expected_char = word[len(input_text):len(input_text)+1]
                    if char.lower() == expected_char.lower():
                        input_text += char
                    else:
                        current_time_limit -= 0



def game_over_screen(score, level):
    font_title = pygame.font.SysFont(None, 50, bold=True)
    font_option = pygame.font.SysFont(None, 36)
    font_option_sel = pygame.font.SysFont(None, 40, bold=True)
    options = ["Restart", "Quit"]
    selected = 0

    while True:
        screen.fill(BLACK)
        title_surf = font_title.render("Permainan Selesai!", True, (255, 100, 100))
        score_surf = font_option.render(f"Skor Akhir: {score}", True, WHITE)
        level_surf = font_option.render(f"Level: {level}", True, WHITE)
        screen.blit(title_surf, ((WIDTH - title_surf.get_width()) // 2, HEIGHT // 4))
        screen.blit(score_surf, ((WIDTH - score_surf.get_width()) // 2, HEIGHT // 4 + 60))
        screen.blit(level_surf, ((WIDTH - level_surf.get_width()) // 2, HEIGHT // 4 + 100))

        for i, option in enumerate(options):
            surf = font_option_sel.render(option, True, (255, 215, 0)) if i == selected else font_option.render(option, True, WHITE)
            x = (WIDTH - surf.get_width()) // 2
            y = HEIGHT // 2 + i * 50
            screen.blit(surf, (x, y))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected == 0

def main():
    paddle = Paddle()
    ball = Ball()
    ball.reset_position(paddle)
    score, lives, level = 0, 3, 1
    typing_words = [
    "Lumba-lumba adalah salah satu hewan paling cerdas di laut dan mampu berkomunikasi dengan berbagai suara unik",
    "Pohon baobab dapat menyimpan hingga 120.000 liter air di batangnya untuk bertahan saat musim kemarau panjang",
    "Bulan adalah satu-satunya satelit alami bumi yang memengaruhi pasang surut air laut di seluruh dunia",
    "Tubuh manusia memiliki sekitar 37 triliun sel yang bekerja sama menjaga fungsi organ dan kesehatan secara keseluruhan",
    "Lebah madu bisa mengenali wajah manusia dan memiliki sistem komunikasi yang sangat kompleks melalui tarian",
    "Paus biru adalah makhluk terbesar di bumi yang pernah hidup, dengan panjang mencapai 30 meter dan berat hingga 200 ton",
    "Kupu-kupu merasakan rasa dengan kakinya, yang memungkinkan mereka menentukan apakah daun cocok untuk bertelur",
    "Gunung Everest terus tumbuh sekitar 4 milimeter setiap tahun akibat pergerakan lempeng tektonik di bawahnya",
    "Sistem saraf manusia dapat mengirimkan sinyal ke seluruh tubuh dengan kecepatan hingga 120 meter per detik",
    "Bulan memiliki lapisan debu halus yang disebut regolith, yang terbentuk dari benturan meteorit selama jutaan tahun"
]

    def generate_blocks(level):
        blocks = []
        colors = [GREEN, RED, BLUE, YELLOW]
        for row in range(0 + level):
            for col in range(0):
                x = 60 + col * 65
                y = 50 + row * 30
                blocks.append(Block(x, y, random.choice(colors)))
        return blocks

    blocks = generate_blocks(level)
    game_started = False
    paused = False
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not game_started and event.key == pygame.K_SPACE:
                    game_started = True
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: paddle.move("left")
        if keys[pygame.K_RIGHT]: paddle.move("right")

        if not game_started:
            ball.reset_position(paddle)
            font = pygame.font.SysFont(None, 30)
            msg = font.render("Tekan [SPACE] untuk memulai permainan", True, WHITE)
            screen.blit(msg, ((WIDTH - msg.get_width()) // 2, HEIGHT // 2))
        elif paused:
            font = pygame.font.SysFont(None, 30)
            pause_text = font.render("PAUSED", True, WHITE)
            instruction_text = font.render("Tekan [ESC] untuk lanjut", True, WHITE)
            center_x = (WIDTH - pause_text.get_width()) // 2
            center_y = HEIGHT // 2
            screen.blit(pause_text, (center_x, center_y - 25))
            screen.blit(instruction_text, ((WIDTH - instruction_text.get_width()) // 2, center_y + 15))
        else:
            ball.move()
            if ball.rect.colliderect(paddle.rect):
                if ball.speed_y > 0:
                    ball.rect.bottom = paddle.rect.top
                    ball.speed_y *= -1

            hit_block = None
            for block in blocks:
                if ball.rect.colliderect(block.rect):
                    hit_block = block
                    break

            if hit_block:
                blocks.remove(hit_block)
                score += 10
                ball.speed_y *= -1

            if ball.rect.top > HEIGHT:
                lives -= 1
                game_started = False
                if lives <= 0:
                    running = False
                else:
                    ball.reset_position(paddle)
                    ball.speed_y = -5

            if not blocks:
                level += 1
                show_colored_level_message(level)
                word = random.choice(typing_words)
                correct, submitted = typing_challenge(word)
                if correct:
                    show_multiline_box("Keren! Kamu lulus tantangan mengetik cepat!")
                    score += 100
                elif submitted:
                    show_multiline_box("Ups! Jawabanmu salah. Tetap semangat!")
                    score -= 50
                else:
                    show_multiline_box("Waktu habis! Coba lagi di level berikutnya ya!")
                    lives -= 1
                    if lives <= 0:
                        running = False
                blocks = generate_blocks(level)
                ball.reset_position(paddle)
                game_started = False

        paddle.draw()
        ball.draw()
        for block in blocks:
            block.draw()

        font = pygame.font.SysFont(None, 28)
        screen.blit(font.render(f"Skor: {score}", True, WHITE), (10, 10))
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, ((WIDTH - level_text.get_width()) // 2, 10))
        screen.blit(font.render("Nyawa:", True, WHITE), (WIDTH - 145, 10))

        for i in range(lives):
            x = WIDTH - 60 + i * 22
            pygame.draw.circle(screen, RED, (x, 20), ball.radius)
            pygame.draw.circle(screen, WHITE, (x, 20), ball.radius, 2)

        pygame.display.flip()

    if game_over_screen(score, level):
        main()
    else:
        pygame.quit(); sys.exit()

if __name__ == "__main__":
    main()
