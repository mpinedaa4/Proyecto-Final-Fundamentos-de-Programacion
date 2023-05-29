from Estudiante import *
import csv
import pandas as pd
import subprocess

class GUI():
    def registro(self):
        layout = [
            [sg.Text('Ingrese el nombre del estudiante'), sg.InputText(key='Nombre')],
            [sg.Text('Ingrese el número de documento del estudiante'), sg.InputText(key='ID')],
            [sg.Text('Ingrese la edad del estudiante'), sg.InputText(key='Edad')],
            [sg.Text('Ingrese la carrera (pregrado) del estudiante'), sg.InputText(key='Carrera')],
            [sg.Button('Guardar'), sg.Button('Salir')]
        ]

        reg = sg.Window('Registrar Estudiante', layout)

        while True:
            event, values = reg.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Salir':
                break
            
            if event == 'Guardar':
                cedulas = []
                with open('datos.csv') as archivo:
                    f = csv.reader(archivo, delimiter=',')
                    for linea in f:
                        cedulas.append(linea[0])

                nombre = values['Nombre']
                ID = values['ID']
                edad = values['Edad']
                carrera = values ['Carrera']

                if ID in cedulas:
                    reg['ID'].update('')
                    sg.popup('Este número de identificación ya se encuentra registrado. Ingrese uno nuevo.')   
                elif len(nombre) > 0 and len(ID) > 0 and len(edad) > 0 and len(carrera) > 0:
                    try:
                        ID = int(ID)
                    except ValueError:
                        reg['ID'].update('')
                        sg.popup('No ha ingresado un número de documento válido.')
                        continue
                    try:
                        edad = int(edad)
                    except ValueError:
                        reg['Edad'].update('')
                        sg.popup('No ha ingresado una edad válida.')
                        continue
                    if edad < 1 or edad > 100:
                        reg['Edad'].update('')
                        sg.popup('La edad está por fuera del rango permitido (1-100). Inténtelo nuevamente.')
                    else:
                        estudiante = Estudiante(ID, nombre, edad, carrera)
                        estudiante.escribir()
                        reg['Nombre'].update('')
                        reg['ID'].update('')
                        reg['Edad'].update('')
                        reg['Carrera'].update('')
                        sg.popup('Se ha registrado el estudiante exitosamente.')
                else:
                    sg.popup('Por favor diligencie todos los campos.')
        reg.close()

    def notas(self):
        layout = [  [sg.Text('Ingrese el número de documento del estudiante'), sg.InputText(key='ID')],
                    [sg.Text('Ingrese la nota que desea agregar'), sg.InputText(key='nota')],
                    [sg.Button('Agregar'), sg.Text(''), sg.Button('Salir')]
                ]
        
        notas = sg.Window('Agregar Nota', layout)

        while True:
            event, values = notas.read()

            if event == 'Agregar':
                personas = []
                with open('datos.csv') as archivo:
                    f = csv.reader(archivo, delimiter=',')
                    for linea in f:
                        estudiante = Estudiante(linea[0], linea[1], linea[2], linea[3])
                        personas.append(estudiante)

                ID = values['ID']
                nota = values['nota']
                existe = False

                for i in personas:
                    if ID == i.ID:
                        try:
                            nota = float(nota)
                            if nota > 5 or nota < 0:
                                sg.popup('No ha ingresado una nota válida. Inténtelo nuevamente.')
                                existe = True
                                break
                            else:
                                i.agregar_nota(nota)
                                sg.popup('La nota fue ingresada con éxito.')
                                existe = True
                        except ValueError:
                            sg.popup('No ha ingresado una nota válida. Inténtelo nuevamente.')
                            existe = True
                if not existe:
                    sg.popup('No existe un estudiante registrado con ese número de documento.')
                    continue
                else:
                    existe = False
                    continue

            if event == sg.WIN_CLOSED or event == 'Salir':
                break
        notas.close()

    def promedio(self):
        layout = [  [sg.Text('Ingrese el número de documento del estudiante'), sg.InputText(key='ID')],
                    [sg.Button('Calcular promedio'), sg.Text(''), sg.Button('Salir')]
                ]
        
        prom = sg.Window('Calcular promedio', layout)

        while True:
            event, values = prom.read()

            if event == 'Calcular promedio':
                personas = []
                with open('datos.csv') as archivo:
                    f = csv.reader(archivo, delimiter=',')
                    for linea in f:
                        estudiante = Estudiante(linea[0], linea[1], linea[2], linea[3])
                        personas.append(estudiante)

                ID = values['ID']
                existe = False

                for i in personas:
                    if ID == i.ID:
                        promedio = i.promedio()
                        if not promedio:
                            existe = True
                            break
                        else:
                            sg.popup(f'El promedio de {i.nombre} es: {promedio}')
                            existe = True
                            break
                if existe:
                    existe = False
                    continue
                else:
                    sg.popup('No existe un estudiante registrado con ese número de documento.')
                    continue

            if event == sg.WIN_CLOSED or event == 'Salir':
                break
        prom.close()


    def buscar(self):
        layout = [  [sg.Text('¿Cómo desea buscar al estudiante?')],
                    [sg.Button('Por nombre'), sg.Button('Por número de documento')],
                    [sg.Button('Por edad'), sg.Button('Por carrera')],
                    [sg.Text('')],
                    [sg.Button('Salir')]
                ]
        buscar = sg.Window('Buscar', layout)

        listado = []

        while True:
            event, values = buscar.read()

            if event == 'Por nombre':
                layout = [  [sg.Text('Ingrese el nombre del estudiante')],
                            [sg.Input(key='nombre')],
                            [sg.Button('Buscar'), sg.Button('Cerrar')]
                        ]
                por_nombre = sg.Window('Buscar por nombre', layout)
                while True:
                    event, values = por_nombre.read()
                    if event == sg.WINDOW_CLOSED or event == 'Cerrar':
                        break
                    if event == 'Buscar':
                        nombre = values['nombre']
                        with open('datos.csv') as archivo:
                            f = csv.reader(archivo, delimiter=',')
                            for linea in f:
                                if nombre.lower() == linea[1].lower():
                                    estudiante = Estudiante(linea[0], linea[1], linea[2], linea[3])
                                    listado.append(estudiante)
                        if len(listado) == 0:
                            sg.popup('No hay estudiantes registrados con ese nombre')
                        else:
                            consolidado = []
                            for i in listado:
                                i.imprimir_estudiante(consolidado)
                            sg.popup_scrolled('Información de estudiantes', ''.join(consolidado))
                            listado = []
                por_nombre.close()

            if event == 'Por número de documento':
                layout = [  [sg.Text('Ingrese el número de documento del estudiante')],
                            [sg.Input(key='ID')],
                            [sg.Button('Buscar'), sg.Button('Cerrar')]
                        ]
                por_ID = sg.Window('Buscar por documento', layout)
                while True:
                    event, values = por_ID.read()
                    if event == sg.WINDOW_CLOSED or event == 'Cerrar':
                        break
                    if event == 'Buscar':
                        ID = values['ID']
                        try:
                            ID = int(ID)
                        except ValueError:
                            sg.popup('No ha ingresado un número de documento válido. Inténtelo nuevamente.')
                            continue
                        with open('datos.csv') as archivo:
                            f = csv.reader(archivo, delimiter=',')
                            for linea in f:
                                if str(ID) == linea[0]:
                                    estudiante = Estudiante(linea[0], linea[1], linea[2], linea[3])
                                    listado.append(estudiante)
                        if len(listado) == 0:
                            sg.popup('No hay estudiantes registrados con ese número de documento')
                        else:
                            consolidado = []
                            for i in listado:
                                i.imprimir_estudiante(consolidado)
                            sg.popup_scrolled('Información de estudiantes', ''.join(consolidado))
                            listado = []
                            continue
                por_ID.close()

            if event == 'Por edad':
                layout = [  [sg.Text('Ingrese la edad del estudiante')],
                            [sg.Input(key='edad')],
                            [sg.Button('Buscar'), sg.Button('Cerrar')]
                        ]
                por_edad = sg.Window('Buscar por edad', layout)
                while True:
                    event, values = por_edad.read()
                    if event == sg.WINDOW_CLOSED or event == 'Cerrar':
                        break
                    if event == 'Buscar':
                        edad = values['edad']
                        try:
                            edad = int(edad)
                        except ValueError:
                            sg.popup('No ha ingresado una edad válida. Inténtelo nuevamente.')
                            continue
                        with open('datos.csv') as archivo:
                            f = csv.reader(archivo, delimiter=',')
                            for linea in f:
                                if str(edad) == linea[2]:
                                    estudiante = Estudiante(linea[0], linea[1], linea[2], linea[3])
                                    listado.append(estudiante)
                        if len(listado) == 0:
                            sg.popup('No hay estudiantes registrados con esa edad')
                        else:
                            consolidado = []
                            for i in listado:
                                i.imprimir_estudiante(consolidado)
                            sg.popup_scrolled('Información de estudiantes', ''.join(consolidado))
                            listado = []
                por_edad.close()

            if event == 'Por carrera':
                layout = [  [sg.Text('Ingrese la carrera del estudiante')],
                            [sg.Input(key='carrera')],
                            [sg.Button('Buscar'), sg.Button('Cerrar')]
                        ]
                por_carrera = sg.Window('Buscar por carrera', layout)
                while True:
                    event, values = por_carrera.read()
                    if event == sg.WINDOW_CLOSED or event == 'Cerrar':
                        break
                    if event == 'Buscar':
                        carrera = values['carrera']
                        with open('datos.csv') as archivo:
                            f = csv.reader(archivo, delimiter=',')
                            for linea in f:
                                if carrera.lower() == linea[3].lower():
                                    estudiante = Estudiante(linea[0], linea[1], linea[2], linea[3])
                                    listado.append(estudiante)
                        if len(listado) == 0:
                            sg.popup('No hay estudiantes registrados con esa carrera')
                        else:
                            consolidado = []
                            for i in listado:
                                i.imprimir_estudiante(consolidado)
                            sg.popup_scrolled('Información de estudiantes', ''.join(consolidado))
                            listado = []
                por_carrera.close()

            if event == sg.WIN_CLOSED or event == 'Salir':
                break
        buscar.close()

    # Funcion para ordenar el csv de mayor a menor longitud de línea
    def obtener_longitud(self, linea):
        return len(linea)
    
    def ordenar(self):
        with open('datos.csv', 'r') as archivo:
            lector_csv = csv.reader(archivo)
            lineas = list(lector_csv)
    # Ordenar la lista de líneas por longitud (de mayor a menor)
        lineas.sort(key=self.obtener_longitud, reverse=True)
        with open('datos.csv', 'w', newline='') as archivo:
            escritor_csv = csv.writer(archivo)
            escritor_csv.writerows(lineas)

    def exportar(self):
        self.ordenar()
        encabezado = ['Número de ID', 'Nombre', 'Edad', 'Carrera']

        with open('datos.csv', 'r') as archivo:
          f = csv.reader(archivo, delimiter=',')
          contador = 1
          for linea in f:
            for i in linea[4:]:
              encabezado.append(f'Nota {contador}')
              contador += 1
            break
        
        with open('datos.csv',newline='') as f:
          r = csv.reader(f)
          datos = [line for line in r]
          
        with open('datos2excel.csv','w',newline='') as f:
            w = csv.writer(f)
            w.writerow(encabezado)
            w.writerows(datos)

        try:
            archivo = pd.read_csv (r'datos2excel.csv', encoding='utf-8')
            archivo.to_excel (r'exportado.xlsx', index = None, header=True)
            sg.popup('El archivo de excel ha sido generado con éxito.')
            exportado = 'exportado.xlsx'
            comando = f'open "{exportado}"'
            subprocess.run(comando, shell=True)
        except:
            sg.popup('Ha ocurrido un error y no se ha generado correctamente el archivo de excel. por favor inténtelo de nuevo.')


    def principal(self):
        sg.theme('DarkAmber')

        layout = [  [sg.Text('Bienvenido al sistema de gestión de estudiantes. ¿Qué desea hacer?')],
                    [sg.Text('')],
                    [sg.Button('Registrar estudiante'), sg.Button('Agregar una nota')],
                    [sg.Button('Calcular promedio'), sg.Button('Buscar un estudiante')],
                    [sg.Button('Exportar excel de estudiantes')],
                    [sg.Text('')],
                    [sg.Button('Salir')],
                    [sg.Text('')]
                ]

        window = sg.Window('Universidad ABC', layout)
        
        while True:
            event,values = window.read()

            if event == 'Registrar estudiante':
                self.registro()

            if event == 'Agregar una nota':
                self.notas()

            if event == 'Calcular promedio':
                self.promedio()

            if event == 'Buscar un estudiante':
                self.buscar()

            if event == 'Exportar excel de estudiantes':
                self.exportar()

            if event == sg.WIN_CLOSED or event == 'Salir':
                break
        