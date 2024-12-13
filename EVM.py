
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


def get_balance(address: str) -> int:
    account = get_account(address)
    return account.get("balance")


def check_balance(address: str, value: int):
    if get_balance(address) < value:
        revert("Balance too low!")


def saveWorldState():
    # TODO implement
    pass


def transfer_ether(sender: str, receiver: str, value: int):
    sender_account = get_eoa(sender)
    receiver_account = get_eoa(receiver)

    sender_account.update({"balance": get_balance(sender) - value})
    receiver_account.update({"balance": get_balance(receiver) + value})
    print(f"Transfered {value} from {sender} to {receiver}.")


def call_contract():
    # TODO
    pass


def create_eoa():
    # TODO
    pass


def create_contract():
    # TODO
    pass


def transaction(sender:     str,
                receiver:   str,
                value:      int,
                calldata:   str,
                gas:        int):

    # Check sender validity (exists and is EOA)
    sender_account: dict = get_eoa(sender)

    # Set transaction origin address
    tx_origin: str = sender

    # Set nonce
    nonce: int = sender_account.get("nonce")

    # Check sender balance
    check_balance(sender, value)

    # TODO implement gas usage

    # Call to account
    if is_account(receiver):

        # Ether transfer    (EOA to EOA         |   no calldata)
        if is_eoa(receiver):
            transfer_ether()

        # Call Contract     (EOA to contract)   |   abi encoded calldata)
        else:
            call_contract()

    # Call to empty address
    else:
        # Create EOA (no calldata)
        if calldata == "":
            create_eoa()

        # Create Contract (bytecode calldata)
        else:
            create_contract()

    # Increase nonce
    sender_account.update({"nonce": nonce + 1})


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
    # TODO implement input validation

    # * Read most recent world state
    global world_state

    with open("./WorldState.txt", 'r') as world_state_file:
        world_state: dict = parse_world_state(world_state_file.readlines()[-1])

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

    # Make transaction
    transaction(i_from, i_to, i_value, i_data, i_gas)

    # Save new world state
    saveWorldState()
