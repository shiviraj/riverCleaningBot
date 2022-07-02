import RPi.GPIO as GPIO
import time

TRIG = 36
ECHO = 38
SERVO = 40
MOTOR_LEFT = 35
MOTOR_RIGHT = 37

def setupBoard():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(SERVO, GPIO.OUT)
  GPIO.setup(TRIG, GPIO.OUT)
  GPIO.setup(ECHO, GPIO.IN)
  GPIO.setup(MOTOR_LEFT, GPIO.OUT)
  GPIO.setup(MOTOR_RIGHT, GPIO.OUT)

def setupServo():
  pwm = GPIO.PWM(SERVO, 50)
  pwm.start(0)
  return pwm

def setAngle(angle, servo):
  duty = angle / 18 + 2
  GPIO.output(SERVO, True)
  servo.ChangeDutyCycle(duty)
  time.sleep(.05)
  GPIO.output(SERVO, False)
  servo.ChangeDutyCycle(0)

def getDistance():
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)
  startTime = time.time()
  stopTime = time.time()
  while GPIO.input(ECHO) == 0:
    startTime = time.time()
  while GPIO.input(ECHO) == 1:
    stopTime = time.time()
  totalTime = stopTime - startTime
  return round(totalTime * 34300 / 2, 2)

def findMinDistance(distances):
  minValue = min(distances.values())
  return {key:value for key,value in distances.items() if value == minValue}

def changeDirection(distanceAndAngle):
  divisor = 30
  distance = list(distanceAndAngle.values())[0]
  angle = list(distanceAndAngle.keys())[0]
  print("nearest object is", angle, "degree", distance, "cm far from the river cleaning bot.")

  if(angle < 90):
    GPIO.output(MOTOR_RIGHT, False)
    time.sleep((90 - angle) / divisor)
    print("moving into left")
  if(angle > 90):
    GPIO.output(MOTOR_LEFT, False)
    time.sleep((angle - 90) / divisor)
    print("moving into right")
  GPIO.output(MOTOR_LEFT, True)
  GPIO.output(MOTOR_RIGHT, True)
  print("moving farward")


if __name__ == "__main__":
  try:
    setupBoard()
    servo = setupServo()
    angle = 0
    direction = 1
    step = 15
    distances = {}
    while True:
      setAngle(angle, servo)
      distance = getDistance()
      distances[angle] = distance
      time.sleep(.3)
      angle += step * direction
      if(angle == 180 or angle == 0):
        direction = direction * -1
        minDistance = findMinDistance(distances)
        changeDirection(minDistance)
        time.sleep(.1)
  finally:
    servo.stop()
    GPIO.cleanup()