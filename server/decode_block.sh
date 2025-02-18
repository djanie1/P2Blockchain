#!/bin/bash
export PATH=$PWD
for file in ../peer3/blocks_folder/*.block
do
    extension=".json"
    folder="blocks_folder/"
    outfile="$folder${file##*/}$extension"
    configtxlator proto_decode --type=common.Block --input="$file" --output="$outfile"
done 
