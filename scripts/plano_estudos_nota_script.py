url = "http://localhost:8069"
db = 'odoov4'
username = 'admin'
password = 'admin'

import xmlrpc.client
import json

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
version = common.version()
uid = common.authenticate(db, username, password, {})

print('Hello -> ' + str(version) + '\nUID -> ' + str(uid))

ficheiro = open('../dados/notasalunos.json')

dados = json.load(ficheiro)

numero = 0
for nota in dados:

        aluno = models.execute_kw(db, uid, password,
                'transum.aluno', 'search_read',
                [[['nr_mecanografico', '=', nota['numero']]]],
                {'fields': ['planos_atuais']})
      
        plano_id = models.execute_kw(db, uid, password,
                'transum.plano_estudos', 'search_read',
                [[['id', '=', aluno[0]['planos_atuais'][0]]]],
                {'fields': ['id']})

        nota_a_inserir = models.execute_kw(db, uid, password,
                        'transum.plano_estudos_uc', 'search_read',
                        [['&',('plano_estudos.id', '=', plano_id[0]['id']),('codigo','=',nota['uc'])]],
                        {'fields': ['codigo','nota']})

        models.execute_kw(db, uid, password, 'transum.plano_estudos_uc', 'write', [[nota_a_inserir[0]['id']], {
                'nota': nota['nota'],
                }])  
        print('Novo update = 'str(numero))
        numero+=1                                     