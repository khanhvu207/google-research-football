import consts

def ball_landing(ball, ball_direction):
	start_height = ball[2]
	end_height = consts.PICK_HEIGHT
	start_speed = ball_direction[2]
	time = np.sqrt(start_speed**2/consts.GRAVITY**2 - 2/consts.GRAVITY*(end_height-start_height)) + start_speed/consts.GRAVITY
	return [ball[0]+ball_direction[0]*time, ball[1]+ball_direction[1]*time]