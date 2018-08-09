from config import CHAIN, REWARD_LIMIT, APP_WAVES_ADDRESS, APP_SECRET_KEY, NODES
import pywaves as pw

pw.setNode(NODES[CHAIN], CHAIN)


class Rewarder:
    def __init__(self):
        self.remaining_waves = REWARD_LIMIT
        self.address = pw.Address(privateKey=APP_SECRET_KEY)

    def send_reward(self, address, amount):
        if amount > self.remaining_waves:
            raise Exception('Insufficient funds')
        recipient = pw.Address(address)
        self.remaining_waves -= amount
        self.address.sendWaves(recipient, amount * 10 ** 8)


rewarder = Rewarder()
