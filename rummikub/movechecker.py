def first_move_checker(move):
  numbers = 0
  for m in move:
    print(m.number)
    numbers += m.number
  if numbers < 30:
    return False
  else:
    return True