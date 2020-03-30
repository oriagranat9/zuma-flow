from Handlers import ScreenHandler, MemoryHandler

screen = ScreenHandler.ScreenCapture('chrome.exe', show_image=True)
# memory_reader = MemoryHandler.MemoryReader("'Zuma Deluxe 1.1.0.0'")
while True:
    # print(memory_reader.read_pointer(0x0005C290, [0x34, 0xd8, 0x4, 0x170, 0x108, 0x8, 0xE8]))
    screen.get_image()
    # out = [1,1,1,0] #['x','y','lc','rc']
    '''
	out meaning:
    x/y - percantages of screen width/hight (from top left) (position = length * node)
	lc - bool for left clicking
	rc - bool for right clicking
	(bool = node > 0.5)
    '''

    '''
	out logic:
    if 'rc':
	    right click

    if 'lc':
        set mouse position (x,y)
		left click
    '''