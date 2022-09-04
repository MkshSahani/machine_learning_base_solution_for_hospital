import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import pymysql


# self created modules
import mail_gen
import mail
import patient_detect_register
class Signup:
	def __init__(self, root, login):
		self.log = login
		root.geometry("1000x600")
		root.title("Sign up")
		root.resizable(0, 0)
		self.back = PhotoImage(file = "back.gif")
		self.background = Label(root, image = self.back)
		self.background.pack()


		self.tabf = Frame(root, height = 600, width = 400, bg = 'white')
		self.tabf.place(x = 550, y = 5)

		self.font1 = ('Times', -30, 'bold underline')
		self.signupl = Label(root, text = 'Sign up', font = self.font1, bg = 'white')
		self.signupl.place(x = 700, y = 10)
		self.font2 = ('Times', -20, 'bold')
		self.usernamel = Label(root, text = 'User Name : ', font = self.font2, bg = 'white')
		self.usernamel.place(x = 600, y = 70)
		self.usernamee = ttk.Entry(root, font = self.font2)
		self.usernamee.place(x = 720, y = 70)

		self.usernamel = Label(root, text = 'Gender : ', font = self.font2, bg = 'white')
		self.usernamel.place(x = 600, y = 120)

		self.gender_ = StringVar()
		self.data2 = ('Male','Female')

		self.asspin = Spinbox(root, values = self.data2,textvariable = self.gender_, font = self.font2, width = 19)
		self.asspin.place(x = 720, y = 120)

		self.asl_ = Label(root, text = "Sign up as : ", font = self.font2, bg = 'white')
		self.asl_.place(x = 600, y = 170)

		self.as_ = StringVar()
		self.data = ('Patient','Doctor')

		self.asspin = Spinbox(root, values = self.data,textvariable = self.as_, font = self.font2, width = 19)
		self.asspin.place(x = 720, y = 170)

		self.fnamel = Label(root, text = 'first name : ', font = self.font2, bg = 'white')
		self.fnamel.place(x = 600, y = 220)
		self.fnamee = ttk.Entry(root, font = self.font2)
		self.fnamee.place(x = 720, y = 220)

		self.lnamel = Label(root, text = 'second name : ', font = self.font2, bg = 'white')
		self.lnamel.place(x = 590, y = 270)
		self.lnamee = ttk.Entry(root, font = self.font2)
		self.lnamee.place(x = 720, y = 270)

		self.addl = Label(root, text = 'address : ', font = self.font2, bg = 'white')
		self.addl.place(x = 600, y = 320)
		self.adde = ttk.Entry(root, font = self.font2)
		self.adde.place(x = 720, y = 320)

		self.phonel = Label(root, text = 'Phone no : ', font = self.font2, bg = 'white')
		self.phonel.place(x = 600, y = 370)
		self.phonee = ttk.Entry(root, font = self.font2)
		self.phonee.place(x = 720, y = 370)

		self.emaill = Label(root, text = 'email : ', font =self.font2, bg= 'white')
		self.emaill.place(x = 600, y = 420)
		self.emailee = ttk.Entry(root, font = self.font2)
		self.emailee.place(x = 720, y = 420)

		self.agel = Label(root, text = 'age  : ', font = self.font2, bg = 'white')
		self.agel.place(x = 600, y = 470)

		self.agee = ttk.Entry(root, font = self.font2)
		self.agee.place(x = 720, y = 470)

		self.registerb = ttk.Button(root, text = "Register", width = 15, command = self.registerdata)
		self.registerb.place(x = 600, y = 520)

		self.exitb = ttk.Button(root, text = "Exit", width = 15, command = self.exit_command)
		self.exitb.place(x = 750, y = 520)
		self.window = root

	def exit_command(self):
		if self.log == True:
			self.window.destroy()
			os.system("python3 firstpage.py")
		else:
			self.window.destroy()
			root1 = Tk()
			obj = patient_detect_register.PatientDetect(root1)
			root1.mainloop()


	def registerdata(self):
		work = self.as_.get()
		username = self.usernamee.get()
		fname = self.fnamee.get()
		lname = self.lnamee.get()
		add = self.adde.get()
		cell = self.phonee.get()
		email = self.emailee.get()
		age = self.agee.get()
		gender = self.gender_.get()
		if username == "" or fname == "" or lname == "" or add == "" or cell == "" or email == "" or age == "":
			messagebox.showinfo("info","some to the field are empty")
		else:
			conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
			if work == "Doctor":
				try:
					sql = f"insert into `Doctor` values('{username}', '{fname}','{lname}', '{add}','{cell}','{email}','{age}','{gender}')"
					c = conn.cursor()
					c.execute(sql)
					conn.commit()
					### give the uid_number

					sql  = f"select d_uid from doc_uid"
					lst = []
					c.execute(sql)
					data_list = c.fetchall()
					for i in data_list:
						for j in i:
							lst.append(j)
					max_uid = max(lst)
					if max_uid == 0:
						uid_assign = 27000
					else:
						uid_assign = max_uid + 1
					sql = f"insert into doc_uid values('{username}', '{uid_assign}')"
					c.execute(sql)
					conn.commit()
					conn.close()
					os.system(f"mkdir doctor_data/{uid_assign}")
					message_body = f"Hello {fname}  {lname} your UID number : {uid_assign}"
					message_body += "\n\n\nFor Any issue contact us as mkshsahani852@gmail.com"
					body_of_mail = mail_gen.generate_mail("System"," ", message_body, email)
					mail.mail_function(email, body_of_mail)
					messagebox.showinfo("info","please be static\nwe need some of your snaps")
					os.system(f"mkdir docdata/{username}")
					os.system(f"python3 first.py docdata {username}")
				except:
					messagebox.showinfo("info","this user name is already taken")

			else:
				try:
					sql = f"insert into `Patient` values('{username}', '{fname}','{lname}', '{add}','{cell}','{email}','{age}','{gender}')"
					c = conn.cursor()
					c.execute(sql)
					conn.commit()

					sql  = "select p_uid from pat_uid"
					lst = []
					c.execute(sql)
					data_list = c.fetchall()
					for i in data_list:
						for j in i:
							lst.append(j)
					max_uid = max(lst)
					if max_uid == 0:
						uid_assign = 61000
					else:
						uid_assign = max_uid + 1
					sql = f"insert into pat_uid values('{username}', '{uid_assign}')"
					c.execute(sql)
					conn.commit()
					conn.close()
					os.system(f"mkdir patient_data/{uid_assign}")
					message_body = f"Hello {fname}  {lname} your UID number : {uid_assign}"
					message_body += "\n\n\nFor Any issue contact us as mkshsahani852@gmail.com"
					body_of_mail = mail_gen.generate_mail("System"," ", message_body, email)
					mail.mail_function(email, body_of_mail)
					messagebox.showinfo("info","please be static\nwe need some of your snaps")
					os.system(f"mkdir patdata/{username}")
					os.system(f"python3 first.py patdata {username}")
				except:
					messagebox.showinfo("info","this user name is already taken")


if __name__ == "__main__":
	root = Tk()
	obj = Signup(root, True)
	root.mainloop()
