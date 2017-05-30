"""Calculate friendships of users"""
USERS = [
    {"id": 0, "name": "Hero"},
    {"id": 1, "name": "Dunn"},
    {"id": 2, "name": "Sue"},
    {"id": 3, "name": "Chi"},
    {"id": 4, "name": "Thor"},
    {"id": 5, "name": "Clive"},
    {"id": 6, "name": "Hicks"},
    {"id": 7, "name": "Devin"},
    {"id": 8, "name": "Kate"},
    {"id": 9, "name": "Klein"}
    ]


FRIENDSHIPS = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]


for user in USERS:
    user["friends"] = []


for i, j in FRIENDSHIPS:
	# this works because users[i] is the user whose id is i
    USERS[i]["friends"].append(USERS[j]) 	# add i as a friend of j
    USERS[j]["friends"].append(USERS[i]) 	# add j as a friend of i


def number_of_friends(user):
    """Determines number of friends each user has"""
    return len(user["friends"])				# length of friend_ids list


total_connections = sum(number_of_friends(user)
                        for user in USERS)	# 24


num_users = len(USERS)
ave_connections = total_connections / num_users  # 2.4


# Create a list (user_id, number_of_friends)
num_friends_by_id = [(user["id"], number_of_friends(user))
						               for user in USERS]

#sorted(num_friends_by_id, key=lambda user_id: num_friends_by_id[0],
#    num_friends_by_id[1])

print(sorted(num_friends_by_id,
             key=lambda num_friends_by_id: num_friends_by_id[1],
             reverse=True))
