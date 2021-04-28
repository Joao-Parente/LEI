import xmlrpc.client
import json

url = "http://localhost:8069"
db = 'odoov3'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
version = common.version()
uid = common.authenticate(db, username, password, {})

ficheiro = open('../dados/curso.json')

dados = json.load(ficheiro)

designacao_curso = dados['designacao']
departamento = dados['departamento']
tipo_curso = dados['tipo']
plano_curso_designacao = dados['plano_curso_designacao']

id_curso = models.execute_kw(db, uid, password, 'transum.curso', 'create', [{
    'designacao': designacao_curso,
    'departamento': departamento,
    'tipo': tipo_curso,
}]) 

print('Curso Inserido com Sucesso!')

ucs_ids = []
numero = 0
for i in dados['plano_curso']:
    id_uc = models.execute_kw(db, uid, password, 'transum.uc', 'create', [{
        'ects': i['creditos'],
        'designacao': i['nomeUC'],
        'codigo': i['codigoUC'],
        'ano': i['ano'],
        'semestre': i['semestre'],
    }])
    ucs_ids.append(id_uc)
    numero+=1

print('Foram Inseridas '+str(numero)+ ' ucs!')    

id_plano_curso = models.execute_kw(db, uid, password, 'transum.plano_curso', 'create', [{
    'codigo': plano_curso_designacao,
    'curso_id': id_curso,
    'ucs': ucs_ids,
}])

print('Plano de Curso inserido com Sucesso!')

ficheiro.close()