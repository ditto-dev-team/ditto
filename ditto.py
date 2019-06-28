import discord
import asyncio
import ditto_backend
import random

class Ditto:

    def __init__(self, client):
        self._client = client
        self.blurple = 0x7289DA

    def check_file_type(self, message):
        """
        Usage: Determines if a message includes a file

        Parameters:
            message (Discord.py message object)

        Returns:
            True if message includes a file; False otherwise
        """

        return len(message.attachments)>0

    def check_for_ditto_react(self, reaction):
        """
        Usage: Checks if the reaction to a post with an attachment is :ditto:

        Parameters:
            reaction (Discord.py reaction object)

        Returns:
            True if the reaction is :ditto:; False otherwise
        """

        ditto_emoji = discord.utils.get(reaction.message.server.emojis, name="ditto")
        ditto_emoji=(str(reaction.emoji)[1:8])
        return ditto_emoji == ':ditto:'

    def start_query(self, command, author_id, file_url):
        ''' Placeholder method for Drey code '''

        pass

    async def on_ditto_react(self, message):
        """
        Usage: When a user reacts to a file with :ditto:, get (or create) the user's directory path,
        and save file to a library or create a new library based on user response

        Parameters:
            message (Discord.py message object)
        """

        user_path = ditto_backend.get_user_dir_path(message.author.id)
        libs = ditto_backend.get_user_libs(message.author.id)
        title = message.author.display_name + '\'s Libraries'
        desc = ''
        for index, lib in enumerate(libs):
            desc += '{}. {}\n'.format(index+1, lib)
        desc += '**$newLibrary** <library name>'
        em = discord.Embed(description=desc, title = title, color = self.blurple)

        await self._client.send_message(message.channel, ('`{}`, what library do you want to save this photo in?'.format(message.author.display_name)))
        await self._client.send_message(message.channel, embed = em)
        response = await self._client.wait_for_message(author=message.author)
        if '$newLibrary' in response.content:
            await self.new_library(response, message.attachments[0])
        elif response.content in libs:
            lib = response.content.strip()
            await self.add_to_library(message, message.attachments[0], lib)
        else:
            lib = response.content.strip()
            await self._client.send_message(message.channel, 'That library doesn\'t exist. Would you like to create it?')
            yesmessage = await self._client.wait_for_message(author=message.author)
            if yesmessage.content.lower().strip() == 'yes':
                ditto_backend.create_lib(message.author.id, lib)
                await self._client.send_message(message.channel, ('New library `' + lib +'` has been created for `{}`'.format(message.author.display_name)))


    async def new_library(self, message, img):
        """
        Usage: Upon user command `$newLibrary`, checks if user has supplied a name for new library;
        Creates a library if so, otherwise prompts for a library name

        Parameters:
            message (Discord.py message object)
        """

        if message.content.startswith('$newLibrary'):
            if len(message.content.split()) > 1:
                new_lib = message.content.split(None, 1)[1]
                if not self.check_for_library(message.author.id, new_lib):
                    ditto_backend.create_lib(message.author.id, new_lib)
                    await self._client.send_message(message.channel, ('New library `' + new_lib +'` has been created for `{}`'.format(message.author.display_name)))
                    await self.add_to_library(message, img, new_lib)
                else:
                    await self._client.send_message(message.channel, ('That library already exists. Adding the file to it anyways.'))
                    await self.add_to_library(message, img, new_lib)

            else:
                await self._client.send_message(message.channel, ('Please provide a name for your new library using `$newLibrary <library name>` or type `$stop` to cancel.'))
                response = await self._client.wait_for_message(author=message.author)
                if '$stop' not in response.content:
                    await self.new_library(response)
                else:
                    await self._client.send_message(message.channel, 'This file has not been saved.')
        else:
            await self._client.send_message(message.channel, ('Please provide a name for your new library using `$newLibrary <library name>` or type `$stop` to cancel.'))
            response = await self._client.wait_for_message(author=message.author)
            if '$stop' not in response.content:
                await self.new_library(response, img)
            else:
                await self._client.send_message(message.channel, 'This file has not been saved.')

    async def delete_library(self, message):
        """
        Usage: Upon user command `$deleteLibrary` and confirmation, deletes an entire library

        Parameters:
            message (Discord.py message object)
        """

        if len(message.content.split()) > 1:
            lib_to_del = message.content.split(None, 1)[1]
            if self.check_for_library(message.author.id, lib_to_del):
                await self._client.send_message(message.channel, ('Are you sure you want to delete the entire library `{}`? Type `yes` to delete.'.format(lib_to_del)))
                response = await self._client.wait_for_message(author=message.author)
                if response.content.lower().strip() == 'yes':
                    success = ditto_backend.remove_lib(message.author.id, lib_to_del)
                    if success:
                        await self._client.send_message(message.channel, ('Library `{}` has been deleted.'.format(lib_to_del)))
                    else:
                        await self._client.send_message(message.channel, 'Sorry, that library could\'t be deleted.')
            else:
                await self._client.send_message(message.channel, 'That library does not exist.')

        else:
            await self._client.send_message(message.channel, ('Please provide a name for the library you want to delete using `$deleteLibrary <library name>`.'))

    async def add_to_library(self, message, img, lib):
        """
        Usage: Adds the file the user reacted to to an existing library

        Parameters:
            message (Discord.py message object): the message that contains the file
			img (Discord.py attachment object): the attachment/ file that you want to save
            lib (str): library name to add file to
        """
        ditto_backend.add_img_to_lib(message.author.id, lib, img.get("filename"), img.get("url"))
        await self._client.send_message(message.channel, 'File added to library `' + lib +'`!')

    def check_for_library(self, user, lib):
        """
        Usage: Checks if a provided library name exists for that user

        Parameters:
            user (int or str): the unique token for the user provided by Discord.py
            lib (str): the name of the library to look for

        Returns:
            True if library exists; False otherwise
        """

        user_libs = ditto_backend.get_user_libs(user)
        return lib in user_libs

    async def share_library(self, message):
        """
        Usage: Upon user command `$Library <library name>`, returns a library to message channel;
        Left and right arrow reactions allow the user to flip through files

        Parameters:
            message (Discord.py message object)
        """

        if len(message.content.split()) > 1:
            lib = message.content.strip().split(None,1)[1]
            if self.check_for_library(message.author.id, lib):
                imgs = ditto_backend.get_lib_images(message.author.id, lib)
                n_imgs = len(imgs)
                n=0
                if len(imgs) == 0:
                    msg = await self._client.send_message(message.channel, 'The library `{}` appears to be empty!'.format(lib))
                    return
                elif len(imgs) == 1:
                    img0 = ditto_backend.get_lib_image(message.author.id, lib, imgs[n])
                    msg = await self._client.send_message(message.channel, '{} Photo Tagged "{}" by {} ({}/{})'.format(n_imgs, lib, message.author.display_name, n+1, n_imgs))
                    img_msg = await self._client.send_file(message.channel, img0)
                elif len(imgs) > 1:
                    img0 = ditto_backend.get_lib_image(message.author.id, lib, imgs[n])
                    msg = await self._client.send_message(message.channel, '{} Photos Tagged "{}" by {} ({}/{})'.format(n_imgs, lib, message.author.display_name, n+1, n_imgs))
                    img_msg = await self._client.send_file(message.channel, img0)

                #desc = '{} Photos Tagged "{}" by {}'.format(n_imgs, lib, message.author.display_name)
                #em = discord.Embed(description=desc, title = lib, color = self.blurple)
                #em.set_image(url = 'attachment://' + img0)
                #await self._client.send_message(message.channel, embed=em)
                #await self._client.http.send_file(message.channel, img0, embed=em.to_dict())

                await self._client.add_reaction(img_msg, '\u2B05') # left arrow
                await self._client.add_reaction(img_msg, '\u27A1') # right arrow
                await self._client.add_reaction(img_msg, '\u274C') # X
                await self.next_img_or_del(msg, img_msg, message.author, lib, n, imgs)
            else:
                await self._client.send_message(message.channel, 'That library does not exist.')

        else:
            await self._client.send_message(message.channel, ('Please provide a library name using `$Library <library name>`'))

    async def next_img_or_del(self, msg, img_msg, author, lib, n, imgs):

        n_imgs = len(imgs)
        user_reaction = await self._client.wait_for_reaction(['\u2B05', '\u27A1','\u274C'], user=author, message=img_msg)
        if user_reaction.reaction.emoji == '\u2B05': # left arrow
            n = n-1 if n>0 else n_imgs-1
            await self._client.delete_message(msg)
            await self._client.delete_message(img_msg)
            img = ditto_backend.get_lib_image(author.id, lib, imgs[n])
            if len(imgs) == 0:
                msg = await self._client.send_message(msg.channel, 'The library {} appears to be empty!)'.format(lib))
            elif len(imgs) == 1:
                msg = await self._client.send_message(msg.channel, '{} Photo Tagged "{}" by {} ({}/{})'.format(n_imgs, lib, author.display_name, n+1, n_imgs))
            elif len(imgs) > 1:
                msg = await self._client.send_message(msg.channel, '{} Photos Tagged "{}" by {} ({}/{})'.format(n_imgs, lib, author.display_name, n+1, n_imgs))

            img_msg = await self._client.send_file(msg.channel, img)
            await self._client.add_reaction(img_msg, '\u2B05') # left arrow
            await self._client.add_reaction(img_msg, '\u27A1') # right arrow
            await self._client.add_reaction(img_msg, '\u274C') # X
            await self.next_img_or_del(msg, img_msg, author, lib, n, imgs)

        elif user_reaction.reaction.emoji == '\u27A1': # right arrow
            n = n+1 if n<n_imgs-1 else 0
            await self._client.delete_message(msg)
            await self._client.delete_message(img_msg)
            img = ditto_backend.get_lib_image(author.id, lib, imgs[n])
            if len(imgs) == 0:
                msg = await self._client.send_message(msg.channel, 'The library {} appears to be empty!)'.format(lib))
            elif len(imgs) == 1:
                msg = await self._client.send_message(msg.channel, '{} Photo Tagged "{}" by {} ({}/{})'.format(n_imgs, lib, author.display_name, n+1, n_imgs))
            elif len(imgs) > 1:
                msg = await self._client.send_message(msg.channel, '{} Photos Tagged "{}" by {} ({}/{})'.format(n_imgs, lib, author.display_name, n+1, n_imgs))

            img_msg = await self._client.send_file(msg.channel, img)
            await self._client.add_reaction(img_msg, '\u2B05') # left arrow
            await self._client.add_reaction(img_msg, '\u27A1') # right arrow
            await self._client.add_reaction(img_msg, '\u274C') # X
            await self.next_img_or_del(msg, img_msg, author, lib, n, imgs)
        elif user_reaction.reaction.emoji == '\u274C':
            img = ditto_backend.get_lib_image(author.id, lib, imgs[n])
            await self._client.send_message(msg.channel, 'Are you sure you want to delete this file? Type `yes` to delete.')
            response = await self._client.wait_for_message(author=author)
            if response.content.lower().strip() == 'yes':
                success = ditto_backend.remove_image(author.id, lib, img.split('/')[-1])
                if success:
                    await self._client.send_message(msg.channel, ('File has been deleted.'))
                else:
                    await self._client.send_message(msg.channel, 'Sorry, that file could\'t be deleted.')


    async def list_libraries(self, message):
        """
        Usage: Upon user command `$myLibraries`, returns a list of the users current libraries to message channel

        Parameters:
            message (Discord.py message object)
        """

        libs = ditto_backend.get_user_libs(message.author.id)

        title = message.author.display_name + '\'s Libraries'
        desc = ''
        for index, lib in enumerate(libs):
            desc += '{}. {}\n'.format(index+1, lib)
        if len(libs) == 0:
            desc+='You don\'t have any libraries yet! React with `:ditto:` to an image to begin!'
        em = discord.Embed(description=desc, title = title, color = self.blurple)
        await self._client.send_message(message.channel, embed = em)

    async def surprise(self, message):
        """
        Usage: Upon user command `$surpriseMe`, returns a randomly chosen photo from any of the user's libraries to message channel

        Parameters:
            message (Discord.py message object)
        """
        user_libs = ditto_backend.get_user_libs(message.author.id)

        if len(message.content.split()) > 1:
            lib = message.content.split(None, 1)[1]
            if lib in user_libs:
                random_img = ditto_backend.get_random_image(message.author.id, lib)
                filename = random_img.split('/')[-1]
                img_url = ditto_backend.get_lib_image(message.author.id, lib, filename)
                await self._client.send_message(message.channel, ('Here\'s a random image from the library `{}`.'.format(lib)))
                await self._client.send_file(message.channel, img_url)
            else:
                await self._client.send_message(message.channel, ('Library not found. Use `$surpriseMe <library name>` to get a random photo from that library.'))

        else:
            await self._client.send_message(message.channel, ('Use `$surpriseMe <library name>` to get a random photo from that library.'))

    async def help_msg(self, message):
        """
        Usage: Upon user command `$help`, returns a help message with bot functionality to message channel

        Parameters: message (Discord.py message object)
        """

        await self._client.send_message(message.channel, 'Hey I\'m Ditto, your media squire for Discord! Here\'s some things I can do for you:')
        em = discord.Embed(color = self.blurple)
        em.add_field(name = ':ditto:', value = 'React to a file with `:ditto:` to save it to a library', inline=False)
        em.add_field(name = '$myLibraries', value = 'View a list of your current libraries', inline=False)
        em.add_field(name = '$Library <library name>', value = 'View a library', inline=False)
        em.add_field(name = '$deleteLibrary <library name>', value = 'Delete a library', inline=False)
        em.add_field(name = '$surpriseMe', value = 'Pick a photo at random', inline=False)
        await self._client.send_message(message.channel, embed=em)

