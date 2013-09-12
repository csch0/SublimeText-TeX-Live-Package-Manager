import sublime, sublime_plugin

import functools, re, subprocess, sys

try:
	from .tex_live_package_manager.progress import ProcessQueueManager
	from .tex_live_package_manager.tools import *
except ValueError:
	from tex_live_package_manager.progress import ProcessQueueManager
	from tex_live_package_manager.tools import *

class TlmgrWindowCommand(sublime_plugin.WindowCommand):

	messages = ["Running", "Finished"]
	sudo = None

	def check_sudo(self, callback):
		proc = subprocess.Popen(["sudo", "-p", "", "-S", "id", "-u"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		if self.sudo:
			proc.stdin.write(bytes("%s\n" % self.sudo, sys.getfilesystemencoding()))
		proc.stdin.flush()

		# Capture output
		stdout = proc.communicate()[0].decode(sys.getfilesystemencoding())
		
		if stdout != "0\n":
			def on_done(s):
				self.sudo = s
				self.check_sudo(callback)			
			self.window.show_input_panel("Root Password:", self.sudo if self.sudo else "", on_done, None, None)
		else:
			callback()

	def run(self, **args):
		# Get tlmgr_executable
		self.tlmgr = tlmgr_executable()

		# Get command
		self.cmd = args.get("cmd", [])
		self.info_type = args.get("info_type", "")
		
		# Create output panel
		self.panel = self.window.get_output_panel("tlmgr")

		def on_access():
			manager = ProcessQueueManager()
			manager.queue("tlmgr_manage_collections", lambda: self.run_async(), self.messages, lambda: self.run_post())	

		# Gain sudo access if required
		if sublime.platform() != "windows" and args.get("sudo", False):
			self.check_sudo(on_access)
		else:
			on_access()

	def run_async(self):
		pass

	def run_post(self):
		pass

	def on_data(self, d):
		self.panel.run_command("tlmgr_append_text", {"string": d})


class TlmgrSimpleCommand(TlmgrWindowCommand):

	def run_async(self):

		print()

		if sublime.platform() == "windows":
			# Close consol on windows
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			proc = subprocess.Popen([self.tlmgr] + self.cmd, startupinfo = startupinfo, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		else:
			proc = subprocess.Popen(["sudo", "-S", self.tlmgr] + self.cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
			if self.sudo:
				proc.stdin.write(bytes("%s\n" % self.sudo, sys.getfilesystemencoding()))
			proc.stdin.flush()

		sublime.set_timeout(lambda: self.window.run_command("show_panel", {"panel": "output.tlmgr"}), 0)

		line = "### TeX Live Package Manager ### [%s]\n" % " ".join(self.cmd)
		sublime.set_timeout(functools.partial(self.on_data, line), 0)

		for line in proc.stdout:
			sublime.set_timeout(functools.partial(self.on_data, line.decode(sys.getfilesystemencoding())), 0)

		# Wait for process to finish
		proc.wait()

class TlmgrInfoCommand(TlmgrWindowCommand):

	items = []

	def run_async(self):

		if sublime.platform() == "windows":
			# Close consol on windows
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			proc = subprocess.Popen([self.tlmgr] + self.cmd, startupinfo = startupinfo, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		else:
			proc = subprocess.Popen([self.tlmgr] + self.cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

		# Communicate
		stdout = proc.communicate()[0].decode(sys.getfilesystemencoding())

		self.items = []

		for line in stdout.strip().split("\n"):
			expr = re.search(r"(?P<i>[\si])\s(?P<name>.*):\s(?P<info>.*)", line.rstrip())
			if expr:
				self.items += [{"name": expr.group("name"), "installed": expr.group("i") == "i", "info": expr.group("info")}]

	def run_post(self):
		items = [["%s (%sinstalled)" % (item["name"], "" if item["installed"] else "not "), item["info"]] for item in self.items]
		sublime.set_timeout(lambda: self.window.show_quick_panel(items, self.on_done), 0)

	def on_done(self, i):
		if i < 0:
			return

		# Get current item
		item = self.items[i]

		# Build available actions
		items = [["..", "Go back to the %s list" % self.info_type]]
		if item["installed"]:
			items += [["Remove", "Remove %s" % item["name"]]]
			items += [["Update", "Update %s" % item["name"]]]
			items += [["Update (Force)", "Update %s" % item["name"]]]
		else:
			items += [["Install", "Install %s" % item["name"]]]

		def on_done(i):
			if i == 0:
				self.show_quick_panel()
			elif i == 1 and item["installed"]:
				if sublime.ok_cancel_dialog("Remove \"%s\"" % item["name"], "Remove"):
					self.window.run_command("tlmgr_simple", {"cmd": ["remove", item["name"]], "sudo": True})
			elif i == 1 and not item["installed"]:
				if sublime.ok_cancel_dialog("Install \"%s\"" % item["name"], "Install"):
					self.window.run_command("tlmgr_simple", {"cmd": ["install", item["name"]], "sudo": True})
			elif i == 2:
				if sublime.ok_cancel_dialog("Update \"%s\"" % item["name"], "Update"):
					self.window.run_command("tlmgr_simple", {"cmd": ["update", item["name"]], "sudo": True})
			elif i == 3:
				if sublime.ok_cancel_dialog("Force Update \"%s\"" % item["name"], "Update"):
					self.window.run_command("tlmgr_simple", {"cmd": ["update", "--force", item["name"]], "sudo": True})

		sublime.set_timeout(lambda: self.window.show_quick_panel(items, on_done), 0)