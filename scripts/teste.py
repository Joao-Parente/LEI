url = "http://localhost:8069"
db = 'odoov3'
username = 'admin'
password = 'admin'

import xmlrpc.client
import json

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
version = common.version()
uid = common.authenticate(db, username, password, {})

print('Hello -> ' + str(version) + '\nUID -> ' + str(uid))

""" ze = models.execute_kw(db, uid, password,
        'transum.plano_curso', 'search_read',
        [[['active', '=', 't']]],
        {'fields': ['codigo', 'curso_id', 'ucs']})    

print('\n\n'+str(ze)+'\n\n') """



ficheiro = open('../dados/alunos.json')

dados = json.load(ficheiro)

#para ir buscar o id do curso
cursos = []
id_curso = models.execute_kw(db, uid, password,
        'transum.curso', 'search_read',
        [[['designacao', '=', 'Mestrado Integrado em Engenharia Informática']]],
        {'fields': ['id']}) 
cursos.append(id_curso[0]['id'])        

print('id curso -> ' + str(id_curso))

numero = 0
for aluno in dados:
        aluno_id = models.execute_kw(db, uid, password, 'transum.aluno', 'create', [{
                'nr_mecanografico': aluno['nr_mecanografico'],
                'login': aluno['email'],
                'password': aluno['email'],
                'name': aluno['name'],
                'curso_id': cursos,
                }])
        print('Vou no aluno = '+str(numero))
        numero+=1        
