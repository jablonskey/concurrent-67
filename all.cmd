echo %1 %2
set /a var = %2 - 1

for /l %%x in (0, 1, %var%) do (
start python client.py %1 %2 %%x)