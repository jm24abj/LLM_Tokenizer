VOCABULARY_SIZE = 276
NUM_OF_MERGES = VOCABULARY_SIZE - 256

text = "There was something in the sky. What exactly was up there wasn't immediately clear. But there was definitely something in the sky and it was getting bigger and bigger."
tokens = text.encode("utf-8")
tokens = list(map(int, tokens))

#print('---')
#print(text)
#print("Text length:", len(text))
#print('---')
#print(tokens)
#print("Number of tokens:", len(tokens))

def getStats(ids):
    counts = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    
    return counts

def mergeAllPairs(stats,tokens):
    ids = list(tokens)

    currentBest = max(stats,key=stats.get)
    allMerges = {}

    for i in range(NUM_OF_MERGES):
        stats = getStats(ids)
        currentBest = max(stats,key=stats.get)
        pairsNewId = 256 + i
        print(f'Merging pair: {currentBest} -> {pairsNewId}')
        ids = mergePair(ids, currentBest, pairsNewId)
        allMerges[currentBest] = pairsNewId

    displayCompressionRatio(len(tokens), len(ids))

    return allMerges

def mergePair(ids, pair, idx):
    newIds = []
    i = 0
    while i < len(ids):

        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            newIds.append(idx)
            i += 2
        else:
            newIds.append(ids[i])
            i += 1

    return newIds

def decode(ids):
    vocab = {idx: bytes([idx]) for idx in range(256)}
    for (p0, p1), idx in merges.items():
        vocab[idx] = vocab[p0] + vocab[p1]

    tokens = b"".join(vocab[id] for id in ids)
    text = tokens.decode("utf-8", errors="replace")
    return text

def encode(text):
    tokens = list(text.encode("utf-8"))
    while len(tokens) > 1:
        stats = getStats(tokens)
        pair = min(stats, key=lambda p: merges.get(p, float('inf')))
        if pair not in merges:
            break
        idx = merges[pair]
        tokens = mergePair(tokens, pair, idx)
    return tokens

def displayCompressionRatio(originalLength, newLength):
    print("----------------------------------------------------")
    print("Original tokens length:", originalLength)
    print("Final tokens length:", newLength)
    print(f"Compression ratio: {originalLength / newLength:.2f}x")
    print("----------------------------------------------------")

stats = getStats(tokens)
#print(sorted(((v, k) for k, v in stats.items()), reverse=True))

merges = mergeAllPairs(stats, tokens)

test = "I'm heading back to Colorado tomorrow after being down in Santa Barbara over the weekend for the festival there. I will be making October plans once there and will try to arrange so I'm back here for the birthday if possible. I'll let you know as soon as I know the doctor's appointment schedule and my flight plans."
test2 = decode(encode(test))
print(test==test2)