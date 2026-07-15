
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
    
from src.mycalpkg.gamepkg import main as game_main

def main():
    print("Hello, World!")
    game_main()

if __name__ == "__main__":
    main()