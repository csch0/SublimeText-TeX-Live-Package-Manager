import sublime, sublime_plugin

import os.path, shutil

class TlmgrClearCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.view.erase(edit, sublime.Region(0, self.view.size()))

class TlmgrAppendTextCommand(sublime_plugin.TextCommand):

	def run(self, edit, string):
		read_only = self.view.is_read_only()
		self.view.set_read_only(False)
		self.view.insert(edit, self.view.size(), string.replace("\r\n", "\n"))
		self.view.set_read_only(read_only)

		# Scroll to the end
		self.view.show(self.view.size())

def tlmgr_executable():
	s = sublime.load_settings("TeX Live Package Manager.sublime-settings")
	for item in s.get("tlmgr_executable", "tlmgr"):
		if hasattr(shutil, 'which'):
			cmd = shutil.which(item)
		elif os.path.isfile(item):
			cmd = item
		else:
			cmd = None
		if cmd:
			return cmd
	return "tlmgr"
