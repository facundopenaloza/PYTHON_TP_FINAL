#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importaciones de librerías standard y propias
import PySimpleGUI as sg
import sys
import clases.casillero
import funciones.funciones_grilla as fg
import funciones.funciones_varias as fv
import funciones.funciones_admin_palabras as ap

# Constantes
HORIZONTAL = 'H'
VERTICAL = 'V'
UPPER = 'U'
LOWER = 'L'
VERBOS = 'V'
ADJETIVOS = 'A'
SUSTANTIVOS = 'S'


def main():
    sg.ChangeLookAndFeel('LightGreen')
    sg.SetOptions(element_padding=(0, 0))
    
    menu_def = [
        ['Palabras', ['Editar Lista']],
        ['Juego', ['Jugar', 'Configuración']],
        ['Ayuda', 'Acerca de Sopa de Letras']
    ]
    
    layout_menu = [
        [sg.Menu(menu_def, tearoff=True)],
        [sg.Text('COLORES')],
        [
            sg.Text('Color para los Adjetivos: ', size=(23, 1)),
            sg.InputCombo(('Rojo', 'Azul', 'Verde'), key='_COLOR_A_', default_value='Rojo', size=(20, 1))
        ],
        [
            sg.Text('Color para los Sustantivos: ', size=(23, 1)),
            sg.InputCombo(('Rojo', 'Azul', 'Verde'), key='_COLOR_S_', default_value='Azul', size=(20, 1))
        ],
        [
            sg.Text('Color para los Verbos: ', size=(23, 1)),
            sg.InputCombo(('Rojo', 'Azul', 'Verde'), key='_COLOR_V_', default_value='Verde', size=(20, 1))
        ],
        [sg.Text('_'  * 100, size=(70, 1))],
        [sg.Text('')],
        [sg.Text('ORIENTACIÓN')],
        [
            sg.Text('Orientación de las palabras: ', size=(23, 1)),
            sg.InputCombo(('Horizontal', 'Vertical'), key='_ORIENTACION_', default_value='Horizontal', size=(20, 1))
        ],
        [sg.Text('_'  * 100, size=(70, 1))],
        [sg.Text('')],
        [sg.Text('CANTIDAD DE PALABRAS A MOSTRAR', size=(40, 1))],
        [
            sg.Text('Cantidad de Adjetivos: ', size=(23, 1)),
            sg.InputCombo(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), key='_CANT_A_', default_value='1', size=(20, 1))
        ],
        [
            sg.Text('Cantidad de Sustantivos: ', size=(23, 1)),
            sg.InputCombo(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), key='_CANT_S_', default_value='1', size=(20, 1))
        ],
        [
            sg.Text('Cantidad de Verbos: ', size=(23, 1)),
            sg.InputCombo(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), key='_CANT_V_', default_value='1', size=(20, 1))
        ],
        [sg.Text('_'  * 100, size=(70, 1))],
        [sg.Text('')],
        [sg.Text('MAYÚSCULAS / MINÚSCULAS', size=(23, 1))],
        [
            sg.Text('Letras en la Sopa: ', size=(23, 1)),
            sg.InputCombo(('Mayúsculas', 'Minúsculas'), key='_MAYMIN_', default_value='Mayúsculas', size=(20, 1))
        ]
    ]
    
    window_menu = sg.Window("SOPA DE LETRAS", default_element_size=(12, 1),
    auto_size_text=False, auto_size_buttons=False,
    default_button_element_size=(12, 1)).Layout(layout_menu)
    
    while True:
        button, values = window_menu.Read()
        
        if button == None or button == 'Exit':
            break
            
        print('Button = ', button)
        
        # ------ Process menu choices ------ #
        if (button == 'Editar Lista'):
            ap.administrar_palabras()
        elif (button == 'Configuración'):
            sg.Popup('Atención', 'Aún no se codificó este apartado.')
        elif (button == 'Acerca de Sopa de Letras'):
            sg.Popup('Atención', 'Aún no se codificó este apartado.')
        elif (button == 'Jugar'):
            jugar(window_menu, values)
            
    window_menu.Close()

def jugar(window_menu, val):

    # Valido que no se repitan los colores para diferentes tipos de
    # palabras
    if ((not val['_COLOR_A_'] in (val['_COLOR_S_'], val['_COLOR_V_']))and
    (not val['_COLOR_S_'] in (val['_COLOR_A_'], val['_COLOR_V_']))and
    (not val['_COLOR_V_'] in (val['_COLOR_A_'], val['_COLOR_S_']))):
        adje_color = fv.asignar_color(val['_COLOR_A_'])
        sust_color = fv.asignar_color(val['_COLOR_S_'])
        verb_color = fv.asignar_color(val['_COLOR_V_'])
    else:
        sg.Popup('Atención', 'No se pueden repetir colores para diferentes tipos de palabras.')
        return

    if (val['_ORIENTACION_'] == 'Horizontal'):
        orientacion = HORIZONTAL
    else:
        orientacion = VERTICAL
    
    if (val['_MAYMIN_'] == 'Mayúsculas'):
        upper_lower = UPPER
    else:
        upper_lower = LOWER

    cant_adj = int(val['_CANT_A_'])
    cant_sust = int(val['_CANT_S_'])
    cant_ver = int(val['_CANT_V_'])

    layout = [
        [sg.Button('Validar'), sg.Button('Salir')],
        [
            sg.Radio('Adjetivos', "R1", key='_RADIO_A_', default=True, size=(10,1), background_color=adje_color, text_color='white'),
            sg.Radio('Sustantivos', "R1", key='_RADIO_S_', size=(10,1), background_color=sust_color, text_color='white'),
            sg.Radio('Verbos', "R1", key='_RADIO_V_', size=(10,1), background_color=verb_color, text_color='white')
        ],
        [sg.Graph((800,800), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False)]
    ]


    window_sopa = sg.Window('SOPA DE LETRAS', ).Layout(layout).Finalize()

    pal_seleccionadas = ap.seleccionar_palabras(cant_adj, cant_sust, cant_ver, upper_lower)
    cant_palabras = len(pal_seleccionadas[ADJETIVOS]) + len(pal_seleccionadas[SUSTANTIVOS]) + len(pal_seleccionadas[VERBOS])
    long_pal_mas_larga = fv.palabra_mas_larga(pal_seleccionadas)
    ancho, alto = fg.grilla_size(cant_palabras, long_pal_mas_larga, orientacion)

    grilla, lista_casilleros = fg.armar_grilla(window_sopa, ancho, alto, pal_seleccionadas, orientacion, upper_lower)

    # for r in lista_casilleros:
    #     for c in r:
    #         print(str(c))

    event = ''

    # Event Loop
    while ((event != 'Validar')and(event != 'Salir')):

        event, values = window_sopa.Read()
        
        print(event, values)
        if event is None or event == 'Salir':
            break
            
        mouse = values['_GRAPH_']

        if event == '_GRAPH_':
            if mouse == (None, None):
                continue
            box_x = mouse[1] // fg.BOX_SIZE
            box_y = mouse[0] // fg.BOX_SIZE
            # print(box_x, box_y)
            # print(str(lista_casilleros[box_x][box_y]))
            
            if (values['_RADIO_A_']):
                color = adje_color
            elif (values['_RADIO_S_']):
                color = sust_color
            elif (values['_RADIO_V_']):
                color = verb_color
            
            lista_casilleros[box_x][box_y].click(color)
            
            if (lista_casilleros[box_x][box_y].esta_seleccionado()):
                grilla.DrawRectangle((box_y * fg.BOX_SIZE + 5, box_x * fg.BOX_SIZE + 3), (box_y * fg.BOX_SIZE + fg.BOX_SIZE + 5, box_x * fg.BOX_SIZE + fg.BOX_SIZE + 3), line_color='black', fill_color=color)
            else:
                grilla.DrawRectangle((box_y * fg.BOX_SIZE + 5, box_x * fg.BOX_SIZE + 3), (box_y * fg.BOX_SIZE + fg.BOX_SIZE + 5, box_x * fg.BOX_SIZE + fg.BOX_SIZE + 3), line_color='black', fill_color='white')
            
            letter_location = (box_y * fg.BOX_SIZE + 18, box_x * fg.BOX_SIZE + 17)
            grilla.DrawText('{}'.format(lista_casilleros[box_x][box_y].get_letra()), letter_location, font='Courier 25')



    if (event == 'Validar'):
        resultado = fg.validar_sopa(lista_casilleros, pal_seleccionadas, cant_palabras, orientacion, adje_color, sust_color, verb_color)
        
        if ((resultado[ADJETIVOS]['ok'])and(resultado[SUSTANTIVOS]['ok'])and(resultado[VERBOS]['ok'])):
            sg.Popup('Felicitaciones', 'Usted ha resuleto la Sopa de Letras de forma correcta.')
        else:
            sg.Popup('Atención!!', 'La solución no fue correcta.\nDetalles:\n' +
            resultado[ADJETIVOS]['info'] + '\n' + resultado[SUSTANTIVOS]['info'] +
            '\n' + resultado[VERBOS]['info'])

    window_sopa.Close()



if __name__ == '__main__':
    main()
