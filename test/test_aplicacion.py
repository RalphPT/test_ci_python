from app import app
import pytest
from flask import Flask


@pytest.fixture() # fixture => en este caso sirve para colocar la configuracion precargada de mi aplicacion de Flask
def cliente(): #la funcion cliente
    client = app.test_client()
    yield client # yield Es como el RETURN, pero solo va a retornar una vez que se haya encontrado o definido determinada variable, en otras palabras no va a esperar a que termine de ejecutarse. Es mucho más eficiente para cuestiones cuando estamos haciendo listas, iterando objetos, etc-

# testeando PROCEDIMIENTO DEL PROYECTO '/actividades'
def test_actividades_get(cliente: Flask): # cliente, debe ser el mismo nombre con el que lleva la función, sino la prueba no funciona
    respuesta = cliente.get('/actividades')
    assert respuesta.json == {
        'message':'Internal Server Error'
    }
def test_registro(cliente: Flask):
    respuesta = cliente.post('/registro', json = {
        'nombre': 'Juan',
        'apellido': 'Vargas',
        'correo': 'jvargas@correo.com',
        'password': 'Welcome123!'
    })

    assert respuesta.status_code == 201
    assert 'message' in respuesta.json
    assert respuesta.json.get('message') == 'Usuario registrado exitosamente'

def test_login(cliente: Flask):
    respuesta = cliente.post('/login', json = {
        'correo': 'jvargas@correo.com',
        'password': 'Welcome123!'
    })
    assert 'content' in respuesta.json
    assert respuesta.status_code == 200

def test_actividades_get_autorizado(cliente: Flask):
    respuesta_login = cliente.post('/login', json = {
        'correo': 'jvargas@correo.com',
        'password': 'Welcome123!'
    })
    token = respuesta_login.json.get('content')
    #print(token)
    respuesta = cliente.get('/actividades', headers = {'Authorization': 'Bearer {}'.format(token)})
    assert respuesta.json == {
        'content': []
    }