import pygame
import time
import random 
pygame.init()

WHITE=(255,255,255)
YELLOW=(255,255,0)
BLUE=(0,0,255)
GREEN=(0,255,0)

FONT=pygame.font.SysFont("comicsans",60)


WIDTH=1000
HEIGHT=800

WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pong")

class Score:
    def __init__(self):
        self.playerOne=0
        self.playerTwo=0

class Collisions:
    def __init__(self):
        self.number=0

class Paddle:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width 
        self.height=height 
        self.y_movement=5

    def draw(self):
        pygame.draw.rect(WIN,WHITE,(self.x,self.y,self.width,self.height),1)
    
    def move_paddle(self,up=True):
        if up and self.y-self.y_movement>=0:
            self.y-=self.y_movement
        elif not up and self.y+self.y_movement+100<=HEIGHT:
            self.y+=self.y_movement


class Ball:
    def __init__(self,x,y,radius):
        self.x=x
        self.y=y
        self.radius=radius 
        self.x_movement=-5 
        self.y_movement=0
        self.MAX_Y=5
        self.COLOR=YELLOW
    
    def draw(self):
        pygame.draw.circle(WIN,self.COLOR,(self.x,self.y),self.radius)
    
    def move(self):
        self.x+=self.x_movement
        self.y+=self.y_movement


def draw():
    for i in range(10,HEIGHT,HEIGHT//10):
        if not i%2:
            pygame.draw.rect(WIN,YELLOW,(WIDTH//2,i,10,50))
    pygame.draw.rect(WIN,(0,0,255),(0,0,WIDTH,HEIGHT),3)


def generateColor():
    x1=random.randint(0,255)
    x2=random.randint(0,255)
    x3=random.randint(0,255)
    if x1==x2==x3==0:
        x1=x1=x3=255
    return (x1,x2,x3)
    

def checkCollision(ball,left_paddle,right_paddle,collisionTracker):
    left_y_upper=left_paddle.y
    left_y_lower=left_paddle.y+100
    right_y_upper=right_paddle.y
    right_y_lower=right_paddle.y+100 
    middle_left=left_paddle.y+50
    middle_right=right_paddle.y+50

    if ball.x_movement<0:
        if ball.x<=20 and ball.y<=left_y_lower and ball.y>=left_y_upper:
            ball.x_movement*=-1
            collisionTracker.number+=1
            if ball.y<middle_left:
                diff=middle_left-ball.y 
                r=diff/50 
                ball.y_movement=-1*ball.MAX_Y*r

            elif ball.y>middle_left:
                diff=ball.y-middle_left
                r=diff/50 
                ball.y_movement=ball.MAX_Y*r
    if ball.y<=0:
        ball.y_movement*=-1 
    if ball.y>=HEIGHT-ball.radius:
        ball.y_movement*=-1
    
    elif ball.x_movement>0:
        if ball.x>=WIDTH-20 and ball.y>=right_y_upper and ball.y<=right_y_lower:
            ball.x_movement*=-1
            collisionTracker.number+=1
            if ball.y<middle_right:
                diff=middle_right-ball.y
                r=diff/50 
                ball.y_movement=-1*ball.MAX_Y*r
            elif ball.y>middle_right:
                diff=ball.y-middle_right 
                r=diff/50
                ball.y_movement=ball.MAX_Y*r 
    if not collisionTracker.number%4 and collisionTracker.number!=0:
        ball.COLOR=generateColor()
        collisionTracker.number+=1
        ball.x_movement+=1
        ball.MAX_Y+=0.5

def resetGame(ball,left_paddle,right_paddle,score):
    if ball.x<(0-ball.radius*2) or ball.x>WIDTH+ball.radius*2:
        if ball.x<0:
            score.playerTwo+=1 
        elif ball.x>0:
            score.playerOne+=1
        ball.x=WIDTH//2
        ball.y=HEIGHT//2
        s=random.randint(0,1)
        ball.x_movement=5
        ball.y_movement=0
        ball.MAX_Y=5
        if s==0:
            ball.x_movement=-1*ball.x_movement 
        else:
            ball.x_movement=ball.x_movement 
        left_paddle.y=HEIGHT//2-50
        right_paddle.y=HEIGHT//2-50
        
        return True

        


def main():
    left_paddle=Paddle(10,HEIGHT//2-50,10,100)
    right_paddle=Paddle(WIDTH-20,HEIGHT//2-50,10,100)
    clock=pygame.time.Clock()
    ball=Ball(WIDTH//2,HEIGHT//2,8)
    collisionTracker=Collisions()
    score=Score()

    run=True
    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False 
        keys=pygame.key.get_pressed()

        draw()
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()
        ball.move()
        checkCollision(ball,left_paddle,right_paddle,collisionTracker)
        x=resetGame(ball,left_paddle,right_paddle,score)
        playerOne=FONT.render(f"Player One: {score.playerOne}",1,WHITE)
        playerTwo=FONT.render(f"Player Two: {score.playerTwo}",1,WHITE)
        WIN.blit(playerOne,(WIDTH//4-playerOne.get_width()//2,20))
        WIN.blit(playerTwo,(WIDTH-WIDTH//4-playerTwo.get_width()//2,20))
        if x:
            time.sleep(2)
    

        if keys[pygame.K_w]:
            left_paddle.move_paddle()
        if keys[pygame.K_s]:
            left_paddle.move_paddle(False)
        if keys[pygame.K_DOWN]:
            right_paddle.move_paddle(False)
        if keys[pygame.K_UP]:
            right_paddle.move_paddle()
        pygame.display.update()
    
    pygame.quit()



if __name__=="__main__":
    main()
