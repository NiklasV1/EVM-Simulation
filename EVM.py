
def parse_storage(raw_storage: str) -> dict:
    if raw_storage == ' ':
        return {}
    # TODO implement

def parse_world_state(raw_state: str) -> dict:
    contracts = raw_state.split('x')
    world_state = {}
    
    for contract in contracts:
        if contract == '':
            continue
        
        contract_fields = contract.split(';')
        world_state.update({contract_fields[0]: {
            "nonce": contract_fields[1],
            "balance": contract_fields[2],
            "storage": parse_storage(contract_fields[3]),
            "code": contract_fields[4],
            "code_hash": contract_fields[5],
        }})
        
    return world_state
        

def revert():
    print("Call reverted!")
    exit(1)
    
def unimplemented(opcode: str):
    print(f"Opcode: {opcode} is currnetly unimplemented!")
    revert()


if __name__ == "__main__":
    
    world_state = {}
    
    
    # * Read input parameters
        
    
    # * Read most recent world state
    with open("./WorldState.txt", 'r') as world_state_file:
        world_state = parse_world_state(world_state_file.readlines()[-1])
        
    print(world_state)
