from dataclasses import dataclass
from ChaOS_constants import CMD_SHORTS, UI_2_PATH_TRANSLATIONS
from file import translate_ui_2_path


@dataclass
class Cmd:
    cmd: str = None
    pri_arg: str = None
    sec_arg: str = None
    ter_arg: str = None
    flags: dict = None
    perm_arg: str = None

    def interpret(self, cmd_split: list):
        try:
            self.cmd = cmd_split[0]
        except IndexError:
            print('You must enter a valid command to interact with the system. ')
        try:
            self.pri_arg = cmd_split[1]
            self.sec_arg = cmd_split[2]
            self.ter_arg = cmd_split[3]
            self.flags = cmd_split[4]
            self.perm_arg = cmd_split[-1]
        except IndexError:
            pass

    def compile(self):
        if self.cmd in CMD_SHORTS.keys():   # compile the command from keyword to cmd
            self.cmd = CMD_SHORTS[self.cmd]

        for attr, value in self.__dict__.items():
            if value and (not value.startswith('--') and '/' in value):   # loop over all attributes and if they're
                # not a builtin and are a path, translate them
                self.__dict__[attr] = translate_ui_2_path(value)




