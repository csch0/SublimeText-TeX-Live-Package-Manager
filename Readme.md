# TeX Live Package Manager

A simple interface for [tlmgr](http://www.tug.org/texlive/tlmgr.html) directly usable from Sublime Text.

## Available Commands

Here a list of the available command, for some command the plugin will ask you for a password which is the root password since some command do need root access.

### TeX Live Package Manager: Update

Update tlmgr itself.

### TeX Live Package Manager: Update Packages

Updates all installed packages

### TeX Live Package Manager: Manage Schemes

Manage the available schemes, check [tug.org](http://www.tug.org/texlive/tlmgr.html) for details.

### TeX Live Package Manager: Manage Collections

Manage the available collections, check [tug.org](http://www.tug.org/texlive/tlmgr.html) for details.

### TeX Live Package Manager: Manage Packages

Manage the available packages, check [tug.org](http://www.tug.org/texlive/tlmgr.html) for details.

### TeX Live Package Manager: Show Log Panel

Show the output panel.

## Screenshots

![Command Palette](https://raw.github.com/wiki/Chris---/SublimeText-TeX-Live-Package-Manager/palette.jpg)
![Command Install](https://raw.github.com/wiki/Chris---/SublimeText-TeX-Live-Package-Manager/install.jpg)
![Command Remove](https://raw.github.com/wiki/Chris---/SublimeText-TeX-Live-Package-Manager/remove.jpg)
![Log Panel 1](https://raw.github.com/wiki/Chris---/SublimeText-TeX-Live-Package-Manager/log_panel_1.jpg)
![Log Panel 2](https://raw.github.com/wiki/Chris---/SublimeText-TeX-Live-Package-Manager/log_panel_2.jpg)

### Using Package Control:

* Bring up the Command Palette (Command+Shift+P on OS X, Control+Shift+P on Linux/Windows).
* Select Package Control: Install Package.
* Select TeX Live Package Manager to install.

### Not using Package Control:

* Save files to the `Packages/TeX Live Package Manager` directory, then relaunch Sublime:
  * Linux: `~/.config/sublime-text-2|3/Packages/TeX Live Package Manager`
  * Mac: `~/Library/Application Support/Sublime Text 2|3/Packages/TeX Live Package Manager`
  * Windows: `%APPDATA%/Sublime Text 2|3/Packages/TeX Live Package Manager`

## Donating

Support this project and [others by chris][gittip] via [gittip][] or [paypal][].

[![Support via Gittip](https://rawgithub.com/chris---/Donation-Badges/master/gittip.jpeg)][gittip][![Support via PayPal](https://rawgithub.com/chris---/Donation-Badges/master/paypal.jpeg)][paypal]

[gittip]: https://www.gittip.com/Chris---
[paypal]: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZWZCJPFSZNXEW

## License

All files in this package is licensed under the MIT license.

Copyright (c) 2013 Chris <chris@latexing.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.