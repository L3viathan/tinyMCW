def cond_tp(player, mc):
    if len(mc.players) == 1:
        old = list(players)[0]
        mc.send("tp {} {}".format(player, old))

_hooks = {'join':cond_tp}
