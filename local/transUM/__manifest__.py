{
    "name": "TransUM",
    "summary": "Aplicação para a transição de planos de estudos",
    'description': "Brevemente irá ser feita uma reestruturação dos Mestrados Integrados da Escola de Engenharia da Universidade do Minho. Este processo fará com que alunos actualmente num plano de estudos tenham de transitar para um novo plano. Tendo isto em conta, no âmbito da unidade curricular de Laboratório em Engenharia Informática da Universidade do Minho, pretendeu-se desenvolver uma aplicação que permita a elaboração dos planos de transição dos alunos do plano de estudos actual para o novo plano de estudos, desta forma, este projecto foi pensado de forma a auxiliar as direcções de curso e os alunos no processo de transição, possibilitando assim uma melhor gestão e planeamento dos diversos cursos que irão ser reestruturados e ainda permitir que os alunos fiquem com clareza sobre a sua situação futura e presente ao nível do curso que frequenta.",
    'author': 'Gonçalo Pinto, João Pedro Parente e José Nuno Costa',
    'category': 'Administration',
    "depends": ["base"],
    "data": [
            "security/groups.xml",
            "security/ir.model.access.csv",
            "views/administrador_view.xml",
            "views/aluno_view.xml", 
            "views/curso_view.xml",           
            "views/direcao_curso_view.xml",   
            "views/docente_view.xml",                
            "views/plano_curso_view.xml", 
            "views/plano_estudos_uc_view.xml", 
            "views/plano_estudos_view.xml", 
            "views/plano_transicao_uc_mostra_view.xml",
            "views/plano_transicao_uc_view.xml", 
            "views/plano_transicao_view.xml", 
            "views/proposta_novo_plano_view.xml",
            "views/uc_view.xml",
            "views/transum_menu.xml",
            "views/transum_message.xml",
            "reports/report_template.xml",
            "reports/report_generate.xml"
    ],
    'application': True,
}
