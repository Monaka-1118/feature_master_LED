function 移動平均 (list2: number[]) {
    total = 0
    for (let 値 of list2) {
        total += 値
    }
    移動平均計算結果 = total / list2.length
    return 移動平均計算結果
}
control.onEvent(EventBusSource.MICROBIT_ID_IO_P16, EventBusValue.MICROBIT_PIN_EVT_FALL, function () {
	
})
input.onButtonPressed(Button.A, function () {
    if (A_flag == 0) {
        Boom_angle = 975
        Arm_angle = 1925
        A_flag = 1
        basic.showLeds(`
            . . # . .
            . # # . .
            . . # . .
            . . # . .
            . # # # .
            `)
    } else if (A_flag == 1) {
        Boom_min = pins.analogReadPin(AnalogPin.P0)
        Arm_Max = pins.analogReadPin(AnalogPin.P1)
        A_flag = 2
        Boom_angle = 1925
        Arm_angle = 975
        basic.showLeds(`
            . . # . .
            . # . # .
            . . . # .
            . . # . .
            . # # # .
            `)
    } else if (A_flag == 2) {
        Boom_Max = pins.analogReadPin(AnalogPin.P0)
        Arm_min = pins.analogReadPin(AnalogPin.P1)
        A_flag = 3
        Boom_angle = 1450
        Arm_angle = 1450
        basic.showLeds(`
            . . # . .
            . # . # .
            . . # # .
            . # . # .
            . . # . .
            `)
    } else if (A_flag == 3) {
        Arm_coefficient = 950 / (Arm_Max - Arm_min)
        Boom_coefficient = 950 / (Boom_Max - Boom_min)
        A_flag = 4
        basic.showLeds(`
            . . # # .
            . # . # .
            . # . # .
            . # # # #
            . . . # .
            `)
    }
})
control.onEvent(EventBusSource.MICROBIT_ID_IO_P16, EventBusValue.MICROBIT_PIN_EVT_RISE, function () {
	
})
let Boom_input_ave = 0
let arm_input_ave = 0
let Boom_coefficient = 0
let Arm_coefficient = 0
let 移動平均計算結果 = 0
let total = 0
let senkai_Angle = 0
let Arm_min = 0
let Arm_Max = 0
let Boom_min = 0
let Boom_Max = 0
let A_flag = 0
let Arm_angle = 0
let Boom_angle = 0
Boom_angle = 1450
Arm_angle = 1450
A_flag = 0
Boom_Max = 0
Boom_min = 0
Arm_Max = 0
Arm_min = 0
let Pen_flag = 90
radio.setGroup(1)
let 移動平均数 = 5
let arm_input = pins.analogReadPin(AnalogPin.P1)
let Boom_input = pins.analogReadPin(AnalogPin.P0)
let Pen_swich = pins.analogReadPin(AnalogPin.P16)
let Arm_val = [Arm_angle]
let Boom_val = [Boom_angle]
let Senkai_val = [senkai_Angle]
for (let index = 0; index < 移動平均数 - 1; index++) {
    Arm_val.push(Arm_angle)
    Boom_val.push(Boom_angle)
    Senkai_val.push(senkai_Angle)
}
basic.showLeds(`
    . . # . #
    . # . # .
    . # . # .
    . # . # .
    . . # . .
    `)
basic.forever(function () {
    radio.sendValue("Arm", Arm_angle)
    radio.sendValue("Boom", Boom_angle)
    radio.sendValue("pen", Pen_flag)
})
basic.forever(function () {
    if (A_flag == 4) {
        arm_input = pins.analogReadPin(AnalogPin.P1)
        Boom_input = pins.analogReadPin(AnalogPin.P0)
        Arm_val.shift()
        Boom_val.shift()
        Senkai_val.shift()
        Arm_val.push(arm_input)
        Boom_val.push(Boom_input)
        移動平均(Arm_val)
        arm_input_ave = 移動平均計算結果
        移動平均(Boom_val)
        Boom_input_ave = 移動平均計算結果
        Arm_angle = Arm_coefficient * (arm_input_ave - Arm_min) + 975
        Boom_angle = Boom_coefficient * (Boom_input_ave - Boom_min) + 975
    }
    if (pins.digitalReadPin(DigitalPin.P2) == 0) {
        Pen_flag = 0
    } else {
        Pen_flag = 1
    }
})
