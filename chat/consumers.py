from channels import Group


def ws_add(message):
    Group('room').add(message.reply_channel)


def ws_message(message):
    print('connected')


def ws_disconnect(message):
    Group('room').discard(message.reply_channel)
