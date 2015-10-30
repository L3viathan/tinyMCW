import pexpect
import re
import sys
from time import sleep

mc = pexpect.spawn("java -jar minecraft_server.jar")

linere = re.compile(r"\[(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})\] \[(?P<thread>[^/]+)\/(?P<level>\w+)\]: (?P<message>.*)")
chatre = re.compile(r"<(?P<player>\w+)> (?P<message>.*)")
sayre = re.compile(r"\[\w+\] (?P<message>.*)")
joinleftre = re.compile(r"(?P<player>\w+) (?P<change>joined|left) the game")

players = set()

def send(command, mc):
    print("> {}".format(command),file=sys.stderr)
    mc.sendline(command)

def handle_chat(message, player, fields, mc):
    if message[0] == "!":
        if message[1:] == "ping":
            send("say pong",mc=mc)
            return
        if message[1:] == "sethome":
            send('/kill @e[type=ArmorStand,name={}-home]'.format(player),mc=mc)
            send('/summon ArmorStand 0 100 0 {{Invisible:1, Marker:1, CustomName:"{}-home"}}'.format(player),mc=mc)
            send('/tp @e[type=ArmorStand,name={}-home] {}'.format(player, player),mc=mc)
            return
        if message[1:] == "home":
            send('/tp {} @e[type=ArmorStand,name={}-home]'.format(player, player),mc=mc)
            return
        if message[1:] == "delhome":
            send('/kill @e[type=ArmorStand,name={}-home]'.format(player, player),mc=mc)
            return

def handle_say(message, fields, mc):
    pass

def handle_join(player, fields, mc):
    if len(players) == 1:
        old = list(players)[0]
        send("tp {} {}".format(player, old),mc=mc)
    players.add(player)
    send("say Hello, {}!".format(player),mc=mc)

def handle_leave(player, fields, mc):
    players.remove(player)
    send("say Goodbye, {}!".format(player),mc=mc)

def handle(line, mc):
    '''Handles line, calls hooks, etc.'''
    match = linere.match(line)
    if match:
        fields = match.groupdict()
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
