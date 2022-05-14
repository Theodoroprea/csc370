import sys

def find_Percentage(argument):
	myList = [["2022-01-28", "Assignment 1 - 20%"],["2022-02-18", "Assignment 2 - 20%"],["2022-03-18", "Assignment 3 -20%"],["2022-04-08","Assignment 4 -20%"], ["2022-01-21", "Quiz 1 - 5%"], ["2022-02-11", "Quiz 2 - 5%"], ["2022-03-11", "Quiz 3 - 5%"], ["2022-04-01","Quiz 4 - 5%"], ["2022-01-10", "Course Start"], ["2022-04-29", "Course End"], ["dropdate100","2022-01-30"], ["dropdate50","2022-02-13"], [["dropdate0","	2022-02-28"]]]
	for i in myList:
		if(argument	== i[0]):
			print(i[1])
			break


if(len(sys.argv) == 1):
	print("Please enter a valid date or dropdate100, dropdate50 or dropdate0 to see the dates at which 100%, 50% and 0% of fees are returned.")
else:
	find_Percentage(sys.argv[1])