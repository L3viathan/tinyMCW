def hello(player, mc):
    mc.sendline("Hello, {}!".format(player))

def goodbye(player, mc):
    mc.sendline("Goodbye {} :(".format(player))

_hooks = {"join":hello, "leave":goodbye}
