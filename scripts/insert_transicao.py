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


with open('../dados/transicao.json', mode='r', encoding='utf8') as ficheiro:
    dados = json.load(ficheiro)

    id_curso_antigo = models.execute_kw(db, uid, password, 'transum.curso', 'search_read', [[['designacao', '=', dados["curso_antigo"]]]], {'fields': ['id']})

    list_cursos_novos = []
    for novo_curso in dados["curso_novos"]:
        id_curso_novo = models.execute_kw(db, uid, password, 'transum.curso', 'search_read', [[['designacao', '=', novo_curso]]], {'fields': ['id']})
        list_cursos_novos.append(id_curso_novo[0]["id"])
    
    id_plano_transicao = models.execute_kw(db, uid, password, 'transum.plano_transicao', 'create',[{
        'designacao': dados['designacao'],
        'curso_id': id_curso_antigo[0]["id"],
        'cursos_novos': list_cursos_novos
    }])
    print('===  Plano Transicao Inserido com Sucesso!     ===')

    count_correspondencias = 0
    for correspondencia in dados['correspondencias']:
        list_ucs_antigas = []
        list_ucs_novas = []
        for antiga in correspondencia['uc_antiga']:
            uc_antiga = models.execute_kw(db, uid, password, 'transum.uc', 'search_read', [[['codigo', '=', antiga]]], {'fields': ['id']})
            list_ucs_antigas.append(uc_antiga[0]['id'])

        for nova in correspondencia['uc_nova']:
            uc_nova = models.execute_kw(db, uid, password, 'transum.uc', 'search_read', [[['codigo', '=', nova]]], {'fields': ['id']})
            list_ucs_novas.append(uc_nova[0]['id'])

        id_plano_transicao_uc = models.execute_kw(db, uid, password, 'transum.plano_transicao_uc', 'create',[{
            'uc_antiga': list_ucs_antigas,
            'uc_nova': list_ucs_novas,
            'plano_transicao': id_plano_transicao
        }])
        count_correspondencias += 1

    print('===  Foram inseridas ' + str(count_correspondencias) + ' Correspondências          ===')

        