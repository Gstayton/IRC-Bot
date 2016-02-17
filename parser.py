from inspect import getmembers, isfunction, getdoc
from enum import Enum
from decimal import *
import random

import utilities


class Payload:
    def __init__(self, payloadType, response, target=None, status=0):
        self.__dict__.update({
            'Type': payloadType,
            'Response': response,
            'Target': target,
            'Status': status
        })
        self.status = status
        self.payloadType = payloadType
        self.response = response
        self.target = target


class PayloadType(Enum):
    CHAT_MESSAGE = 'chatmsg'
    SYS_MESSAGE  = 'sysmsg'
    NONE         = 'none'


class Commands():
    @staticmethod
    async def convert(cmd, args):
        "Usage: {cmdChar}convert [float][f/c]"
        tokens = args.split(' ')
        if tokens[0][-1:] == 'f':
            temp = str(round((float(tokens[0][:-1]) - 32) / 1.8, 1)) + 'c'
        elif tokens[0][-1:] == 'c':
            temp = str(round((float(tokens[0][:-1]) * 1.8) + 32, 1)) + 'f'

        return Payload(
            PayloadType.CHAT_MESSAGE,
            tokens[0] + ' = ' + temp
        )

    @staticmethod
    async def reload(cmd, args):
        "Reload command parser module"
        return Payload(
            PayloadType.SYS_MESSAGE,
            'reload'
            )

    @staticmethod
    async def roll(cmd, args):
        "Roll the dice!\n {cmdChar}roll [number]d[sides]"
        if not args:
            return Payload(
                PayloadType.CHAT_MESSAGE,
                "No arguments, try {} [number]d[sides]".format(Chat.cmdChar)
            )
        roll = args.replace(" ", "")
        num, sides = roll.partition('d')[::2]
        try:
            num = int(float(num))
            sides = Decimal(sides)
        except:
            return Payload(
                PayloadType.CHAT_MESSAGE,
                "Malformed request, try {}help roll".format(Chat.cmdChar)
            )
        if (sides > 1) and (sides <= 9999) and (num >= 1) and (num <= 9999):
            result = round(
                sum(random.uniform(
                    1/(1 * (10 ** sides.as_tuple().exponent)),
                    float(sides)) for die in range(num)
                    ),
                abs(sides.as_tuple().exponent)
            )
            if result.is_integer():
                result = int(result)
        else:
            result = "Invalid request, try {}help roll".format(Chat.cmdChar)
        return Payload(
            PayloadType.CHAT_MESSAGE,
            str(result)
        )

    @staticmethod
    async def about(cmd, args):
        "General information about this bot"
        message = "A bot for IRC written in Python by Nathan Thomas (AKA Kosan Nicholas)\n"
        message += "Source available at http://github.com/Gstayton/WABot\n"
        message += "Current version: 0.1.0"

        return Payload(
            PayloadType.CHAT_MESSAGE,
            message
            )

    @staticmethod
    async def ping(cmd, args):
        "Check alive status of bot"
        print("Pinged")
        return Payload(
            PayloadType.CHAT_MESSAGE,
            "pong {0}".format(args)
            )

    @staticmethod
    async def ud_define(cmd, args):
        """
        {cmdChar}ud_define [search term]
        Returns the first result from urbandictionary.com for [search term],
        truncated to 300 characters or less
        """
        define = await utilities.Urban.search(args, 300)
        return Payload(
            PayloadType.CHAT_MESSAGE,
            define
            )

    @staticmethod
    async def help(cmd, args):
        "Display available commands"
        func_list = [o for o in getmembers(Commands) if isfunction(o[1])]
        helpText = ""
        if args:
            if " " in args:
                helpText = "Invalid search"
            else:
                for f in func_list:
                    if args.lower() == f[0] and getdoc(f[1]):
                        helpText = "Usage for {0}{1}: \n".format(Chat.cmdChar, args)
                        helpText += getdoc(f[1]).format(cmdChar=Chat.cmdChar)
                if not helpText:
                    helpText = "No help available for '{0}'".format(args)
        else:
            helpText = "Currently implemented commands: \n"
            for f in func_list:
                helpText += Chat.cmdChar + f[0] + ", "

            helpText += "\nFor more info, try {0}help [command]".format(Chat.cmdChar)

        return Payload(
            PayloadType.CHAT_MESSAGE,
            helpText
            )


class Chat():
    cmdChar = "."

    def __init__(self):
        self.commands = {}

        func_list = [o for o in getmembers(Commands) if isfunction(o[1])]

        for func in func_list:
            self.commands[func[0]] = func[1]

    def parse(self, msg, target, invoker):
        if msg[0] != self.cmdChar:
            return Payload(
                1,
                PayloadType.NONE,
                None
                )
        if " " in msg:
            cmd = msg[1:msg.find(" ")]
            args = msg[msg.find(" ") + 1:]
        else:
            cmd = msg[1:]
            args = ""
        print("COMMAND : " + cmd)
        if cmd in self.commands:
            return self.commands[cmd](cmd, args)
        else:
            return Payload(
                    1,
                    PayloadType.NONE,
                    None
                    )
