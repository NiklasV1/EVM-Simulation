
def parse_storage(raw_storage: str) -> dict:
    # TODO implement
    pass


def parse_code(raw_code: str) -> list:
    # TODO implement
    pass


class AccountStorage:

    isEmpty:    bool
    values:     dict

    def __init__(self, storage_string: str):
        if storage_string == 'X':
            self.isEmpty = True
            self.values = {}
        else:
            self.isEmpty = False
            self.values = parse_storage(storage_string)

    def __str__(self):
        if self.isEmpty:
            return 'X'
        # TODO
        return "storage"


class AccountCode:

    isEmpty:    bool
    bytecode:   list

    def __init__(self, bytecode_string: str):
        if bytecode_string == 'X':
            self.isEmpty = True
            self.bytecode = []
        else:
            self.isEmpty = False
            self.bytecode = parse_code(bytecode_string)

    def __str__(self):
        if self.isEmpty:
            return 'X'
        return ''.join(self.bytecode)


class Account:

    address:    str
    nonce:      int
    balance:    int
    storage:    AccountStorage
    code:       AccountCode
    code_hash:  str

    def __init__(self,
                 address:           str,
                 nonce:             int,
                 balance:           int,
                 storage_string:    str,
                 bytecode_string:   str,
                 code_hash:         str):

        self.address = address
        self.nonce = nonce
        self.balance = balance
        self.storage = AccountStorage(storage_string)
        self.code = AccountCode(bytecode_string)
        self.code_hash = code_hash

    def __str__(self):
        return f"Address: {self.address}, " +\
            f"Nonce: {self.nonce}, " +\
            f"Balance: {self.balance}, " +\
            f"Storage: {self.storage}, " +\
            f"Code: {self.code}, " +\
            f"Code Hash: {self.code_hash}"


def parse_account(line: str) -> Account:
    account_fields = line.split(';')

    return Account(account_fields[0],       # Address
                   int(account_fields[1]),  # Nonce
                   int(account_fields[2]),  # Balance
                   account_fields[3],       # Storage
                   account_fields[4],       # Code
                   account_fields[5],       # CodeHash
                   )


def read_world_state() -> dict:
    # TODO update
    try:
        with open("./Current-World-State-Number.txt", "r") as number_file:
            number = int(number_file.read())

        with open(f"./World-States/State_{number}.csv", "r") as state_file:
            lines = [line.strip() for line in state_file.readlines()]

        accounts = [parse_account(line) for line in lines[1:] if len(line) > 0]
        world_state = {account.address: account for account in accounts}

        return world_state, number

    except Exception as exception:
        revert(f"Failed to load world state!\nException: {exception}")

    else:
        print("World state loaded successfully.")


def revert(message: str):
    print(message)
    print("Call reverted!")
    exit(1)


def unimplemented(opcode: str):
    revert(f"Opcode: {opcode} is currently unimplemented!")


def print_world_state(number: int):
    print(f"World state {number}:")
    for account in world_state.values():
        print(str(account))
    print()


def is_account(address: str) -> bool:
    return world_state.get(address) is not None


def is_eoa(address: str) -> bool:
    if not is_account(address):
        return False
    account: Account = get_account(address)

    if not account.code.isEmpty:
        return False

    return True


def get_account(address: str) -> Account:
    account: Account = world_state.get(address)
    if not account:
        revert("Account does not exist!")
    return account


def get_eoa(address: str) -> Account:
    account: Account = get_account(address)

    if not account.code.isEmpty:
        revert("Account is not externally owned!")

    return account


def get_balance(address: str) -> int:
    account: Account = get_account(address)
    return account.balance


def check_balance(address: str, value: int):
    if get_balance(address) < value:
        revert("Balance too low!")


def write_world_state(number: int):
    print_world_state(number)
    # TODO implement
    pass


def transfer_ether(sender: str, receiver: str, value: int):
    sender_account: Account = get_eoa(sender)
    receiver_account: Account = get_eoa(receiver)

    sender_account.balance -= value
    receiver_account.balance += value
    print(f"Transfered {value} from {sender} to {receiver}.\n")


def call_contract():
    # TODO
    print("Called contract TODO.\n")


def create_eoa():
    # TODO
    print("Created new externally owned account at TODO.\n")


def create_contract():
    # TODO
    print("Created new contract at TODO.\n")


def transaction(sender:     str,
                receiver:   str,
                value:      int,
                calldata:   str,
                gas:        int):

    # Check sender validity (exists and is EOA)
    sender_account: Account = get_eoa(sender)

    # Set transaction origin address
    tx_origin: str = sender

    # Check sender balance
    check_balance(sender, value)

    # TODO implement gas usage

    # Call to account
    if is_account(receiver):

        # Ether transfer    (EOA to EOA)
        if is_eoa(receiver):
            transfer_ether(sender, receiver, value)

        # Call Contract     (abi encoded calldata)
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
    sender_account.nonce += 1


if __name__ == "__main__":

    # * Read input parameters
    # Parameter format: --param_name=param_value
    # Parameters:
    # from:     address     |   Sender account address (must be EOA)
    # to:       address     |   Receiver address
    # value:    int         |   Ether amount in Wei
    # data:     str         |   Calldata string (optional)
    # gas:      int         |   Maximum amount of gas for the transaction

    i_from = "0x4838b106fce9647bdf1e7877bf73ce8b0bad5f40"
    i_to = "0x2056b106fce9647bdf1e7877bf73ce8b0bad5f40"
    i_value = 10
    i_data = ""
    i_gas = 0

    # TODO implement CLI input parameters
    # TODO implement input validation

    # * Read most recent world state
    global world_state
    global world_state_number

    world_state, world_state_number = read_world_state()

    if not world_state:
        revert("Loading world state failed!")

    print_world_state(world_state_number)

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
    world_state_number += 1
    write_world_state(world_state_number)
