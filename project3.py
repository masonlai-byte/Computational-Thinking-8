Travaling_points = 0
Sports_points = 0 
gaming_points = 0 
napping_points = 0

answer1 = input ("do you want to A play Soccer, B go to Mexico, C play Rocket League D sleep")
if answer1 == "B":
    Travaling_points += 1
elif answer1 == "A":
    Sports_points += 1
elif answer1 == "C":
    gaming_points += 3
    # No bais here ;)
elif answer1 == "D":
    napping_points +=1
answer2 = input ("Do you, A like being active outside, B Like screens and the unatral dopamine it gives you, C Likes views from planes, D Like your dreams.")
if answer2 == "D":
    napping_points += 1
elif answer2 == "B":
    gaming_points += 3
    # Again, no bais a all
elif answer2 == "A":
    Sports_points += 1
elif answer2 == "C":
    Travaling_points += 1
answer3 = input ("Do you like, A Fresh air, B Inside your room air C High altitude air D cold air")
if answer3 == "D":
    napping_points += 1
elif answer3 == "B":
    gaming_points += 3
    
elif answer3 == "A":
    Sports_points += 1
elif answer3 == "C":
    Travaling_points += 1
answer4 = input ("Do you, A touch grass, B Touch 3D printed grass, C Like plane food, D have a cold pilow ")
if answer4 == "D":
    napping_points += 1
elif answer4 == "B":
    gaming_points += 3
    
elif answer4 == "A":
    Sports_points += 1
elif answer4 == "C":
    Travaling_points += 1
answer5 = input ("Do you like, A Using yor brain for storts, B Using your brain for strategy games, C exploring new places, D Having Lucid dreams.")
if answer4 == "D":
    napping_points += 1
elif answer4 == "B":
    gaming_points += 3
    
elif answer4 == "A":
    Sports_points += 1
elif answer4 == "C" or "c":
    Travaling_points += 1

if Sports_points > Travaling_points and Sports_points > gaming_points and Sports_points > napping_points:
    print ("You are a sports player, nice, you probably like being outside!")
if Travaling_points > Sports_points and Travaling_points > gaming_points and Travaling_points > napping_points:
    print ("You are a travaler") 
if gaming_points > Sports_points and gaming_points > Travaling_points and gaming_points > napping_points:
    print ("You are a gamer")     
if napping_points > Sports_points and napping_points > gaming_points and napping_points > Travaling_points:
    print ("You must love sleep!")