import n26.api as api
import click
import datetime
from tabulate import tabulate

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# Cli returns command line requests
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Interact with the https://n26.com API via the command line."""


@cli.command()
def info():
    """ Get account information """
    account_info = api.Api()
    print('Account info:')
    print('-------------')
    # TODO: make it python2 compatible using unicode
    print('Name: ' + str(account_info.get_account_info()['firstName'] + ' ' +
                         account_info.get_account_info()['lastName']))
    print('Email: ' + account_info.get_account_info()['email'])
    print('Nationality: ' + account_info.get_account_info()['nationality'])
    print('Phone: ' + account_info.get_account_info()['mobilePhoneNumber'])


@cli.command()
def balance():
    """ Show account balance """
    balance = api.Api()
    print('Current balance:')
    print('----------------')
    print(str(balance.get_balance()['availableBalance']))


@cli.command()
# @click.option('--all', default=False, help='Blocks all n26 cards.')
def card_block():
    """ Blocks the card. """
    card = api.Api()
    for i in card.get_cards():
        card_id = i['id']
        card.block_card(card_id)
        print('Blocked card: ' + card_id)


@cli.command()
def card_unblock():
    """ Unblocks the card. """
    card = api.Api()
    for i in card.get_cards():
        card_id = i['id']
        card.unblock_card(card_id)
        print('Unblocked card: ' + card_id)


@cli.command()
def limits():
    """ Show n26 account limits  """
    limits = api.Api()
    print(limits.get_account_limits())


@cli.command()
def contacts():
    """ Show your n26 contacts  """
    contacts = api.Api()
    print('Contacts:')
    print('---------')
    print(contacts.get_contacts())


@cli.command()
def statements():
    """ Show your n26 statements  """
    statements = api.Api()
    print('Statements:')
    print('-----------')
    print(statements.get_statements())


@cli.command()
@click.option('--limit', default=20, help='Limit transaction output.')
def transactions(limit):
    """ Show transactions (default: 20) """
    transactions = api.Api()
    output = transactions.get_transactions_limited(str(limit))
    print('Transactions:')
    print('-------------')
    li = []
    for i, val in enumerate(output):
        li.append([
            str(val.get('amount')),
            insertNewlines(val.get('merchantName', val.get('partnerName')), 30),
            insertNewlines(val.get('referenceText'), 100),
            datetime.datetime.fromtimestamp(val.get('confirmed', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')
        ])

    # Tabulate
    table = li
    headers = ['amount', 'partner/merchant', 'reference-text', 'confirmed']
    print(tabulate(table, headers, tablefmt='simple', numalign='right', floatfmt=".2f"))


def insertNewlines(text, lineLength):
    if text is None or not len(text):
        return
    if len(text) <= lineLength:
        return text
    else:
        return text[:lineLength] + '\n' + insertNewlines(text[lineLength:], lineLength)



if __name__ == '__main__':
    cli()
