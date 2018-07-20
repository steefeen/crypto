from ecdsa import SigningKey


class person:


    def __init__(self, name):
        self.name = name
        self.sk = SigningKey.generate()
        self.vk = self.sk.get_verifying_key()
        signature = self.sk.sign("message")
        self.vk.verify(signature, "message")

    def getName(self):
        return self.name

    def sign(sefl, hash):
        return sefl.sk.sign(hash)

    def get_verifying_key(self):
        return self.vk

    def verify(self, signature ,message):
        return self.vk.verify(signature, message)