import pexpect
import re
import sys
from time import sleep
from glob import glob
from collections import defaultdict
from importlib import import_module
linere = re.compile(r"\[(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})\] \[(?P<thread>[^/]+)\/(?P<level>\w+)\]: (?P<message>.*)")
chatre = re.compile(r"<(?P<player>\w+)> (?P<message>.*)")
sayre = re.compile(r"\[\w+\] (?P<message>.*)")
joinleftre = re.compile(r"(?P<player>\w+) (?P<change>joined|left) the game")

hooks = defaultdict(list)

for plugin in glob("plugins/*.py"):
    print("Module found:",plugin, file=sys.stderr)
    p = import_module(plugin.replace("/",".").replace(".py",""))
    for hook in p._hooks:
        hooks[hook].append(p._hooks[hook])

class Minecraft():
    '''Global State Object.'''
    def __init__(self, filename="minecraft_server.jar"):
        self.proc = pexpect.spawn("java -jar {}".format(filename))
        self.players = set()
    def send(self, message):
        print(">",message,file=sys.stderr)
        self.proc.sendline(message)

mc = Minecraft()

def handle(line, mc):
    '''Handles line, calls hooks, etc.'''
    match = linere.match(line)
    if match:
        fields = match.groupdict()
        for hook in hooks.get('all',()):
            hook(fields=fields, mc=mc)
        print("<",fields['message'],file=sys.stderr)

        match = chatre.match(fields['message'])
        if match:
            chat = match.groupdict()
            if chat['message'][0] == "!":
                for hook in hooks.get('command',()):
                    command = chat['message'][1:].split()
                    hook(command=command[0], args=command[1:], player=chat['player'], mc=mc)
            else:
                for hook in hooks.get('chat',()):
                    hook(message=chat['message'], player=chat['player'], mc=mc)

        match = sayre.match(fields['message'])
        if match:
            say = match.groupdict()
            for hook in hooks.get('say',()):
                hook(message=say['message'], mc=mc)

        match = joinleftre.match(fields['message'])
        if match:
            joinleft = match.groupdict()
            if joinleft['change'] == "joined":
                for hook in hooks.get('join',()):
                    hook(player=joinleft['player'], mc=mc)
                mc.players.add(joinleft['player'])
            else:
                for hook in hooks.get('leave',()):
                    hook(player=joinleft['player'], mc=mc)
                mc.players.remove(joinleft['player'])

while True:
    try:
        mc.proc.expect("^.*\r\n", timeout=5)
        handle(mc.proc.after.decode(), mc=mc)
    except pexpect.TIMEOUT:
        pass
    except pexpect.EOF:
        break
