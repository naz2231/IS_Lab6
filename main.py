
import docx
import random
import string
import time
import codecs
from itertools import permutations, product
MOD = 256


def readDoc(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def KSA(key):  # ключовий алгоритм планування потоку
    key_length = len(key)
    # створити масив "S" у межах послідовності MOD: [0,1,2, ... , 255]
    S = list(range(MOD))
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # реверс значень
    return S


def PRGA(s):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + s[i]) % MOD
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % MOD]
        yield k


def RC4logic(key, text):
    key = [ord(s) for s in key]
    keystream = PRGA(KSA(key))

    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))
        res.append(val)
    return ''.join(res)


def encrypt(key, text):
    text = [ord(c) for c in text]
    return RC4logic(key, text)


def decrypt(key, text):
    ciphertext = codecs.decode(text, 'hex_codec')
    res = RC4logic(key, ciphertext)
    return codecs.decode(res, 'hex_codec').decode('utf-8')


def keygen(alphabet, keyLen):
    return product(alphabet, repeat=keyLen)


def hack(original, encrypted, alphabet, keyLen=0):
    if keyLen == 0:
        keyLen = len(original)//3
    for hackedKey in keygen(alphabet, keyLen):
        # print(''.join(hackedKey))
        try:
            if decrypt(''.join(hackedKey), encrypted) == original:
                print('\nВзломаний текст')
                print(decrypt(''.join(hackedKey), encrypted))
                print('\nВзломаний ключ', ''.join(hackedKey))
                return ''.join(hackedKey)
        except:
            pass


def main():
    text = readDoc('./input.docx')
    alphabet = [i for i in string.ascii_letters]
    print("Вхідний текст: ")
    print(text)
    key = ''.join([random.choice(alphabet)
                   for n in range(len(text) // 3)])
    print("key: ")
    print(key)
    startTime = time.perf_counter_ns()
    encryptedText = encrypt(key, text)

    print("Час шифрування: ", (time.perf_counter_ns() - startTime)/1000000)
    print('\nЗашифрований текст:', '\n')
    print(encryptedText)

    file = open("output.txt", "w")
    file.write(encryptedText)
    file.close()

    startTime = time.perf_counter_ns()
    decryptedText = decrypt(key, encryptedText)
    print("Час розшифрування: ", (time.perf_counter_ns() - startTime)/1000000)
    print('Розшифрований текст', '\n')
    print(decryptedText)

    startTime = time.perf_counter_ns()
    hack(text, encryptedText, alphabet)
    print("Час злому: ", (time.perf_counter_ns() - startTime)/1000000)


main()
