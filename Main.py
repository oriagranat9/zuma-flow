from Handlers import ScreenHandler, MemoryHandler

# screen = ScreenHandler.ScreenCapture("", show_image=True)
memory_reader = MemoryHandler.MemoryReader("Zuma")

print(memory_reader.read_address(0x0b842d10))
# screen.get_image()
