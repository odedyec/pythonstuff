import simpleguitk as simplegui

def downkey():
	global gas
	gas 0.5

def upkey():
	global gas
	gas = 0
	
frame = simplegui.create_frame('NN_driver', 500, 500)
frame.set_canvas_background('White')
frame.set_keydown_handler(downkey)
frame.set_keyup_handler(upkey)

frame.start()
