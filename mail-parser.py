#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import datetime
import time
import mimetypes
import email
import email.header
import shutil
import unicodedata
import traceback
import fnmatch
from HTMLParser import HTMLParser
hParser = HTMLParser()

"""Настройки путей и прочего"""
#Путь до папки с письмами (до ящика)
mail_path = 'in'
#Путь до места хранения обработанных писем и вложений
store_path = 'out' 
#Путь до папки информирования о новом письме
ns_head_path = 'unprocessed' 
#Если не пусто - перемещать обработанные письма из ящика в эту папку
move_path = 'old' 
#Ошибочно-распознанные файлы перемещать в эту папку
move_path_bad = 'bad' 
#Удалять ли письма из ящика после "прочтения" (нельзя использовать вместе с move_path)
delete_mail = False 
#Черный список адресатов, письма от которых принимать не надо (в нижнем регистре!)
mail_from_blacklist = [] 

"""Системные настройки"""
charset = 'utf-8' #cp866 не всегда преобразует символы и валится в ошибку, пусть будет utf-8

def filter_filename(fname): #фильтр плохих символов для имени файла
	fname = fname.replace('"', '_')
	fname = fname.replace('/', '_')
	fname = fname.replace('\\', '_')
	fname = fname.replace(':', '_')
	fname = fname.replace('*', '_')
	fname = fname.replace('?', '_')
	fname = fname.replace('<', '_')
	fname = fname.replace('>', '_')
	fname = fname.replace('|', '_')
	return fname
	
def mail_file_clean(fname): #финальные действия с файлом письма
	global move_path
	global delete_mail
	if move_path <> '':
		shutil.move(fname, os.path.join(move_path, os.path.basename(fname)))
	else: 
		if delete_mail: #Если нужно - удаляем файл письма
			os.remove(fname)

def filter_header(str): #фильтруем строку, получающуюся из шапки, чтобы питон мог корректно ее раскодировать
	str = str.replace('\r\n\t', ' ')
	if '^' in str: return str #Лень обрабатывать, если есть наш спец-символ - выходим
	
	#Блок проверки на наличие в конце закодированной строки пробела
	str_tmp = str.replace('?', '^')
	str = ''
	for word_str in str_tmp.split():
		if fnmatch.fnmatch(word_str, '*^?^=*'): #если есть потенциально вхождение, которое может поломать наш код ниже - найдем с какого символа надо менять
			index = 1
			while not fnmatch.fnmatch(word_str[:index], '*^?^=*'):
				index += 1
			word_str = word_str[:index] + word_str[index:].replace('^=', '^= ')
		else:
			word_str = word_str.replace('^=', '^= ')
		str += ' ' + word_str
	str = str[1:].replace('^','?')
	
	str = str.replace('	', ' ')
	return str
	
def filter_specchars(str):	#фильтруем хитрые utf-8 символы, которые 100% не распознает прогресс
	global charset
	str = str.decode(charset, errors='ignore').encode('cp866', errors='ignore').decode('cp866').encode(charset)
	return str

def html2text(strText): #преобразование html в текст
	global hParser
	str1 = strText
	int2 = str1.lower().find("<body")
	if int2>0:
		str1 = str1[int2:]
	int2 = str1.lower().find("</body>")
	if int2>0:
		str1 = str1[:int2]
	#Какие теги на что меняются (\t - табуляция, \r - новая строка)
	list1 = ['<br>','<tr','<th','<td','</p>','li>','</h','div>']
	list2 = ['\r',  '\r', '\t', '\t', '\r',  '\r', '\r', '\r']
	bolFlag1 = True
	bolFlag2 = True
	strReturn = ""
	for int1 in range(len(str1)):
		str2 = str1[int1]
		for int2 in range(len(list1)):
			if str1[int1:int1+len(list1[int2])].lower() == list1[int2]:
				strReturn = strReturn + list2[int2]
		if str1[int1:int1+7].lower() == '<script' or str1[int1:int1+9].lower() == '<noscript':
			bolFlag1 = False
		if str1[int1:int1+6].lower() == '<style':
			bolFlag1 = False
		if str1[int1:int1+7].lower() == '</style':
			bolFlag1 = True
		if str1[int1:int1+9].lower() == '</script>' or str1[int1:int1+11].lower() == '</noscript>':
			bolFlag1 = True
		if str2 == '<':
			bolFlag2 = False
		if bolFlag1 and bolFlag2 and (ord(str2) != 10) :
			strReturn = strReturn + str2
		if str2 == '>':
			bolFlag2 = True
		if bolFlag1 and bolFlag2:
			strReturn = strReturn.replace(chr(32)+'\r', '\r')
			strReturn = strReturn.replace('\t\r', '\r')
			strReturn = strReturn.replace('\r'+chr(32), '\r')
			#strReturn = strReturn.replace('\r\t', '\r')
			strReturn = strReturn.replace('\r\r', '\r')
	strReturn = strReturn.replace('\r', '\r\n')
	strReturn = hParser.unescape(strReturn)
	return strReturn
	
"""Основной код"""	
print 'KDC mail parser\n'	

have_errors = False
msg_count = 0
msg_count_s = 0

if move_path <> '':
	if not os.path.exists(move_path):
		os.makedirs(move_path)
if not os.path.exists(ns_head_path):
	os.makedirs(ns_head_path)
			
for msgfile in glob.glob(os.path.join(mail_path, "*.msg")):
	
	msg_count += 1
	store_path_local = None
	
	try:
		with open(msgfile, 'r') as mailfile:	
			mail = email.message_from_file(mailfile)
			
		msgfile_name = os.path.basename(msgfile)
		print (msgfile_name)
		
		#Собираем поля шапки
			#От
		mail_from = email.utils.getaddresses([mail.get('from')])
		for ind in enumerate(mail_from):
			i = ind[0]
			for txt,chrst in email.header.decode_header(filter_header(mail_from[i][0])):
				if chrst:
					mail_from[i] = filter_specchars(txt.decode(chrst).encode(charset)), mail_from[i][1].lower()
				else:
					mail_from[i] = filter_specchars(txt.encode(charset)), mail_from[i][1].lower()
			#Кому
		mail_to = [('','')]
		if 'to' in mail:
			mail_to = email.utils.getaddresses([mail.get('to')])
			for ind in enumerate(mail_to):
				i = ind[0]
				for txt,chrst in email.header.decode_header(filter_header(mail_to[i][0])):
					if chrst:
						mail_to[i] = filter_specchars(txt.decode(chrst).encode(charset)), mail_to[i][1].lower()
					else:
						mail_to[i] = filter_specchars(txt.encode(charset)), mail_to[i][1].lower()
			#Копия
		mail_cc = [('','')]
		if 'cc' in mail:
			mail_cc = email.utils.getaddresses([mail.get('cc')])
			for ind in enumerate(mail_cc):
				i = ind[0]
				for txt,chrst in email.header.decode_header(filter_header(mail_cc[i][0])):
					if chrst:
						mail_cc[i] = filter_specchars(txt.decode(chrst).encode(charset)), mail_cc[i][1].lower()
					else:
						mail_cc[i] = filter_specchars(txt.encode(charset)), mail_cc[i][1].lower()
			#Тема
		mail_subject = ''
		if 'Subject' in mail:			
			for txt,chrst in email.header.decode_header(filter_header(mail.get('Subject'))):
				try:
					if chrst:
						try:
							mail_subject += txt.decode(chrst).encode(charset)
						except:
							mail_subject += txt.encode(charset)
					else:
						#Иногда тема не выгрузится в нужной нам кодировке и свалится в ошибку т.к. не закодирована вообще, пробуем раскодировать из кодировки письма
						try:
							mail_subject += txt.decode(mail.get_content_charset()).encode(charset)
						except:
							mail_subject += txt.encode(charset)
				except:
					mail_subject = "<!!!Тема не распознана!!!>"
			mail_subject = filter_specchars(mail_subject.strip())			
			
			#Дата\время сообщения
		email_date = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(mail['date'])))
		
		#store_path_local = os.path.join(store_path, email_date.strftime('%Y-%m-%d'), os.path.splitext(msgfile_name)[0])
		store_path_local = os.path.join(email_date.strftime('%Y-%m-%d'), os.path.splitext(msgfile_name)[0])
				
		break_flag = False
		
		#Проверка на черный список адресатов
		if not break_flag:
			if mail_from[0][1].lower() in mail_from_blacklist:
				break_flag = True
		
		#Проверка на то, обрабатывали ли мы уже такое письмо
		if not break_flag:
			while os.path.isdir(os.path.join(store_path, store_path_local)): 
				existing_msg_date = ''
				try:
					with open(os.path.join(store_path, store_path_local, 'header.dat'), "r") as h_file:
						for line in h_file:
							if existing_msg_date == '+':						
								existing_msg_date = line.rstrip()
								break
							if '--msg_date--' in line:
								existing_msg_date = '+'						
				except:
					pass
				else:
					if str(existing_msg_date) == str(email_date): #письмо уже обрабатывали, пропустим
						break_flag = True
						break
				store_path_local+='_' #Если не обрабатывали а просто такое же название - допишем символ к нему	
				
		if break_flag:
			mail_file_clean(msgfile)
			continue

		print (store_path_local)

		os.makedirs(os.path.join(store_path, store_path_local))
		
		#Копируем файл письма в папку с исходными сообщениями
		shutil.copy2(msgfile, os.path.join(store_path, store_path_local))
		
		mail_body = ''
		mail_type = ''
		expected_charset = ''
		
		#Пишем тело письма
		for part in mail.walk():		
			if part.get_content_maintype() != 'text':
				continue	
			if part.get('Content-Disposition'): #Этот тэг по-идее только у вложений
				continue	
				
			if mail_type == 'html':
				continue #Если уже есть тело письма в html - пропустим
			if 'html' in part.get_content_type():
				mail_type = 'html'
				mail_body = part.get_payload(decode=True)
				expected_charset = part.get_content_charset()
				if not expected_charset:
					expected_charset = mail.get_content_charset()
				if not expected_charset:
					expected_charset = 'utf-8'
				#Пытаемся раскодировать кодировку
				decoded_body = ''
				try:
					decoded_body = mail_body.decode(expected_charset).encode(charset)
				except:
					#пробуем с другой кодировкой
					expected_charset = 'cp1251'
					try:						
						decoded_body = mail_body.decode(expected_charset).encode(charset)
					except:
						#и еще раз
						expected_charset = 'koi8-r'
						try:
							decoded_body = mail_body.decode(expected_charset).encode(charset)
						except:
							raise #вытаскиваем ошибку, явно что-то не то с кодировкой
						pass
					pass
				if 'charset' in mail_body: #Если в html есть указание кодировки - не будем ее указывать
					expected_charset = ''
				
				#Переводим в plain-text				
				decoded_body = html2text(decoded_body.decode(charset))								
				#Пишем txt часть отдельно
				with open(os.path.join(store_path, store_path_local, 'body.txt'), 'wb') as file:
					file.write(filter_specchars(decoded_body.encode(charset)))
			else:
				mail_type = 'txt'
				current_charset = part.get_content_charset()
				if not current_charset:
					current_charset = mail.get_content_charset()
				if not current_charset:
					#Пытаемся раскодировать кодировку
					expected_charset = 'utf-8'
					decoded_body = ''
					try:
						decoded_body = mail_body.decode(expected_charset).encode(charset)
					except:
						#пробуем с другой кодировкой
						expected_charset = 'cp1251'
						try:						
							decoded_body = mail_body.decode(expected_charset).encode(charset)
						except:
							#и еще раз
							expected_charset = 'koi8-r'
							try:
								decoded_body = mail_body.decode(expected_charset).encode(charset)
							except:
								raise #вытаскиваем ошибку, явно что-то не то с кодировкой
							pass
						pass
					mail_body = decoded_body
				else:	
					mail_body = unicode(part.get_payload(decode=True), str(current_charset), "ignore").encode(charset, 'ignore')
					expected_charset = charset
				mail_body = filter_specchars(mail_body)
		if mail_type == '': #Если тела нет - тип не проставлялся, пусть для единообразия он будет
			mail_type = 'txt'
		with open(os.path.join(store_path, store_path_local, 'body.' + mail_type), 'wb') as file:
				file.write(mail_body)
			
		#Сохраняем вложения из письма
		atts = []
		for part in mail.walk():	
			if (part.get_content_maintype() == 'text' and not part.get('Content-Disposition')) or part.is_multipart():
				continue
			att_filename = part.get_filename()
			filename_found = False
			try: #иногда имя не распознается, не знаю, что-то с письмом или стандартной библиотекой, так что добавил такой костыль
				email.header.decode_header(filter_header(att_filename))
				filename_found = True
			except:
				filename_found = False
				pass	
			if not att_filename or att_filename == '' or not filename_found: #Имени файла нет, пытаемся угадать расширение
				if att_filename and att_filename <> '' and not filename_found: #в случае с кривым именем пробуем расширение взять с него
					ext = os.path.splitext(att_filename)[1]
				else:
					ext = mimetypes.guess_extension(part.get_content_type())
				if not ext:				
					ext = '.xls' #Если расширение не угадалось, ставим по умолчанию
				att_filename = 'Part' + ext
			else: #имя файла есть, пытаемся его перекодировать в нужную кодировку		
				att_filename_tmp = att_filename
				att_filename = ''
				for att_filename_tmp,chrst in email.header.decode_header(filter_header(att_filename_tmp)):
					if chrst:
						att_filename_tmp = att_filename_tmp.decode(chrst, errors='ignore')
					att_filename += ' ' + att_filename_tmp
				att_filename = att_filename.strip()
			try:
				att_filename = filter_specchars(filter_filename(att_filename).encode(charset, errors='ignore')).decode(charset, errors='ignore')
			except:
				att_filename = filter_specchars(filter_filename(att_filename))
			while os.path.exists(os.path.join(store_path, store_path_local, att_filename)) or att_filename.lower() == 'header.dat': #проверка на наличие файла, если есть - дописываем _ в начало
				att_filename = '_' + att_filename
			if att_filename == 'winmail.dat':
				print '!!!winmail'
			with open(os.path.join(store_path, store_path_local, att_filename), 'wb') as file:
				file.write(part.get_payload(decode=True))
			atts.append(att_filename.encode(charset))
		
		#Собираем шапку
		header_data = {'orig_filepath':msgfile, 'processed_path':store_path_local, 'processed_path_full':os.path.join(store_path, store_path_local), 'orig_file':msgfile_name, 'msg_date':str(email_date), 'processed_date':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'msg_from':mail_from, 'msg_to':mail_to, 'msg_cc':mail_cc, 'msg_subject':mail_subject, 'msg_att':atts, 'msg_body_type':mail_type, 'msg_body_expected_charset':expected_charset}	
		
		#Пишем шапку с данными для Progress
		header_txt = ''
		for key, value in header_data.iteritems():
			header_txt += '--' + str(key) + '--\n'
			if type(value) is list or type(value) is tuple:
				for subval in value:
					if type(subval) is list or type(subval) is tuple:
						for subsubval in subval:
							header_txt += str(subsubval) + '\t'
					else:
						header_txt += str(subval) + '\t'
			else:
				header_txt += str(value)
			header_txt = header_txt.rstrip('\t') + '\n'
		
		with open(os.path.join(store_path, store_path_local, 'header.dat'), 'w') as file:
			file.write(header_txt)
		ns_head_file = os.path.splitext(msgfile_name)[0] + '.dat'
		while os.path.exists(os.path.join(ns_head_path, ns_head_file)):
			ns_head_file = '_' + ns_head_file		
		shutil.copy2(os.path.join(store_path, store_path_local, 'header.dat'), os.path.join(ns_head_path, ns_head_file))
		
		msg_count_s += 1
		
		#перемещаем или удаляем файл при необходимости
		mail_file_clean(msgfile)
		
		print
	
	except: #В случае ошибки переходим к следующему файлу	
		if store_path_local is not None and os.path.isdir(os.path.join(store_path, store_path_local)) and store_path_local != '':
			shutil.rmtree(os.path.join(store_path, store_path_local)) #удаление директории кривого письма
		traceback.print_exc()
		if move_path_bad <> '':
			shutil.move(msgfile, os.path.join(move_path_bad, os.path.basename(msgfile)))
		have_errors = True
		continue

print str(msg_count_s) + ' mails processed' 		
print str(msg_count) + ' mails all'
		
if have_errors: #В случае если были ошибки - не будем закрывать консоль какое-то время
	print '\n!!!ERROR FILES FOUND, PLEASE CHECK!!!\n'
	time.sleep(10)


	
	