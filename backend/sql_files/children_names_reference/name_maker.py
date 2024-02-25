from random import randint

name_file = open("names", "r")
name = name_file.readlines()
name_file.close()
names = []
for n in name:
    names.append(n.strip())
name.clear()


# Assuming you have a list containing 20 empty lists
empty_lists = [[] for _ in range(20)]

# Calculate how many names each list should receive
names_per_list = len(names) // len(empty_lists)

# Iterate through the empty lists and assign names to each
for i, empty_list in enumerate(empty_lists):
    start_index = i * names_per_list
    end_index = start_index + names_per_list
    empty_list.extend(names[start_index:end_index])

# If there are any remaining names, distribute them evenly among the lists
remaining_names = len(names) % len(empty_lists)
for i in range(remaining_names):
    empty_lists[i].append(names[names_per_list * len(empty_lists) + i])

class_id = 1
for classroom in empty_lists:
    print(f"-- Class {class_id}")
    for name in classroom:
        # INSERT INTO CHILD (CHILD_FNAME, CHILD_LNAME, CHILD_AGE, CLASS_ID) VALUES ('Lucas', 'Jackson', 6, 13);
        first = name.split(" ")[0]
        last = name.split(" ")[1]

        print(f"INSERT INTO CHILD (CHILD_FNAME, CHILD_LNAME, CHILD_AGE, CLASS_ID) VALUES ('{first}', '{last}', {randint(5,7)}, {class_id});")
    class_id += 1
    print()


