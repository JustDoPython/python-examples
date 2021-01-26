from faker import Faker
from faker.providers import BaseProvider

faker = Faker(locale='zh_CN')
print(f'name: {faker.name()}')
print(f'address: {faker.address()}')
print(f'date: {faker.date()}')


class MyProvider(BaseProvider):
    def foo(self):
        return 'bar'


faker.add_provider(MyProvider)
print(f'foo: {faker.foo()}')
