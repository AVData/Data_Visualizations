from wrangle.wrangle import wrangle_function

t_test, p_value, df = wrangle_function('sleepdata')

print(f'T-test: {t_test} \nP-value: {p_value} \nDF-head: {df.head(3)}')
