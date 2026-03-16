from __future__ import annotations
from alfred.cli.commands import handle_command


class AlfredShell:
    def __init__(self, runtime) -> None:
        self.runtime = runtime

    def run(self) -> None:
        print("Alfred ready. Enter 888/999/666, status, consult <topic>, world <topic>, improve <target>, open-chatgpt [topic], tick, exit")
        while True:
            try:
                raw = input("alfred> ")
                result = handle_command(self.runtime, raw)
                if result:
                    print(result)
            except SystemExit:
                print("Exiting Alfred.")
                break
