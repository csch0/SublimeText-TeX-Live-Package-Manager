import sublime, sublime_plugin

import threading

class ProcessQueueManager():

	__shared = {}

	items = []
	thread = None

	# Current item details
	messages = None
	function = None
	callback = None

	# Progress Bar preferences
	i = 0
	size = 8
	add = 1

	def __new__(cls, *args, **kwargs):
		inst = object.__new__(cls)
		inst.__dict__ = cls.__shared
		return inst

	def queue(self, unique_id, function, messages, callback):
		print(unique_id, function, messages, callback)
		self.items += [{"function": function, "messages": messages, "callback": callback}]

		if not self.thread or not self.thread.is_alive():
			sublime.set_timeout(lambda: self.run(), 100)

	def run(self):

		# If thread available and running
		if self.thread and self.thread.is_alive():
				# Recall run
				self.progress()
				sublime.set_timeout(lambda: self.run(), 100)

		# Stop if thread available, not running and no item is available
		elif self.thread and not self.thread.is_alive() and not self.items:
				sublime.status_message(self.messages[1])

				# Callback
				sublime.set_timeout(self.callback, 0)

				# Reset progress details
				self.i = 0
				self.callback = None
				self.function = None
				self.message = None

		# If no thread availale or not running
		elif not self.thread or not self.thread.is_alive():

			# Check for callback of old item
			if self.callback:
				sublime.set_timeout(self.callback, 0)
				self.callback = None

			# Queue available
			if self.items:
				item = self.items.pop(0)
				self.callback = item["callback"]
				self.function = item["function"]
				self.messages = item["messages"]

				# Start thread for current item
				self.thread = HelperThread(self.function)
				self.thread.start()

				# Call run to start updating progress
				sublime.set_timeout(lambda: self.run(), 100)

	def progress(self):

		# Calculate items on the left size
		before = self.i % self.size
		after = self.size - (before + 1)

		# Print the actual progress
		sublime.status_message('%s [%s=%s]' % (self.messages[0], ' ' * before, ' ' * after))

		# Invert increment if reached the end or start
		if not after:
			self.add =  -1
		elif not before:
			self.add = 1

		self.i += self.add


class HelperThread(threading.Thread):

	def __init__(self, function):
		self.function = function if isinstance(function, list) else [function]
		threading.Thread.__init__(self)

	def run(self):
		for function in self.function:
			function()


def ProgressFunction(function, messages, callback):
	t = ThreadThread(function)
	t.start()
	Progress(t, messages[0], messages[1], callback)