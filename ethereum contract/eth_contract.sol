// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;
// data storage

contract UpdateLedger{
    
    struct transx{
        string value;
        uint num;
    }
    transx[] public tx_list;
    string public og_channel_ID;
    string public og_timestamp;
    string public og_tx_id;
    string public og_tx_creator;
    uint public tx_num;
    
    string public og_blkhash;
    uint public og_blk_number;
    string public og_prevhash;


    function set(string[] memory tx_lists, uint tx_nums, string memory channel, string memory stamp, string memory tx_id, string memory creator, string memory blkhash, uint blknumber, string memory prevhash) public{
        tx_num = tx_nums;
        og_blk_number = blknumber;
        for (uint i = 0; i < tx_num; i++){
            transx memory newTx = transx(tx_lists[i], og_blk_number);
            tx_list.push(newTx);
        }
        og_channel_ID = channel;
        og_timestamp = stamp;
        og_tx_id = tx_id;
        og_tx_creator = creator;
        og_blkhash = blkhash;
        og_blk_number = blknumber;
        og_prevhash = prevhash;
    }

    function get() public view returns (transx [] memory, string memory, string memory, string memory, string memory, string memory, string memory){
        return (tx_list, og_channel_ID, og_timestamp, og_tx_id, og_tx_creator, og_blkhash, og_prevhash);        
    }

}