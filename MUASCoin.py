import hashlib
from person import person

#every node has a name and a secret key for signing



def generateTransaction(fromWho, toWho, signatures):
    #fromWho: list of Names
    #toWho: dictionary of Name/Value pairs
    HashOfTransaction = makeHash(fromWho, toWho)
    # for p in toWho:
    #         signatures[p[0].getName()] = p[0].sign(HashOfTransaction)
    return {"HashOfTransaction": HashOfTransaction,
            "signatures": signatures,
            "output": toWho,
            "input": fromWho}

def makeHash(input, output):
    inputString = ""
    outputString = ""
    if input[0] != None:
        inputString = str(input)
    if output[0] != None:
        outputString = str(output)
    return hashlib.sha256(inputString + outputString).hexdigest()

def generateBlock(transaction, nounce):

    block = {
        "nounce": nounce,
        "transaction": transaction
    }
    return block
