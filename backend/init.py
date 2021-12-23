from json import loads


with open("config.json", "r") as f:
    config = loads(f.read())

if not config["admin"]["is_setup"]:
    while True:
        password = input("New Admin Password: ").rstrip()
        confirm = input("Confirm Password: ").rstrip()

        if password == confirm:
            print("[~] Creating Admin Account")
            break

