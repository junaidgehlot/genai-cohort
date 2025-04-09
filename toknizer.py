def vocab():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()+-=[]{}|;:',.<>?/ "
    vocab_tokens = {char: ord(char) for char in chars}
    token_vocab = {ascii_val: char for char, ascii_val in vocab_tokens.items()}  
    return vocab_tokens, token_vocab

def encoder(sentence):
    vocab_tokens, _ = vocab()  
    tokens = [vocab_tokens[char] for char in sentence if char in vocab_tokens]
    return tokens

def decoder(tokens):
    _, token_vocab = vocab() 
    sentence = ''.join([token_vocab[token] for token in tokens if token in token_vocab]) 
    return sentence

def start():
    print('Do you want to encode or decode? (type "encode" or "decode")')
    encode_or_decode = input().strip().lower()
    if encode_or_decode == 'encode':
        print('Type text to encode (type "exit" to quit):')
        while True:
            text = input()
            if text.lower() == 'exit':
                break
            print(f"Encoded: {encoder(text)}")
    elif encode_or_decode == 'decode':
        print('Type tokens to decode as a comma-separated list (type "exit" to quit):')
        while True:
            token_input = input()
            if token_input.lower() == 'exit':
                break
            try:
                tokens = list(map(int, token_input.split(',')))
                print(f"Decoded: {decoder(tokens)}")
            except ValueError:
                print("Invalid input. Please enter a comma-separated list of integers.")

start()