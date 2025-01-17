from string import Template

ss = {'token': 'eyJ0eXAiOiJKIjYxMjQwNjYyNzE5NjQ1NjQ5NjQzIiwiaW'}
url = 'https://api.mind.com/v1/customers?token=${token}'
print(Template(url).substitute(ss))
