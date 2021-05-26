import json
import xmlrpc.client

url = "http://localhost:8069"
db = 'odoov6'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
version = common.version()
uid = common.authenticate(db, username, password, {})


with open('../dados/alunos.json', mode='r', encoding='utf8') as ficheiro:
    dados = json.load(ficheiro)

    # INSERT ALUNOS
    count_alunos = 0
    for aluno in dados:
        id_curso = models.execute_kw(db, uid, password, 'transum.curso', 'search_read', [[['designacao', '=', aluno["curso_id"]]]], {'fields': ['id']})

        aluno_id = models.execute_kw(db, uid, password, 'transum.aluno', 'create',[{
            'nr_mecanografico': aluno['nr_mecanografico'],
            'login': aluno['email'],
            'password': aluno['nr_mecanografico'],
            'name': aluno['name'],
            'curso_id': [id_curso[0]["id"]]
        }])
        count_alunos += 1
        print('===  Aluno   ::  ' + str(count_alunos) + '  ===')