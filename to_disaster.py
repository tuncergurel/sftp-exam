import os
import time
import paramiko
import tarfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sftp_exam():
	remote_server_ip =   #remote_server['ip'] 
	remote_server_user = #remote_server['username']
	remote_server_pass = #remote_server['password']


	dis_server_ip =   #dis_server['ip'] 
	dis_server_user = #dis_server['username']
	dis_server_pass = #dis_server['password']


	print("connecting to server")
	local_path = #local path --exam "/home/user/exam.tar.gz"
	remote_path = #remote path 
	dis_path = #dis path

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname = remote_server_ip, username = remote_server_user, password = remote_server_pass)
	print("connected")

	try:
		stdin, stdout, stderr = ssh.exec_command("sudo tar -czvf exam.tar.gz --path")
		stdin.write(remote_server_pass + "\n")
		stdin.flush()

		exit_status = stdout.channel.recv_exit_status()
		if exit_status == 0:
			print ("Tar completed")
		else:
			print("Error",stderr,exit_status)

	except ValueError as msg:
		print(msg)

	
	try:
		sftp = ssh.open_sftp()
		sftp.get(remote_path, local_path)
		time.sleep(1)
		print("File taken")
		
		sftp.close()
		ssh.close()
	except:
		
		print("Error")

	
	print("Connecting To dis")

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname = dis_server_ip, username = dis_server_user, password = dis_server_pass)

	try:
		sftp = ssh.open_sftp()
		sftp.put(local_path, dis_path)
		time.sleep(1)
		
		print("File sended")
	except:
		print("Error")

	



	try:
		stdin, stdout, stderr = ssh.exec_command("sudo -S mv --path /exam.tar.gz")
		stdin.write(dis_server_pass + "\n")
		stdin.flush()
		
		stdin, stdout, stderr = ssh.exec_command("sudo -S cd / ")
		stdin.write(dis_server_pass + "\n")
		stdin.flush()
	
		stdin, stdout, stderr = ssh.exec_command("sudo -S tar -xvf /exam.tar.gz")
		stdin.write(dis_server_pass + "\n")
		stdin.flush()
			
		exit_status = stdout.channel.recv_exit_status()
		if exit_status == 0:
			print ("Tar opened")
		else:
			print("Error",stderr,exit_status)
		
			sftp.close()
			ssh.close()
	except ValueError as msg:
		print (msg)

	message = """Transfer Completed"""
	msg = MIMEMultipart()
	msg['from'] = #sender mail
	recipients = #recipients
	msg['To'] = recipients
	msg['Subjects'] = 'Transfer'
	msg.attach(MIMEText(message, 'html'))
	server = smtplib.SMTP(#server)

	server.sendmail(msg['From'], recipients, msg.as_string())
	server.quit()


if __name__ == '__main__':
	sftp_exam()

