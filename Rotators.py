# Rotators.py

# Implements the rotation method three different ways.

from copy import copy


def Swap(array, left, right):
	temp = copy(array[left])
	array[left]=copy(array[right])
	array[right]=temp
	yield 1


def ReverseAll(array, shift):
	yield from Reverse(array, 0, len(array))

def Reverse(array, start, finish):
	finish -= 1
	while start<finish:
		yield from Swap(array, start, finish)
		start += 1
		finish -= 1


def ReverseRotation(array, shift):
	yield from Reverse(array, 0, len(array))
	shift = len(array)-shift
	yield from Reverse(array, 0, shift)
	yield from Reverse(array, shift, len(array))
