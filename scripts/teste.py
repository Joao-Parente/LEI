url = "http://localhost:8069"
db = 'odoov3'
username = 'admin'
password = 'admin'

import xmlrpc.client

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
version = common.version()
uid = common.authenticate(db, username, password, {})

print('Hello -> ' + str(version) + '\nUID -> ' + str(uid))

#inserir um curso
""" id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
    'name': "New Partner",
}]) """

""" ze = models.execute_kw(
    db, uid, password, 'transum.curso', 'fields_get',
    [], {'attributes': ['designacao', 'departamento', 'tipo']}) """

ze = models.execute_kw(db, uid, password,
        'transum.curso', 'search_read',
        [[['active', '=', 't']]],
        {'fields': ['designacao', 'departamento', 'tipo']})    

print('\n\n'+str(ze)+'\n\n')