# Imports
import numpy as np

def is_binary_number(input_str):
    # Check if the input string consists only of 0s and 1s
    if all(bit in '01' for bit in input_str):
        return True
    else:
        return False

def get_binary_input():
    while True:
        binaryText = input("Enter a binary number: ")
        if is_binary_number(binaryText):
            return binaryText
        else:
            print(f"Invalid input. '{binaryText}' is not a binary number. Please try again.")

def get_integer_input(prompt, min_value = 1):
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


# Functions of hamming code-------------------------------------------
def emitter_converter(size_par, data):
    """
    :param size_par: how many parity bits the message must have
    :param data:  information bits
    :return: message to be transmitted by unreliable medium
            - bits of information merged with parity bits

    >>> emitter_converter(4, "101010111111")
    ['1', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1', '1', '1', '1', '1', '1']
    >>> emitter_converter(5, "101010111111")
    Traceback (most recent call last):
        ...
    ValueError: size of parity don't match with size of data
    """
    if size_par + len(data) <= 2**size_par - (len(data) - 1):
        raise ValueError("size of parity don't match with size of data")

    data_out = []
    parity = []
    bin_pos = [bin(x)[2:] for x in range(1, size_par + len(data) + 1)]

    # sorted information data for the size of the output data
    data_ord = []
    # data position template + parity
    data_out_gab = []
    # parity bit counter
    qtd_bp = 0
    # counter position of data bits
    cont_data = 0

    for x in range(1, size_par + len(data) + 1):
        # Performs a template of bit positions - who should be given,
        # and who should be parity
        if qtd_bp < size_par:
            if (np.log(x) / np.log(2)).is_integer():
                data_out_gab.append("P")
                qtd_bp = qtd_bp + 1
            else:
                data_out_gab.append("D")
        else:
            data_out_gab.append("D")

        # Sorts the data to the new output size
        if data_out_gab[-1] == "D":
            data_ord.append(data[cont_data])
            cont_data += 1
        else:
            data_ord.append(None)

    # Calculates parity
    qtd_bp = 0  # parity bit counter
    for bp in range(1, size_par + 1):
        # Bit counter one for a given parity
        cont_bo = 0
        # counter to control the loop reading
        cont_loop = 0
        for x in data_ord:
            if x is not None:
                try:
                    aux = (bin_pos[cont_loop])[-1 * (bp)]
                except IndexError:
                    aux = "0"
                if aux == "1" and x == "1":
                    cont_bo += 1
            cont_loop += 1
        parity.append(cont_bo % 2)

        qtd_bp += 1

    # Mount the message
    cont_bp = 0  # parity bit counter
    for x in range(size_par + len(data)):
        if data_ord[x] is None:
            data_out.append(str(parity[cont_bp]))
            cont_bp += 1
        else:
            data_out.append(data_ord[x])

    return data_out


def receptor_converter(size_par, data):
    """
    >>> receptor_converter(4, "1111010010111111")
    (['1', '0', '1', '0', '1', '0', '1', '1', '1', '1', '1', '1'], True)
    """
    # data position template + parity
    data_out_gab = []
    # Parity bit counter
    qtd_bp = 0
    # Counter p data bit reading
    cont_data = 0
    # list of parity received
    parity_received = []
    data_output = []

    for x in range(1, len(data) + 1):
        # Performs a template of bit positions - who should be given,
        #  and who should be parity
        if qtd_bp < size_par and (np.log(x) / np.log(2)).is_integer():
            data_out_gab.append("P")
            qtd_bp = qtd_bp + 1
        else:
            data_out_gab.append("D")

        # Sorts the data to the new output size
        if data_out_gab[-1] == "D":
            data_output.append(data[cont_data])
        else:
            parity_received.append(data[cont_data])
        cont_data += 1

    # -----------calculates the parity with the data
    data_out = []
    parity = []
    bin_pos = [bin(x)[2:] for x in range(1, size_par + len(data_output) + 1)]

    #  sorted information data for the size of the output data
    data_ord = []
    # Data position feedback + parity
    data_out_gab = []
    # Parity bit counter
    qtd_bp = 0
    # Counter p data bit reading
    cont_data = 0

    for x in range(1, size_par + len(data_output) + 1):
        # Performs a template position of bits - who should be given,
        # and who should be parity
        if qtd_bp < size_par and (np.log(x) / np.log(2)).is_integer():
            data_out_gab.append("P")
            qtd_bp = qtd_bp + 1
        else:
            data_out_gab.append("D")

        # Sorts the data to the new output size
        if data_out_gab[-1] == "D":
            data_ord.append(data_output[cont_data])
            cont_data += 1
        else:
            data_ord.append(None)

    # Calculates parity
    qtd_bp = 0  # parity bit counter
    for bp in range(1, size_par + 1):
        # Bit counter one for a certain parity
        cont_bo = 0
        # Counter to control loop reading
        cont_loop = 0
        for x in data_ord:
            if x is not None:
                try:
                    aux = (bin_pos[cont_loop])[-1 * (bp)]
                except IndexError:
                    aux = "0"
                if aux == "1" and x == "1":
                    cont_bo += 1
            cont_loop += 1
        parity.append(str(cont_bo % 2))

        qtd_bp += 1

    # Mount the message
    cont_bp = 0  # Parity bit counter
    for x in range(size_par + len(data_output)):
        if data_ord[x] is None:
            data_out.append(str(parity[cont_bp]))
            cont_bp += 1
        else:
            data_out.append(data_ord[x])

    ack = parity_received == parity
    return data_output, ack


# Message/word to be encoded and decoded with hamming
binaryText = get_binary_input()

# number of parity bits
sizePari = get_integer_input("Enter the size of parity bit: ")

# location of the bit that will be forced an error
be = get_integer_input("Enter the location of the bit that will be forced an error: ")

# Prints the binary of the string
print("Input in binary is '" + binaryText + "'")

# total transmitted bits
totalBits = len(binaryText) + sizePari
print("Size of data is " + str(totalBits))

print("\n --Message exchange--")
print("Data to send ------------> " + binaryText)
dataOut = emitter_converter(sizePari, binaryText)
print("Data converted ----------> " + "".join(dataOut))
dataReceiv, ack = receptor_converter(sizePari, dataOut)
print(
    "Data receive ------------> "
    + "".join(dataReceiv)
    + "\t\t -- Data integrity: "
    + str(ack)
)


print("\n --Force error--")
print("Data to send ------------> " + binaryText)
dataOut = emitter_converter(sizePari, binaryText)
print("Data converted ----------> " + "".join(dataOut))

# forces error
dataOut[-be] = "1" * (dataOut[-be] == "0") + "0" * (dataOut[-be] == "1")
print("Data after transmission -> " + "".join(dataOut))
dataReceiv, ack = receptor_converter(sizePari, dataOut)
print(
    "Data receive ------------> "
    + "".join(dataReceiv)
    + "\t\t -- Data integrity: "
    + str(ack)
)