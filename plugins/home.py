def home(command, args, player, mc):
        if command == "sethome":
            mc.send('/kill @e[type=ArmorStand,name={}-home]'.format(player))
            mc.send('/summon ArmorStand 0 100 0 {{Invisible:1, Marker:1, CustomName:"{}-home"}}'.format(player))
            mc.send('/tp @e[type=ArmorStand,name={}-home] {}'.format(player, player))
            return
        if command == "home":
            mc.send('/tp {} @e[type=ArmorStand,name={}-home]'.format(player, player))
            return
        if command == "delhome":
            mc.send('/kill @e[type=ArmorStand,name={}-home]'.format(player, player))
            return

_hooks = {'command':home}
