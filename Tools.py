import sublime, sublime_plugin

class TlmgrClearCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.view.erase(edit, sublime.Region(0, self.view.size()))


class TlmgrAppendTextCommand(sublime_plugin.TextCommand):

	def run(self, edit, string):
		read_only = self.view.is_read_only()
		self.view.set_read_only(False)
		self.view.insert(edit, self.view.size(), string)
		self.view.set_read_only(read_only)

		# Scroll to the end
		self.view.show(self.view.size())