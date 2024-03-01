#!/usr/bin/env python


import grovepi
import config
import time

currently_shooting = 0

def init_grovepi_board():
    grovepi.pinMode(config.GROVEPI_CHANNEL_THROTTLE_L, "OUTPUT")
    grovepi.pinMode(config.GROVEPI_CHANNEL_THROTTLE_R, "OUTPUT")
    grovepi.pinMode(config.GROVEPI_CHANNEL_THROTTLE_TURRET, "OUTPUT")
    grovepi.pinMode(config.GROVEPI_CHANNEL_DIRECTION_L, "OUTPUT")
    grovepi.pinMode(config.GROVEPI_CHANNEL_DIRECTION_R, "OUTPUT")
    grovepi.pinMode(config.GROVEPI_CHANNEL_DIRECTION_TURRET_1, "OUTPUT")
    grovepi.pinMode(config.GROVEPI_CHANNEL_DIRECTION_TURRET_2, "OUTPUT")
    grovepi.pinMode(config.GROVEPI_CHANNEL_GUN, "OUTPUT")
    grovepi.pinMode(config.GROVEPI_CHANNEL_BUZZER, "OUTPUT")


    grovepi.analogWrite(config.GROVEPI_CHANNEL_THROTTLE_L, 0)
    grovepi.analogWrite(config.GROVEPI_CHANNEL_THROTTLE_R, 0)
    grovepi.analogWrite(config.GROVEPI_CHANNEL_THROTTLE_TURRET, 0)

    grovepi.digitalWrite(config.GROVEPI_CHANNEL_DIRECTION_L, 0)
    grovepi.digitalWrite(config.GROVEPI_CHANNEL_DIRECTION_R, 0)
    grovepi.digitalWrite(config.GROVEPI_CHANNEL_DIRECTION_TURRET_1, 0)
    grovepi.digitalWrite(config.GROVEPI_CHANNEL_DIRECTION_TURRET_2, 0)
    grovepi.digitalWrite(config.GROVEPI_CHANNEL_GUN, 0)

    # Buzz to confirm successful initialization
    grovepi.digitalWrite(config.GROVEPI_CHANNEL_BUZZER, 1)
    time.sleep(1)
    grovepi.digitalWrite(config.GROVEPI_CHANNEL_BUZZER, 0)



def move_tank(throttle_l, throttle_r):

    direction_l = 0
    direction_r = 0
    
    if throttle_l < 0:
        direction_l = 1
        throttle_l *= -1

    if throttle_r < 0:
        direction_r = 1
        throttle_r *= -1

    pwm_l = throttle2pwm(throttle_l)
    pwm_r = throttle2pwm(throttle_r)

    if config._debug:
        print("PWM left: %d, direction left: %d" % (pwm_l, direction_l))
        print("PWM right: %d, direction right: %d" % (pwm_r, direction_r))

    grovepi.digitalWrite(config.GROVEPI_CHANNEL_DIRECTION_L, direction_l)
    grovepi.analogWrite(config.GROVEPI_CHANNEL_THROTTLE_L, pwm_l)
    grovepi.digitalWrite(config.GROVEPI_CHANNEL_DIRECTION_R, direction_r)
    grovepi.analogWrite(config.GROVEPI_CHANNEL_THROTTLE_R, pwm_r)


def move_turret(throttle_t):
    if throttle_t < 0:
        grovepi.digitalWrite(GROVEPI_CHANNEL_DIRECTION_TURRET_1, 1)
        grovepi.digitalWrite(GROVEPI_CHANNEL_DIRECTION_TURRET_2, 0)
    elif throttle_t > 0:
        grovepi.digitalWrite(GROVEPI_CHANNEL_DIRECTION_TURRET_1, 0)
        grovepi.digitalWrite(GROVEPI_CHANNEL_DIRECTION_TURRET_2, 1)
    else:
        grovepi.digitalWrite(GROVEPI_CHANNEL_DIRECTION_TURRET_1, 0)
        grovepi.digitalWrite(GROVEPI_CHANNEL_DIRECTION_TURRET_2, 0)



def throttle2pwm(throttle):
    if throttle == 0:
        return 0
    else:
        return (config.GROVEPI_PWM_MAX - config.GROVEPI_PWM_MIN) * throttle + config.GROVEPI_PWM_MIN


def shoot():
    if currently_shooting == 0:
        currently_shooting = 1
        grovepi.digitalWrite(GROVEPI_CHANNEL_GUN, 1)
        time.sleep(1800000 / 1000000.0)
        grovepi.digitalWrite(GROVEPI_CHANNEL_GUN, 0)
        currently_shooting = 0

