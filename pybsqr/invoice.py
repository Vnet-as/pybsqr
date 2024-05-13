from lxml import objectify

from .base import BySquare


class InvoiceBySquare(BySquare):

    def xml_to_fields(self, xml=None) -> list[str]:
        if xml is None:
            xml = self.xml

        fields = []

        fields.append(xml.findtext("{*}InvoiceID", ""))
        fields.append(xml.findtext("{*}IssueDate").replace("-", ""))
        fields.append(xml.findtext("{*}TaxPointDate", "").replace("-", ""))
        fields.append(xml.findtext("{*}OrderID", ""))
        fields.append(xml.findtext("{*}DeliveryNoteID", ""))
        fields.append(xml.findtext("{*}LocalCurrencyCode"))

        fields.append(xml.findtext("{*}ForeignCurrencyCode", ""))
        fields.append(xml.findtext("{*}CurrRate", ""))
        fields.append(xml.findtext("{*}ReferenceCurrRate", ""))

        supplier_party = xml.find("{*}SupplierParty")
        fields.append(supplier_party.findtext("{*}PartyName"))
        fields.append(supplier_party.findtext("{*}CompanyTaxID", ""))
        fields.append(supplier_party.findtext("{*}CompanyVATID", ""))
        fields.append(supplier_party.findtext("{*}CompanyRegisterID", ""))

        supplier_postal_address = supplier_party.find("{*}PostalAddress")
        fields.append(supplier_postal_address.findtext("{*}StreetName"))
        fields.append(supplier_postal_address.findtext("{*}BuildingNumber", ""))
        fields.append(supplier_postal_address.findtext("{*}CityName"))
        fields.append(supplier_postal_address.findtext("{*}PostalZone"))
        fields.append(supplier_postal_address.findtext("{*}State", ""))
        fields.append(supplier_postal_address.findtext("{*}Country"))

        supplier_contact = supplier_party.find("{*}Contact")
        fields.append(supplier_contact.findtext("{*}Name", ""))
        fields.append(supplier_contact.findtext("{*}Telephone", ""))
        fields.append(supplier_contact.findtext("{*}EMail", ""))

        customer_party = xml.find("{*}CustomerParty")
        fields.append(customer_party.findtext("{*}PartyName"))
        fields.append(customer_party.findtext("{*}CompanyTaxID", ""))
        fields.append(customer_party.findtext("{*}CompanyVATID", ""))
        fields.append(customer_party.findtext("{*}CompanyRegisterID", ""))
        fields.append(customer_party.findtext("{*}PartyIdentification", ""))

        fields.append(xml.findtext("{*}NumberOfInvoiceLines", ""))
        fields.append(xml.findtext("{*}InvoiceDescription", ""))

        if xml.findtext("{*}NumberOfInvoiceLines", "") == "":
            invoice_line = xml.find("{*}SingleInvoiceLine")
            fields.append(invoice_line.findtext("{*}OrderLineID", ""))
            fields.append(invoice_line.findtext("{*}DeliveryNoteLineID", ""))
            fields.append(invoice_line.findtext("{*}ItemName", ""))
            fields.append(invoice_line.findtext("{*}ItemEANCode", ""))
            fields.append(
                invoice_line.findtext("{*}PeriodFromDate", "").replace("-", "")
            )
            fields.append(invoice_line.findtext("{*}PeriodToDate", "").replace("-", ""))
            fields.append(invoice_line.findtext("{*}InvoicedQuantity"))
        else:
            fields.extend([""] * 7)

        tax_summaries = xml.find("{*}TaxCategorySummaries")
        fields.append(str(tax_summaries.countchildren()))
        for summary in tax_summaries.iterchildren():
            fields.append(summary.findtext("{*}ClassifiedTaxCategory"))
            fields.append(summary.findtext("{*}TaxExclusiveAmount"))
            fields.append(summary.findtext("{*}TaxAmount"))
            fields.append(summary.findtext("{*}AlreadyClaimedTaxExclusiveAmount"))
            fields.append(summary.findtext("{*}AlreadyClaimedTaxAmount"))

        monetary_summary = xml.find("{*}MonetarySummary")
        fields.append(monetary_summary.findtext("{*}PayableRoundingAmount"))
        fields.append(monetary_summary.findtext("{*}PaidDepositsAmount"))

        self._fields = fields

        return fields

    def generate_code(self, fields: list[str] | None = None):
        if fields is None:
            fields = self.fields

        code = self._generate_code(fields, 0x10)

        self._code = code
        return code

    def generate_qr(self, code: str | None = None, frame: bool = False, format="PNG"):
        if code is None:
            code = self.code
        frame_name = "invoice_by_square_frame" if frame else None
        return self._generate_qr(code, frame_name, format)
