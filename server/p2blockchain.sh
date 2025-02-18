#!/bin/bash
#start=`date +%s%N`
blk=`date +%s%N`
./Block_fetch.sh
blkend=`date +%s%N`
echo "Execution time was `expr $blkend - $blk` nanoseconds." >> time/up1_blkf_time.txt
start=`date +%s%N`
./decode_block.sh
python3 hashing_files.py
./create_torrent.sh
end=`date +%s%N`
echo "Execution time was `expr $end - $start` nanoseconds." >> time/up1_time.txt
#python3 server.py
python3 main.py blocks_folder.torrent
