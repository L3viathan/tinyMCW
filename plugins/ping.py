def pong(command, args, player, mc):
    if command == "ping":
        mc.sendline("say Pong!")

_hooks = {'command':pong}
