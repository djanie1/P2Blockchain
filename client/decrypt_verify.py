from tinyec import registry
import secrets
import pickle
import os
from Crypto.Cipher import AES
import hashlib, binascii
import subprocess


class Decryption(object):
    def __init__(self) -> None:
        pass

    def keygen(self):
        #Decryption key generation
        print("Generating keys")
        curve = registry.get_curve('brainpoolP256r1')

        privKey = secrets.randbelow(curve.field.n)
        pubKey = privKey * curve.g

        return privKey, pubKey

        # pickle.dump(pubKey, open(dir+'/public_key.pem', 'wb'))

        # pickle.dump(privKey, open(dir+'/private_key.pem', 'wb'))


            
    #Decryption
    # def ecc_calc_decryption_key(self, privKey, ciphertextPubKey):
    #     sharedECCKey = ciphertextPubKey * privKey
    #     return sharedECCKey

    def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
        aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
        plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
        return plaintext

    def ecc_point_to_256_bit_key(point):
        sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
        sha.update(int.to_bytes(point.y, 32, 'big'))
        return sha.digest()

    def decrypt_ECC(encryptedMsg, privKey):
        (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
        sharedECCKey = privKey * ciphertextPubKey
        secretKey = Decryption.ecc_point_to_256_bit_key(sharedECCKey)
        plaintext = Decryption.decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
        return plaintext

    def large_AES(secretKey, nonce):
        aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
        return (aesCipher)

    def large_keyGen(privKey, ciphertextPubKey):
        sharedECCKey = privKey * ciphertextPubKey
        secretKey = Decryption.ecc_point_to_256_bit_key(sharedECCKey)
        #print(f'secret key: {secretKey}')
        return (secretKey)

    def large_decrypt_ECC(block, aesCipher):
        plaintext = aesCipher.decrypt(block)
        return plaintext

    def large_verify(aesCipher, authTag):
        aesCipher.verify(authTag)
        print('Verify complete')
        return True

    # def decrypt(dir):
    #     privKey = pickle.load(open(dir+'/private_key.pem', 'rb'))
    #     #sharedECCKey = Decryption.ecc_calc_decryption_key

    #     #encryptedMsg = pickle.load(open('BC_data/hashes.txt', 'rb'))

    #     #decryptedMsg = decrypt_ECC(encryptedMsg, privKey)

    #     #dir1 = os.path.dirname(os.path.realpath(__file__))
    #     #dir1 = '/home/seth/Desktop'
    #     testFiles = '/testFiles/'
    #     print("Decrypting Data")
    #     #ext = 'txt'

    #     for file in sorted(os.listdir(dir+testFiles)):
    #         #if file.endswith(ext):
    #         dec_file = dir+testFiles+file
    #         encryptedMsg = pickle.load(open(dec_file, 'rb'))
    #         decryptedMsg = Decryption.decrypt_ECC(encryptedMsg, privKey)
    #         with open(dec_file, 'wb') as dec:
    #             dec.write(decryptedMsg)    

    #     #with open('BC_data/hashes.txt', 'wb') as dec_file:
    #     #    dec_file.write(decryptedMsg)
    #     print("Decryption Complete")

    def verify():
        #Data Hash Verification
        wd = os.path.dirname(os.path.realpath(__file__))
        #wd = '/home/seth/Desktop/'
        #wd1 = '/home/seth/Desktop/testFiles'
        #wd = '/home/seth/Desktop/Demo/socket_communication/client/'
        #wd = os.path.dirname(os.path.realpath(__file__)) #Use this for python files
        #wd = os.getcwd() #Use this for jupyter notebooks
        #dataloc = '/testFiles/'
        #dir = wd + dataloc
        old_file = 'blocks_folder/blockhash.txt'

        #ver = 'b3sum --check '+dir+old_file
        ver = 'b3sum --check '+wd+'/'+old_file
        cmd2 = 'cd '+wd+'/blocks_folder/; '+ver
        proc2 = subprocess.run(cmd2, shell=True)
        #cmd3 = 'python3 create_tx.py'
        #proc3 = subprocess.run(cmd3, shell=True)
