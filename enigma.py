# Rotors

# Rotor I: EKMFLGDQVZNTOWYHXUSPAIBRCJ
ROTOR_I = [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9]
I_NOTCH = 16  # Q

# Rotor II: AJDKSIRUXBLHWTMCQGZNPYFVOE
ROTOR_II = [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4]
II_NOTCH = 4  # E

# Rotor III: BDFHJLCPRTXVZNYEIWGAKMUSQO
ROTOR_III = [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14]
III_NOTCH = 21  # V

# Rotor IV: ESOVPZJAYQUIRHXLNFTGKDCMWB
ROTOR_IV = [4, 18, 14, 21, 15, 25, 9, 0, 24, 16, 20, 8, 17, 7, 23, 11, 13, 5, 19, 6, 10, 3, 2, 12, 22, 1]
IV_NOTCH = 9  # J

# Rotor V: VZBRGITYUPSDNHLXAWMJQOFECK
ROTOR_V = [21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10]
V_NOTCH = 25  # Z


# Reflectors

# UKW-A: EJMZALYXVBWFCRQUONTSPIKHGD
UKW_A = [4, 9, 12, 25, 0, 11, 24, 23, 21, 1, 22, 5, 2, 17, 16, 20, 14, 13, 19, 18, 15, 8, 10, 7, 6, 3]

# UKW-B: YRUHQSLDPXNGOKMIEBFZCWVJAT
UKW_B = [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19]

# UKW-C: FVPJIAOYEDRZXWGCTKUQSBNMHL
UKW_C = [5, 21, 15, 9, 8, 0, 14, 24, 4, 3, 17, 25, 23, 22, 6, 2, 20, 19, 1, 10, 16, 18, 13, 12, 7, 11]


# Convert character to index
def char_to_index(letter):
    return ord(letter) - 65


# Convert string of characters into list of indexes
def chars_to_index_list(letters):
    return [ord(char) - 65 for char in letters]



# Plugboard Generation
def generate_plugboard(pairs):
    # generate list of numbers 0 -> 25
    plugboard = list(range(26))
    
    if pairs:
        for pair in pairs.upper().split():
            if len(pair) != 2:
                raise ValueError(f"Invalid pair: {pair}")
            
            # number versions of the ASCII characters
            a = char_to_index(pair[0])
            b = char_to_index(pair[1])
            
            # place pairings into the plugboard
            plugboard[a] = b
            plugboard[b] = a

    return plugboard


# Forward move
def rotor_foward(wiring, input_idx, position, ring_setting):
    offset = (position - ring_setting) % 26
    shifted = (input_idx + offset) % 26
    out_idx = wiring[shifted]
    result = (out_idx - offset) % 26
    return result


# Backward move
def rotor_backward(wiring, input_idx, position, ring_setting):
    offset = (position - ring_setting) % 26
    shifted = (input_idx + offset) % 26
    out_idx = wiring.index(shifted)
    result = (out_idx - offset) % 26
    return result


# Encode One letter
def encode_letter(rotors, notches, reflector, starting_positions, ring_settings, index):

    # Step rotors
    mid_at_notch = starting_positions[1] == notches[1]
    right_at_notch = starting_positions[2] == notches[2]

    if mid_at_notch:
        starting_positions[0] += 1
        starting_positions[1] += 1
    if right_at_notch:
        starting_positions[1] += 1
    # right always steps
    starting_positions[2] += 1


    index = rotor_foward(rotors[2], index, starting_positions[2], ring_settings[2])
    index = rotor_foward(rotors[1], index, starting_positions[1], ring_settings[1])
    index = rotor_foward(rotors[0], index, starting_positions[0], ring_settings[0])

    index = reflector[index]

    index = rotor_backward(rotors[0], index, starting_positions[0], ring_settings[0])
    index = rotor_backward(rotors[1], index, starting_positions[1], ring_settings[1])
    index = rotor_backward(rotors[2], index, starting_positions[2], ring_settings[2])

    return index


if __name__ == "__main__":
    out = []
    count = 0

    # Enigma setup
    rotors = [ROTOR_II, ROTOR_III, ROTOR_I]
    notches = [II_NOTCH, III_NOTCH, I_NOTCH]
    reflector = UKW_B
    plugboard = generate_plugboard("BD GF AC OK PE")
    starting_positions = chars_to_index_list("IMD")
    ring_settings = chars_to_index_list("KDM")
    #input_text = "HELLOMYNAMEISTHEO"
    input_text = "VAJBPGKXPBFAXHDIF"

    for char in input_text:
        index = char_to_index(char)
        index = plugboard[index]
        index = encode_letter(rotors, notches, reflector, starting_positions, ring_settings, index)
        index = plugboard[index]
        out.append(chr(index + 65))

        count += 1

        if count % 5 == 0:
            out.append(" ")


    print("".join(out))