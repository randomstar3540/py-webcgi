import sys
import socket
import os
import time

STATUS = {'200': '200 OK', '404': '404 File not found', '406': '406 Not Acceptable', '500': '500 Internal Server Error'}
ERR_MSG = {'404': '404 Not Found', '406': '406 Not Acceptable', '500': '500 Internal Server Error'}
ERROR_HTML = "<html>\n<head>\n\t<title>{}</title>\n</head>\n<body bgcolor=\"white\">\n<center>\n\t<h1>{}</h1>\n</center>\n</body>\n</html>\n"

# print the error message in stderr and exit the program
def eprint_exit(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	exit(0)

# print the error message in stderr only
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

# read the config file with filename from argv and check if it is valid
def setup():
	if len(sys.argv) < 2:
		eprint_exit("Missing Configuration Argument")
	if os.path.isfile(sys.argv[1]) != True:
		eprint_exit("configuration file not found")

	if os.stat(sys.argv[1]).st_size == 0:
		eprint_exit("configuration file empty")

	f = open (sys.argv[1],"r")
	lines = f.read().splitlines()
	f.close()
	for i in range(len(lines)):
		lines[i] = lines[i].split('=')
	if len(lines) != 4 or lines[0][0] != 'staticfiles' or lines[1][0] != 'cgibin' or lines[2][0] != 'port' or lines[3][0] != 'exec':
		eprint_exit("Missing Field From Configuration File")
	return lines

# handle the connection request, determines if it is a get request or post request
# determines if it need to excute the cgi scripts
# Return: return the response content (String)
def handleresource(METHOD, CONFIG, RESOURCE, HEADERS):
	if RESOURCE == '/':
		RESOURCE += 'index.html'

	path = RESOURCE.split('?')[0]
	extname = path.split('.')[-1]
	query = ''
	if len(RESOURCE.split('?')) > 1 :
		query = RESOURCE.split('?')[-1]
		os.environ['QUERY_STRING'] = query

	if os.path.isfile(CONFIG[0][1]+path) != True and os.path.isfile('.'+path) != True:
		content = ERROR_HTML.format(ERR_MSG['404'],ERR_MSG['404']).encode()
		return response(content,'text','html','404')
	
	if METHOD == 'POST' and extname != 'py':
		message = 'GET DATA: ' + HEADERS['Body']
		content = ERROR_HTML.format('DATA RECEIVED',message).encode()
		res_content = response(content,'text','html','200')
		return res_content

	
	if extname == 'txt' or extname == 'html' or extname == 'css' or extname == 'xml' or extname == 'js':
		with open(CONFIG[0][1]+path,'r') as f:
			lines = f.read()
			f.close()
			lines = lines.encode()
			if extname == 'js':
				return response(lines,'application','javascript','200')
			elif extname == 'txt':
				return response(lines,'text','plain','200')
			else:
				return response(lines,'text',extname,'200')
	elif extname == 'jpg' or extname == 'jpeg' or extname == 'png':
		with open(CONFIG[0][1]+path,'rb') as f:
			lines = f.read()
			f.close()
			if extname == 'png':
				return response(lines,'image','png','200')
			else:
				return response(lines,'image','jpeg','200')
	elif extname == 'py':
		r,w = os.pipe()
		child = os.fork()
		if child == 0:
			newenv = os.environ.copy()
			os.close(r)
			os.dup2(w,1)
			argv = ['python3','.'+path]
			os.execve('/usr/bin/python3',argv,newenv)
			print("Something went wrong")
			os._exit(-1)
		else:
			os.close(w)
			r = os.fdopen(r)
			out = r.read()
		child, status = os.waitpid(child, 0)
		if status == 0:
			return response(out.encode(),'text','html','200')
		else:
			content = ERROR_HTML.format(ERR_MSG['500'],ERR_MSG['500']).encode()
			return response(content,'text','html','500')
	elif extname == 'sh':
		r,w = os.pipe()
		child = os.fork()
		if child == 0:
			newenv = os.environ.copy()
			os.close(r)
			os.dup2(w,1)
			argv = ['sh','./'+path]
			os.execve('/usr/bin/sh',argv,newenv)
			print("Something went wrong")
			os._exit(-1)
		else:
			os.close(w)
			r = os.fdopen(r)
			out = r.read()
		child, status = os.waitpid(child, 0)
		if status == 0:
			return response(out.encode(),'text','html','200')
		else:
			content = ERROR_HTML.format(ERR_MSG['500'],ERR_MSG['500']).encode()
			return response(content,'text','html','500')
	else:
		content = ERROR_HTML.format(ERR_MSG['500'],ERR_MSG['500']).encode()
		return response(content,'text','html','500')


def response(content, content_type, file_type, code):
	accept = os.environ.get('HTTP_ACCEPT')

	if accept != None and accept != '*/*':
		if content_type not in accept or file_type not in accept:
			content = ERROR_HTML.format(ERR_MSG['406'],ERR_MSG['406']).encode()
			res_content = 'HTTP/1.1 ' + STATUS['406'] + '\nContent-Type: {}/{}\n\n'.format('text','html')
			res_content = res_content.encode()
			res_content += content
			return res_content

	if (content_type == 'text' or content_type == 'application') and "Status-Code:" in content.decode():
		result_content = content.decode()
		result_content_final = content.decode().split('\n')
		for i in result_content.split('\n'):
			if "Status-Code:" in i:
				status_str = i.split(': ')[1]
				result_content_final.remove(i)
		content = '\n'.join(result_content_final).encode()
		res_content = 'HTTP/1.1 ' + status_str + '\nContent-Type: {}/{}\n\n'.format(content_type,file_type)
	elif(content_type == 'text' or content_type == 'application') and "Content-Type:" in content.decode():
		res_content = 'HTTP/1.1 ' + STATUS[code] + '\n'
	else:
		res_content = 'HTTP/1.1 ' + STATUS[code] + '\nContent-Type: {}/{}\n\n'.format(content_type,file_type)
	res_content = res_content.encode()
	res_content += content
	return res_content
	

def handlerequest(conn, CONFIG):
	data = conn.recv(1024)
	data = data.decode().strip().splitlines()

	if data == []:
		conn.close()
		return

	METHOD = data[0].split()[0]
	RESOURCE = data[0].split()[1]
	HTTP_PROTOCOL = data[0].split()[2]
	


	os.environ['REQUEST_METHOD'] = METHOD
	os.environ['REQUEST_URI'] = RESOURCE
	
	HEADERS = {}
	if METHOD != 'POST':
		for i in data[1:]:
			HEADERS[i.split(': ')[0]] = i.split(': ')[1]
	else:
		for i in data[1:-2]:
			HEADERS[i.split(': ')[0]] = i.split(': ')[1]
		HEADERS['Body'] = data[-1]
	
	for k, v  in HEADERS.items():
		if k == 'Host':
			os.environ["HTTP_HOST"] = v
		elif k == 'User-Agent':
			os.environ["HTTP_USER_AGENT"] = v
		elif k == 'Accept':
			os.environ["HTTP_ACCEPT"] = v
		elif k == 'Accept-Encoding':
			os.environ["HTTP_ACCEPT_ENCODING"] = v
		elif k == 'Content-Length':
			os.environ["CONTENT_LENGTH"] = v
		elif k == 'Content-Type':
			os.environ["CONTENT_TYPE"] = v
	content = handleresource(METHOD, CONFIG, RESOURCE, HEADERS)
	conn.send(content)
	conn.close()

def main():
	CONFIG = setup()
	HOST = '127.0.0.1'
	PORT = int(CONFIG[2][1])

	child = []

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		os.environ['SERVER_ADDR'] = HOST
		os.environ['SERVER_PORT'] = str(PORT)
		s.listen()
		while True:
			conn, addr = s.accept()
			pid = os.fork()
			if pid == 0:
				if len(addr) != 2:
					# Invalid income data
					os._exit(1)
				os.environ['REMOTE_ADDRESS'] = addr[0]
				os.environ['REMOTE_PORT'] = str(addr[1])
				handlerequest(conn, CONFIG)
				os._exit(0)
			else:
				child.append(pid)
			conn.close()
		s.close()


if __name__ == '__main__':
	main()