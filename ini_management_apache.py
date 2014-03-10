#!/usr/bin/python
#-*-coding:utf-8-*-
#- management_apache Class

#- AdminServer / System Management Server
#- Copyright (C) 2014 GoldraK & Interhack 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 
# You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>

# WebSite: http://adminserver.org/
# Email: contacto@adminserver.org
# Facebook: https://www.facebook.com/pages/Admin-Server/795147837179555?fref=ts
# Twitter: https://twitter.com/4dminserver

#- imports necessary
import sys
sys.path.append('modules/management_apache/model')
from management import management
from generate import generate

class add(object):

	#- @output.[option](default, error)(text) -> printed by stdout
	#- @translate.[option](init('nameTranslate')) -> initializes the translation file
	#- @log.[option](write)(text,*1) -> 1 is error -> saves information in the logs
	#- @installer -> module for install dependencies -> nonoperating

	def __init__(self, output, translate, log, installer):
		#- Operations
		#- Example:
		interpret = translate.init('management_apache')
		_ = interpret.ugettext
		output.default(_('Management Apache'))
		def __menu__():
			output.default(_('1 - Add host'))
			output.default(_('2 - Edit host'))
			output.default(_('3 - Delete host'))
			output.default(_('4 - Activate host'))
			output.default(_('5 - Regenerate'))
			output.default(_('6 - Restart Service Apache'))
			output.default('0 - Exit')

		def option1():
			management.add_host(_, log)
		
		def option2():
			management.edit_host(_, output, log)

		def option3():
			management.delete_host(_, output, log)

		def option4():
			management.activate_host(_, output, log)

		def option5():
			generate.all('all', '')

		def option6():
			management.reload_service(_, output, log)
		
		__menu__()

		control = True
		while control == True:
			sentencia = raw_input("apache >> ")
			if sentencia == '1':
				option1()
				__menu__()
			elif sentencia == '2':
				option2()
				__menu__()
			elif sentencia == '3':
				option3()
				__menu__()
			elif sentencia == '4':
				option4()
				__menu__()
			elif sentencia == '5':
				option5()
				__menu__()
			elif sentencia == '6':
				option6()
				__menu__()
			elif sentencia == '0':
				control = False
			else:
				output.default(_('Invalid option'))

class help(object):
	@staticmethod
	#- @translate.[option](init('nameTranslate')) -> initializes the translation file
	def info(translate):
		return 'This module is created to manage apache from creating domains to advanced system settings'

	@staticmethod
	#- Especificamos si necesita el modulo paquetes adicionales.
	def package():
		#- List of extra dependencies needed by the module
		addtionalPackage = []
		return additionalPackage