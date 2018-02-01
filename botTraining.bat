REM @echo off

for /l %%g in (0, 1, 99) do (
	for /l %%s in (0, 1, 49) do (
		C:\ProgramData\Anaconda3\python C:\Users\alexa\Documents\PythonProjects\TestJeux\TrainBot.py --generation=%%g --specie=%%s
	)
	C:\ProgramData\Anaconda3\python C:\Users\alexa\Documents\PythonProjects\TestJeux\createNewGeneration.py --generation=%%g
)

pause