import json
import xmlrpc.client

url = "http://localhost:8069"
db = 'odoov6'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

version = common.version()
print('=== Version :: ' + str(version) + "      ===")

uid = common.authenticate(db, username, password, {})
print('=== UID :: ' + str(uid) + "      ===\n")

with open('../dados/notasalunos.json', mode='r', encoding='utf8') as ficheiro:
	dados = json.load(ficheiro)
	counter = 0

	for nota in dados:
		aluno = models.execute_kw(db, uid, password, 'transum.aluno', 'search_read', 
            [[['nr_mecanografico', '=', nota['numero']]]],
            {'fields': ['planos_atuais']})
		
		plano_estudos_id = models.execute_kw(db, uid, password, 'transum.plano_estudos', 'search_read',
			[[['id', '=', aluno[0]['planos_atuais'][0]]]],
            {'fields': ['id']})
		
		uc_pln_stds = models.execute_kw(db, uid, password, 'transum.plano_estudos_uc', 'search_read', [[
			'&', ('plano_estudos.id', '=', plano_estudos_id[0]['id']), ('codigo', '=', nota['uc'])]],
			{'fields': ['codigo', 'nota']})
		
		models.execute_kw(db, uid, password, 'transum.plano_estudos_uc', 'write',
			[[uc_pln_stds[0]['id']], 
			{'nota': nota['nota']}])
		
		counter += 1
		print('=== UPDATE Nº ' + str(counter) + '	===')

print('\n=== Th-th-th-that\'s all folks! ===\n')