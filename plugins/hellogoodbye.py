def hello(player, mc):
    mc.send("Hello, {}!".format(player))

def goodbye(player, mc):
    mc.send("Goodbye {} :(".format(player))

_hooks = {"join":hello, "leave":goodbye}
