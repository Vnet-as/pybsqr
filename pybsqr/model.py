from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic_xml import BaseXmlModel, RootXmlModel, element


NS_MAP = {
    "": "http://www.bysquare.com/bysquare",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class PaymentOption(Enum):
    paymentorder = "paymentorder"

    def __str__(self):
        return str(2 ** list(PaymentOption).index(self))


class BankAccount(BaseXmlModel, tag="BankAccount", nsmap=NS_MAP):
    iban: str = element(tag="IBAN")
    bic: str = element(tag="BIC", default="")


class BankAccounts(BaseXmlModel, tag="BankAccounts", nsmap=NS_MAP):
    bank_account: List[BankAccount]


class Payment(BaseXmlModel, tag="Payment", nsmap=NS_MAP):
    payment_options: PaymentOption = element(tag="PaymentOptions")
    amount: str = element(tag="Amount")
    currency_code: str = element(tag="CurrencyCode")
    payment_due_date: date = element(tag="PaymentDueDate")
    variable_symbol: str = element(tag="VariableSymbol")
    constang_symbol: str = element(tag="ConstantSymbol")
    specific_symbol: str = element(tag="SpecificSymbol")
    originators_reference_information: str = element(
        tag="OriginatorsReferenceInformation", default=""
    )
    payment_note: str = element(tag="PaymentNote")
    bank_accounts: BankAccounts
    beneficiary_name: str = element(tag="BeneficiaryName")
    beneficiary_address_line_1: str = element(tag="BeneficiaryAddressLine1")


class Payments(BaseXmlModel, tag="Payments", nsmap=NS_MAP):
    payment: list[Payment]


class Pay(BaseXmlModel, tag="Pay", nsmap=NS_MAP):
    invoice_id: str = element(tag="InvoiceID", default="")
    payments: Payments


class PostalAddress(BaseXmlModel, tag="PostalAddress", nsmap=NS_MAP):
    street_name: str = element(tag="StreetName")
    bulding_number: str = element(tag="BuildingNumber", default="")
    city_name: str = element(tag="CityName")
    postal_zone: str = element(tag="PostalZone")
    country: str = element(tag="Country")


class Contact(BaseXmlModel, tag="Contact", nsmap=NS_MAP):
    name: str = element(tag="Name", default="")
    telephone: str = element(tag="Telephone", default="")
    email: str = element(tag="EMail", default="")


class SupplierParty(BaseXmlModel, tag="SupplierParty", nsmap=NS_MAP):
    party_name: str = element(tag="PartyName")
    company_tax_id: str = element(tag="CompanyTaxID", default="")
    company_vat_id: str = element(tag="CompanyVATID", default="")
    company_register_id: str = element(tag="CompanyRegisterID", default="")
    postal_address: PostalAddress
    contact: Contact


class CustomerParty(BaseXmlModel, tag="CustomerParty", nsmap=NS_MAP):
    party_name: str = element(tag="PartyName")
    company_tax_id: str = element(tag="CompanyTaxID", default="")
    company_vat_id: str = element(tag="CompanyVATID", default="")
    company_register_id: str = element(tag="CompanyRegisterID", default="")
    party_identification: str = element(tag="PartyIdentification", default="")


class SingleInvoiceLine(BaseXmlModel, tag="SingleInvoiceLine", nsmap=NS_MAP):
    order_line_id: str = element(tag="OrderLineID", default="")
    delivery_note_line_id: str = element(tag="DeliveryNoteLineID", default="")
    item_name: str = element(tag="ItemName")
    invoiced_quantity: Decimal = element(tag="InvoicedQuantity")
    unit_price_tax_exclusive_amount: Decimal | str = element(
        tag="UnitPriceTaxExclusiveAmount", default=""
    )
    unit_price_tax_inclusive_amount: Decimal | str = element(
        tag="UnitPriceTaxInclusiveAmount", default=""
    )
    unit_price_tax_amount: Decimal | str = element(tag="UnitPriceTaxAmount", default="")


class TaxCategorySummary(BaseXmlModel, tag="TaxCategorySummary", nsmap=NS_MAP):
    classified_tax_category: Decimal = element(tag="ClassifiedTaxCategory")
    tax_exclusive_amount: Decimal = element(tag="TaxExclusiveAmount")
    tax_inclusive_amount: Decimal | str = element(tag="TaxInclusiveAmount", default="")
    tax_amount: Decimal = element(tag="TaxAmount")
    already_claimed_tax_exclusive_amount: Decimal = element(
        tag="AlreadyClaimedTaxExclusiveAmount"
    )
    already_claimed_tax_inclusive_amount: Decimal | str = element(
        tag="AlreadyClaimedTaxInclusiveAmount", default=""
    )
    already_claimed_tax_amount: Decimal = element(tag="AlreadyClaimedTaxAmount")
    difference_tax_exclusive_amount: Decimal | str = element(
        tag="DifferenceTaxExclusiveAmount", default=""
    )
    difference_tax_inclusive_amount: Decimal | str = element(
        tag="DifferenceTaxInclusiveAmount", default=""
    )
    difference_tax_amount: Decimal | str = element(
        tag="DifferenceTaxAmount", default=""
    )


class TaxCategorySummaries(BaseXmlModel, tag="TaxCategorySummaries", nsmap=NS_MAP):
    tax_category_summary: list[TaxCategorySummary]


class MonetarySummary(BaseXmlModel, tag="MonetarySummary", nsmap=NS_MAP):
    # tax_exclusive_amount: Decimal | str = element(tag='TaxExclusiveAmount', default='')
    # tax_inclusive_amount: Decimal | str = element(tag='TaxInclusiveAmount', default='')
    # tax_amount: Decimal | str = element(tag='TaxAmount', default='')
    payable_rounding_amount: Decimal = element(tag="PayableRoundingAmount")
    paid_deposits_amount: Decimal = element(tag="PaidDepositsAmount")
    # payable_amount: Decimal | str = element(tag='PayableAmount', default='')


class Invoice(BaseXmlModel, tag="Invoice", nsmap=NS_MAP):
    invoice_id: str = element(tag="InvoiceID", default="")
    issue_date: date = element(tag="IssueDate")
    tax_point_date: date = element(tag="TaxPointDate", default="")
    order_id: str = element(tag="OrderID", default="")
    delivery_note_id: str = element(tag="DeliverryNoteID", default="")
    local_currency_code: str = element(tag="LocalCurrencyCode")
    supplier_party: SupplierParty
    customer_party: CustomerParty
    # number_of_invoice_lines: Optional[int] = element(tag='NumberOfInvoiceLines')
    # invoice_description: Optional[str] = element(tag='InvoiceDescription')
    single_invoice_line: SingleInvoiceLine
    tax_category_summaries: TaxCategorySummaries
    monetary_summary: MonetarySummary
    payment_means: str = element(tag="PaymentMeans")


class BySquare(RootXmlModel):
    root: Pay | Invoice
