import os
import subprocess
import secrets
import pickle
from tinyec import registry
from Crypto.Cipher import AES
import hashlib, binascii

class Encryption(object):
    def __init__(self) -> None:
        pass

    def splitter(string: str):
        newString = string.split(' ')
        return newString[0]

    # def gen_hash(self, files):
    #     #Generate hashes
    #     print("Generating hashes")
    #     old_file = 'hashes.txt'
    #     new_file = 'hashes_old.txt'

    #     #dir = 'BC_data/'
    #     #dir = '/home/seth/Desktop/'
    #     real_path = os.path.dirname(os.path.realpath(__file__))
    #     #ext = 'bin'
    #     #testFiles = '/testFiles'

    #     try:
    #         open(old_file, 'x')
    #     except FileExistsError:
    #         if os.path.exists(new_file):
    #             os.remove(new_file)
    #             os.rename(old_file, new_file)
    #             open(old_file, 'x')
    #         else:
    #             os.rename(old_file, new_file)
    #             open(old_file, 'x')

    #     with open(old_file, "a") as hashfile:
    #         for file in sorted(files):
    #             #if file.endswith(ext):
    #             location = real_path+'/'+file
    #             cmd = (['b3sum', location])
    #             proc = subprocess.check_output(cmd)
    #             newProc = proc.decode()
    #             hash = Encryption.splitter(newProc)
    #             hashfile.write(hash+"  "+file+"\n")

    def ecc_calc_encryption_keys(self, pubKey):
        curve = registry.get_curve('brainpoolP256r1')
        ciphertextPrivKey = secrets.randbelow(curve.field.n)
        ciphertextPubKey = ciphertextPrivKey * curve.g
        sharedECCKey = pubKey * ciphertextPrivKey
        return (sharedECCKey, ciphertextPubKey, ciphertextPrivKey)

    # def keygen(self, pubKey):
    #     #Generate Encryption keys   
    #     #print("Generating keys")  
    #     #pubKey = pickle.load(open('/public_key.pem', 'rb'))

    #     (encrypt_key, ciphertextPubKey, ciphertextPrivKey) = Encryption.ecc_calc_encryption_keys(pubKey)

    #     pickle.dump(encrypt_key, open('/encrypt_key.pem', 'wb'))

    #     pickle.dump(ciphertextPubKey, open('/ciphertextPubKey.pem', 'wb'))

    #     pickle.dump(ciphertextPrivKey, open('/ciphertextPrivKey.pem', 'wb'))
        
    #     return encrypt_key

    #encrypt_key is sharedECCKey
    def encrypt_AES_GCM(msg, secretKey):
        aesCipher = AES.new(secretKey, AES.MODE_GCM)
        ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
        return (ciphertext, aesCipher.nonce, authTag)
    
    def ecc_point_to_256_bit_key(point):
        sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
        sha.update(int.to_bytes(point.y, 32, 'big'))
        return sha.digest()

    def encrypt_ECC(msg, encrypt_key, ciphertextPubKey):
        secretKey = Encryption.ecc_point_to_256_bit_key(encrypt_key)
        ciphertext, nonce, authTag = Encryption.encrypt_AES_GCM(msg, secretKey)
        return (ciphertext, nonce, authTag, ciphertextPubKey)

    def large_encrypt_ECC(aesCipher, msg):
        block = aesCipher.encrypt(msg)
        return (block)


    def large_digest(aesCipher):
        authTag = aesCipher.digest()
        return (authTag)


    def large_AES(sharedECCKey):
        secretKey = Encryption.ecc_point_to_256_bit_key(sharedECCKey)
        #print(f'secret key: {secretKey}')
        aesCipher = AES.new(secretKey, AES.MODE_GCM)
        return (aesCipher, aesCipher.nonce)




    # def encrypt(self):
    #     #Encrypt data
    #     #with open('BC_data/hashes.txt', 'rb') as file:
    #     #    original = file.read()
    #     print("Encrypting data")
    #     dir = '/home/seth/Desktop'

    #     pubKey = pickle.load(open(dir+'/public_key.pem', 'rb'))

    #     encrypt_key = pickle.load(open(dir+'/encrypt_key.pem', 'rb'))

    #     ciphertextPubKey = pickle.load(open(dir+'/ciphertextPubKey.pem', 'rb'))

    #     #dir = 'BC_data/'
    #     #ext = 'txt'
    #     #dir1 = os.path.dirname(os.path.realpath(__file__))
    #     dir = '/home/seth/Desktop'
    #     testFiles = '/testFiles'

    #     for file in sorted(os.listdir(dir+testFiles)):
    #         #if file.endswith(ext):
    #         enc_file = dir+testFiles+'/'+ file
    #         with open(enc_file, 'rb') as enc:
    #             original = enc.read()
    #             encryptedMsg = Encryption.encrypt_ECC(original, encrypt_key, ciphertextPubKey)
    #             pickle.dump(encryptedMsg, open(enc_file, 'wb'))
    #     print("Encryption complete")