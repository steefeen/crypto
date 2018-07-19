import ecdsa

#every node has a name and a secret key for signing
persons = ["Alice", "Bob", "Carol", "Doris", "Eve"]
nodes = {}

for element in persons:
    nodes.update({element: ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)})

transactions = []

def generateTransaction(fromWho, toWho, transActionNumber):
    #fromWho: list of Names
    #toWho: dictionary of Name/Value pairs
    signatures = [nodes[x].sign("message") for x in fromWho] #ToDo: has to sign transaction from before
    previousTransaction = None
    nonce = None
    proofOfWork = None
    return {"transActionNumber": transActionNumber,
            "type": None,
            "signatures": signatures,
            "previousTransaction": previousTransaction,
            "output": toWho,
            "nonce": nonce,
            "proofOfWork": proofOfWork}

print(generateTransaction(["Alice"],{"Bob": 25},0))
print(generateTransaction([], {},1))