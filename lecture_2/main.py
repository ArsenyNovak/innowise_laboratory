def generate_profile(age):
    if 0 <= age <= 12:
        return 'Child'
    if 13 <= age <= 19:
        return 'Teenager'
    if age > 20:
        return 'Adult'


user_name = input('Enter your full name: ')
birth_year_str = input('Enter your birth year: ')
birth_year = int(birth_year_str)

# calculate age
current_age = 2025 - birth_year

hobbies = []

# input and store hobbies
while True:
    hobby = input('Enter a favorite hobby or type "stop" to finish: ')
    if hobby.lower() == 'stop':
        break
    else:
        hobbies.append(hobby)

# determination life stage
life_stage = generate_profile(current_age)

user_profile = {
    'name': user_name,
    'age': current_age,
    'stage': life_stage,
    'hobbies': hobbies
}

# print profile
print(
    f'---\n'
    f'Profile Summary:\n'
    f'Name: {user_profile['name']}\n'
    f'Age: {user_profile['age']}\n'
    f'Life Stage: {user_profile['stage']}'
    )
if hobbies:
    print(f'Favorite Hobbies ({len(user_profile['hobbies'])}):')
    for hobby in user_profile['hobbies']:
        print(f'- {hobby}')
else:
    print('You didn\'t mention any hobbies.')
print('---')

