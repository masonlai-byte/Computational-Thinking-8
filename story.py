place = input("You wake up. Where do you go today? The mall or the beach: ").strip().lower()

if "mall" in place:
  print("You spend money on new shoes and pretzels.")
elif "beach" in place:
  print("You get sand in your shoes and swim in the ocean.")
else:
  print("You stay home and sleep all day.")