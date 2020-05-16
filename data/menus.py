'''Main menu'''
MENU = {}
MENU['1'] = "Seleccionar temas"
MENU['2'] = "Continuar con la última elección (Intro)"
MENU['3'] = "Mostrar resultados"
MENU['4'] = "Configuración"
MENU['5'] = "Salir (e)"

'''Settings menu'''
itema = {}
itema['n'] = '1'
itema['des'] = 'Número de preguntas en cada test'
itema['londes'] = 'Las preguntas se dividen en test. Selecciona el número de preguntas de cada examen: '
itema['var'] = 'nquest'
itema['type'] = 'int'
itemb = {}
itemb['n'] = '2'
itemb['des'] = 'Porcentaje de preguntas a repetir en cada test'
itemb['londes'] = 'Cada examen consta de preguntas nuevas y preguntas repetidas que se han fallado previamente.' \
                  ' En esta variable hay que definir el porcentaje de preguntas repetidas en tanto por uno.'
itemb['var'] = 'prep'
itemb['type'] = 'float'
itemc = {}
itemc['n'] = '3'
itemc['des'] = 'Listado de las respuestas de las preguntas (con número o letra)'
itemc['londes'] = 'Selecciona una de las siguientes opciones para listar las respuestas de las preguntas:\n' \
                  '1. Listar con a,b,c y d.\n' \
                  '2. Listar con 1,2,3 y 4'
itemc['var'] = 'list_type'
itemc['type'] = 'int'
itemd = {}
itemd['n'] = '4'
itemd['des'] = 'Resetear preguntas'
itemd['londes'] = 'Selecciona una de las siguientes opciones:\n' \
                  '1. Reestablecer todo.\n' \
                  '2. Reestablecer contadores de preguntas.\n' \
                  '3. Reestablecer preguntas descartadas.'
itemd['var'] = 'list_type'
itemd['type'] = ''
SETTINGS_MENU = [itema, itemb, itemc, itemd]