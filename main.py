from src.adapters.cli import CLI

if __name__ == "__main__":
    try:
        CLI.hello()
    except ValueError as e:
        print("Ошибка ввода:", e)
