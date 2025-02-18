#!/bin/bash
start=`date +%s%N`
python3 client.py
#end=`date +%s%N`
#echo "Execution time was `expr $end - $start` nanoseconds." >> time/down1_time.txt
python3 main.py blocks_folder.torrent
#./decode_block.sh
#python3 create_tx.py
end=`date +%s%N`
echo "Execution time was `expr $end - $start` nanoseconds." >> time/down1_time.txt
creat=`date +%s%N` 
python3 create_tx.py
endcr=`date +%s%N`
echo "Execution time was `expr $endcr - $creat` nanoseconds." >> time/txn_cr_time.txt
#fuser -k 8469/udp
#python3 serve.py
