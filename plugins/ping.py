def pong(command, args, player, mc):
    if command == "ping":
        mc.send("say Pong!")

_hooks = {'command':pong}
