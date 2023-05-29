import shutil
import csv
import PySimpleGUI as sg

class Estudiante():
  def __init__(self, ID, nombre, edad, carrera):
    self.nombre = nombre
    self.ID = ID
    self.edad = edad
    self.carrera = carrera
    self.notas = []

  def agregar_nota(self, nota):
    temp = open('temp', 'w')
    with open('datos.csv', 'r') as f:
      for line in f:
        if line.startswith(self.ID):
          line = line.strip() + ',' + str(nota) + '\n'
        temp.write(line)
    temp.close()
    shutil.move('temp', 'datos.csv')

  def guardar_notas(self):
    with open('datos.csv') as archivo:
      f = csv.reader(archivo, delimiter=',')
      for linea in f:
        if linea[0] == self.ID and len(linea) >= 5:
          for i in linea[4:]:
            self.notas.append(float(i))

  def promedio(self):
    promedio = 0
    self.guardar_notas()
    if len(self.notas) == 0:
      sg.popup(f'{self.nombre} no tiene notas ingresadas.')
      return False
    else:
      for i in self.notas:
        promedio += i
      promedio /= len(self.notas)
    return promedio

  def escribir(self):
    f = open('datos.csv','a+')
    f.write(f'{str(self.ID)},{self.nombre},{str(self.edad)},{self.carrera}' + '\n')

  def imprimir_estudiante(self, lista):
    lista.append(f'Nombre del estudiante: {self.nombre}' + '\n' +
             f'Número de documento del estudiante: {self.ID}' + '\n' +
             f'Edad del estudiante: {self.edad}' + '\n' +
             f'Carrera del estudiante: {self.carrera}' + '\n' +
             '--------------------------------------------------------' + '\n')
