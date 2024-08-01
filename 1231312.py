from asyncio import sleep, run
from getpass import getpass
from json import load
from os import _exit
from re import search
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError, UserBannedInChannelError, FloodWaitError, ChatWriteForbiddenError
from datetime import datetime
import pytz
import requests
from colorama import init, Fore, Style

init(autoreset=True)

print(f"""````````````````_10000¶000081__``````````````````` 
`````````````__111__```````___11_````````````````` 
``````````_¶01111_111111111_11111009 _````````````` 
`````````1¶0801111_111111111_1111__1801``````````` 
````````09___1¶_1111111111111_111111_1801````````` 
```````¶1_____90_111 111111111111_1_111_100_``````` 
``````01_______01_11111111111111111______108_````` 
`````89_111____1¶_1111_1_1_11111111111111_¶¶¶8```` 
```` `01809008___¶9_1111_1_1_111_1111111_1_¶9_9¶``` 
````_8__```_101__¶_1111111_1_1_1_1_1_111_1¶___9¶`` 
````_¶1801____1__80_111_1_______1_11111_ _¶¶_1__01` 
````80¶¶¶¶¶9______09___1_10080111111_1___¶1_11110` 
``_01``¶¶099_______00__1081111¶_1_11111_0¶__1_1_0` 
_191_____________1118080 1_____¶1_11111__¶0__11__0_ 
¶________________111_____11__10_111_1__1¶9__1_1_0_ 
1191_1___________111111_1___90___1_111_9¶1_1_1110` 
``91``__ _________111111___100__1111111_1¶_11_1110` 
``0¶091___________11111180¶1_1_1_1_111_8¶______¶`` 
``_¶¶¶¶1__________11111_1_09_11_1_111_81_011 1101`` 
```¶¶¶____________1111___11¶1__1_1_1109``¶¶¶¶¶¶``` 
````9`____________111_____1_081__1980_```0¶880¶_`` 
````0____________1111______1 _189¶8_`````89`___1¶`` 
```_¶11_11111_111111_______11___0_``````¶_11__101` 
````_999199890911111________111_01`````10_1111_98` 
```````````` ``10111__________11_81`````18___1__10` 
```````````````011____________111¶`````09__1_1_10` 
```````````````19_______________101````98_1_1__1 0` 
````````````````¶________________1¶_```_0_1__1_09` 
````````````````01_________________01```1011`__¶_` 
````````````````_¶______________ ____90_``_¶¶¶¶¶9`` 
`````````````````09___________________0_``0¶¶¶¶_`` 
``````````````````01___________________¶_`101110`` 
```````````````` ``_0___________________10`8____0_` 
``````````````````10_1_111111111111111__1¶1__1_01` 
`````````````````_0111111_____________1_1¶1_1_108` 
` ````````````````__``_`_`````````````````01__1_81`""")
class Bot:
    def __init__(self, phone_number: str, api_id: int, api_hash: str, discord_webhook: str) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.discord_webhook = discord_webhook
        self.client = TelegramClient(self.phone_number, self.api_id, self.api_hash)
        self.status = True
        self.messages_delay = 10  # Задержка между сообщениями
        self.groups_delay = 1800  # Задержка между группами
        self.sent_messages_count = 0

    def get_moscow_time(self) -> str:
        return datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')

    def load_json_file(self, file_name: str) -> dict:
        try:
            with open(f'assets/{file_name}', 'r', encoding='utf-8') as file:
                return load(file)
        except FileNotFoundError:
            print(f"{Fore.RED}[{self.get_moscow_time()}] [-] Error: File {file_name} not found.")
            return {}
        except Exception as e:
            print(f"{Fore.RED}[{self.get_moscow_time()}] [-] Error: {type(e).__name__}: {str(e)}")
            return {}

    async def login(self) -> bool:
        try:
            await self.client.connect()
            if not await self.client.is_user_authorized():
                await self.client.send_code_request(self.phone_number)
                await self.client.sign_in(self.phone_number, input(f"{Fore.YELLOW}[{self.get_moscow_time()}] [?] Access code: "))
                if not await self.client.is_user_authorized():
                    print(f"{Fore.RED}[{self.get_moscow_time()}] [-] Login failed.")
                    return False
            return True
        except SessionPasswordNeededError:
            await self.client.sign_in(password=getpass(f"{Fore.YELLOW}[{self.get_moscow_time()} MSK] Password: "))
            return True
        except Exception as e:
            print(f"{Fore.RED}[{self.get_moscow_time()}] [-] Login failed due to {type(e).__name__}: {str(e)}")
            return False

    async def send_message(self, local_chat_id):
        local_chat_entity = await self.client.get_entity(local_chat_id)
        for message_id, channel_ids in self.data.get(local_chat_id, {}).items():
            text = await self.client.get_messages(local_chat_entity, ids=int(message_id))
            for channel_id in channel_ids:
                try:
                    match = search(r'https://t.me/[^/]+/(\d+)', channel_id)
                    if match:
                        channel_entity = await self.client.get_entity(channel_id.split('/' + match.group(1))[0])
                        await self.client.send_message(channel_entity, text, reply_to=int(match.group(1)))
                    else:
                        channel_entity = await self.client.get_entity(int(channel_id))
                        await self.client.send_message(channel_entity, text)
                    self.sent_messages_count += 1
                    print(f"{Fore.GREEN}[{self.get_moscow_time()}] [+] Successfully forwarded {local_chat_id} {message_id} to {channel_id}!")
                except UserBannedInChannelError as e:
                    print(f"{Fore.RED}[{self.get_moscow_time()}] [-] {local_chat_id} to {channel_id} [UserBannedInChannelError]: You have been banned from sending messages to groups/supergroups until {e.time}!")
                except FloodWaitError as e:
                    print(f"{Fore.RED}[{self.get_moscow_time()}] [-] {local_chat_id} to {channel_id} [FloodWaitError]: must wait for {e.seconds} seconds.")
                except ChatWriteForbiddenError as e:
                    print(f"{Fore.RED}[{self.get_moscow_time()}] {local_chat_id} to {channel_id} [ChatWriteForbiddenError]: You can't write in this chat.")
                except Exception as e:
                    print(f"{Fore.RED}[{self.get_moscow_time()}] [-] {local_chat_id} to {channel_id} [{type(e).__name__}]: {str(e)}")
                await sleep(self.messages_delay)

    async def send_discord_notification(self, message: str):
        try:
            payload = {
                "content": message
            }
            response = requests.post(self.discord_webhook, json=payload)
            if response.status_code == 204:
                print(f"{Fore.GREEN}[{self.get_moscow_time()}] [+] Successfully sent message to Discord webhook!")
            else:
                print(f"{Fore.RED}[{self.get_moscow_time()}] [-] Failed to send message to Discord webhook. Status code: {response.status_code}")
        except Exception as e:
            print(f"{Fore.RED}[{self.get_moscow_time()}] [-] Failed to send message to Discord webhook. Error: {type(e).__name__}: {str(e)}")

    async def main(self) -> None:
        if not await self.login():
            print(f"[{self.get_moscow_time()}] [-] Exiting the program...")
            return
        while self.status:
            try:
                self.data = self.load_json_file("data.json")
                if not self.data:
                    print(f"[{self.get_moscow_time()}] [-] No data to process.")
                    await sleep(self.groups_delay)
                    continue
                for chat_id in self.data:
                    print(f"{Fore.YELLOW}[{self.get_moscow_time()}] [?] Processing chat_id: {chat_id}")
                    await self.send_message(chat_id)
                print(f"[{self.get_moscow_time()}] [+] Successfully forwarded all messages!")
                await self.send_discord_notification(f"Successfully forwarded {self.sent_messages_count} message(-s) b2.")
                await sleep(self.groups_delay)
            except KeyboardInterrupt:
                self.status = False
                break
            except Exception as e:
                print(f"{Fore.RED}[{self.get_moscow_time()}] An issue occurred [{type(e).__name__}]: {str(e)}")
        _exit(-3)



if __name__ == "__main__":
    bot = Bot("number", 22211343, "0372bcd24abeccb55d763ee22346f7f2", "webhook discord")
    run(bot.main())
