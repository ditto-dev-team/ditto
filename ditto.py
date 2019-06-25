import discord
import asyncio

class Ditto:

        def __init__(self, client):
                self._client = client
                #other things

        def check_file_type(self, message):
                ''' Determine the file type of a message that has been reacted to (message.attachments)'''

                return len(message.attachments)>0 # returns True if message includes an attachment

        def check_for_ditto_react(self, reaction):
                ''' Check if the reaction to the post is a ditto '''

                ditto_emoji = discord.utils.get(reaction.message.server.emojis, name="ditto")
                ditto_emoji=(str(ditto_emoji)[1:8])
                return ditto_emoji == ':ditto:'

        def start_query(self, command, author_id, file_url):
                ''' Placeholder method for Drey code '''

                pass

        async def prompt_user(self, message):
                ''' Start here if user reacts :ditto: on a file '''

                self.start_query('get_user_libs', message.author.id, message.attachments[0].get("url"))
                libs = ['Dog Memes', 'Food'] # this will be output of query
                await self._client.send_message(message.channel, ('`{}`, what library do you want to save this photo in?'.format(message.author.display_name)))
                title = message.author.display_name + '\'s Libraries'
                desc = ''
                for lib in range(len(libs)):
                    desc += str((lib+1)) + '. ' + libs[lib]+'\n'
                desc += '**$newLibrary** <library name>'
                em = discord.Embed(description=desc, title = title, color = 0x7289DA)

                #def check(msg):
                #    if msg.content.startswith('$newLibrary'):
                #        return True

                await self._client.send_message(message.channel, embed = em)
                response = await self._client.wait_for_message(author=message.author)
                if '$newLibrary' in response.content:
                    await self.new_library(message, response)
                elif response.content in libs:
                    await self.add_to_library(message, response)
                else:
                    await self._client.send_message(message.channel, 'That library doesn\'t exist. Use `$newLibrary <library name>` to create a new library.')
                    response = await self._client.wait_for_message(author=message.author)
                    if response.content.startswith('$newLibrary'):
                        await self.new_library(message, response)
                    elif response.content in libs:
                        await self.add_to_library(message, response)


        async def new_library(self, message, response):
                ''' $newLibrary - Create new library with $newLibrary command - user inputted library name '''
                if len(response.content.split())>1:
                    new_lib = response.content.split(' ', 1)[1]
                    self.start_query('create_new_lib', message.author.id, message.attachments[0].get("url"))
                    await self._client.send_message(message.channel, ('New library `' + new_lib +'` has been created for `{}`'.format(message.author.display_name)))
                else:
                    await self._client.send_message(message.channel, ('Please provide a name for your new library using `$newLibrary <library name>`'))
                    response = await self._client.wait_for_message(author=message.author)
                    if response.content.startswith('$newLibrary'):
                        await self.new_library(message, response)

        async def add_to_library(self, message, response):
                ''' Add file to existing library '''
                lib = response.content
                self.start_query('add_to_lib', message.author.id, message.attachments[0].get("url")) # send lib here too
                await self._client.send_message(message.channel, 'File added to library `' + lib +'`!')



        def check_for_library(self):
                ''' Check if user response for library option is valid'''
                pass

        async def share_library(self, message):
                ''' $Library <library name> - Returns a library to message channel where left and right arrows can flip through files'''

                await self._client.send_message(message.channel, 'Here is a placeholder that will be your library')


        def surprise(self):
                ''' $surpriseMe - Returns a randomly chosen photo '''
                pass


