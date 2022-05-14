import os.path

import requests, time, json, ntpath


class Controller:
    def __init__(self, file_path):
        self.file_path = file_path
        self.channels = []
        self.load_percentage = 0
        self.auth = ""
        self.previous_delete = False

    # Loads parameter file into the program, returns the channel object:
    # [{guild_name: GU_NAME, channel_id: ID, channel_name: CH_NAME, last_message: MSG_ID}, ...]
    def load_file(self):
        try:
            file_auth = open("./auth.txt", "r+", encoding="utf-8")
            self.auth = file_auth.readline().replace("\n", "")
            if len(self.auth) < 1 or self.auth.startswith("#"):
                print("""It seems you have not properly configured your auth.txt. Please check the github page for
                instructions on how to get it! {LINK} """)
            file_auth.close()
            file = open(self.file_path, "r+", encoding="utf-8")
            lines = file.readlines()
            increase = 100/len(lines)
            for line in lines:
                if len(line) < 2:
                    continue
                if line.count(';') == 3:  # This means it has other properties like the channel and guild names
                    x = line.replace("\n", "").split(';')
                    if x[1] == "":
                        continue
                    if x[0] == "" or x[2] == "":
                        y = self.request_channel_info(x[1])
                    else:
                        y = {
                            "guild_name": x[0],
                            "channel_id": x[1],
                            "channel_name": x[2],
                            "last_message": ""
                            }
                    # If x > 3 There's a previous message saved, include it in the object and ask to delete later
                    if len(x) > 3 and len(x[3]) > 1:
                        self.previous_delete = True
                        y["last_message"] = x[3]
                else:  # otherwise, perform an internal request for the channel and guild name
                    y = self.request_channel_info(line.replace("\n", ""))
                self.channels.append(y)
                self.load_percentage = self.load_percentage + increase
            file.close()
            self.save_file()
        except OSError:
            print("""ERROR IN LOADING FILE ! Check to see if you followed all the required parameters and
            that the auth.txt contains your discord authentication code!""")
    
    # Main sending function, very important
    def send_message(self, attachment_paths, message, delay, spoiler, legacy, save_msg_ids):
        print(legacy)
        self.previous_delete = save_msg_ids
        if attachment_paths:
            ret = self.send_message_attachments(
                attachment_paths,
                self.channels[0],
                message,
                spoiler,
                save_msg_ids)
            if ret and not legacy:
                message = message + "\n" + "\n".join(ret)
        self.load_percentage = 0
        increase = 100/len(self.channels)
        for i in range(len(self.channels)):
            if i == 0 and attachment_paths:
                continue
            if delay > 0:
                time.sleep(delay)
            if not legacy:
                self.send_message_text_only(message, self.channels[i], save_msg_ids)
            else:
                self.send_message_attachments(
                    attachment_paths,
                    self.channels[i],
                    message,
                    spoiler,
                    save_msg_ids)
            self.load_percentage += increase
        self.save_file()

    def send_message_attachments(self, attachment_paths, channel, message, spoiler, save_msg_ids):
        url = "https://discordapp.com/api/v9/channels/" + channel["channel_id"] + "/messages"
        ret = []
        f = {}
        for i in range(len(attachment_paths)):
            if attachment_paths[i] == "":
                continue
            try:
                temp = open(attachment_paths[i], "rb")
                name = ntpath.basename(temp.name)
                if spoiler:
                    name = "SPOILER_" + name
                if name in f:
                    # This is to avoid duplicate keys in case the files have the same name
                    name, extension = os.path.splitext(name)
                    name = name + str(i) + extension
                    print(name)
                f[name] = temp.read()
            except OSError:
                print("Something went wrong while attempting to open the attachment!")
                return [], ""
        data = {"payload_json": json.dumps({"content": message, "tts": False})}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Authorization": self.auth
            }
        x = requests.post(url, headers=headers, data=data, files=f)
        resp = json.loads(x.text)
        if "channel_id" in resp.keys():
            print("Sent successfully to channel \"{}\" in the server \"{}\"!".format(
                channel["channel_name"], channel["guild_name"]
                ))
            for attach in resp["attachments"]:
                if spoiler:

                    # Weird note: Apparently the only way for an embed to appear in a spoilered
                    # link is if there's a space between the pipes and the link
                    # Also I wasted about 2 hours trying to figure out a way to circunvent
                    # this and all I had to do was add two spaces. Pain.
                    # Thank you reddit user ShesJustAGlitch for the solution.
                    # Stackoverflow is overrated

                    ret.append("|| {} ||".format(attach["url"]))
                else:
                    ret.append(attach["url"])
            if save_msg_ids:
                channel["last_message"] = resp["id"]
            return ret
        else:
            print(x.text)
            return ""

    def send_message_text_only(self, message, channel, save_msg_ids):
        url = "https://discordapp.com/api/v9/channels/" + channel["channel_id"] + "/messages"

        headers = {"authorization": self.auth, "content-type": "application/x-www-form-urlencoded"}

        x = requests.post(url, headers=headers, data={"content": message, "tts": False})

        resp = json.loads(x.text)
        if "channel_id" in resp.keys():
            print("Sent successfully to channel \"{}\" in the server \"{}\"!".format(
                channel["channel_name"], channel["guild_name"]
                ))
            if save_msg_ids:
                channel["last_message"] = resp["id"]
        else:
            print(x.text)
    
    # Saves the {FILE}_gen version of input
    def save_file(self):
        if not self.file_path.endswith("_gen.txt"):
            name, extension = os.path.splitext(self.file_path)
            self.file_path = name + "_gen" + extension
        write = ""
        for i in self.channels:
            temp = "{};{};{};{}".format(
                i["guild_name"],
                i["channel_id"],
                i["channel_name"],
                i["last_message"]
                )
            write = write + temp + "\n"
        try:
            file = open(self.file_path, "w+", encoding="utf-8")
            file.write(write)
            file.close()
            print("New file successfully saved! Use [FILENAME]_gen next time you open the program.")
        except OSError:
            print("Error in opening/saving file!")
    
    # Loops to delete all messages that have an id
    def delete_message_all(self):
        self.load_percentage = 0
        increase = 100 / len(self.channels)
        for i in self.channels:
            time.sleep(1)  # Safety delay to avoid getting rate limited
            if i["last_message"] != "":
                self.delete_message_one(i["last_message"], i["channel_id"])
                i["last_message"] = ""
            self.load_percentage += increase
        print("All previous messages successfully deleted!")

    # delete_message(discord_auth_code, message_id_to_be_deleted) -> None
    def delete_message_one(self, message_id, channel_id):
        print(message_id)
        url = "https://discord.com/api/v9/channels/{}/messages/{}".format(channel_id, message_id)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Authorization": self.auth
            }
        x = requests.delete(url, headers=headers)
        print(x.text)
    
    # INTERNALS
    
    def request_channel_info(self, channel_id):
        ret = {"guild_name": "", "channel_id": channel_id, "channel_name": "", "last_message": ""}
        url = "https://discord.com/api/v9/channels/" + channel_id
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Authorization": self.auth
            }
        x = requests.get(url, headers=headers)
        j = json.loads(x.text)
        if 'name' in j: # GET successful, save channel name and guild id
            ret["channel_name"] = j["name"]
            url = "https://discord.com/api/v9/guilds/" + j["guild_id"]
            x = requests.get(url, headers=headers)
            j = json.loads(x.text)
            if 'name' in j:
                ret["guild_name"] = j["name"]
        return ret