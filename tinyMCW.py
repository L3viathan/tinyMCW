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

class Minecraft():
    '''Global State Object.'''
    def __init__(self, filename="minecraft_server.jar"):
        self.proc = pexpect.spawn("java -jar {}".format(filename))
        self.players = set()
        self._hooks = defaultdict(list)
        self.load_plugins()
    def load_plugins(self):
        for plugin in glob("plugins/*.py"):
            print("Loading plugin",plugin, file=sys.stderr)
            p = import_module(plugin.replace("/",".").replace(".py",""))
            for hook in p._hooks:
                self._hooks[hook].append(p._hooks[hook])
    def call_hooks(self, hookid, **kwargs):
        for hook in self._hooks.get(hookid,()):
            hook(mc=self, **kwargs)
    def send(self, message):
        print(">",message,file=sys.stderr)
        self.proc.sendline(message)

mc = Minecraft()

def handle(line, mc):
    '''Handles line, calls hooks, etc.'''
    match = linere.match(line)
    if match:
        fields = match.groupdict()
        mc.call_hooks('all',fields=fields)
        print("<",fields['message'],file=sys.stderr)

        match = chatre.match(fields['message'])
        if match:
            chat = match.groupdict()
            if chat['message'][0] == "!":
                command = chat['message'][1:].split()
                mc.call_hooks('command',command=command[0], args=command[1:], player=chat['player'])
            else:
                mc.call_hooks('chat',message=chat['message'], player=chat['player'])

        match = sayre.match(fields['message'])
        if match:
            say = match.groupdict()
            mc.call_hooks('say',message=say['message'])

        match = joinleftre.match(fields['message'])
        if match:
            joinleft = match.groupdict()
            if joinleft['change'] == "joined":
                mc.call_hooks('join',player=joinleft['player'])
                mc.players.add(joinleft['player'])
            else:
                mc.call_hooks('leave',player=joinleft['player'])
                mc.players.remove(joinleft['player'])

while True:
    try:
        mc.proc.expect("^.*\r\n", timeout=5)
        handle(mc.proc.after.decode(), mc=mc)
    except pexpect.TIMEOUT:
        pass
    except pexpect.EOF:
        break
