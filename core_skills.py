import random

rand_list = [random.randint(1, 20) for i in range(1, 10)]
print(rand_list)

list_comprehension_below_10 = [i for i in rand_list if i < 10]
print(list_comprehension_below_10)

list_comprehension_below_10 = filter(lambda x: x < 10, rand_list)
