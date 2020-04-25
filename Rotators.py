# Rotators.py

# Implements the rotation method three different ways.

from copy import copy


def Swap(array, left, right):
	temp = copy(array[left])
	array[left]=copy(array[right])
	array[right]=temp
	yield 1


def Reverse(array):
	left = 0
	right = len(array)-1
	while left<right:
		yield from Swap(array, left, right)
		left += 1
		right -= 1
