from __future__ import print_function, unicode_literals

from models.formula import Formula
from services.common_service import CommonService
from services.base_calc_service import BaseCalcService
from services.single_digi_add_service import SingleDigiAddService
from services.single_digi_sub_service import SingleDigiSubService
from pyfiglet import figlet_format
from PyInquirer import prompt

print(figlet_format('CALC EXERCISE'))

questions = [
    {
        'type': 'checkbox',
        'message': 'Select calc type.',
        'name': 'calc_types',
        'choices': [
            {
                'name': 'add (+)'
            },
            {
                'name': 'sub (-)'
            },
        ]
     }
]
answers = prompt(questions)
calc_types: list[str] = answers.get('calc_types')

# TODO: もっと良い命名がありそう、、
def execute(calc_service: BaseCalcService, title: str):
    common_service = CommonService()
    formulas = common_service.create_formulas(
        calc_service.get_exercise_parts(),
        calc_service.validater
    )
    common_service.export_exercise(title, formulas)

if ('add (+)' in calc_types) : execute(SingleDigiAddService(), 'たしざんのもんだい')  
if ('sub (-)' in calc_types) : execute(SingleDigiSubService(), 'ひきざんのもんだい')