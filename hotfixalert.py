#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""


	Hot Fix Alert - Displays a notification when a software has a new version
	Copyright (C) 2017 Rômulo Mendes Figueiredo

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.



	Compatible softwares:
	---------------------
	- Aker Alert 6.8 Patch 1
	- Central VOIP - Intelbras CIP-850

	How to install:
	---------------
	$ sudo apt-get install python-pip python-dbus python-dev build-essential
	$ sudo pip install notify2 beautifulsoup4

	How to run:
	-----------
	$ chmod +x ./hotfixalert > /tmp/hotfixalert.log
	$ ./hotfixalert &



"""

DEBUG=False
SLEEP=30

import os
import sys
import time
import urllib2

try:
	from bs4 import BeautifulSoup
except ImportError:
	print("Require BeautifulSoup")
	sys.exit(1)

try:
	import notify2
except ImportError:
	print("Require python-dbus\n$sudo apt-get install python-dbus")
	print("Require notify2\n$sudo pip install notify2")
	sys.exit(1)

notify2.init("hotfixalert")
n = notify2.Notification("Title", "Message")
n.set_urgency(notify2.URGENCY_CRITICAL)

def out(msg):
	arq = file('/tmp/hotfixalert.log', 'a')
	if (type(msg) == unicode):
		if DEBUG: print(msg.encode('utf-8'))
		arq.write(msg.encode('utf-8')+"\n")
	else:
		if DEBUG: print(str(msg))
		arq.write(str(msg)+"\n")
	arq.close()
	

def check_aker():
	out("\naker: ini")
	URL="http://download.aker.com.br/index.php?path=prod%2Fcurrent%2Fatualizacoes%2Faker-firewall-6.8%2Fpatch-1%2F64bits/"
	ICON="/usr/share/icons/hicolor/32x32/apps/aker_icon.png"
	VERSAO=50

	page = urllib2.urlopen(URL)
	out(page)
	soup = BeautifulSoup(page, "lxml")

	qtd = len(soup.findAll('tr', 'snF'))
	out(qtd)

	if qtd<>VERSAO:
		msg="New hot fix is available"
		out(msg)
		n.update("Aker", msg, ICON)
		n.show()

	out("aker: fim")

def check_cip850():
	out("\ncip850: ini")

	URL="http://www.intelbras.com.br/empresarial/telefonia/gateways/ip/cip-850"
	VERSAO="2.08.10"
	ICON="/usr/share/icons/gnome/32x32/devices/gnome-modem.png"

	page = urllib2.urlopen(URL)
	out(page)
	soup = BeautifulSoup(page, "lxml")
	tags = soup.findAll("span", "node-title")

	for t in tags:
		if DEBUG: print(t)
		pos = t.text.find("web")
		if DEBUG: print(pos)
		if (pos<>-1):
			out(t.text)
			versao = t.text.split(" ")[3]
			out(versao)

	if versao<>VERSAO:
		msg = "Version {v} is available".format(v=versao)
		out(msg)
		n.update("Central CIP-850", msg, ICON)
		n.show()

	out("cip850: fim")


while True:
	try:
		check_aker()
		time.sleep(SLEEP)
		check_cip850()
		time.sleep(SLEEP)
	except Exception as e:
		out("\n\nError: " + e.message + "\n\n")
		time.sleep(SLEEP)
		pass
