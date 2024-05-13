from datetime import date
from decimal import Decimal
from enum import Enum

from lxml import etree, objectify

from .invoice import InvoiceBySquare
from .pay import PayBySquare
from .xml import makeparser


NS_MAP = {
    None: "http://www.bysquare.com/bysquare",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class PaymentType(Enum):
    PAYMENTORDER = "paymentorder"
    STANDINGORDER = "standingorder"
    DIRECTDEBIT = "directdebit"


class PaymentMean(Enum):
    MONEYTRANSFER = "moneyTransfer"
    CASH = "cash"
    COD = "cashOnDelivery"
    CREDITCARD = "creditCard"
    ADVANCE = "advance"
    MUTUALOFFSET = "mutualOffset"
    OTHER = "other"


def create_pay_by_square(
    *,
    invoice_number: int | str = "",
    payment_types: list[PaymentType] | None = None,
    amount: str | Decimal,
    currency_code: str = "EUR",
    payment_due_date: str | date,
    variable_symbol: str = "",
    constant_symbol: str = "",
    specific_symbol: str = "",
    originator_reference: str = "",
    payment_note: str = "",
    bank_account_iban: str,
    bank_account_bic: str = "",
    beneficiary_name: str = "",
    beneficiary_address_line1: str = "",
    beneficiary_address_line2: str = "",
) -> PayBySquare:
    xml = etree.Element(
        "Pay",
        attrib={"{http://www.w3.org/2001/XMLSchema-instance}type": "Pay"},
        nsmap=NS_MAP,
    )
    etree.SubElement(xml, "InvoiceID").text = invoice_number
    payments = etree.SubElement(xml, "Payments")
    payment = etree.SubElement(payments, "Payment")
    etree.SubElement(payment, "PaymentOptions").text = " ".join(
        map(lambda pt: pt.value, payment_types or [PaymentType.PAYMENTORDER])
    )
    etree.SubElement(payment, "Amount").text = str(amount)
    etree.SubElement(payment, "CurrencyCode").text = currency_code
    etree.SubElement(payment, "PaymentDueDate").text = (
        payment_due_date.isoformat()
        if isinstance(payment_due_date, date)
        else payment_due_date
    )
    if variable_symbol or constant_symbol or specific_symbol:
        etree.SubElement(payment, "VariableSymbol").text = variable_symbol
        etree.SubElement(payment, "ConstantSymbol").text = constant_symbol
        etree.SubElement(payment, "SpecificSymbol").text = specific_symbol
    else:
        etree.SubElement(payment, "OriginatorsReferenceInformation").text = (
            originator_reference
        )
    etree.SubElement(payment, "PaymentNote").text = payment_note
    accounts = etree.SubElement(payment, "BankAccounts")
    account = etree.SubElement(accounts, "BankAccount")
    etree.SubElement(account, "IBAN").text = bank_account_iban
    etree.SubElement(account, "BIC").text = bank_account_bic
    # etree.SubElement(payment, 'StandingOrderExt')
    # etree.SubElement(payment, 'DirectDebitEx
    etree.SubElement(payment, "BeneficiaryName").text = beneficiary_name
    etree.SubElement(payment, "BeneficiaryAddressLine1").text = (
        beneficiary_address_line1
    )
    etree.SubElement(payment, "BeneficiaryAddressLine2").text = (
        beneficiary_address_line2
    )

    xml_str = etree.tostring(xml)
    parser = makeparser()
    return PayBySquare(objectify.fromstring(xml_str, parser))


def create_invoice_by_square(
    *,
    invoice_number: str,
    issue_date: str | date,
    tax_date: str | date,
    currency_code: str = "EUR",
    supplier_name: str,
    supplier_ico: str = "",
    supplier_dic: str = "",
    supplier_icdph: str = "",
    supplier_street: str,
    supplier_street_number: str = "",
    supplier_city: str,
    supplier_zip: str,
    supplier_state: str = "",
    supplier_country: str = "SVK",
    supplier_contact_name: str = "",
    supplier_contact_phone: str = "",
    supplier_contact_email: str = "",
    customer_name: str,
    customer_ico: str = "",
    customer_dic: str = "",
    customer_icdph: str = "",
    invoice_item_count: int,
    invoice_description: str = "",
    invoice_item_text: str = "",
    invoice_item_quantity: int = 1,
    invoice_item_order_line_id: str = "",
    invoice_item_delivery_note_line_id: str = "",
    invoice_item_ean_code: str = "",
    invoice_item_period_from: str | date = "",
    invoice_item_period_to: str | date = "",
    tax_summaries: list[dict],
    total_rounding_amount: str | Decimal = "0",
    total_deposit_amount: str | Decimal = "0",
    payment_means: list[PaymentMean] | None = None,
) -> InvoiceBySquare:
    xml = etree.Element(
        "Invoice",
        attrib={"{http://www.w3.org/2001/XMLSchema-instance}type": "Invoice"},
        nsmap=NS_MAP,
    )

    etree.SubElement(xml, "InvoiceID").text = invoice_number
    etree.SubElement(xml, "IssueDate").text = (
        issue_date.isoformat() if isinstance(issue_date, date) else issue_date
    )
    etree.SubElement(xml, "TaxPointDate").text = (
        tax_date.isoformat() if isinstance(tax_date, date) else tax_date
    )
    etree.SubElement(xml, "LocalCurrencyCode").text = currency_code

    supplier = etree.SubElement(xml, "SupplierParty")
    etree.SubElement(supplier, "PartyName").text = supplier_name
    etree.SubElement(supplier, "CompanyTaxID").text = supplier_dic
    etree.SubElement(supplier, "CompanyVATID").text = supplier_icdph
    etree.SubElement(supplier, "CompanyRegisterID").text = supplier_ico

    postal_address = etree.SubElement(supplier, "PostalAddress")
    etree.SubElement(postal_address, "StreetName").text = supplier_street
    etree.SubElement(postal_address, "BuildingNumber").text = supplier_street_number
    etree.SubElement(postal_address, "CityName").text = supplier_city
    etree.SubElement(postal_address, "PostalZone").text = supplier_zip
    etree.SubElement(postal_address, "State").text = supplier_state
    etree.SubElement(postal_address, "Country").text = supplier_country

    contact = etree.SubElement(supplier, "Contact")
    etree.SubElement(contact, "Name").text = supplier_contact_name
    etree.SubElement(contact, "Telephone").text = supplier_contact_phone
    etree.SubElement(contact, "EMail").text = supplier_contact_email

    customer = etree.SubElement(xml, "CustomerParty")
    etree.SubElement(customer, "PartyName").text = customer_name
    etree.SubElement(customer, "CompanyTaxID").text = customer_dic
    etree.SubElement(customer, "CompanyVATID").text = customer_icdph
    etree.SubElement(customer, "CompanyRegisterID").text = customer_ico

    if not invoice_item_count:
        etree.SubElement(xml, "NumberOfInvoiceLines").text = "0"
    elif invoice_item_count > 1:
        etree.SubElement(xml, "NumberOfInvoiceLines").text = str(invoice_item_count)
        etree.SubElement(xml, "InvoiceDescription").text = invoice_description
    else:
        single_invoice = etree.SubElement(xml, "SingleInvoiceLine")
        etree.SubElement(single_invoice, "OrderLineID").text = (
            invoice_item_order_line_id
        )
        etree.SubElement(single_invoice, "DeliveryNoteLineID").text = (
            invoice_item_delivery_note_line_id
        )
        if invoice_item_text:
            etree.SubElement(single_invoice, "ItemName").text = invoice_item_text
        else:
            etree.SubElement(single_invoice, "ItemEANCode").text = invoice_item_ean_code
        if invoice_item_period_from and invoice_item_period_to:
            etree.SubElement(single_invoice, "PeriodFromDate").text = (
                invoice_item_period_from.isoformat
                if isinstance(invoice_item_period_from, date)
                else invoice_item_period_from
            )
            etree.SubElement(single_invoice, "PeriodToDate").text = (
                invoice_item_period_to.isoformat
                if isinstance(invoice_item_period_to, date)
                else invoice_item_period_to
            )
        etree.SubElement(single_invoice, "InvoicedQuantity").text = str(
            invoice_item_quantity
        )

    tax_cat_summaries = etree.SubElement(xml, "TaxCategorySummaries")

    for tax_category in tax_summaries:
        tax_cat_summary = etree.SubElement(tax_cat_summaries, "TaxCategorySummary")
        etree.SubElement(tax_cat_summary, "ClassifiedTaxCategory").text = str(
            tax_category["tax_category"]
        )
        etree.SubElement(tax_cat_summary, "TaxExclusiveAmount").text = str(
            tax_category["price_ex_vat"]
        )
        etree.SubElement(tax_cat_summary, "TaxAmount").text = str(
            tax_category["vat_amount"]
        )
        etree.SubElement(tax_cat_summary, "AlreadyClaimedTaxExclusiveAmount").text = (
            str(tax_category.get("deposit_price_ex_vat", 0))
        )
        etree.SubElement(tax_cat_summary, "AlreadyClaimedTaxAmount").text = str(
            tax_category.get("deposit_vat_amount", 0)
        )

    summary = etree.SubElement(xml, "MonetarySummary")
    etree.SubElement(summary, "PayableRoundingAmount").text = str(total_rounding_amount)
    etree.SubElement(summary, "PaidDepositsAmount").text = str(total_deposit_amount)

    etree.SubElement(xml, "PaymentMeans").text = " ".join(
        map(lambda pm: pm.value, payment_means or [PaymentMean.MONEYTRANSFER])
    )

    xml_str = etree.tostring(xml)
    parser = makeparser()
    return InvoiceBySquare(objectify.fromstring(xml_str, parser))
