import pexpect
import re
import sys
from time import sleep
from glob import glob
from collections import defaultdict
from importlib import import_module

mc = pexpect.spawn("java -jar minecraft_server.jar")

hooks = defaultdict(list)

for plugin in glob("plugins/*.py"):
    print("Module found:",plugin, file=sys.stderr)
    p = import_module(plugin.replace("/",".").replace(".py",""))
    for hook in p._hooks:
        hooks[hook].append(p._hooks[hook])

linere = re.compile(r"\[(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})\] \[(?P<thread>[^/]+)\/(?P<level>\w+)\]: (?P<message>.*)")
chatre = re.compile(r"<(?P<player>\w+)> (?P<message>.*)")
sayre = re.compile(r"\[\w+\] (?P<message>.*)")
joinleftre = re.compile(r"(?P<player>\w+) (?P<change>joined|left) the game")

players = set()

def send(command, mc):
    print("> {}".format(command),file=sys.stderr)
    mc.sendline(command)

def handle_chat(message, player, fields, mc):
    for hook in hooks.get('chat',()):
        hook(message=message, player=player, mc=mc)
    if message[0] == "!":
        for hook in hooks.get('command',()):
            command = message[1:].split()
            hook(command=command[0], args=command[1:], player=player, mc=mc)

def handle_say(message, fields, mc):
    for hook in hooks.get('say',()):
        hook(message=message, mc=mc)

def handle_join(player, fields, mc):
    for hook in hooks.get('join',()):
        hook(player=player, mc=mc)
    '''For the following functionality, we will probably need some global object which everyone gets (instead of mc).
    We can then have extensible ".send()" methods, etc., and some global properties accessible to plugins.'''
    if len(players) == 1:
        old = list(players)[0]
        send("tp {} {}".format(player, old),mc=mc)
    players.add(player)

def handle_leave(player, fields, mc):
    for hook in hooks.get('leave',()):
        hook(player=player, mc=mc)
    players.remove(player)

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
            return handle_chat(message=chat['message'].strip(), player=chat['player'], fields=fields, mc=mc)

        match = sayre.match(fields['message'])
        if match:
            say = match.groupdict()
            return handle_say(message=say['message'], fields=fields, mc=mc)

        match = joinleftre.match(fields['message'])
        if match:
            joinleft = match.groupdict()
            if joinleft['change'] == "joined":
                return handle_join(player=joinleft['player'], fields=fields, mc=mc)
            else:
                return handle_leave(player=joinleft['player'], fields=fields, mc=mc)

while True:
    try:
        mc.expect("^.*\r\n", timeout=5)
        handle(mc.after.decode(), mc=mc)
    except pexpect.TIMEOUT:
        pass
    except pexpect.EOF:
        break
