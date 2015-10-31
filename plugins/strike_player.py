def strike_player(command, args, player, mc):
    if command == "strike":
        if len(args) > 0:
            print("Summoning lightning bolt at {}".format(args[0]))
            mc.send("execute {} ~ ~ ~ summon LightningBolt".format(args[0]))

_hooks = {'command':strike_player}
