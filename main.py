from logging import exception
import boto3
from boto3.dynamodb.conditions import Key, Attr


def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def load_table(db):
    try:
        table = dynamodb.Table(db)
        return table
    except Exception as e:
        print(e)


def put_item(table, name, ip, os):
    try:
        table.put_item(
            Item={
                'name': name,
                'ip': ip,
                'os': os,
            }
        )
    except Exception as e:
        print(e)


def get_item(table, name, ip):
    try:
        response = table.get_item(
            Key={
                'name': name,
                'ip': ip,
            }
        )
        item = response['Item']
        print(item)
    except Exception as e:
        print(e)


def search_by_ip(table, ip):
    try:
        response = table.scan(
            FilterExpression=Attr('ip').eq(ip)
        )
        items = response['Items']
        print(items)
    except Exception as e:
        print(e)


def search_by_hostname(table, name):
    try:
        response = table.scan(
            FilterExpression=Attr('name').eq(name)
        )
        items = response['Items']
        return items
    except Exception as e:
        print(e)


def delete_item_by_hostname(table, name):
    try:
        items = search_by_hostname(table, name)
        table.delete_item(
            Key={
                'ip': items[0]['ip'],
                'name': items[0]['name'],
            }
        )
    except Exception as e:
        print(e)


menu_options = {
    1: 'Get Item',
    2: 'Put Item',
    3: 'Search By IP',
    4: 'Search By Hostname',
    5: 'Delete Item By Hostname',
    6: 'Exit',
}


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('hosts')
    while (True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
            db = input("Please type the name of the table:\n")
            table = load_table(db)
            name = input("Please type the name of the server:\n")
            ip = input("Please type the IP of the server:\n")
            get_item(table, name, ip)
            print('\n')
        elif option == 2:
            db = input("Please type the name of the table:\n")
            table = load_table(db)
            name = input("Please type the name of the server:\n")
            ip = input("Please type the IP of the server:\n")
            os = input("Please type the OS of the server:\n")
            put_item(table, name, ip, os)
            print('\n')
        elif option == 3:
            db = input("Please type the name of the table:\n")
            table = load_table(db)
            ip = input("Please type the IP of the server:\n")
            search_by_ip(table, ip)
            print('\n')
        elif option == 4:
            db = input("Please type the name of the table:\n")
            table = load_table(db)
            name = input("Please type the name of the server:\n")
            server = search_by_hostname(table, name)
            print(server)
            print('\n')
        elif option == 5:
            db = input("Please type the name of the table:\n")
            table = load_table(db)
            name = input("Please type the name of the server:\n")
            delete_item_by_hostname(table, name)
            print('\n')
        elif option == 6:
            print('Bye...')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 6.')
