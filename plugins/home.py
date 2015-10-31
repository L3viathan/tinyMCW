def home(command, args, player, mc):
        if command == "sethome":
            mc.sendline('/kill @e[type=ArmorStand,name={}-home]'.format(player))
            mc.sendline('/summon ArmorStand 0 100 0 {{Invisible:1, Marker:1, CustomName:"{}-home"}}'.format(player))
            mc.sendline('/tp @e[type=ArmorStand,name={}-home] {}'.format(player, player))
            return
        if command == "home":
            mc.sendline('/tp {} @e[type=ArmorStand,name={}-home]'.format(player, player))
            return
        if command == "delhome":
            mc.sendline('/kill @e[type=ArmorStand,name={}-home]'.format(player, player))
            return

_hooks = {'command':home}
