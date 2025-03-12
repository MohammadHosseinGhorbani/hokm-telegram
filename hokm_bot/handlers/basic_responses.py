import json
import i18n
from ..database.funcs import set_gorup_language, database_config


@database_config
async def start_command(update, context):
    await update.message.reply_text(i18n.t("hokm.messages.hello"))


@database_config
async def help_command(update, context):
    await update.message.reply_text(i18n.t("hokm.messages.help"))


# from ..utils import stickers_unique
# a = list(stickers_unique)
# b = ['AgAD1BkAAk13cFA', 'AgADKRkAAk5wcFA', 'AgADUxsAAokrcFA', 'AgADUxcAAlRzcVA', 'AgADWhYAAux5aVA', 'AgADgBUAAtLrcFA', 'AgADxxkAAt0RcVA', 'AgADfRcAAnnkcFA', 'AgADohcAAsI9cFA', 'AgADQRoAAr-AaFA', 'AgADSxYAApUrcFA', 'AgADWBoAAmxlcVA', 'AgADZBoAAmH5cVA', 'AgADuBkAA7tpUA', 'AgAD0xcAArU1cFA', 'AgADxxcAAqPTcFA', 'AgADLRgAAoZ-cVA', 'AgAD7hUAAtaCcVA', 'AgADZBUAAh9fcFA', 'AgAD_BsAAgoYaVA', 'AgADCBcAAg-QaVA', 'AgAD5RUAApTpcVA', 'AgADeBwAAiNQaVA', 'AgADjxsAAjXlaVA', 'AgADYBQAAgw7cVA', 'AgADdRkAAuEFcVA', 'AgAD8BcAAjwrcFA', 'AgADXRYAAjXtcVA', 'AgAD5hMAAqVecVA', 'AgADWxcAAtwicFA', 'AgADThsAAhkFaVA', 'AgAD9h4AAt1JaVA', 'AgADyhcAAmB2cVA', 'AgADSxsAAmJqaFA', 'AgAD3hcAAt_kcFA', 'AgADyxcAAhBtcFA', 'AgADmhsAAjKyaVA', 'AgADjRcAAn0zaVA', 'AgADLhQAAixXcFA', 'AgADexsAAoNOcVA', 'AgADYhYAAp05cVA', 'AgADnRUAAkxWaVA', 'AgADZRcAAohVcVA', 'AgADWRYAAhOKcFA', 'AgADBBYAAvTccFA', 'AgADihkAAgfNcVA', 'AgAD_CAAAqSGcVA', 'AgADNxoAAm57cVA', 'AgADRhUAAn8LcVA', 'AgADbRgAAtlScFA', 'AgADyhQAAm1ecFA', 'AgADrBcAAik_cVA', 'AgADOxUAAndXeFA', 'AgADDRoAAioteVA', 'AgADSRoAAicRgVA', 'AgAD0BgAAhOIgFA', 'AgADzBcAAsOAcFA', 'AgAD0BgAAkYGcFA', 'AgADyhcAAvejcVA', 'AgAD9xYAAuwzcVA', 'AgADWBkAAsEiaFA', 'AgAD5BYAAtf-cFA', 'AgADbhgAAhdieVA', 'AgADnRYAAjD1eVA', 'AgAD6xYAAsxIeFA', 'AgADfRgAAiOHeFA', 'AgADLB0AAiY-eVA', 'AgADCRkAAg8meVA', 'AgAD8hUAAqNTeFA', 'AgADyhkAAus7eFA', 'AgAD9hgAAtRceVA', 'AgADJBkAAjlccFA', 'AgADmBgAAkc4eVA', 'AgADmhgAAnFUcFA', 'AgADaRkAAhgCeVA', 'AgADCxkAAmEFeVA', 'AgADExoAAkPLeVA', 'AgADURgAAp6ceFA', 'AgAD4BcAAnMHeFA', 'AgADpRcAAltUeVA', 'AgADMhcAAoYjeVA', 'AgADmBUAAvFpeFA', 'AgADehsAAjdGeVA', 'AgADPxkAAksccFA', 'AgADExoAAixTcVA', 'AgADuxUAAkoxeFA', 'AgAD9hYAAmMMeVA', 'AgADtBgAAlHTeFA', 'AgADYBgAAmqUeFA', 'AgADRQ4BAAHlNnhQ', 'AgAD6BoAArCGeFA', 'AgADIhkAAmb9cVA', 'AgAD9BgAAle7cFA', 'AgADbxcAAhnceFA', 'AgAD_BQAAifKeVA', 'AgADdRYAApyOeVA', 'AgADRx8AAgQFeFA', 'AgAD5RYAAoHQeFA', 'AgADjRcAAkHoeVA', 'AgADrBYAAnJjcVA', 'AgAD0RgAAsXeeVA', 'AgADzRoAArrzeFA', 'AgADhxYAAn8peFA', 'AgADERoAAnAkeFA', 'AgADNRkAAnTIeVA', 'AgADpBkAAiEdeFA', 'AgAD3B0AAsRoeVA', 'AgADthMAAsEUeVA', 'AgADnRkAAhgneFA', 'AgADkhYAAtxTcVA', 'AgADmRoAAnWJeVA', 'AgADmRUAAjcEeFA', 'AgAD6hcAAqg4eVA', 'AgADsBQAAurreFA']
# print(json.dumps(dict(zip(a, b))))

async def get_sticker_id(update, context):
    b.append(update.message.sticker.file_unique_id)
    await update.message.reply_text(str(b))

