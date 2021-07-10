from enum import IntEnum


class WindowHandle(IntEnum):
    Login_Win = 0
    Register_Win = 1
    Main_Win = 2


class Communicate:
    def communicate(self, window_handles):
        print("We're here")
        self.handles = window_handles
