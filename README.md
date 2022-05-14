# DOPPELGANGER - DISCORD SELF-POSTING BOT
<p align="center">
  <img src="https://i.imgur.com/WdIPCoj.png">
</p>

----

### CURRENT VERSION: BETA 1.0

#### Created by Berahthraben

WARNING: DISCORD HAS SPECIFIC TERMS STATING THAT SELF-BOTS ARE FORBIDDEN. ALTHOUGH THERE'S DEFENSIVE MEASURES IN THE PROGRAM I DO NOT TAKE RESPONSBILITY FOR BANS THAT MIGHT OCCUR IF YOU ABUSE THIS.

## Quick guide links

[HOW TO USE THIS](https://github.com/Berahthraben/Doppelganger#how-to-use-it)

[HOW TO ENABLE DEVELOPER MODE](https://github.com/Berahthraben/Doppelganger#how-to-get-your-discord-authorization)

[HOW TO GET YOUR DISCORD AUTHENTICATION](https://github.com/Berahthraben/Doppelganger#how-to-get-your-discord-authorization)

[TIPS](https://github.com/Berahthraben/Doppelganger#how-to-get-your-discord-authorization)

[LICENSE](https://github.com/Berahthraben/Doppelganger#license)

# How to use it

1. Download the project from this link and extract it anywhere: [[DOWNLOAD]](https://github.com/Berahthraben/Doppelganger/archive/refs/heads/master.zip)

2. Make sure you have [Python3.10](https://www.python.org/downloads/) installed. In future version the program will come pre-packaged with a dist.

3. Install the requirements by running ```INSTALL REQUIREMENTS.bat``` . Alternatively if you're an advanced user, open a command window on the folder that contains the ```requirements.txt``` file and run
    - ```pip install ./requirements.txt```

4. Make sure you have [DEVELOPER MODE ENABLED](https://www.howtogeek.com/714348/how-to-enable-or-disable-developer-mode-on-discord/) on discord.

5. Find your Discord Authorization code (tutorial on that further down)

![Auth code](https://i.imgur.com/EC4avVp.png)

    - WARNING: THIS CODE CAN GIVE ANYONE FULL ACCESS TO YOUR DISCORD ACCOUNT. **NEVER** SHARE IT.

6. Copy the code inside the file called ```auth.txt``` . Make sure there's nothing else inside the file aside from the code itself. You only need to do this once.

![Auth.txt](https://i.imgur.com/XEro6K0.png)

7. Copy the IDs of every channel you wish the messages to be sent one (Right click > Copy ID)

![Copy ID](https://i.imgur.com/4myt3hi.png)

8. Place each code in a straight line inside any text file. A dummy file called ```example.txt``` was included to help.

![example.txt](https://i.imgur.com/M1YeoP4.png)

9. Run the program by draggin this newly created text file to ```DRAG FILE HERE.bat```

![drag file](https://i.imgur.com/Qy4etWn.png)

10. If everything worked correctly the program should now start. It will now check each ID and create a new file called ```X_gen.txt```, where X is the name of the original file you dragged onto the program. The next time you open the program use the generated file so it's faster.

![First opening](https://i.imgur.com/JoV7otO.png)

11. Now you're on the main screen! From here you should have everything figured out, but here's a quick explanation of what every major thing does:
    - **INCLUDE ATTACHMENTS**: Enables the attachment bar so you can include files/images
    - **SAFETY DELAY**: Enable this to make the program wait 2 - 3 seconds in-between each message so discord doesn't rate-limit you
    - **SAVE MESSAGE IDS**: Enable this to save the sent messages IDs. The next time you send messages the program will prompt you to delete previous messages. This is useful if you are advertising something that you don't want to spam (like a Twitch stream!).
    - **SPOILER IMAGES**: Spoilers any attachments that are images.
    - **LEGACY MODE**: The way the program works is that it'll send the image to the very first channel listed, and then send a link to the image to all other channels. This is so that uploading/sending is faster. However, if you wish to upload all attachments each time enable this checkmark.
    - **PLUS BUTTON (+)**: Adds another bar to the attachments so you can send multiple files in one message!
    - **SEND MESSAGE**: Start sending the messages!

12. Enjoy!

## How to get your Discord Authorization

1. Start by logging into Discord in your favorite browser (https://discordapp.com/)

2. Press Ctrl + Shift + E to open the Network developer tab.

![Network](https://i.imgur.com/uf4jsVb.png)

3. Send a message in any channel. A bunch of new lines should popup. On the "filter URLs" field type in "messages". If everything went correctly you should see one line that has only "messages" on it's "File" Column.
![messages](https://i.imgur.com/9b24wKN.png)

4. Click on it. On the rightmost part you should see a tab named "headers" and a "Filter Headers" textfield. Type "Authorization" on it. A field should pop up with your authorization code! It should look similar to the image (it's unique to every user).

![Authorizationcomplete](https://i.imgur.com/R31Q784.png)

    - **WARNING: *DO NOT* SHARE THIS CODE WITH *ANYONE* UNLESS YOU WANT TO GET YOUR DISCORD ACCOUNT COMPROMISED**

5. There you go! Now include that code in the auth.txt file so the program works correctly!

## Some tips!

- You can still add IDs to ```X_gen.txt``` files! Just place the ID in any new line and the program will process them automatically the next time you open up.
- It's highly recommended to keep both the safety delay and save message ids checkboxes enabled. The first one to prevent being rate-limited and the second in case you misstyped something and wish to repost.
- You can resend a message or do a completely different one without re-starting the program! However to change the target channels you'll need to restart with the appropriate file as parameter.
- The program cannot be stopped unless forcibly closed after the "Send Message" button has been clicked. Make sure everything is correct before doing it and wait for it to finish to use the delete feature!

## LICENSE

Code is literally open-source and fully UNtrademarked. Anyone with google and way too much time in their hands can do this shit. Literally just use this for whatever you want!