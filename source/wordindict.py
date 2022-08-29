import enchant
d = enchant.Dict("en_GB")


x = d.suggest('app-y')


x = d.suggest('-lal--')
print(x)