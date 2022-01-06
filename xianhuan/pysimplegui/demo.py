#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import PySimpleGUI as sg

layout = [
    [sg.Text('一句话概括Python')],
    [sg.Input(key='-INPUT111-')],
    [sg.Input(key='-INPUT222-')],
    [sg.Button('确认'), sg.Button('取消')],
    [sg.Text('输出：'), sg.Text(key='-OUTPUT-')]
]
window = sg.Window('PySimpleGUI Demo', layout)
while True:
    event, values = window.read()
    print(event)
    print(values)
    if event in (None, '取消'):
        break
    else:
        window['-OUTPUT-'].update(values['-INPUT222-'])
window.close()

