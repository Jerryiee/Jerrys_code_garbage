# Include the library files
import RPi.GPIO as GPIO
import tkinter as tk
from piservo import Servo

# Include the motor control pins
ENA = 18
IN1 = 24
IN2 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)

servo = Servo(13)
servo_min = 45
servo_max = 105
servo_position = 75
servo.write(servo_position)

# Create a Tkinter window with two sliders
window = tk.Tk()
window.geometry('400x150')
window.title("Motor and Servo Control")
motor_slider = tk.Scale(window, from_=-100, to=100, orient=tk.HORIZONTAL, label="Motor Speed")
motor_slider.pack()
servo_slider = tk.Scale(window, from_=servo_min, to=servo_max, orient=tk.HORIZONTAL, label="Servo Position")
servo_slider.pack()

pwm = GPIO.PWM(ENA, 100)
pwm.start(0)

def set_motor_speed(value):
    duty_cycle = (abs(value) / 100) * 100
    if value > 0:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    elif value < 0:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(duty_cycle)

def set_servo_position(value):
    global servo_position
    if value < servo_min:
        servo_position = servo_min
    elif value > servo_max:
        servo_position = servo_max
    else:
        servo_position = value
    servo.write(servo_position)

# Update the motor speed and servo position based on the slider values
def update_controls(motor_value, servo_value):
    motor_value = int(motor_value)  # Convert motor value to an integer
    servo_value = int(servo_value)  # Convert servo value to an integer
    set_motor_speed(motor_value)
    set_servo_position(servo_value)

motor_slider.config(command=lambda value: update_controls(value, servo_slider.get()))
servo_slider.config(command=lambda value: update_controls(motor_slider.get(), value))

window.mainloop()
