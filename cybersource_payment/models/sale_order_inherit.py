from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import json
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_capture_in_cybersource(self):
        self.ensure_one()
        payment_provider = self.env['payment.provider'].search([('code', '=', 'cybersource')], limit=1)
        if not payment_provider:
            raise UserError(_("Cybersource payment provider is not configured."))

        payload = {
            "clientReferenceInformation": {
                "code": self.name
            },
            "processingInformation": {
                "capture": True
            },
            "orderInformation": {
                "amountDetails": {
                    "totalAmount": self.amount_total,
                    "currency": self.currency_id.name
                },
                "billTo": {
                    "firstName": self.partner_id.name,
                    "lastName": self.partner_id.name,
                    "address1": self.partner_id.street,
                    "locality": self.partner_id.city,
                    "administrativeArea": self.partner_id.state_id.code,
                    "postalCode": self.partner_id.zip,
                    "country": self.partner_id.country_id.code,
                    "email": self.partner_id.email
                }
            },
            "paymentInformation": {
                "card": {
                    "number": "4111111111111111",
                    "expirationMonth": "12",
                    "expirationYear": "2031",
                    "securityCode": "123"
                }
            }
        }

        try:
            response = payment_provider.make_payment_request(payload)
            print(response)
            if response.get('status') == 'AUTHORIZED':
                self.action_confirm()
                if self.state=='to_approve':
                    self.approve_order()
                invoice = self._create_invoices()  # Create the invoice
                if invoice:
                    invoice.action_post()  # Post the invoice

                self.env['payment.transaction'].create({
                    'reference':self.name,
                    'amount': self.amount_total,
                    'currency_id': self.currency_id.id,
                    'provider_id': payment_provider.id,
                    'reference': self.name,
                    'partner_id': self.partner_id.id,
                    'state': 'done',
                    'payment_method_id':payment_provider.id,
                })
            else:
                raise ValidationError(_("Payment failed: %s" % response.get('message', '')))
        except Exception as e:
            raise ValidationError(_("Payment failed: %s" % str(e)))