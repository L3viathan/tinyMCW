#TinyMCW

*lightweight wurstminebot alternative*

# What?

[Wurstminebot](https://github.com/wurstmineberg/wurstminebot) (and now [systemd-minecraft](https://github.com/wurstmineberg/systemd-minecraft)) is a tool primarily invented to sync IRC with ingame Minecraft chat, but later expanded to additional functionality, such as world and backup management, among lots of other stuff. It is also tightly connected with the [Wurstmineberg API](https://github.com/wurstmineberg/api.wurstmineberg.de), which is really neat, too. These tools are great, but primarily designed for our custom setup, and really not feasible to deploy in 5 minutes on a new server. This is an attempt to write a lightweight alternative that allows some of their functionality, while still being quick to deploy and easy to manage.

# Installation

This wrapper script requires Python3 and pexpect (installable through pip), nothing else, and can be set up in 1 minute: The only other requirement is that the Minecraft server jar file is called `minecraft_server.jar`. To start the server, simply run the Python script.

# Usage

Out of the box it does almost nothing, but it will be easily extensible through hooks. As a demonstration, the following additional functionality comes out of the box:

- Greeting every new player and saying goodbye
- When the second player joins, they are teleported to the first player
- The `!ping` command, to which the server will reply with "pong"
- `!sethome`, `!home`, and `!delhome`, implemented with armorstands

At the moment, all commands can be run by everyone, but that will change in the near future.
