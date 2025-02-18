import os
import subprocess, shutil

def splitter(string: str):
    newString = string.split(' ')
    return newString[0]

def gen_hash():
    #Generate hashes
    print("Generating hashes")
    old_file = 'blockhash.txt'
    new_file = 'blockhash_old.txt'
    blk_loc = 'blocks_folder/'   #blocks directory
    files = os.listdir(blk_loc)

    #dir = 'BC_data/'
    #dir = '/home/seth/Desktop/'
    real_path = os.path.dirname(os.path.realpath(__file__))
    #ext = 'bin'
    #testFiles = '/testFiles'

    try:
        open(old_file, 'x')
    except FileExistsError:
        if os.path.exists(new_file):
            os.remove(new_file)
            os.rename(old_file, new_file)
            open(old_file, 'x')
        else:
            os.rename(old_file, new_file)
            open(old_file, 'x')

    with open(old_file, "a") as hashfile:
        for file in sorted(files):
            #if file.endswith(ext):
            location = real_path+'/'+blk_loc+file
            cmd = (['b3sum', location])
            proc = subprocess.check_output(cmd)
            newProc = proc.decode()
            hash = splitter(newProc)
            hashfile.write(hash+"  "+file+"\n")
            
    shutil.move(old_file, blk_loc+old_file)  #blocks directory
    #os.rename(old_file, blk_loc+old_file)
    #os.replace(old_file, blk_loc+old_file)

gen_hash()
