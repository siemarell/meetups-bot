from telegram.ext.filters import BaseFilter, Filters


class EndsWithNonBreakingSpace(BaseFilter):
    def filter(self, message):
        return message.text.endswith('\u00A0')


menu_command_filter = Filters.text & EndsWithNonBreakingSpace()