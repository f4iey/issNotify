#Fonctionnement général du bot
import discord
import datetime
import issNotify
import requests
helpMessage = "\t\tCommandes du bot:\a\n**CQ CQ**: *Pour envoyer un appel cw sonore*\n**CQ ping**: *Renvoie `Pong!` si tout se passe bien!*\n**CQ ISS**: *Pour rafraîchir les dernières activités de la Station Spatiale*\n\t`-lastest` permet de montrer les activités passées*\n"


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == client.user:
            return
        if message.content.startswith('CQ'):
            if message.content[2:] == 'ping' or message.content[2:] == ' ping':
                    await message.channel.send('Pong!')
            elif message.content[2:] == 'help' or message.content[2:] == ' help':
                await message.author.send(helpMessage)
                await message.channel.send('**{0.author}**, un message privé à été envoyé ;)'.format(message))
            elif message.content[2:] == 'ISS' or message.content[2:] == ' ISS':
                await message.channel.send(issNotify.scan('http://www.ariss-f.org/category/sstv/'))
                await message.channel.send(issNotify.scan('http://www.ariss-f.org/category/contact-ariss/'))
                await message.channel.send("C'est tout pour le moment sur ISS!")
            elif message.content[2:] == 'ISS -lastest' or message.content[2:] == ' ISS -lastest':
                html = requests.get("http://www.ariss-f.org/category/sstv/").text
                parser = issNotify.ARISSScanner()
                parser.moni()
                parser.feed(html)
                await message.channel.send(parser.getTitle())
                await message.channel.send(parser.getArticleURL())
                html = requests.get("http://www.ariss-f.org/category/contact-ariss/").text
                parser = issNotify.ARISSScanner()
                parser.moni()
                parser.feed(html)
                await message.channel.send(parser.getTitle())
                await message.channel.send(parser.getArticleURL())
            elif message.content[2:] == 'CQ' or message.content[2:] == ' CQ':
                #on envoie le CQ.wav
                await message.channel.send('CQDX!\nSi vous avez besoin, taper **CQ help**', file=discord.File('cqcq.mp3'))
            else:
                await message.channel.send('Pas de QRU! Commande invalide!')
    async def on_socket_raw_receive(self, msg):
        if datetime.datetime.now().hour == 17:
            await msg.channel.send(issNotify.scan('http://www.ariss-f.org/category/sstv/'))
            await msg.channel.send(issNotify.scan('http://www.ariss-f.org/category/contact-ariss/'))
            await msg.channel.send("C'est tout pour le moment sur ISS!")
client = MyClient()
client.run('discord-token')
