import base64
import json
import os
import re
import random
from typing import List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------- Configuration ----------
poppler_path = r'C:\poppler-23.11.0\Library\bin'
os.environ["PATH"] += os.pathsep + poppler_path

class ImageProcessor:
    # ---------- Encode image ----------
    def encode_image(self, image_file) -> str:
        try:
            image_file.seek(0)
        except Exception:
            pass
        data = image_file.read()
        try:
            image_file.seek(0)
        except Exception:
            pass
        return base64.b64encode(data).decode("utf-8")

    def encode_image_to_base64(self, pil_image):
        """Convert PIL image to base64 string"""
        from io import BytesIO
        buffer = BytesIO()
        pil_image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

class GeminiSession:
    def __load_gemini_keys(self):
        try:
            with open('config/gemini_keys.json', 'r') as f:
                keys_data = json.load(f)
            return list(keys_data.values())
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def __init__(self):
        self.keys = self.__load_gemini_keys()
        if not self.keys:
            raise RuntimeError("No Google API keys available")
        self.index = random.randint(0, len(self.keys) - 1)
        self.current_key = None
        self.client = None
        self.get_new_key()

    def get_new_key(self):
        """Get a new API key for the session"""
        self.index += 1
        if self.index >= len(self.keys):
            self.index = 0
        self.current_key = self.keys[self.index]
        self.client = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            google_api_key=self.current_key
        )
        print(f"Switched to API key: {self.current_key[:8]}...")

    def _find_working_key(self):
        """Find and set a working API key"""
        for api_key in self.keys:
            try:
                test_client = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    temperature=0.3,
                    google_api_key=api_key
                )
                # Test the key with a minimal request
                self.current_key = api_key
                self.client = test_client
                print(f"Using API key: {api_key[:8]}...")
                return
            except Exception as e:
                continue
        raise RuntimeError("No working Google API keys found")

    def call_api(self, prompt: str, base64_image: str) -> dict:
        """Make API call with the established session key"""
        if not self.client:
            raise RuntimeError("No active API session")

        try:
            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            )

            response = self.client.invoke([message])
            output = response.content.strip()

            # Parse JSON response with multiple fallback strategies
            return self._parse_json_response(output)

        except Exception as e:
            raise RuntimeError(f"API call failed: {str(e)}")

    def _parse_json_response(self, output: str) -> dict:
        """Parse JSON response with multiple fallback strategies"""
        # Store original output for debugging
        original_output = output

        # Strategy 1: Basic cleanup
        try:
            cleaned = re.sub(r"^```json|^```|```$", "", output.strip(), flags=re.MULTILINE).strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Strategy 2: Extract JSON from anywhere in the response
        try:
            # Find JSON block between braces
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        # Strategy 3: Fix common JSON issues
        try:
            # Remove extra commas, fix quotes, etc.
            fixed_json = self._fix_common_json_issues(output)
            return json.loads(fixed_json)
        except json.JSONDecodeError:
            pass

        # Strategy 4: Try to extract and rebuild JSON structure
        try:
            return self._rebuild_json_structure(output)
        except:
            pass

        print(f"'{original_output[:500]}...'")

        return {
            "BankAccountNo": "",
            "BankName": "",
            "Transactions": [],
            "parsing_error": "Failed to parse API response",
            "raw_response": original_output[:200] + "..." if len(original_output) > 200 else original_output
        }

    def _fix_common_json_issues(self, text: str) -> str:
        text = re.sub(r"```(?:json)?\s*", "", text)
        text = re.sub(r"```\s*$", "", text)
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        text = re.sub(r'(?<!\\)"(?=.*")', '\\"', text)
        start = text.find('{')
        end = text.rfind('}') + 1

        if start != -1 and end > start:
            return text[start:end]

        return text

    def _rebuild_json_structure(self, text: str) -> dict:
        result = {
            "BankAccountNo": "",
            "BankName": "",
            "Transactions": []
        }

        bank_account_match = re.search(r'"BankAccountNo"\s*:\s*"([^"]*)"', text)
        if bank_account_match:
            result["BankAccountNo"] = bank_account_match.group(1)

        bank_name_match = re.search(r'"BankName"\s*:\s*"([^"]*)"', text)
        if bank_name_match:
            result["BankName"] = bank_name_match.group(1)

        transactions_match = re.search(r'"Transactions"\s*:\s*\[(.*?)\]', text, re.DOTALL)
        if transactions_match:
            transactions_text = transactions_match.group(1)
            result["Transactions"] = self._extract_transactions(transactions_text)

        return result

    def _extract_transactions(self, transactions_text: str) -> List[dict]:
        transactions = []
        transaction_blocks = re.findall(r'\{[^}]*\}', transactions_text)

        for block in transaction_blocks:
            try:
                transaction = json.loads(block)
                transactions.append(transaction)
            except:
                transaction = {
                    "TransactionDate": "",
                    "Particulars": "",
                    "InstrumentNo": "",
                    "MonDebit": 0,
                    "MonCredit": 0,
                    "MonBalance": 0
                }
                transactions.append(transaction)

        return transactions

FIRST_PAGE_PROMPT = """
Extract the bank account number, bank name, and ALL transactions from the FIRST PAGE of the bank statement.

Use the following JSON structure strictly:
- Return ONLY valid JSON (no markdown, no comments).
- Remember this is every sensitive data, do not miss any rows. You will calculate the balance based on the transactions. 
- Always calculate debit, credit, and balance based on the transactions. do calculate if any data debited then from balance will previous balance minus debit, and if any data credited then from balance will be previous balance plus credit. Recheck validation by checking the balance of the last transaction.
- A transaction = a row that contains a transaction date. Do NOT include headers/footers or "Opening/Closing Balance" rows.
- Skip any rows that do not contain a Transaction Date.
- Strip currency symbols and thousand separators. Parse negatives (e.g., "(1,234.56)") correctly.
- For other missing fields, use "" for text and 0 for numbers.
- Preserve the order of transactions exactly as they appear.
- Dates must be in yyyy-mm-dd format (no time).
- This very important notes to you that do not skip any single row, you will calculate the balance based on the transactions. then you will return the json with the following structure:

JSON format:
{
  "BankAccountNo": "",
  "BankName": "",
  "Transactions": [
    {
      "TransactionDate": "",
      "Particulars": "",
      "InstrumentNo": "",
      "MonDebit": 0,
      "MonCredit": 0,
      "MonBalance": 0
    }
  ]
}
"""

OTHER_PAGES_PROMPT = """
Extract ALL transactions from THIS PAGE of the bank statement into the JSON structure below.

Rules (follow strictly):
- Return ONLY valid JSON (no markdown, no comments).
- Remember this is every sensitive data, do not miss any rows. You will calculate the balance based on the transactions. 
- Always calculate debit, credit, and balance based on the transactions. do calculate if any data debited then from balance will previous balance minus debit, and if any data credited then from balance will be previous balance plus credit. Recheck validation by checking the balance of the last transaction.
- A transaction = a row that contains a transaction date. Do NOT include headers/footers or "Opening/Closing Balance" rows.
- Skip any rows that do not contain a Transaction Date.
- Merge wrapped/multi-line descriptions into the previous transaction's "Particulars".
- Preserve the original row order.
- For other missing fields, use "" for text and 0 for numbers.
- Dates must be normalized to yyyy-mm-dd (no time). Recognize common variants like dd/mm/yyyy, dd-mm-yyyy, dd-MMM-yyyy, yyyy/mm/dd. If the date is unreadable, set "TransactionDate": "" (still include the row).
- Strip currency symbols and thousand separators. Parse negatives (e.g., "(1,234.56)") correctly.
- InstrumentNo should be "" if not present.
- This very important notes to you that do not skip any single row, you will calculate the balance based on the transactions. then you will return the json with the following structure:

JSON format:
{
  "Transactions": [
    {
      "TransactionDate": "",
      "Particulars": "",
      "InstrumentNo": "",
      "MonDebit": 0,
      "MonCredit": 0,
      "MonBalance": 0
    }
  ]
}
"""

def convert_pdf_to_images(pdf_path, dpi=300):
    from pdf2image import convert_from_path
    return convert_from_path(pdf_path, dpi=dpi, poppler_path=None)

def analyze_image_with_prompt(image, prompt, gemini_session):
    processor = ImageProcessor()
    base64_img = processor.encode_image_to_base64(image)

    try:
        return gemini_session.call_api(prompt, base64_img)
    except Exception as e:
        return {"error": f"ERROR: {str(e)}"}

def process_standard_bank_statement_service(pdf_path):
    """
    Service layer function to process Standard bank statement files
    This function handles the business logic for bank statement processing using Gemini AI
    """
    try:
        images = convert_pdf_to_images(pdf_path)
        full_data = {
            "BankAccountNo": "",
            "BankName": "",
            "Transactions": []
        }

        gemini_session = GeminiSession()

        for idx, image in enumerate(images):
            print(f"Processing page {idx + 1}...")
            is_first = (idx == 0)
            prompt = FIRST_PAGE_PROMPT if is_first else OTHER_PAGES_PROMPT

            result = analyze_image_with_prompt(image, prompt, gemini_session)

            if "error" in result:
                print(f"⚠️ API Error on page {idx + 1}: {result['error']}")
                continue

            try:
                if is_first:
                    full_data["BankAccountNo"] = result.get("BankAccountNo", "")
                    full_data["BankName"] = result.get("BankName", "")
                    full_data["Transactions"].extend(result.get("Transactions", []))
                else:
                    full_data["Transactions"].extend(result.get("Transactions", []))

                print(f"✅ Successfully parsed page {idx + 1} with {len(result.get('Transactions', []))} transactions")

            except Exception as e:
                print(f"Failed to process page {idx + 1}: {e}")
                print("Raw response:")
                print("-" * 50)
                print(result)
                print("-" * 50)
                print()

        return full_data
    except Exception as e:
        raise Exception(f"Service error in Standard bank statement processing: {str(e)}")
