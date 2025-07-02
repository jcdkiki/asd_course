import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--shift', type=int)
    args = parser.parse_args()
    
    SHIFT = args.shift
    
    # Ваш код, использующий SHIFT
    print(SHIFT * int(input()))

if __name__ == "__main__":
    main()