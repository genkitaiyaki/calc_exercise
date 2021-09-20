from models.formula import Formula
from services.common_service import CommonService
from services.base_calc_service import BaseCalcService
from services.single_digi_add_service import SingleDigiAddService
from services.single_digi_sub_service import SingleDigiSubService

# TODO: もっと良い命名がありそう、、
def execute(calc_service: BaseCalcService, title: str):
    common_service = CommonService()
    formulas = common_service.create_formulas(
        calc_service.get_exercise_parts(),
        calc_service.validater
    )
    common_service.export_exercise(title, formulas)

execute(SingleDigiAddService(), 'たしざんのもんだい')
execute(SingleDigiSubService(), 'ひきざんのもんだい')