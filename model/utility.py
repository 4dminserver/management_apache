#!/usr/bin/python
#-*-coding:utf-8-*-
#- utility DNS Class

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

import sys, os, subprocess
sys.path.append('modules/management_apache/model')
from generate import generate

class utility(object):
	@staticmethod
	def edit_host(translate, output, id_domain, conectionBrain, log):
		cursor = conectionBrain.cursor()
		cursor.execute("SELECT * FROM apache WHERE id = '" + id_domain + "'")
		for info in cursor:
			_ = translate

			domain_name = raw_input(_('Domain Name ') + str(info[1]) + ': ')
			email = raw_input(_('Email Contact ') + str(info[2]) + ': ')
			path_server = raw_input(_('Path Server ') + str(info[3]) + ': ')
			rewriteValue = 'y' if str(info[4]) else 'n'
			rewrite = raw_input(_('ReWrite ') + str(rewriteValue) + ': ')
			indexOfValue = 'y' if str(info[5]) else 'n'
			indexOf =  raw_input(_('IndexOf ') + str(indexOfValue) + ': ')


			control = False

			valores = ''

			if domain_name != "":
				control = True
				valores += "domain = '" + str(domain_name) + "', "

			if email != "":
				control = True
				valores += "email = '" + str(email) + "', "

			if path_server != "":
				control = True
				valores += "path_domain = '" + str(path_server) + "', "
			
			if rewrite != "":
				control = True
				if rewrite == 'y':
					r_value = '1'
				else:
					r_value = '0'
				valores += "rewrite = '" + str(r_value) + "', "
			
			if indexOf != "":
				control = True
				if indexOf == 'y':
					i_value = '1'
				else:
					i_value = '0'
				valores += "indexOf = '" + str(i_value) + "', "
			
			if control == True:
				final = valores + 'F'
				cursor.execute("UPDATE apache SET "  + final.split(', F')[0] + " WHERE id = '" + str(info[0]) + "'")
				conectionBrain.commit()
				generate.all(str(info[0]), conectionBrain)
				if domain_name == "":
					edit_host = str(info[1])
				else:
					edit_host = domain_name
				log.write(_('Edit host ') + str(edit_host))

	@staticmethod
	def delete_host(translate, output, id_domain, conectionBrain, log):
		_ = translate
		sentencia = raw_input('disable[0]/delete[1]: [0] ')
		if sentencia == '':
			sentencia = '0'
		while sentencia != '0' and sentencia != '1':
			output.error(_('Option not valid'))
			sentencia = raw_input('disable[0]/delete[1]: [0] ')
		cursor = conectionBrain.cursor()
		cursor.execute("SELECT domain FROM apache WHERE id = '" + str(id_domain) + "'")
		for info in cursor:
			domain = info[0]

		if sentencia == '0':
			cursor.execute("UPDATE apache SET status = '0' WHERE id = '" + id_domain + "'")
		else:
			cursor.execute("DELETE FROM apache WHERE id = '" + id_domain + "'")
		conectionBrain.commit()
		command_deteleSite = 'a2dissite ' + str(domain)
		deleteSite = subprocess.Popen(command_deteleSite, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		deleteSite_error = deleteSite.stderr.read()
		if deleteSite_error != '': 
			log.write(_('Failed delete host'), 1)
		else:
			os.system('rm -f /etc/apache2/sites-available/' + domain)
			log.write(_('Delete host ') + str(domain))

	@staticmethod
	def activate_host(translate, output, id_domain, conectionBrain, log):
		_ = translate
		cursor = conectionBrain.cursor()
		cursor.execute("UPDATE apache SET status = '1' WHERE id = '" + str(id_domain) + "'")
		conectionBrain.commit()
		generate.all(id_domain, conectionBrain)
		cursor.execute("SELECT domain FROM apache WHERE id = '" + str(id_domain) + "'")
		for info in cursor:
			domain_name = info[0]
		command_addSite = 'a2ensite ' + str(domain_name)
		addSite = subprocess.Popen(command_addSite, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		addSite_error = addSite.stderr.read()
		if addSite_error != '': 
			log.write(_('Failed active host'), 1)
		else:
			log.write(_('Active host ') + str(domain_name))