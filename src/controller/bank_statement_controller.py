from flask import jsonify, request
import os
import tempfile
from werkzeug.utils import secure_filename
from src.helper.response_helper import set_response_headers
from src.service.jamuna_bank_statement_service import process_bank_statement_service
from src.service.ebl_bank_statement_service import process_ebl_bank_statement_service
from src.service.ncc_bank_statement_service import process_ncc_bank_statement_service
from src.service.city_bank_statement_service import process_city_bank_statement_service
from src.service.ucb_bank_statement_service import process_ucb_bank_statement_service
from src.service.midland_bank_statement_service import process_midland_bank_statement_service
from src.service.bcb_bank_statement_service import process_bcb_bank_statement_service
from src.service.standard_bank_statement_service import process_standard_bank_statement_service
from src.service.bank_asia_statement_service import process_bank_asia_statement_service
from src.service.mtbl_bank_statement_service import process_mtbl_bank_statement_service

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_jamuna_bank_statement_api():
    """
    Controller function to process general bank statement files (using jamuna service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_bank_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400

def process_ebl_bank_statement_api():
    """
    Controller function to process general bank statement files (using EBL service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_ebl_bank_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400

def process_ncc_bank_statement_api():
    """
    Controller function to process general bank statement files (using NCC service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_ncc_bank_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400

def process_city_bank_statement_api():
    """
    Controller function to process general bank statement files (using City service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_city_bank_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400

def process_ucb_bank_statement_api():
    """
    Controller function to process general bank statement files (using UCB service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_ucb_bank_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400

def process_midland_bank_statement_api():
    """
    Controller function to process general bank statement files (using UCB service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_midland_bank_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400

def process_bcb_bank_statement_api():
    """
    Controller function to process general bank statement files (using UCB service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_bcb_bank_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400

def process_standard_bank_statement_api():
    """
    Controller function to process general bank statement files (using UCB service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_standard_bank_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400

def process_bank_asia_statement_api():
    """
    Controller function to process general bank statement files (using UCB service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_bank_asia_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400

def process_mtbl_bank_statement_api():
    """
    Controller function to process general bank statement files (using UCB service)
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            response = jsonify({
                'success': False,
                'error': 'No file provided in the request'
            })
            response = set_response_headers(response)
            return response, 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            response = jsonify({
                'success': False,
                'error': 'No file selected'
            })
            response = set_response_headers(response)
            return response, 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            response = jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload PDF, PNG, JPG, or JPEG files only.'
            })
            response = set_response_headers(response)
            return response, 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filename.rsplit(".", 1)[1].lower()}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # Process the bank statement using service layer
            result = process_mtbl_bank_statement_service(temp_file_path)

            # Clean up temporary file
            os.unlink(temp_file_path)

            # Return the bank statement data directly
            response = jsonify(result)
            response = set_response_headers(response)
            return response, 200

        except Exception as processing_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

            response = jsonify({
                'success': False,
                'error': f'Error processing bank statement: {str(processing_error)}'
            })
            response = set_response_headers(response)
            return response, 400

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
        response = set_response_headers(response)
        return response, 400