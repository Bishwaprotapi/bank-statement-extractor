from flask import Blueprint
from src.controller.bank_statement_controller import (process_jamuna_bank_statement_api,
                                                      process_ebl_bank_statement_api,
                                                      process_ncc_bank_statement_api,
                                                      process_city_bank_statement_api,
                                                      process_ucb_bank_statement_api,
                                                      process_midland_bank_statement_api,
                                                      process_bcb_bank_statement_api,
                                                      process_standard_bank_statement_api,
                                                      process_bank_asia_statement_api,
                                                      process_mtbl_bank_statement_api)

bank_statement_blueprint = Blueprint('bank_statement', __name__)
bank_statement_blueprint.route('/process_jamuna_bank_statement', methods=['POST'])(process_jamuna_bank_statement_api)
bank_statement_blueprint.route('/process_ebl_bank_statement', methods=['POST'])(process_ebl_bank_statement_api)
bank_statement_blueprint.route('/process_ncc_bank_statement', methods=['POST'])(process_ncc_bank_statement_api)
bank_statement_blueprint.route('/process_city_bank_statement', methods=['POST'])(process_city_bank_statement_api)
bank_statement_blueprint.route('/process_ucb_bank_statement', methods=['POST'])(process_ucb_bank_statement_api)
bank_statement_blueprint.route('/process_midland_bank_statement', methods=['POST'])(process_midland_bank_statement_api)
bank_statement_blueprint.route('/process_bcb_bank_statement', methods=['POST'])(process_bcb_bank_statement_api)
bank_statement_blueprint.route('/process_standard_bank_statement', methods=['POST'])(process_standard_bank_statement_api)
bank_statement_blueprint.route('/process_bank_asia_statement', methods=['POST'])(process_bank_asia_statement_api)
bank_statement_blueprint.route('/process_mtbl_bank_statement', methods=['POST'])(process_mtbl_bank_statement_api)
