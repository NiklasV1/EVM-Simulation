
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
            "nonce": int(contract_fields[1]),
            "balance": int(contract_fields[2]),
            "storage": parse_storage(contract_fields[3]),
            "code": contract_fields[4],
            "code_hash": contract_fields[5],
        }})

    return world_state


def revert(message: str):
    print(message)
    print("Call reverted!")
    exit(1)


def unimplemented(opcode: str):
    revert(f"Opcode: {opcode} is currnetly unimplemented!")


def is_account(address: str) -> bool:
    return world_state.get(address) is not None


def is_eoa(address: str) -> bool:
    if not is_account(address):
        return False
    account = get_account(address)

    if account.get("code") != ' ':
        return False

    return True


def get_account(address: str) -> dict:
    account = world_state.get(address)
    if not account:
        revert("Account does not exist!")
    return account


def get_eoa(address: str) -> dict:
    account = get_account(address)

    if account.get("code") != ' ':
        revert("Account is not externally owned!")

    return account


if __name__ == "__main__":

    # * Read input parameters
    # Parameter format: --param_name=param_value
    # Parameters:
    # from:     address     |   Sender account address (must be EOA)
    # to:       address     |   Receiver address
    # value:    int         |   Ether amount in Wei
    # data:     str         |   Calldata string (optional)
    # gas:      int         |   Maximum amount of gas for the transaction

    i_from = "4838b106fce9647bdf1e7877bf73ce8b0bad5f40"
    i_to = ""
    i_value = 0
    i_data = ""
    i_gas = 0

    # TODO implement CLI input parameters

    # * Read most recent world state
    global world_state

    with open("./WorldState.txt", 'r') as world_state_file:
        world_state = parse_world_state(world_state_file.readlines()[-1])

    if not world_state:
        revert("Loading world state failed!")

    print(world_state)

    # * Make transaction
    # Required parameters:
    # from:     address     |   Origin address
    # to:       address     |   Receiver address
    # nonce:    int         |   Origin nonce
    # value:    int         |   Ether amount in Wei
    # data:     str         |   Calldata string
    # gas:      int         |   Maximum amount of gas for the transaction

    # Check sender validity (exists and is EOA)
    sender = get_eoa(i_from)

    # Set from
    p_from = i_from

    # Set transaction origin address
    tx_origin = i_from

    # Set to
    p_to = i_to

    # Set nonce
    p_nonce = sender.get("nonce")

    # Check value validity

    # Set calldata

    # set gas

    # Make transaction

    # Increase nonce

    # Save new world state
