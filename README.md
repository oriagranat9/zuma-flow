# zuma-flow
Ai learns to play zuma

 out = [1,1,1,0] #['x','y','lc','rc']
   
	out meaning:
    x/y - percantages of screen width/hight (from top left) (position = length * node)
	lc - bool for left clicking
	rc - bool for right clicking
	(bool = node > 0)
    '''

    '''
	out logic:
    if 'rc':
	    right click
    if 'lc':
        set mouse position (x,y)
		left click
    '''