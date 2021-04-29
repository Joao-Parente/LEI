import json
import xmlrpc.client

url = "http://localhost:8069"
db = 'odoov4'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
version = common.version()
uid = common.authenticate(db, username, password, {})

with open('../dados/curso.json', mode='r', encoding='utf8') as ficheiro:
    dados = json.load(ficheiro)

    # INSERT CURSO 
    id_curso = models.execute_kw(db, uid, password, 'transum.curso', 'create', [{
        'designacao': dados['designacao'],
        'departamento': dados['departamento'],
        'tipo': dados['tipo']
    }])
    cursos = [id_curso]
    print('===  Curso Inserido com Sucesso!     ===')

    # INSERT UC's
    list_ucs = []
    count_ucs = 0
    for uc in dados['plano_curso']:
        id_uc = models.execute_kw(db, uid, password, 'transum.uc', 'create',[{
            'ects': uc['creditos'],
            'designacao': uc['nomeUC'],
            'codigo': uc['codigoUC'],
            'ano': uc['ano'],
            'semestre': uc['semestre']
        }])
        list_ucs.append(id_uc)
        count_ucs += 1
    print('===  Foram inseridas ' + str(count_ucs) + ' UCs          ===')
   
    # INSERT PLANO DE CURSO
    id_plano_curso = models.execute_kw(db, uid, password, 'transum.plano_curso', 'create',[{
        'codigo': dados['plano_curso_designacao'],
        'curso_id': id_curso,
        'ucs': list_ucs
    }])
    print('=== Plano_Curso Inserido c/ Sucesso! ===')


with open('../dados/alunos.json', mode='r', encoding='utf8') as ficheiro:
    dados = json.load(ficheiro)

    # INSERT ALUNOS
    count_alunos = 0
    for aluno in dados:
        aluno_id = models.execute_kw(db, uid, password, 'transum.aluno', 'create',[{
            'nr_mecanografico': aluno['nr_mecanografico'],
            'login': aluno['email'],
            'password': aluno['nr_mecanografico'],
            'name': aluno['name'],
            'curso_id': cursos
        }])
        count_alunos += 1
        print('===  Aluno   ::  ' + str(count_alunos) + '  ===')