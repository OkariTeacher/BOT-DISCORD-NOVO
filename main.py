import discord
from discord.ext import commands
from model import get_class


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'LOGAMOS COMO: {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'OLÁ EU SOU {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("HE" * count_heh)

@bot.command()
async def check(ctx):
    # $check + imagem anexada -> o bot analisa a imagem.

    # Confere se a mensagem veio com algum anexo.
    # Lista vazia = False, então só entra aqui se tiver pelo menos um arquivo.
    if ctx.message.attachments:

        # A pessoa pode mandar várias imagens de uma vez,
        # então o bot analisa uma por uma.
        for attachment in ctx.message.attachments:

            # Guarda o nome do arquivo e o link dele no Discord.
            # (Nenhum dos dois é usado depois, então dá pra apagar essas duas linhas caso você não use.)
            file_name = attachment.filename
            file_url = attachment.url

            # Baixa a imagem do Discord e salva na pasta do projeto,
            # com o mesmo nome que a pessoa enviou.
            await attachment.save(f"./{attachment.filename}")

            # Manda a imagem pro modelo analisar e responde no chat com o resultado:
            # model_path  -> o modelo do Teachable Machine
            # labels_path -> o arquivo com os nomes das classes (ex: pombo | pardal)
            # image_path  -> a imagem que acabamos de baixar
            await ctx.send(get_class(model_path="./model_unquant.tflite", labels_path="labels.txt", image_path=f"./{attachment.filename}"))

    # Se não veio nenhum anexo, avisa a pessoa.
    else:
        await ctx.send("Você esqueceu de enviar a imagem :(")
        
bot.run("TOKEN")
