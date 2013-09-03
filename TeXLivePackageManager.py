import sublime, sublime_plugin

import re, subprocess, sys

try:
	from .tex_live_package_manager.progress import ProcessQueueManager
	from .tex_live_package_manager.tools import *
except ValueError:
	from tex_live_package_manager.progress import ProcessQueueManager
	from tex_live_package_manager.tools import *

class TlmgrWindowCommand(sublime_plugin.WindowCommand):

	messages = ["Running", "Finished"]

	def run(self, **args):
		manager = ProcessQueueManager()
		manager.queue("tlmgr_manage_collections", lambda: self.run_async(**args), self.messages, lambda: self.run_post())

	def run_async(self):
		pass

	def run_post(self):
		pass


class TlmgrSimpleCommand(TlmgrWindowCommand):

	def access_as_sudo(self, callback):
		proc = subprocess.Popen(["sudo", "-p", "", "-S", "echo"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		stdout, stderr = proc.communicate();

		def on_done(s):
			proc = subprocess.Popen(["sudo", "-p", "", "-S", "echo"], stdin = subprocess.PIPE)
			proc.communicate(bytes("%s\n" % s, "utf-8"));

			# Check for sudo again
			self.access_as_sudo(callback)

		# If error, ask for password
		if stderr:
			self.window.show_input_panel("Root Password:", "", on_done, None, None)
		else:
			callback()

	def run_async(self, cmd):

		def on_done():
			# Start the actual command
			proc = subprocess.Popen(["sudo", "tlmgr"] + cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

			# Create output view
			view = self.window.create_output_panel("tlmgr")
			self.window.run_command("show_panel", {"panel": "output.tlmgr"})

			view.run_command("tlmgr_append_text", {"string": "### TeX Live Package Manager ### [%s]\n" % " ".join(cmd)})

			for line in proc.stdout:
				view.run_command("tlmgr_append_text", {"string": line.decode(sys.getfilesystemencoding())})

			# Wait for process to finish
			proc.wait()

		self.access_as_sudo(on_done)


class TlmgrInfoCommand(TlmgrWindowCommand):

	command = ["tlmgr", "info"]
	info_type = "packages"

	def show_quick_panel(self):
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
					self.window.run_command("tlmgr_simple", {"cmd": ["remove", item["name"]]})
			elif i == 1 and not item["installed"]:
				if sublime.ok_cancel_dialog("Install \"%s\"" % item["name"], "Install"):
					self.window.run_command("tlmgr_simple", {"cmd": ["install", item["name"]]})
			elif i == 2:
				if sublime.ok_cancel_dialog("Update \"%s\"" % item["name"], "Update"):
					self.window.run_command("tlmgr_simple", {"cmd": ["update", item["name"]]})
			elif i == 3:
				if sublime.ok_cancel_dialog("Force Update \"%s\"" % item["name"], "Update"):
					self.window.run_command("tlmgr_simple", {"cmd": ["update", "--force", item["name"]]})

		sublime.set_timeout(lambda: self.window.show_quick_panel(items, on_done), 0)

	def run_async(self):

		proc = subprocess.Popen(self.command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		communicate = proc.communicate();
		stdout = communicate[0].decode(sys.getfilesystemencoding())
		stderr = communicate[1].decode(sys.getfilesystemencoding())

		self.items = []

		for line in stdout.strip().split("\n"):
			expr = re.search(r"(?P<i>[\si])\s(?P<name>.*):\s(?P<info>.*)", line)
			if expr:
				self.items += [{"name": expr.group("name"), "installed": expr.group("i") == "i", "info": expr.group("info")}]

		self.show_quick_panel()


class TlmgrManageCollectionsCommand(TlmgrInfoCommand):

	command = ["tlmgr", "info", "collections"]
	info_type = "collections"


class TlmgrManagePackagesCommand(TlmgrInfoCommand):

	pass


class TlmgrManageSchemesCommand(TlmgrInfoCommand):

	command = ["tlmgr", "info", "schemes"]
	info_type = "schemes"
