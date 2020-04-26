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


def SwapRange(array, start, finish, otherStart):
	while start<finish:
		yield from Swap(array, start, otherStart)
		start=start+1
		otherStart=otherStart+1

def RotateSwap(array, start, finish, shift):
	if shift==0:
		return
	if start==finish:
		return
	if shift==finish-start:
		return
	if shift <= (finish-start)/2:
		yield from SwapRange(array, start, start+shift, start+shift)
		yield from RotateSwap(array, start+shift, finish, shift)
	else:
		rangeSize = (finish-start)-shift
		yield from SwapRange(array, start, start+rangeSize, start+shift)
		yield from RotateSwap(array, start+rangeSize, finish, shift-rangeSize)
	return

def SwapRotation(array, shift):
	yield from RotateSwap(array, 0, len(array), shift)
