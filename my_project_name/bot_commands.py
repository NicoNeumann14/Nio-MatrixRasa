from nio import AsyncClient, MatrixRoom, RoomMessageText

from my_project_name.chat_functions import react_to_event, send_text_to_room
from my_project_name.config import Config
from my_project_name.storage import Storage
import requests


class Command:
    def __init__(
        self,
        client: AsyncClient,
        store: Storage,
        config: Config,
        command: str,
        room: MatrixRoom,
        event: RoomMessageText,
    ):
        """A command made by a user.

        Args:
            client: The client to communicate to matrix with.

            store: Bot storage.

            config: Bot configuration parameters.

            command: The command and arguments.

            room: The room the command was sent in.

            event: The event describing the command.
        """
        self.client = client
        self.store = store
        self.config = config
        self.command = command
        self.room = room
        self.event = event
        self.args = self.command.split()[1:]

    async def process(self):
        """Process the command"""
        if self.command.startswith("echo"):
            await self._echo()
        elif self.command.startswith("react"):
            await self._react()
        elif self.command.startswith("help"):
            await self._show_help()
        else:
            await self._unknown_command()

    async def _echo(self):
        """Echo back the command's arguments"""
        response = " ".join(self.args)
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _react(self):
        """Make the bot react to the command message"""
        # React with a start emoji
        reaction = "⭐"
        await react_to_event(
            self.client, self.room.room_id, self.event.event_id, reaction
        )

        # React with some generic text
        reaction = "Some text"
        await react_to_event(
            self.client, self.room.room_id, self.event.event_id, reaction
        )

    async def _show_help(self):
        """Show the help text"""
        if not self.args:
            text = (
                "Hello, I am a bot made with matrix-nio! Use `help commands` to view "
                "available commands."
            )
            await send_text_to_room(self.client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "rules":
            text = "These are the rules!"
        elif topic == "commands":
            text = "Available commands: ..."
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)

    async def _unknown_command(self):
        text= ""
        #s = f"Hallo, Unknown command '{self.command}'++ HalloÄnderung Hier'{self.room}'. Try the 'help' command for more information.",
        url = 'http://chatbotrasa-rasa-server-1:5005/webhooks/rest/webhook'

 
        #Call an RasaCore
        body = {"sender":"senderBOT","message":self.command}
        response = requests.post(url,json=body)

        #linkResponseNew = linkResponse.replace("\\","")
    
        #Verarbeitung der Response vom RasaCore
        responseList = response.json()
        for resp in responseList:
            if "text" in resp:
                text += resp["text"] 
            if "image" in resp:
                text += " "+resp["image"] 


        await send_text_to_room(
            self.client,
            self.room.room_id,
            text
        )
