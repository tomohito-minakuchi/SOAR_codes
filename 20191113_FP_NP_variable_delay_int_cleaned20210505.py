from gpiozero import Button
from gpiozero import LED
from gpiozero import OutputDevice
from gpiozero.tools import sleep
import time
from datetime import datetime
import pandas as pd
import numpy as np

## ============ CONSTANTS =============

IR_1 = Button(21)
LED_1 = LED(16)
IR_2 = Button(12)
LED_2 = LED(20)
# LED_red1 = LED(5)
# LED_red2 = LED(6)
tdt_out1 = LED(13)
tdt_out2 = LED(26)


## == preset the variable delays and interaction times==
delay_min = float(input("What is the minimum of the random delay (s)?  "))
delay_max = float(input("What is the maximum of the random delay (s)? "))
preset_delays = delay_min + np.random.rand(200)*(delay_max-delay_min) # uniform distribution between the max and min of the delay

interaction_min = float(input("What is the minimum of the interaction time (s)? " ))
interaction_max = float(input("What is the maximum of the interaction time (s)? " ))
preset_interactions = interaction_min + np.random.rand(200)*(interaction_max-interaction_min)

## == poke record file initialization ==
mouse_id = input("The mouse ID is ")
print("Start")
expdate = datetime.now().strftime("%Y-%m-%d_%H%M_")
file_name = expdate + mouse_id

start_time = time.time() # record the onset time of the experiment

dfdelayinteraction = pd.DataFrame(np.array([preset_delays, preset_interactions]).T, columns = ['delays', 'interaction times'])
dfdelay.to_csv(file_name + "_variabledelays.csv")

dfsuccess = pd.DataFrame([['start', start_time]] ,  columns=['id', 'time'])
dfright = pd.DataFrame([['start', start_time]] ,  columns=['id', 'time'])
dfwrong = pd.DataFrame([['start', start_time]] ,  columns=['id', 'time'])
dfsuccess.to_csv(file_name + "_reward_delivery.csv")
dfright.to_csv(file_name + "_rightpoke.csv")
dfwrong.to_csv(file_name + "_wrongpoke.csv")

poke_success = False					# Determinator of platform activation

# Direction set to not active high == goes up when False
motor_1_dir = OutputDevice(4, active_high = False, initial_value = False)
### PWM turns on when True
motor_1_pwm = OutputDevice(17, active_high = True, initial_value = True)
### PWM copy for TDT
motor_1_pwm_copy = OutputDevice(18, active_high = True, initial_value = True)

##

def motor_down(motor_1_dir, motor_1_pwm, motor_1_pwm_copy):
    time.sleep(preset_delays[reward_counter-1])
    motor_1_dir.off()
    motor_1_pwm.on()
    motor_1_pwm_copy.on()
    time.sleep(4)
    motor_1_pwm.off()
    motor_1_pwm_copy.off()
    time.sleep(preset_interactions[reward_counter-1])
    motor_1_dir.on()
    motor_1_pwm.on()
    motor_1_pwm_copy.on()
    time.sleep(4)
    motor_1_pwm.off()
    motor_1_pwm_copy.off()

def reward_delivery():
    global poke_success
#    if IR_1.is_active and poke_success == False:
    if poke_success == False:
        poke_time = time.time()
        poke_success = True
        motor_down(motor_1_dir,motor_1_pwm, motor_1_pwm_copy)
        temp = pd.DataFrame([['reward delivery', poke_time - start_time]])
        temp.to_csv(file_name + "_reward_delivery.csv", mode='a', header = False)
        poke_success = False

def rightpoke():
    poke_time = time.time()
    temp = pd.DataFrame([['poke', poke_time - start_time]])
    temp.to_csv(file_name + "_rightpoke.csv", mode='a', header = False)
    print (poke_time - start_time, 'right poke')

def wrongpoke():
    poke_time = time.time()
    temp = pd.DataFrame([['poke', poke_time - start_time]])
    temp.to_csv(file_name + "_wrongpoke.csv", mode='a', header = False)
    print (poke_time - start_time, 'wrong poke')

LED_1.source = (IR_1.values)
LED_2.source = (IR_2.values)
# LED_red1.source = (IR_1.values)
# LED_red2.source = (IR_2.values)
tdt_out1.source = (IR_1.values)
tdt_out2.source = (IR_2.values)

motor_1_pwm.off()
motor_1_pwm_copy.off()
motor_1_dir.off()

IR_1.when_released = rightpoke
IR_2.when_released = wrongpoke

reward_counter = 0
while True:
    sleep(0.001)
    if IR_1.is_pressed == False:
        reward_counter += 1
        print ('The ',reward_counter, ' th Reward delivery start!')
        reward_delivery()
