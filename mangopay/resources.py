from .base import BaseApiModel

from .fields import (PrimaryKeyField, EmailField, CharField,
                     BooleanField, DateTimeField, DateField,
                     IntegerField, ManyToManyField,
                     ForeignKeyField, AmountField, OneToOneField)

from .utils import Choices
from .query import InsertQuery, UpdateQuery, SelectQuery


class BaseModel(BaseApiModel):
    id = PrimaryKeyField(api_name='ID')
    tag = CharField(api_name='Tag')
    creation_date = DateTimeField(api_name='CreationDate')
    update_date = DateTimeField(api_name='UpdateDate')


class User(BaseModel):
    TYPE_CHOICES = Choices(
        ('NATURAL_PERSON', 'natural', 'Natural person'),
        ('LEGAL_PERSONALITY', 'legal', 'Legal personality')
    )

    password = CharField(api_name='Password', required=True)
    email = EmailField(api_name='Email', required=True)
    first_name = CharField(api_name='FirstName', required=True)
    last_name = CharField(api_name='LastName', required=True)
    has_register_mean_of_payment = BooleanField(api_name='HasRegisterMeanOfPayment')
    can_register_mean_of_payment = BooleanField(api_name='CanRegisterMeanOfPayment')
    ip_address = CharField(api_name='IP', required=True)
    birthday = DateField(api_name='Birthday')
    nationality = CharField(api_name='Nationality', required=True)
    type = CharField(api_name='PersonType', required=True,
                     choices=TYPE_CHOICES, default=TYPE_CHOICES.natural)
    personal_wallet_amount = AmountField(api_name='PersonalWalletAmount')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class Beneficiary(BaseModel):
    user = ForeignKeyField(User, api_name='UserID', required=True,
                           related_name='beneficiaries')
    bank_account_owner_name = CharField(api_name='BankAccountOwnerName', required=True)
    bank_account_owner_address = CharField(api_name='BankAccountOwnerAddress', required=True)
    bank_account_iban = CharField(api_name='BankAccountIBAN', required=True)
    bank_account_bic = CharField(api_name='BankAccountBIC', required=True)

    class Meta:
        verbose_name = 'beneficiary'
        verbose_name_plural = 'beneficiaries'


class Wallet(BaseModel):
    users = ManyToManyField(User, api_name='Owners', related_name='wallets')
    name = CharField(api_name='Name', required=True)

    description = CharField(api_name='Description', required=True)
    raising_goal_amount = AmountField(api_name='RaisingGoalAmount', required=True)
    collected_amount = AmountField(api_name='CollectedAmount')
    spent_amount = AmountField(api_name='SpentAmount')
    amount = AmountField(api_name='Amount')
    contribution_limit_date = DateTimeField(api_name='ContributionLimitDate')

    # is_closed = BooleanField(api_name='IsClosed')
    # expiration_date = DateTimeField(api_name='ExpirationDate', required=True)
    # remaining_amount = AmountField(api_name='RemainingAmount')

    class Meta:
        verbose_name = 'wallet'
        verbose_name_plural = 'wallets'

    def __str__(self):
        return self.name


class PaymentCard(BaseApiModel):
    id = PrimaryKeyField(api_name='ID')
    tag = CharField(api_name='Tag', required=True)
    owner = ForeignKeyField(User, api_name='OwnerID', required=True,
                            related_name='payment_cards')
    card_number = CharField(api_name='CardNumber', required=True)
    redirect_url = CharField(api_name='RedirectURL')
    template_url = CharField(api_name='TemplateURL')
    return_url = CharField(api_name='ReturnURL', required=True)
    culture = CharField(api_name='Culture')
    # payment_url = CharField(api_name='PaymentURL')

    class Meta:
        verbose_name = 'card'
        verbose_name_plural = 'cards'


class Contribution(BaseModel):
    user = ForeignKeyField(User, api_name='UserID', required=True,
                           related_name='contributions')
    wallet = ForeignKeyField(Wallet, api_name='WalletID', required=True,
                             related_name='contributions')
    amount = AmountField(api_name='Amount', required=True)
    client_fee_amount = AmountField(api_name='ClientFeeAmount')
    is_succeeded = BooleanField(api_name='IsSucceeded')
    is_completed = BooleanField(api_name='IsCompleted')
    payment_url = CharField(api_name='PaymentURL')
    template_url = CharField(api_name='TemplateURL')
    return_url = CharField(api_name='ReturnURL', required=True)
    register_mean_of_payment = BooleanField(api_name='RegisterMeanOfPayment')
    error = CharField(api_name='Error')
    payment_card = ForeignKeyField(PaymentCard, api_name='PaymentCardID')
    culture = CharField(api_name='Culture')
    type = CharField(api_name='Type')  # type of transaction: payline, ogone
    payment_method = CharField(api_name='PaymentMethodType')
    answer_code = CharField(api_name='AnswerCode')
    answer_message = CharField(api_name='AnswerMessage')
    # leetchi_fee_amount = AmountField(api_name='LeetchiFeeAmount')

    class Meta:
        verbose_name = 'contribution'
        verbose_name_plural = 'contributions'

    def __str__(self):
        return self.amount

    def is_success(self):
        return self.is_succeeded and self.is_completed


# TODO: ImmediateContribution RecurrentContribution


class WithdrawalContribution(BaseModel):
    user = ForeignKeyField(User, api_name='UserID', required=True,
                           related_name='withdrawal_contributions')
    wallet = ForeignKeyField(Wallet, api_name='WalletID',
                             related_name='withdrawal_contributions')
    amount_declared = AmountField(api_name='AmountDeclared', required=True)
    status = CharField(api_name='Status')
    amount = AmountField(api_name='Amount')
    generated_reference = CharField(api_name='GeneratedReference')
    commentary = CharField(api_name='Commentary')
    bank_account_owner = CharField(api_name='BankAccountOwner', required=True)
    bank_account_iban = CharField(api_name='BankAccountIBAN', required=True)
    bank_account_bic = CharField(api_name='BankAccountBIC', required=True)

    class Meta:
        verbose_name = 'contributions-by-withdrawal'
        verbose_name_plural = 'contributions-by-withdrawal'


class Withdrawal(BaseModel):
    user = ForeignKeyField(User, api_name='UserID', required=True,
                           related_name='withdrawals')
    wallet = ForeignKeyField(Wallet, api_name='WalletID', required=True,
                             related_name='withdrawals')
    amount = AmountField(api_name='Amount', required=True)
    amount_without_fees = AmountField(api_name='AmountWithoutFees')
    client_fee_amount = AmountField(api_name='ClientFeeAmount')
    is_completed = BooleanField(api_name='IsCompleted')
    is_succeeded = BooleanField(api_name='IsSucceeded')
    beneficiary = ForeignKeyField(Beneficiary, required=True, api_name='BeneficiaryID')
    error = CharField(api_name='Error')

    # leetchi_fee_amount = AmountField(api_name='LeetchiFeeAmount')
    # bank_account_owner_name = CharField(api_name='BankAccountOwnerName')
    # bank_account_owner_address = CharField(api_name='BankAccountOwnerAddress')
    # bank_account_iban = CharField(api_name='BankAccountIBAN')
    # bank_account_bic = CharField(api_name='BankAccountBIC')

    class Meta:
        verbose_name = 'withdrawal'
        verbose_name_plural = 'withdrawals'


class Transfer(BaseModel):
    payer = ForeignKeyField(User, api_name='PayerID', required=True)
    beneficiary = ForeignKeyField(User, api_name='BeneficiaryID', required=True)

    amount = AmountField(api_name='Amount', required=True)
    client_fee_amount = AmountField(api_name='ClientFeeAmount')

    payer_wallet = ForeignKeyField(Wallet,
                                   api_name='PayerWalletID',
                                   related_name='payer_transfers',
                                   required=True)
    beneficiary_wallet = ForeignKeyField(Wallet,
                                         api_name='BeneficiaryWalletID',
                                         required=True,
                                         related_name='beneficiary_transfers_set')

    class Meta:
        verbose_name = 'transfer'
        verbose_name_plural = 'transfers'

    def __str__(self):
        return self.payer

# class TransferRefund(BaseModel):
#     user = ForeignKeyField(User,
#                            api_name='UserID',
#                            required=True,
#                            related_name='transfer_refunds')
#     transfer = ForeignKeyField(Transfer,
#                                api_name='TransferID',
#                                required=True,
#                                related_name='transfer_refunds')
#
#     class Meta:
#         verbose_name = 'transfer-refund'
#         verbose_name_plural = 'transfer-refunds'


class Refund(BaseModel):
    user = ForeignKeyField(User, api_name='UserID', required=True,
                           related_name='refunds')
    contribution = ForeignKeyField(Contribution,
                                   api_name='ContributionID',
                                   required=True,
                                   related_name='refunds')

    is_succeeded = BooleanField(api_name='IsSucceeded')
    is_completed = BooleanField(api_name='IsCompleted')

    error = CharField(api_name='Error')

    class Meta:
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'

    def is_success(self):
        return self.is_succeeded and self.is_completed


class StrongAuthentication(BaseModel):
    user = OneToOneField(User, api_name='UserID',
                         required=True,
                         related_name='strong_authentication')
    beneficiary = ForeignKeyField(Beneficiary, api_name='BeneficiaryID')
    url_request = CharField(api_name='UrlRequest')
    is_transmitted = BooleanField(api_name='IsDocumentsTransmitted')
    is_completed = BooleanField(api_name='IsCompleted')
    is_succeeded = BooleanField(api_name='IsSucceeded')
    message = CharField(api_name='Message')

    class Meta:
        verbose_name = 'strongAuthentication'
        verbose_name_plural = 'strongAuthentication'

        urls = {
            InsertQuery.identifier: lambda params: '/users/%s/strongAuthentication' % params['user_id'],
            UpdateQuery.identifier: lambda params, reference: '/users/%s/strongAuthentication' % params['user_id']
        }


class Operation(BaseModel):
    user = ForeignKeyField(User, api_name='UserID', required=True,
                           related_name='operations')
    wallet = ForeignKeyField(Wallet, api_name='WalletID', required=True,
                             related_name='operations')
    amount = AmountField(api_name='Amount', required=True)

    transaction_type = CharField(api_name='TransactionType')
    transaction_id = IntegerField(api_name='TransactionID')

    class Meta:
        verbose_name = 'operation'
        verbose_name_plural = 'operations'
