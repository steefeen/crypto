import ecdsa

#every node has a name and a secret key for signing
persons = ["Alice", "Bob", "Carol", "Doris", "Eve"]
nodes = {}

for element in persons:
    nodes.update({element: ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)})

transactions = []

def generateTransaction(fromWho, toWho, transActionNumber, type):
    #fromWho: list of Names
    #toWho: dictionary of Name/Value pairs
    signatures = None#[nodes[x].sign("message") for x in fromWho] #ToDo: has to sign transaction from before
    return {"transActionNumber": transActionNumber, #ToDo: has to be a hash
            "type": type,
            "signatures": signatures,
            "output": toWho}
