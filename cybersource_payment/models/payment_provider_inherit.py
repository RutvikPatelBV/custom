import json
import logging
import hashlib
import hmac
import base64
from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
import requests
import pytz

_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('cybersource', "Cybersource")], ondelete={'cybersource': 'set default'})
    cybersource_merchant_id = fields.Char(
        string="Merchant ID",
        help="The merchant ID to use with this provider",
        required_if_provider='cybersource', groups='base.group_system')
    cybersource_api_key_id = fields.Char(
        string="API Key ID", help="The API key ID for the Cybersource account", required_if_provider='cybersource',
        groups='base.group_system')
    cybersource_secret_key = fields.Char(
        string="Secret Key", help="The secret key for the Cybersource account",
        required_if_provider='cybersource', password=True, groups='base.group_system')

    def make_payment_request(self, payload):
        utc_now = datetime.now(pytz.UTC)
        time = utc_now.strftime('%a, %d %b %Y %H:%M:%S GMT')

        payload_bytes = json.dumps(payload).encode('utf-8')
        digest = self.get_digest(payload_bytes)
        signature = self.get_signature('POST', time, digest)

        headers = {
            "host": "apitest.cybersource.com",
            "signature": signature,
            "digest": digest,
            "v-c-merchant-id": self.cybersource_merchant_id,
            "date": time,
            "Content-Type": "application/json"
        }

        request_target = 'https://apitest.cybersource.com/pts/v2/payments'

        try:
            response = requests.post(request_target, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def get_signature(self, method, time, digest):
        secret_key = self.cybersource_secret_key
        merchant_id = self.cybersource_merchant_id
        key_id = self.cybersource_api_key_id

        resource = '/pts/v2/payments'
        request_host = 'apitest.cybersource.com'
        header_list = []

        header_list.append(f'keyid="{key_id}"')
        header_list.append('algorithm="HmacSHA256"')
        postheaders = "host date request-target digest v-c-merchant-id"
        header_list.append(f'headers="{postheaders}"')

        signature_list = [
            f'host: {request_host}\n',
            f'date: {time}\n',
            f'request-target: {method.lower()} {resource}\n',
            f'digest: {digest}\n',
            f'v-c-merchant-id: {merchant_id}'
        ]

        sig_value = ''.join(signature_list)
        secret = base64.b64decode(secret_key)
        hash_value = hmac.new(secret, sig_value.encode('utf-8'), hashlib.sha256)
        signature = base64.b64encode(hash_value.digest()).decode('utf-8')

        header_list.append(f'signature="{signature}"')
        token = ', '.join(header_list)
        return token

    @staticmethod
    def get_digest(payload):
        hashobj = hashlib.sha256()
        hashobj.update(payload)
        hash_data = hashobj.digest()
        digest = base64.b64encode(hash_data).decode('utf-8')
        return f'SHA-256={digest}'


