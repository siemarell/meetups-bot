from telegram.ext.filters import BaseFilter


class ReplyToForward(BaseFilter):
    def filter(self, message):
        return message.reply_to_message and message.reply_to_message.forward_from


reply_to_forward = ReplyToForward()