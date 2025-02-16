package main

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/hyperledger/fabric-contract-api-go/contractapi" //init module
)

// SmartContract provides functions for managing an Asset
type SmartContract struct {
	contractapi.Contract
}

// Asset describes basic details of what makes up a simple asset
type Asset struct {
	Hash     string `json:"Hash"`
	ID       string `json:"ID"`
	Location string `json:"Location"`
	Owner    string `json:"Owner"`
}

// InitLedger adds a base set of assets to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	assets := []Asset{
		{ID: "asset1", Hash: "55a782f7a72e8affadb2c0c392c4e78e4f75d9e3a0980f535febbf1850fc87aa", Location: "/home/$USER/data/Results_00001.csv", Owner: "Peer1"},
		{ID: "asset2", Hash: "19e0aa67e60ccf8dcdc6bcb1cc443dd48dd7d9020824b76c1b211e0414ab6ad3", Location: "/home/$USER/data/Results_00002.csv", Owner: "Peer1"},
		{ID: "asset3", Hash: "57c4927c6a3dfc7fb61b2ba0ce974d1681ef1592a7382d807513fbd6e21b1a2b", Location: "/home/$USER/data/Results_00003.csv", Owner: "Peer1"},
		{ID: "asset4", Hash: "f3f93d743cc4244fd702fa0535b46247682f10cc43b96f663298459dd258daff", Location: "/home/$USER/data/Results_00004.csv", Owner: "Peer1"},
		{ID: "asset5", Hash: "a46d145c9697afc921cc3d5bfb6bc57cd421c7deacf233529f7715147ff8ac6c", Location: "/home/$USER/data/Results_00005.csv", Owner: "Peer1"},
		{ID: "asset6", Hash: "cd613f8cd6396da9a29c78742a4e8aca4e4666e6e27f9b4f52be1bcf03ba38bc", Location: "/home/$USER/data/Results_00006.csv", Owner: "Peer1"},
		{ID: "asset7", Hash: "9a96ebcf6bb8521bad11828932ca9e5579f2e9720c9f4b6ac0279b6ab37a589c", Location: "/home/$USER/data/Results_00007.csv", Owner: "Peer1"},
		{ID: "asset8", Hash: "3b20c62a0124a2224c51dc1835405bef25191a32519f5e9f5a993166d56f5338", Location: "/home/$USER/data/Results_00008.csv", Owner: "Peer1"},
		{ID: "asset9", Hash: "d45f45ee505e77cb5951b7cde0c3487142d3e30a54e8cfe8d1564a36b7cba7f1", Location: "/home/$USER/data/Results_00009.csv", Owner: "Peer1"},
		{ID: "asset10", Hash: "3eeace201ed24f73e8d21890588cb5ef0a38a325e2e4d5b05b2669d9ae648dbc", Location: "/home/$USER/data/Results_00010.csv", Owner: "Peer1"},
	}

	for _, asset := range assets {
		assetJSON, err := json.Marshal(asset)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(asset.ID, assetJSON)
		if err != nil {
			return fmt.Errorf("failed to put to world state. %v", err)
		}
	}

	return nil
}

// CreateAsset issues a new asset to the world state with given details.
func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface, id string, hash string, location string, owner string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", id)
	}

	asset := Asset{
		ID:       id,
		Hash:     hash,
		Location: location,
		Owner:    owner,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// ReadAsset returns the asset stored in the world state with given id.
func (s *SmartContract) ReadAsset(ctx contractapi.TransactionContextInterface, id string) (*Asset, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", id)
	}

	var asset Asset
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

// UpdateAsset updates an existing asset in the world state with provided parameters.
func (s *SmartContract) UpdateAsset(ctx contractapi.TransactionContextInterface, id string, hash string, location string, owner string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", id)
	}

	// overwriting original asset with new asset
	asset := Asset{
		ID:       id,
		Hash:     hash,
		Location: location,
		Owner:    owner,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// DeleteAsset deletes an given asset from the world state.
func (s *SmartContract) DeleteAsset(ctx contractapi.TransactionContextInterface, id string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", id)
	}

	return ctx.GetStub().DelState(id)
}

// AssetExists returns true when asset with given ID exists in world state
func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}

// TransferAsset updates the owner field of asset with given id in world state.
func (s *SmartContract) TransferAsset(ctx contractapi.TransactionContextInterface, id string, newOwner string) error {
	asset, err := s.ReadAsset(ctx, id)
	if err != nil {
		return err
	}

	asset.Owner = newOwner
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// GetAllAssets returns all assets found in world state
func (s *SmartContract) GetAllAssets(ctx contractapi.TransactionContextInterface) ([]*Asset, error) {
	// range query with empty string for startKey and endKey does an
	// open-ended query of all assets in the chaincode namespace.
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var assets []*Asset
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var asset Asset
		err = json.Unmarshal(queryResponse.Value, &asset)
		if err != nil {
			return nil, err
		}
		assets = append(assets, &asset)
	}

	return assets, nil
}

func main() {
	assetChaincode, err := contractapi.NewChaincode(&SmartContract{})
	if err != nil {
		log.Panicf("Error creating asset-transfer-basic chaincode: %v", err)
	}

	if err := assetChaincode.Start(); err != nil {
		log.Panicf("Error starting asset-transfer-basic chaincode: %v", err)
	}
}
