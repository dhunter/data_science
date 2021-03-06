"""Calculate friendships of users"""
from collections import Counter, defaultdict


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


INTERESTS = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"),
    (2, "Python"), (2, "scikit-learn"), (2, "scipy"), (2, "numpy"),
    (2, "statsmodels"), (2, "pandas"),
    (3, "R"), (3, "Python"), (3, "statistics"), (3, "regression"),
    (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"),
    (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"), (5, "Haskell"),
    (5, "programming languages"),
    (6, "statistics"), (6, "probability"), (6, "mathematics"),
    (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"),
    (8, "neural networks"), (8, "deep learning"), (8, "Big Data"),
    (8, "artificial intelligence"),
    (9, "Hadoop"), (9, "Java"), (9, "MapReduce"), (9, "Big Data")
    ]


SALARIES_AND_TENURES = [
    (83000, 8.7),
    (88000, 8.1),
    (48000, 0.7),
    (76000, 6),
    (69000, 6.5),
    (76000, 7.5),
    (60000, 2.5),
    (83000, 10),
    (48000, 1.9),
    (63000, 4.2)
    ]

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


#  Adding friend of friends functionality
def not_the_same(user, other_user):
    """two users are not the same if they have different ids"""
    return user["id"] != other_user["id"]

def not_friends(user, other_user):
    """other_user is not a friend if they're not in user["friends"];
    that is, if they're not_the_same as all the people in user["friends"]"""
    return all(not_the_same(friend, other_user)
               for friend in user["friends"])

def friend_of_friend_ids(user):
    """Count number of friends' friends"""
    return Counter(foaf["id"]
                   for friend in user["friends"]    # for each of my friends
                   for foaf in friend["friends"]    # count _their_ friends
                   if not_the_same(user, foaf)      # who aren't me
                   and not_friends(user, foaf))     # and aren't my friends.

print(friend_of_friend_ids(USERS[3]))


#  Show number of users who have a common interest, even if not friends.
user_ids_by_interest = defaultdict(list)

for user_id, interest in INTERESTS:
    user_ids_by_interest[interest].append(user_id)


interests_by_user_id = defaultdict(list)

for user_id, interest in INTERESTS:
    interests_by_user_id[user_id].append(interest)


def most_common_interests_with(user):
    """Determine which user has most interests in common with given user"""
    return Counter(interested_user_id
                   for interest in interests_by_user_id[user["id"]]
                   for interested_user_id in user_ids_by_interest[interest]
                   if interested_user_id != user["id"])

print(most_common_interests_with(USERS[3]))


#  Show salary by tenure for data scientists.
def tenure_bucket(tenure):
    if tenure < 2:
        return "less than two"
    elif tenure < 5:
        return "between two and five"
    else:
        return "more than five"


salary_by_tenure_bucket = defaultdict(list)

for salary, tenure in SALARIES_AND_TENURES:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)

average_salary_by_tenure_bucket = {
    tenure_bucket: sum(salary) / len(salary)
    for tenure_bucket, salary in salary_by_tenure_bucket.items()
}

print(average_salary_by_tenure_bucket)
