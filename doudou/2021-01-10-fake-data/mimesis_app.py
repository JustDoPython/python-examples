from mimesis import Person
from mimesis import Address
from mimesis import Food

print("#" * 30 + " person " + "#" * 30)
person = Person('zh')
print(f'name: {person.surname() + "" + person.name()}')
print(f'sex: {person.sex()}')
print(f'academic degree: {person.academic_degree()}')

print("*" * 30 + " person data " + "*" * 30)
print('\n'.join(('%s:%s' % item for item in person._data.items())))

print("#" * 30 + " address " + "#" * 30)
address = Address("zh")
print(f'continent: {address.continent()}')
print(f'province: {address.province()}')
print(f'city: {address.city()}')
print(f'street name: {address.street_name()}')

print("*" * 30 + " address data " + "*" * 30)
print('\n'.join(('%s:%s' % item for item in address._data.items())))

print("#" * 30 + " food " + "#" * 30)
food = Food("zh")
print(f'dish: {food.dish()}')
print(f'drink: {food.drink()}')

print("*" * 30 + " food data " + "*" * 30)
print('\n'.join(('%s:%s' % item for item in food._data.items())))
