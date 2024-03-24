def 移動平均(list2: List[number]):
    global total, 移動平均計算結果
    total = 0
    for 値 in list2:
        total += 値
    移動平均計算結果 = total / len(list2)
    return 移動平均計算結果

def on_microbit_id_io_p16_pin_evt_fall():
    pass
control.on_event(EventBusSource.MICROBIT_ID_IO_P16,
    EventBusValue.MICROBIT_PIN_EVT_FALL,
    on_microbit_id_io_p16_pin_evt_fall)

def on_button_pressed_a():
    global Boom_angle, Arm_angle, A_flag, Boom_min, Arm_Max, Boom_Max, Arm_min, Arm_coefficient, Boom_coefficient
    if A_flag == 0:
        Boom_angle = 975
        Arm_angle = 1925
        A_flag = 1
        basic.show_leds("""
            . . # . .
            . # # . .
            . . # . .
            . . # . .
            . # # # .
            """)
    elif A_flag == 1:
        Boom_min = pins.analog_read_pin(AnalogPin.P0)
        Arm_Max = pins.analog_read_pin(AnalogPin.P1)
        A_flag = 2
        Boom_angle = 1925
        Arm_angle = 975
        basic.show_leds("""
            . . # . .
            . # . # .
            . . . # .
            . . # . .
            . # # # .
            """)
    elif A_flag == 2:
        Boom_Max = pins.analog_read_pin(AnalogPin.P0)
        Arm_min = pins.analog_read_pin(AnalogPin.P1)
        A_flag = 3
        Boom_angle = 1450
        Arm_angle = 1450
        basic.show_leds("""
            . . # . .
            . # . # .
            . . # # .
            . # . # .
            . . # . .
            """)
    elif A_flag == 3:
        Arm_coefficient = 950 / (Arm_Max - Arm_min)
        Boom_coefficient = 950 / (Boom_Max - Boom_min)
        A_flag = 4
        basic.show_leds("""
            . . # # .
            . # . # .
            . # . # .
            . # # # #
            . . . # .
            """)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_microbit_id_io_p16_pin_evt_rise():
    pass
control.on_event(EventBusSource.MICROBIT_ID_IO_P16,
    EventBusValue.MICROBIT_PIN_EVT_RISE,
    on_microbit_id_io_p16_pin_evt_rise)

Boom_input_ave = 0
arm_input_ave = 0
Boom_coefficient = 0
Arm_coefficient = 0
移動平均計算結果 = 0
total = 0
senkai_Angle = 0
Arm_min = 0
Arm_Max = 0
Boom_min = 0
Boom_Max = 0
A_flag = 0
Arm_angle = 0
Boom_angle = 0
Boom_angle = 1450
Arm_angle = 1450
A_flag = 0
Boom_Max = 0
Boom_min = 0
Arm_Max = 0
Arm_min = 0
Pen_flag = 90
radio.set_group(1)
移動平均数 = 5
arm_input = pins.analog_read_pin(AnalogPin.P1)
Boom_input = pins.analog_read_pin(AnalogPin.P0)
Pen_swich = pins.analog_read_pin(AnalogPin.P16)
Arm_val = [Arm_angle]
Boom_val = [Boom_angle]
Senkai_val = [senkai_Angle]
for index in range(移動平均数 - 1):
    Arm_val.append(Arm_angle)
    Boom_val.append(Boom_angle)
    Senkai_val.append(senkai_Angle)
basic.show_leds("""
    . . # . #
    . # . # .
    . # . # .
    . # . # .
    . . # . .
    """)

def on_forever():
    radio.send_value("Arm", Arm_angle)
    radio.send_value("Boom", Boom_angle)
    radio.send_value("pen", Pen_flag)
basic.forever(on_forever)

def on_forever2():
    global arm_input, Boom_input, arm_input_ave, Boom_input_ave, Arm_angle, Boom_angle, Pen_flag
    if A_flag == 4:
        arm_input = pins.analog_read_pin(AnalogPin.P1)
        Boom_input = pins.analog_read_pin(AnalogPin.P0)
        Arm_val.shift()
        Boom_val.shift()
        Senkai_val.shift()
        Arm_val.append(arm_input)
        Boom_val.append(Boom_input)
        移動平均(Arm_val)
        arm_input_ave = 移動平均計算結果
        移動平均(Boom_val)
        Boom_input_ave = 移動平均計算結果
        Arm_angle = Arm_coefficient * (arm_input_ave - Arm_min) + 975
        Boom_angle = Boom_coefficient * (Boom_input_ave - Boom_min) + 975
    if pins.digital_read_pin(DigitalPin.P2) == 0:
        Pen_flag = 55
    else:
        Pen_flag = 100
basic.forever(on_forever2)
