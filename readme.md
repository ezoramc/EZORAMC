How to create a minecraft java + bedrock server in github
- Create a repository in github 
- Create a codespace on that repository
- Download these essential files
- PAPER MC (https://papermc.io/downloads/all?project=paper)
- Via Backwards (https://modrinth.com/plugin/viabackwards)
- Via Version (https://modrinth.com/plugin/viaversion)
- Playit plugin (optional for java players who want to join without tailscale) (https://playit.gg/download/plugins)
- Geyser MC (https://geysermc.org/download)
- Floodgate (https://geysermc.org/download)
- Paste your paper download in Codespace's file manager
- Type (nano start) in your terminal 
- Paste (java -Xmx8G -Xms8G -jar server.jar nogui) then press ctrl+o, then enter and then ctrl+x, you can also edit it according to your need e.g. (java -Xmx12G -Xms12G -jar server.jar nogui) for 12gb ram server
 - download tailscale (for java + bedrock connection) 
 - by typing (curl -fsSL https://tailscale.com/install.sh | sh) in your terminal
 - then type (sudo tailscale up) to start tailscale
 - if it shows error then type (sudo tailscaled &)
 - inside it type (sudo tailscale up) and press enter
 - after that a link will apper, hover your mouse on it and press ctrl+click (left click of your mouse)
 - Login with the account of your choice which you are comfortable in sharing with others 
 - after logging in, either take your ip from tailscale admin console (wil appear in front of codespace) and or just type (tailscale ip) in your terminal
 - Then type bash start in your terminal
 - It will auto stop after 30-40 seconds and generate some files and folders in your codespace's file manager
 -Click on the file named eula.txt. Inside it change (eula=false) to (eula=true)
 - Then paste floodgate, geysermc, via version, via backwards and playit into your plugins folder
- After that type bash start (to start the server) in your terminal
- A link will appear, ctrl+click on it. It will take you to playit's login page. After logging in it will assign your server's tunnel to an agent. After assigning it will also give you the ip to join your server and will also show it in your github's terminal. it will be something like "xyz.joinmc.link". Share this ip with java players who do not want to download tailscale but it will not work for Bedrock players. After setting playit up come back to your codespace
- The terminal is being used as minecraft's admin panel so create another terminal by clicking the plus icon (right side to ports in terminal) or just press ctrl+shift+C
- In this new terminal, type (tailscale status) in your terminal to check if tailscale is running or not. If it shows your devices, it's running
- If you are in linux, download tailscale the same way you did it in terminal and (use tailscale up) in your PC's terminal to turn on tailscale and connect to your minecraft server, Use (sudo tailscale down) to disable it
- To connect to the server in bedrock, install tailscale app, login with the account which has github codespace's machine, then turn on tailscale, go to minecraft, go to server, click on add server, paste the ip (get it from the app itself (the ip showing on the right side of your codespace's machine) or just type (taliscale ip) in the terminal), the default port of geyser mc is (19132) but it's configurable
- Make sure your friends are using same tailscale account as you and tailscale is on in all devices
- You have to enable tailscale manually in the terminal by typing (sudo tailscale &) everytime you start the terminal




Additional Note - Tailscale is a DNS which also can be used to access links that don't work in your device or region e.g. DONKEY.TO
