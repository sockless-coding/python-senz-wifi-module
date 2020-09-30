import argparse
import senzwifi

from enum import Enum

def main():
    parser = argparse.ArgumentParser(
        description='Read or change status of Senz-Wifi devices')

    parser.add_argument(
        'username',
        help='Username for Senz-Wifi')

    parser.add_argument(
        'password',
        help='Password for Senz-Wifi')

    parser.add_argument(
        '-r', '--raw',
        help='Raw dump of response',
        type=str2bool, nargs='?', const=True,
        default=False)

    commandparser = parser.add_subparsers(
        help='commands',
        dest='command')

    commandparser.add_parser(
        'list',
        help="Get a list of all devices")

    get_parser = commandparser.add_parser(
        'get',
        help="Get status of a device")

    get_parser.add_argument(
        dest='device',
        type=int,
        help='Device number #')

    args = parser.parse_args()

    session = senzwifi.Session(args.username, args.password, raw=args.raw)
    session.login()
    try:
        if args.command == 'list':
            print("list of devices and its device id (1-x)")
            for idx, device in enumerate(session.get_devices()):
                if(idx > 0):
                    print('')

                print("device #{}".format(idx + 1))
                print_result(device, 4)
        
        if args.command == 'get':
            if int(args.device) <= 0 or int(args.device) > len(session.get_devices()):
                raise Exception("device not found, acceptable device id is from {} to {}".format(1, len(session.get_devices())))

            device = session.get_devices()[int(args.device) - 1]
            print("reading from device '{}' ({})".format(device['name'], device['serial']))

            print_result( session.get_device(device['serial']) )

    except senzwifi.ResponseError as ex:
        print(ex.text)

def print_result(obj, indent = 0):
    for key in obj:
        value = obj[key]

        if isinstance(value, dict):
            print(" "*indent + key)
            print_result(value, indent + 4)
        elif isinstance(value, Enum):
            print(" "*indent + "{0: <{width}}: {1}".format(key, value.name, width=25-indent))
        elif isinstance(value, list):
            print(" "*indent + "{0: <{width}}:".format(key, width=25-indent))
            for elt in value:
                print_result(elt, indent + 4)
                print("")
        else:
            print(" "*indent + "{0: <{width}}: {1}".format(key, value, width=25-indent))

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')