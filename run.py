import argparse
from core import core

if __name__ == '__main__':
    parser.add_argument('-o', '--output_type')
    args = parser.parse_args()
    output_type = args.output_type
    if output_type == 'h' or output_type == 'hotkey':
        from hotkeyModule import hotkeyModule
        output_module = hotkeyModule
    elif output_type == 'o' or output_type == 'obs':
        from obsModule import obsModule
        output_module = obsModule
    elif output_type == 'w' or output_type == 'windowOutput':
        from windowModule import windowModule
        output_module = windowModule
    else:
        print("output argument -o must be either hotkey(\'h\'), obs(\'o\'), or window(\'w\')")
        quit()

    coreObj = core(output_module)
    coreObj.run()

        
