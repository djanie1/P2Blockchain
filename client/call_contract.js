var abi = [
	{
		"inputs": [],
		"name": "get",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "og_blk_number",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "og_blkhash",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "og_channel_ID",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "og_prevhash",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "og_timestamp",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "og_tx_creator",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "og_tx_id",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "tx_lists",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "tx_nums",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "channel",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "stamp",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "tx_id",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "creator",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "blkhash",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "blknumber",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "prevhash",
				"type": "string"
			}
		],
		"name": "set",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "tx_list",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
];

var address = "0xc861faf0a79f73b7f3dc3b83f877ef23b3a9a5f5";
var updater = eth.contract(abi).at(address)
eth.defaultAccount=eth.accounts[0]

loadScript('blocks_folder/transactions.js');
console.log(data1)
updater.set(data1,data2,data3,data4,data5,data6,data7,data8,data9);
//miner.setEtherbase(eth.accounts[0])
//miner.start()
