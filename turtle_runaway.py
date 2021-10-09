# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.

import turtle, random , time


class RunawayGame:
    def __init__(self, canvas, chaser, runner, catch_radius=10, init_dist=400):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'

        self.chaser.shape('turtle')
        self.chaser.color('blue')
        self.chaser.penup()
        self.chaser.setx(-init_dist / 2)

        self.runner.shape('turtle')
        self.runner.color('red')
        self.runner.penup()
        self.runner.setx(+init_dist / 2)
        self.runner.setheading(180)
        


        # Instantiate an another turtle for drawing (time,score, game_status)
        self.drawer1 = turtle.RawTurtle(canvas)
        self.drawer1.hideturtle()
        self.drawer1.penup() 
        
        self.drawer2 = turtle.RawTurtle(canvas)
        self.drawer2.hideturtle()
        self.drawer2.penup() 
        
        self.drawer3 = turtle.RawTurtle(canvas)
        self.drawer3.hideturtle()
        self.drawer3.penup() 
        
        # create turtle's food
        self.food = turtle.RawTurtle(canvas)
        self.food.shape('circle')
        self.food.color('yellow')
        self.food.penup()
        self.food.sety(-init_dist/2)
        
        
        # creat game stadium
        self.drawer2 = turtle.RawTurtle(canvas)    
        self.drawer2.hideturtle()
        self.drawer2.speed(0)
        self.drawer2.penup()
        self.drawer2.setpos(300,-300)
        self.drawer2.pendown()
        self.drawer2.setheading(90)
        for i in range(4):
            self.drawer2.forward(600)
            self.drawer2.left(90)

    def is_catch(self):
        p = self.food.pos()
        q = self.runner.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
    
    def is_catch_chaser(self):
        p = self.chaser.pos()
        q = self.runner.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
  
    def start(self, ai_timer_msec=100, score=0):
        self.ai_timer_msec = ai_timer_msec
        self.score=score
        self.start_time=time.time()
        self.canvas.ontimer(self.step, self.ai_timer_msec) 
        
    def step(self):
        self.chaser.run_ai(self.runner) 
        self.runner.run_ai(self.chaser)
        
        # penalty if go out stadium
        if (self.runner.xcor()<-300 or self.runner.xcor()>300):
            self.score=self.score-3
        if (self.runner.ycor()<-300 or self.runner.ycor()>300):
            self.score=self.score-3
            
        # penalty if runner meet chaser
        if self.is_catch_chaser()==True:
            self.score=self.score-1
            
        # New food created and reward when runner meets food 
        if self.is_catch()==False:
            pass
        else:
            new_x=random.randint(-300,300)
            new_y=random.randint(-300,300)
            self.food.goto(new_x,new_y)
            
            self.score=self.score+1
            
        
        elapse=time.time()-self.start_time
        
        #draw elapsed time
        self.drawer1.undo()
        self.drawer1.penup()
        self.drawer1.setpos(-430, 200)
        self.drawer1.write(f'Time {elapse:.0f}', font={'Arial',12})  
        
        #draw score
        self.drawer2.undo()
        self.drawer2.penup()
        self.drawer2.setpos(-430,150)
        self.drawer2.write(f'Score {self.score}',font={'굴림',12})
        
        #draw game_status
        self.drawer3.undo()
        self.drawer3.penup()
        self.drawer3.setpos(-430,100)
        self.drawer3.write('In game',font={'굴림',12})
        
        # Game Over when time is over 100
        if elapse>100:
            self.drawer3.undo()
            self.drawer3.write("Game Over",font={'굴림',12})
            return
        
        self.canvas.ontimer(self.step, self.ai_timer_msec) 
    

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opponent):
        pass
    

class OpponentMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=30):
        super().__init__(canvas)
        self.step_move = step_move

    def run_ai(self, opponent):
        prob = random.random()
        opp_pos=opponent.pos()
        ang=self.towards(opp_pos)
        if prob <= 0.2:
            self.setheading(ang)
            self.forward(self.step_move)
    
      

if __name__ == '__main__':
  
   
    canvas = turtle.Screen()
    canvas.title("Turtle Runaway")

  
    chaser = OpponentMover(canvas)
    runner = ManualMover(canvas)

    game = RunawayGame(canvas, chaser, runner)
    game.start()
    


    canvas.mainloop()
    
