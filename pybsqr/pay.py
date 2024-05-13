from lxml import objectify

from .base import BySquare


class PayBySquare(BySquare):

    def xml_to_fields(self, xml=None) -> list[str]:
        if xml is None:
            xml = self.xml

        fields = []

        fields.append(xml.findtext("{*}InvoiceID", ""))
        # Payments count
        find = objectify.ObjectPath("Pay.Payments")
        fields.append(str(find(xml).countchildren()))
        # Iterate over payments
        for payment in find(xml).iterchildren():
            find = objectify.ObjectPath("Payment.PaymentOptions")
            payment_option = find(payment).text
            fields.append(
                str(
                    {"paymentorder": 1, "standingorder": 2, "directdebit": 4}[
                        payment_option
                    ]
                )
            )
            fields.append(payment.findtext("{*}Amount"))
            fields.append(payment.findtext("{*}CurrencyCode"))
            fields.append(payment.findtext("{*}PaymentDueDate").replace("-", ""))
            fields.append(payment.findtext("{*}VariableSymbol", ""))
            fields.append(payment.findtext("{*}ConstantSymbol", ""))
            fields.append(payment.findtext("{*}SpecificSymbol", ""))
            fields.append(payment.findtext("{*}OriginatorsReferenceInformation", ""))
            fields.append(payment.findtext("{*}PaymentNote", ""))

            bank_accounts = payment.find("{*}BankAccounts")
            # Bank accounts count
            fields.append(str(bank_accounts.countchildren()))
            # Iterate over bank accounts
            for account in bank_accounts.iterchildren():
                fields.append(account.findtext("{*}IBAN"))
                fields.append(account.findtext("{*}BIC", ""))

            fields.extend(
                ["0", "0"]
            )  # TODO: implement StandingOrderExt and DirectDebitExt
            fields.append(payment.findtext("{*}BeneficiaryName", ""))
            fields.append(payment.findtext("{*}BeneficiaryAddressLine1", ""))
            fields.append(payment.findtext("{*}BeneficiaryAddressLine2", ""))

        self._fields = fields

        return fields

    def generate_code(self, fields: list[str] | None = None):
        if fields is None:
            fields = self.fields

        code = self._generate_code(fields, 0x00)

        self._code = code
        return code

    def generate_qr(self, code: str | None = None, frame: bool = True, format="PNG"):
        if code is None:
            code = self.code
        frame_name = "pay_by_square_frame" if frame else None
        return self._generate_qr(code, frame_name, format)
