import cv2
import mediapipe as mp
import pygame
import time
import random
from Paddle import Paddle
from Ball import Ball
from handDetectingModule import handDetector


# Game Initialization
pygame.init()
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
FPS = 60
#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#velocity or speed
VEL = 4
colors = [(255, 0, 0),(0, 255, 0),(0, 0, 255),(0, 255, 255), (255, 0, 255), (255, 255, 0)]
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 10
Leftcolor = random.choice(colors)
Rightcolor = random.choice(list(filter(lambda color: color != Leftcolor, colors)))

clock = pygame.time.Clock()

left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                        2, PADDLE_WIDTH, PADDLE_HEIGHT, Leftcolor)
right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                        2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, Rightcolor)
ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

left_score = 0
right_score = 0


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) -
                                right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle, vel=4):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True, VEL=vel)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False, VEL=vel)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True, VEL=vel)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False, VEL=vel)


#MediaPipe Initialization


cap = cv2.VideoCapture(0)
pTime = 0
cTime = 0
detector = handDetector()

while True:
    #mediapipe
    success, img = cap.read()
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    if fps<10:
        VEL = 20
    elif fps < 20 and fps > 10:
        VEL = 10
    else :
        VEL = 4
    img = detector.findHands(img, Leftcolor, Rightcolor)
    detector.findPosition(img, left_paddle, right_paddle, Leftcolor, Rightcolor, VEL)
    flipimg = cv2.flip(img,1)
    cv2.line(flipimg,(320,0),(320,480),(0,0,0),5)
    cv2.putText(flipimg, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    cv2.imshow("Image", flipimg)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    
    #game code
    clock.tick(FPS)
    draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    handle_paddle_movement(keys, left_paddle, right_paddle)
    detector.findPosition(img, left_paddle, right_paddle, Leftcolor, Rightcolor)

    ball.move(VEL)
    handle_collision(ball, left_paddle, right_paddle)

    if ball.x < 0:
        right_score += 1
        ball.reset()
    elif ball.x > WIDTH:
        left_score += 1
        ball.reset()

    won = False
    if left_score >= WINNING_SCORE:
        won = True
        win_text = "Left Player Won!"
    elif right_score >= WINNING_SCORE:
        won = True
        win_text = "Right Player Won!"

    if won:
        text = SCORE_FONT.render(win_text, 1, WHITE)
        WIN.blit(text, (WIDTH//2 - text.get_width() //
                        2, HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()
        left_score = 0
        right_score = 0
cap.release()      
pygame.quit()

