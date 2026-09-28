answer1 = input("Hey! The weather seems nice. Do you want to head out to the park? (yes/no/maybe): ")

if answer1.lower() == "yes":
    answer2 = input("Awesome! While we are there, do you want to play some sports? (yes/no/maybe): ")
    
    if answer2.lower() == "yes":
        sport = input("Cool, I have some gear packed. Do you want to play soccer, basketball, or tennis?: ").lower()
        if sport in ["soccer", "basketball"]:
            print(f"Awesome choice! Let's grab the ball and go play some {sport}.")
        elif sport == "tennis":
            print("Sweet! I will grab the rackets and the net.")
        else:
            print(f"Sounds fun! Let's go try to play some {sport}.")
            
    elif answer2.lower() == "maybe":
        print("We can bring a Frisbee just in case we change our minds.")
        
    else:
        answer3 = input("No worries, we can just relax. Do you want to do a sleepover later tonight instead? (yes/no/maybe): ")
        if answer3.lower() == "yes":
            answer4 = input("Sounds great! wanna stay up all night? (yes/no/maybe): ")
            if answer4.lower() == "yes":
                print("Time to grind rankkkkkkkkk!")
            elif answer4.lower() == "maybe":
                print("We will see how much energy we have left.")
            else:
                print("So lame vro.")
        elif answer3.lower() == "maybe":
            print("Let's see how tired we feel later tonight.")
        else:
            print("Sounds good! We can just hang out at the park for a bit.")

elif answer1.lower() == "maybe":
    print("Let's wait an hour and check the sky again!")

else:
    movie_genre = input("No problem at all! Do you want to watch an action movie, a comedy, or horror?: ").lower()
    if movie_genre in ["action", "comedy"]:
        print(f"Awesome choice! We will pop some popcorn and get a great {movie_genre} movie ready.")
    elif movie_genre == "horror":
        print("Spooky choice! Let's lock the doors and turn off all the lights.")
    else:
        print(f"Sounds fun! Let's watch some {movie_genre} and stay cozy.")
