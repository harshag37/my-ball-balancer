import pygame as py
import pymunk as pm
import random as rd
import pymunk.pygame_util
import math
py.init()
def borders(space):
    body=pm.Body(body_type=pm.Body.STATIC)
    body.position=(450,0)
    shape1 = pm.Poly.create_box(body,(900,30))
    body2=pm.Body(body_type=pm.Body.STATIC)
    body2.position=(0,250)
    shape2 = pm.Poly.create_box(body2,(30,500))
    body3=pm.Body(body_type=pm.Body.STATIC)
    body3.position=(900,250)
    shape3 = pm.Poly.create_box(body3,(30,500))
    body4=pm.Body(body_type=pm.Body.STATIC)
    body4.position=(450,500)
    shape4 = pm.Poly.create_box(body4,(900,30))
    space.add(shape1,shape2,shape3,shape4)
def create_ball(space):
    body=pm.Body(body_type=pm.Body.DYNAMIC)
    body.position=(b_x,b_y)
    shape=pm.Circle(body,25)
    shape.elasticity = 0.9
    shape.friction=0.8
    shape.density=1
    space.add(body,shape)
    return body
def create_ledge(space):
    body=pm.Body(body_type=pm.Body.DYNAMIC)
    body.position=(400,250)
    shape = pm.Poly.create_box(body,(600,20))
    joint=pm.constraint.PivotJoint(space.static_body,body,(400,250))
    #joint_motor.max_bias = 2000
    joint.collide_bodies = True
    shape.elasticity = 0.9
    shape.friction=0.8
    shape.density=0.5
    space.add(body,shape,joint)
    return body
def motor(space):
    joint_motor=pm.constraint.SimpleMotor(space.static_body,ledge_body,0)
    joint_motor.max_force = 0
    joint_motor.collide_bodies = True
    joint = pm.constraint.RotaryLimitJoint(space.static_body,ledge_body,-3.14/8,3.14/8)
    space.add(joint_motor,joint)
    
    return(joint_motor)

window=py.display.set_mode((900,500),0,32)
draw_options = pm.pygame_util.DrawOptions(window)
py.display.set_caption("Ball Balancing")
py.display.update()
space=pm.Space()
space.gravity=(0,-500)
clock=py.time.Clock()
ball_body=create_ball(space)
ledge_body=(create_ledge(space))
joint_motor=motor(space)
borders(space)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
white=(255,255,255)
black=(0,0,0)
quit_game=False
b_x=500
b_y=400
fps=60
error=0
prev_error=0
kp=0.55
ki=0.05
kd=65

while not quit_game:
    for event in py.event.get():
        if event.type==py.QUIT:
            quit_game=True
        if event.type==py.KEYDOWN:
            if event.key==py.K_ESCAPE:
                quit_game=True
            elif event.key==py.K_RIGHT:
                ball_body.position[0]+=100
    window.fill(green)
    space.debug_draw(draw_options)
    space.step(1/50)
    clock.tick(fps)
    x=ball_body.position

    error= ((400-x[0])/350)+(-1*ball_body.velocity[0]/100)
    total_error=kp*error+kd*(error-prev_error)+ki*(error+prev_error)
    rot_speed =total_error
    prev_error=error
    space.remove(joint_motor)
    print (rot_speed)
    joint_motor=pm.constraint.SimpleMotor(space.static_body,ledge_body,rot_speed)
    joint_motor.max_force = 800000000
    joint_motor.collide_bodies = True
    space.add(joint_motor)
    # print((ledge_body.angle)*180/3.14)
    py.display.update()
py.quit()
quit()
