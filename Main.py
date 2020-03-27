from Handlers import ScreenHandler, MemoryHandler
main_process_name = "chrome"
screen = ScreenHandler.ScreenCapture(main_process_name, show_image=True)
memory_reader = MemoryHandler.MemoryReader(main_process_name)

# memory_reader.read_address()
# screen.get_image()

