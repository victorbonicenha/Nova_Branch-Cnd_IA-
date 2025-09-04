import telegram
import asyncio
import requests

class TelegramSend:

    def __init__(self, name):
        self.name = name

    def telegram_bot(self, message, itoken, chat_id):
        """Telegram Bot
        :param message: Mensagem a ser enviada pelo telegram;
        :param itoken: Token do bot no telegram;
        :param chat_id: id da conversa ou do grupo a qual as mensagens vão ser direcionadas;
        :return: Retorna um json com todos os parâmetros e status da mensagem.
        """
        url = "https://api.telegram.org/bot" + itoken + "/sendMessage?chat_id=" + str(chat_id) + "&text=" + self.name + " " + message
        resposta = requests.get(url) 
        return resposta.json()

    def telegram_bot_image(self, message, itoken, chat_id, path_image):
        """Telegram Bot
        :param message: Mensagem a ser enviada pelo telegram;
        :param itoken: Token do bot no telegram;
        :param chat_id: id da conversa ou do grupo a qual as mensagens vão ser direcionadas;
        :param path_image: caminho da imagem que vai ser enviada;
        :return: Retorna um json com todos os parâmetros e status da mensagem.
        """
        bot = telegram.Bot(token=itoken)

        async def send_image():
            with open(path_image, 'rb') as img:
                await bot.send_photo(chat_id=chat_id, photo=img)
        asyncio.run(send_image())
        url = "https://api.telegram.org/bot" + itoken + "/sendMessage?chat_id=" + str(chat_id) + "&text=" + self.name + " " + message
        resposta = requests.get(url) 
        return resposta.json()