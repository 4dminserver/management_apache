#!/usr/bin/python
#-*-coding:utf-8-*-
#- Add DNS Class

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

import sqlite3, sys, subprocess
sys.path.append('model')
from teco import color

class management(object):
	
	@staticmethod
	def add_host(translate, log):
		_ = translate
		domain_name = raw_input(_('Domain Name: '))
		while domain_name == "":
			domain_name = raw_input(_('Domain Name: '))
		email = raw_input(_('Email Contact: '))
		while email == "":
			email = raw_input(_('Email Contact: '))
		path_server = raw_input(_('Path Server: '))
		while path_server == "":
			path_server = raw_input(_('Path Server: '))
		rewrite = raw_input(_('ReWrite [y/N]: '))
		indexOf =  raw_input(_('IndexOf [y/N]: '))
		
		if rewrite == 'y':
			rewrite = '1'
			rewriteValues = "\n\t\tRewriteEngine On"
		else:
			rewrite = '0'
			rewriteValues = ""

		if indexOf == 'y':
			indexOf = '1'
			indexOfValues = "\n\t\tOptions Indexes FollowSymLinks MultiViews"
		else:
			indexOf = '0'
			indexOfValues = ""

		conectionBrain = sqlite3.connect('modules/management_apache/brain/apache.db')
		apache = conectionBrain.cursor()
		apache.execute("INSERT INTO apache (domain, email, path_domain, rewrite, indexOf, status) VALUES ('" + domain_name + "', '" + email + "', '" + path_server + "', '" + rewrite + "', '" + indexOf + "', '1')")
		conectionBrain.commit()

		save = open('/etc/apache2/sites-available/' + domain_name, 'w')
		save.write("""<VirtualHost *:80>
	ServerAdmin """ + email + """
	ServerName """ + domain_name + """
	ServerAlias www.""" + domain_name + """
	DocumentRoot """ + path_server + """
	<Directory />
		Options FollowSymLinks
		AllowOverride None
	</Directory>
	<Directory """ + path_server + """>""" + indexOfValues + rewriteValues + """
		AllowOverride None
		Order allow,deny
		allow from all
	</Directory>


	ErrorLog ${APACHE_LOG_DIR}/error.log

	# Possible values include: debug, info, notice, warn, error, crit,
	# alert, emerg.
	LogLevel warn

	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>""")
		command_addSite = 'a2ensite ' + str(domain_name)
		addSite = subprocess.Popen(command_addSite, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		addSite_error = addSite.stderr.read()
		if addSite_error != '': 
			log.write(_('Failed create host'), 1)
		else:
			log.write(_('Add host ') + str(domain_name))


	@staticmethod
	def edit_host(translate, output, log):
		_ = translate
		conectionBrain = sqlite3.connect('modules/management_apache/brain/apache.db')
		apache = conectionBrain.cursor()
		apache.execute("SELECT id, domain FROM apache WHERE status = '1'")
		contador = 0
		domains_active = {}
		for domain in apache:
			contador +=1
			domains_active[domain[0]] = domain[1]

		for domain in domains_active:
			output.default(str(domain) + ' - ' + domains_active[domain])
		output.default("0 - Exit")

		control = True
		while control == True:
			sentencia = raw_input("apache[edit] >> ")
			try:
				if int(sentencia) < 0:
					output.default(_('Must be a positive number'))
				elif sentencia == '0':
					control = False
				
				elif domains_active[int(sentencia)]:
					sys.path.append('modules/management_apache/model')
					from utility import utility
					utility.edit_host(_, output, sentencia, conectionBrain, log)
					control = False
			except:
				output.error(_('Must be listed'))

	@staticmethod
	def delete_host(translate, output, log):
		_ = translate
		conectionBrain = sqlite3.connect('modules/management_apache/brain/apache.db')
		bind = conectionBrain.cursor()
		bind.execute("SELECT id, domain FROM apache WHERE status = '1'")
		contador = 0
		domains_active = {}
		for domain in bind:
			contador +=1
			domains_active[domain[0]] = domain[1]

		for domain in domains_active:
			output.default(str(domain) + ' - ' + domains_active[domain])
		output.default("0 - Exit")

		control = True
		while control == True:
			sentencia = raw_input("apache[delete] >> ")
			try:
				if int(sentencia) < 0:
					output.default(_('Must be a positive number'))
				elif sentencia == '0':
					control = False
				
				elif domains_active[int(sentencia)]:
					sys.path.append('modules/management_apache/model')
					from utility import utility
					utility.delete_host(_, output, sentencia, conectionBrain, log)
					control = False
			except:
				output.error(_('Must be listed'))

	@staticmethod
	def activate_host(translate, output, log):
		_ = translate
		conectionBrain = sqlite3.connect('modules/management_apache/brain/apache.db')
		bind = conectionBrain.cursor()
		bind.execute("SELECT id, domain FROM apache WHERE status = '0'")
		contador = 0
		domains_active = {}
		for domain in bind:
			contador +=1
			domains_active[domain[0]] = domain[1]

		for domain in domains_active:
			output.default(str(domain) + ' - ' + domains_active[domain])
		output.default("0 - Exit")

		control = True
		while control == True:
			sentencia = raw_input("apache[activate] >> ")
			try:
				if int(sentencia) < 0:
					output.default(_('Must be a positive number'))
				elif sentencia == '0':
					control = False
				
				elif domains_active[int(sentencia)]:
					sys.path.append('modules/management_apache/model')
					from utility import utility
					utility.activate_host(_, output, sentencia, conectionBrain, log)
					control = False
			except:
				output.error(_('Must be listed'))

	@staticmethod
	def reload_service(translate, output, log):
		_ = translate
		output.default(color('magenta',_('Restarting Service...')))
		command_restart = '/etc/init.d/apache2 reload'
		restart = subprocess.Popen(command_restart, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		restart_error = restart.stderr.read()
		if restart_error != '':
			output.error(color('amarillo', restart_error))
			output.error(color('rojo',_('Failed to restart service or warnings out')))
			log.write(_('Failed service or warnings out'), 1)
		else:
			output.default(color('verde', _('Restart service ok')))
			log.write(_('Restart service ok'))