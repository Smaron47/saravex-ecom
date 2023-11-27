 # Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import requests
import os 
import json
from random import random
#from datetime import datetime




#now=datetime.now()
UPLOAD_FOLDER = '/pictures'
app = Flask(__name__)
app.secret_key="fuckyou"
j=os.getcwd()+"/static/img/product"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#l=os.listdir(j)
def datas(s):
	try:
		datas=open(s,"r")
		datas=datas.read()
		datas=datas[1:len(datas)-1]
		#print(datas)
		datas=datas.replace("'","\"")
		datas=json.loads(datas)
		return datas
	except:
		datas=open(s,"r")
		datas=datas.read()
		datas=datas[1:len(datas)-2]
		#print(datas)
		datas=datas.replace("'","\"")
		datas=json.loads(datas)
		return datas	

def lod(e,rea):
		rea=rea.replace("'","")
		rea=rea.replace("'","\"")
		print(type(rea))
		print(rea)
		
		rea=json.loads(rea)	
		updic={e:rea}
		updic=str(updic)
		updic=updic.replace("'","\"")
		print(updic)
		print(type(updic))
		updic=json.loads(updic)
		return updic

def wri(fn,da):
	file=open(fn,"w")
	file.write(f"'{da}'")
	file.close()





@app.route('/', methods=['get'])
def index():
	'''print(os.getcwd())
	prod=datas("tryp")'''
	try:
		url = ('http://ip-api.com/json/{}'.format(request.headers.get('X-Forwarded-For')))
		r = requests.get(url)
		j = json.loads(r.text)
		city = j['country']
		
	except:
		city = ""
		print(city)
	session['country'] = city
	#print(r.text,request.headers.get('X-Forwarded-For'))
	li={}
	da=datas('catagory')
	for i in da:
		m=(list(da[i].values())[0])['pic'][0]
		print(m)
		li.update({i:m})
		print(li)
	session['cata'] = da
	session['lip'] = li
	dl=list(da.keys())[:5]
	session['dl']=dl
	if 'user' in session:
		user = session['user']
		email=session['email']
		dat=datas("regi")
		session['product']=dat[email]['products']
		session['cart'] = len(dat[email]['products'])
		return render_template("home_image_slider.html",user=user,city=city,product=session['product'],catagory=da,li=li,cart=session['cart'],dl=session['dl'])
	else:
		return render_template("home_image_slider.html",city=city,catagory=da,li=li,dl=session['dl'])
@app.route('/login', methods=['get','post'])
def login():
	print(os.getcwd())
	return render_template("login.html",city=session['country'],catagory=session['cata'],li=session['lip'],dl=session['dl'])
@app.route('/register', methods=['get','post'])
def register():
	print(os.getcwd())
	return render_template("register.html",city=session['country'])
@app.route('/searche_name',methods=['GET',"POST"])
def searche_name():
	name=request.form['searche_name']
	cat=datas('catagory')
	produc=datas("product")
	if name in cat:
		dat=cat[name]
		print(dat)
		if 'user' in session:
			return render_template("product_search_page.html",data=dat,user=session['user'],cart=session['cart'],dl=session['dl'],city=session['country'])
		else:
			return render_template("product_search_page.html",data=dat,dl=session['dl'],city=session['country'])
	else:

		li={}
		try:
			for i in produc:
				if name in produc[i]['descip']:
					print(produc[i],i)
					li.update({i:produc[i]})				
			print(li)
			if 'user' in session:

				return render_template("product_search_page.html",data=li,user=session['user'],cart=session['cart'],dl=session['dl'],city=session['country'])
			else:
				return render_template("product_search_page.html",data=li,dl=session['dl'],city=session['country'])
		except:
			if 'user' in session:

				return render_template("product_search_page.html",data="No Search match",user=session['user'],cart=session['cart'],dl=session['dl'],city=session['country'])
			else:
				return render_template("product_search_page.html",data="No Search match",dl=session['dl'],city=session['country'])
@app.route('/cat_book',methods=['GET',"POST"])
def cat_book():
	name="book"
	cat=datas('catagory')
	produc=datas("product")
	li={}
	if name in cat:
		dat=cat[name]
		print(dat)
		return render_template("product_search_page.html",city=session['country'],data=dat,user=session['user'],cart=session['cart'],dl=session['dl'])
	else:

		try:
			for i in produc:
				if name in produc[i]['descip']:
					li.update(i)				

			return render_template("product_search_page.html",city=session['country'],data=li,user=session['user'],cart=session['cart'],dl=session['dl'])
		except:
			return render_template("product_search_page.html",city=session['country'],data="No Search match",dl=session['dl'],user=session['user'],cart=session['cart'])

@app.route("/test" , methods=['GET', 'POST'])
def test():
	select = request.form['Pri Pos']
	print(str(select))
	return(str(select)) # just to see what select is



@app.route("/test1" , methods=['GET', 'POST'])
def test1():
	return render_template('404.html') # just to see what select is



@app.route("/catagory_i/<search_item>" , methods=['GET', 'POST'])
def catagory_i(search_item):
	si=search_item
	data=datas('catagory')
	dat=data[si]
	if 'user' in session:
		return render_template("product_search_page.html",city=session['country'],dl=session['dl'],data=dat,user=session['user'],cart=session['cart'])
	else:
		return render_template("product_search_page.html",city=session['country'],dl=session['dl'],data=dat)









@app.route('/profile',methods=['GET',"POST"])
def profile():
	try:
		user=session['user']
		email=session['email']
		return render_template("your_account.html",dl=session['dl'],user=user,city=session['country'],cart=session['cart'])
	except:
		return render_template("home_image_slider.html",dl=session['dl'],city=session['city'],catagory=session['cata'],li=session['lip'])
@app.route('/address',methods=['GET',"POST"])
def address():
	user=session['user']
	email=session['email']
	dat=datas("regi")
	try:
		addr=dat[email]['address']
	except:
		addr=''
	return render_template("your_addresses.html",city=session['country'],dl=session['dl'],user=user,cart=session['cart'],addr=addr)

@app.route('/add_new_address',methods=['GET',"POST"])
def add_new_address():
	user=session['user']
	email=session['email']
	return render_template("add_new_address.html",city=session['country'],dl=session['dl'],user=user,cart=session['cart'])

@app.route('/seller_account_register',methods=['GET',"POST"])
def seller_account_register():
	user=session['user']
	email=session['email']
	return render_template("seller_account_register.html",dl=session['dl'],user=user,city=session['country'],email=email,cart=session['cart'])






@app.route('/address_change',methods=['GET',"POST"])
def address_change():
	user=session['user']
	email=session['email']
	name=request.form['username']
	country=request.form['country']
	number=request.form['mobileNumber']
	house=request.form['houseNumber']
	area=request.form['area']
	landmark=request.form['landmark']
	city=request.form['city']
	state=request.form['state']
	addressty=request.form['addressType']
	print(addressty)
	f=datas("regi")
	if email in f:
		if 'address' in f[email]:
			rea=str({f'"name":"{name}","number":"{number}","house":"{house}","area":"{area}","city":"{city}","state":"{state}","country":"{country}"'})
			up=lod(addressty,rea)
			f[email]['address'].update(up)
		else:
			f[email].update({'address':{}})
			rea=str({f'"name":"{name}","number":"{number}","house":"{house}","area":"{area}","city":"{city}","state":"{state}","country":"{country}"'})
			up=lod(addressty,rea)
			print(up)
			f[email]['address'].update(up)
		
		file=open("regi","w")
		file.write(f"'{f}'")
		file.close()
	return render_template("your_addresses.html",user=user,city=session['country'])






@app.route("/get_regi", methods=["GET","POST"])
def get_regi():
	try:
		name=request.form["uname"]
		email=request.form["email"]
		passw=request.form["pass"]
		passw1=request.form["pass1"]
		if passw==passw1:
			rea=str({f'"name":"{name}","email":"{email}","passw":"{passw}"'})
			


			up=lod(email,rea)
			up[email].update({"products":{},"address":{}})
			dat=datas("regi")
			#print(dat,type(dat))
			dat.update(up)
			print(dat)
			file=open("regi","w")
			file.write(f"'{dat}'")
			file.close()
			session['user'] = name
			session['email'] = email
			f=open(email,"a")
			f.write(f"'{up}'")
			f.close()
			return render_template("home_image_slider.html",city=session['country'],dl=session['dl'],user=name,catagory=session['cata'],li=session['lip'])
	except:
		return render_template("404.html",data="Some Porblem Found.. Please Try Again Later.",city=session['country'])
@app.route("/get_login", methods=["GET","POST"])
def get_login():
	
	email=request.form["email"]
	passw=request.form["passw"]
	print(email,passw)
	session['user'] = email
	k=datas("regi")
	if email == k[email]['email'] and passw == k[email]['passw']:
		session['user'] = k[email]['name']
		session['email'] = k[email]['email']
		session['cart'] = len(k[email]['products'])
		return render_template("home_image_slider.html",city=session['country'],dl=session['dl'],user=k[email]['name'],catagory=session['cata'],li=session['lip'],cart=session['cart'])
	elif email =="Smaronbi" and passw=="Smaronbi":
		return render_template("admin-index.html",city=session['country'],dl=session['dl'],user=session['user'])
	return render_template("404.html",city=session['country'],dl=session['dl'],user=session['user'],data="Problem in login.. Please register or Login letter")

@app.route('/logout',methods=['GET',"POST"])
def logout():
	print(session)
	session.pop("email",None)
	session.pop("user",None)
	session.pop('cart',None)
	return render_template("home_image_slider.html",city=session['country'],dl=session['dl'],catagory=session['cata'],li=session['lip'])



@app.route('/seller_account_intro',methods=['GET',"POST"])
def seller_account_intro():
	k=datas('regi')
	if 'user' in session:
		user=session['user']
		if 'seller' in k[session['email']]:
			return render_template("your_seller_account.html",dl=session['dl'],user=user,city=session['country'],cart=session['cart'])
		return render_template("seller_account_intro.html",dl=session['dl'],user=user,city=session['country'],cart=session['cart'])
	else:
		return render_template("home_slider_image.html",dl=session['dl'],city=session['country'])



@app.route("/get_seller_regi", methods=["GET","POST"])
def get_seller_regi():
	
	busname=request.form["sellerName"]
	busdes=request.form["sellerDescription"]
	
	email=session['email']
	rea=str({f'"email":"{email}","business":"{busname}","business_description":"{busdes}"'})
	up=lod(email,rea)
	up[email].update({"products":{}})
	seller=datas('sellers')
	seller.update(up)
	file=open("sellers","w")
	file.write(f"'{seller}'")
	file.close()
	dat=datas('regi')
	dat[email].update({'seller':'True'})

	file=open("regi","w")
	file.write(f"'{dat}'")
	file.close()
	user=session['user']
	return render_template("your_seller_account.html",dl=session['dl'],user=user,city=session['country'])

@app.route('/product_up',methods=['GET',"POST"])
def product_up():
	k=datas('regi')
	if 'user' in session:
		user=session['user']
		if 'seller' in k[session['email']]:
			return render_template("add_new_product.html",cata=session['cata'],dl=session['dl'],user=user,city=session['country'],cart=session['cart'])
		return render_template("add_new_product.html",cata=session['cata'],dl=session['dl'],user=user,city=session['country'],cart=session['cart'])
	else:
		return render_template("add_new_product.html",cata=session['cata'],dl=session['dl'],city=session['country'])

@app.route('/upload_product',methods=['GET',"POST"])
def upload_product():
	k=datas('regi')
	cat=datas('catagory')
	products=datas('product')
	product_id=str(random())
	pTitel=request.form['title']
	descip=request.form['description']
	discount=request.form['discount']
	price=request.form['price']
	number=request.form['number']
	pil=[]



	file=request.files['file1']
	pn=file.filename
	pn=pn.split(".")
	pn[0]=product_id
	file.save(f'{j}/{pn[0]+"1."+pn[1]}')
	pil.append(f'img/product/{pn[0]+"1."+pn[1]}')

	file=request.files['file2']
	pn=file.filename
	pn=pn.split(".")
	pn[0]=product_id
	file.save(f'{j}/{pn[0]+"2."+pn[1]}')
	pil.append(f'img/product/{pn[0]+"2."+pn[1]}')

	file=request.files['file3']
	pn=file.filename
	pn=pn.split(".")
	pn[0]=product_id
	file.save(f'{j}/{pn[0]+"3."+pn[1]}')
	pil.append(f'img/product/{pn[0]+"3."+pn[1]}')

	file=request.files['file4']
	pn=file.filename
	pn=pn.split(".")
	pn[0]=product_id
	file.save(f'{j}/{pn[0]+"4."+pn[1]}')
	pil.append(f'img/product/{pn[0]+"4."+pn[1]}')


	print(pil)




	if product_id in products:
		product_id=str(random())
	if 'user' in session:
		user=session['email']
		user1=session['user']
		rea=str({f'"titel":"{pTitel}","descip":"{descip}","price":"{price}","discount":"{discount}","number":"{number}","pic":{pil},"seller":"{user1}","seller_email":"{user}"'})
		if 'seller' in k[session['email']]:
			select = request.form.get('productCategory')
			if select in cat:
				up=lod(product_id,rea)
				cat[select].update(up)
				products.update(up)
				wri('catagory',cat)
				sl=datas('sellers')
				sl[session['email']]['products'].update(up)
				wri('sellers',sl)
				wri('product',products)
				return render_template("your_seller_account.html",dl=session['dl'],user=session['user'],city=session['country'])
			else:
				up=lod(product_id,rea)
				cat.update({f"{select}":{}})
				cat[select].update(up)
				products.update(up)
				wri('catagory',cat)
				sl=datas('sellers')
				sl[session['email']]['products'].update(up)
				wri('sellers',sl)
				wri('product',products)
				return render_template("your_seller_account.html",dl=session['dl'],user=session['user'],cart=session['cart'],city=session['country'])
	return render_template("404.html",city=session['country'],dl=session['dl'],data="Something Went Wrong While UPLOADING.. ",user=session['user'])


@app.route('/product/<record_id>', methods=['get','post'])
def product(record_id):
	f=record_id
	dat=datas("product")
	dat=dat[f]
	try:
		return render_template("product_main_page.html",dl=session['dl'],city=session['country'],dat=dat,user=session['user'],i=f,cart=session['cart'])
	except:
		return render_template("product_main_page.html",dl=session['dl'],city=session['country'],dat=dat,i=f)
@app.route('/myproduct', methods=['get','post'])
def myproduct():
	try:
		user=session['user']
		k=datas('sellers')
		dat=k[user]['products']
		return render_template("your_orders.html",dl=session['dl'],user=user,city=session['country'],dat=dat,cart=session['cart'])

	except:
		data="Please Login or Create New Account"
		return render_template("404.html",city=session['country'],dl=session['dl'],data=data)




@app.route('/product_list',methods=['GET','POST'])
def product_list():
	try:
		user=session['email']
		data=datas('sellers')
		productL=data[user]['products']
		return render_template("your_orders.html",city=session['country'],dl=session['dl'],dat=productL,user=session['user'],cart=session['cart'])
	except:
		return render_template("404.html",city=session['country'],dl=session['dl'],data="Please Login, or Uplaod Products to your shop",user=session['user'])



@app.route('/your_orders',methods=['GET','POST'])
def your_orders():
	if 'user' in session:

		try:
			user=session['email']
			data=datas('regi')
			productL=data[user]['products']
			print(productL)
			s=0
			for i in productL:
				s=s+int(productL[i]['price'])
			session['stp']=s
			return render_template("your_orders.html",dl=session['dl'],total=s,dat=productL,user=session['user'],city=session['country'],cat="-",u='')
		except:
			
			return render_template("404.html",dl=session['dl'],city=session['country'],cat="-",u='1')
	else:
		return render_template("404.html",dl=session['dl'],city=session['country'],cat="-")
@app.route('/add_to_cart/<p_id>',methods=['GET','POST'])
def add_to_cart(p_id):

		try:
			p=p_id
			user=session['email']
			product=datas('product')
			data=datas('regi')
			productL=data[user]['products']
			productL.update({p:product[p]})
			wri("regi",data)
			print(session['product'])
			return render_template("product_main_page.html",dl=session['dl'],city=session['country'],dat=product[p],user=session['user'],i=p,cart=session['cart'])
		except:
			return render_template("404.html",city=session['country'],dl=session['dl'],data="Please Login, or Uplaod Products to your shop")
	
@app.route('/about_us', methods=['get','post'])
def about_us():
	if 'user' in session:
		return render_template("about_us.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'])
	else:
		return render_template("about_us.html",dl=session['dl'],city=session['country'])

@app.route('/contactus', methods=['get','post'])
def contactus():
	if 'user' in session:
		return render_template("contactus.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'])
	else:
		return render_template("contactus.html",dl=session['dl'],city=session['country'])


@app.route('/confirm_order/<p_id>', methods=['get','post'])
def confirm_order(p_id):
	p=p_id
	f=datas('regi')
	addr=f[session['email']]['address']
	if 'user' in session:
		if len(addr) == 0:
			return render_template("select_payment_method.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'])
		else:
			return render_template("select_payment_method.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'],addr=addr,pid=p)
	else:
		return render_template("select_payment_method.html")

@app.route('/cancel_order/<p_id>', methods=['get','post'])
def cancel_order(p_id):
	try:
		p=p_id
		dat=datas("regi")
		dat[session['email']]['products'].pop(p)
		wri('regi',dat)
		return render_template("your_orders.html",dl=session['dl'],city=session['country'],user=session['user'],dat=dat[session['email']]['products'],total=session['stp'],cart=session['cart'])
	except:
		return render_template("404.html",dl=session['dl'],city=session['country'],user=session['user'],dat="Please Try Again")




@app.route('/terms_and_condition', methods=['get','post'])
def terms_and_condition():
	if 'user' in session:
		return render_template("termsandcondi.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'])
	else:
		return render_template("termsandcondi.html",dl=session['dl'],city=session['country'])
@app.route('/faq', methods=['get','post'])
def faq():
	if 'user' in session:
		return render_template("faq.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'])
	else:
		return render_template("faq.html",dl=session['dl'],city=session['country'])

@app.route('/privacy_policy', methods=['get','post'])
def privacy_policy():
	if 'user' in session:
		return render_template("privacy-policy.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'])
	else:
		return render_template("privacy-policy.html",dl=session['dl'],city=session['country'])
@app.route('/return_policy', methods=['get','post'])
def return_policy():
	if 'user' in session:
		return render_template("return_policy.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'])
	else:
		return render_template("return_policy.html",dl=session['dl'],city=session['country'])



@app.route('/buy/<pid>', methods=['get','post'])
def buy(pid):
	p=pid
	f=datas('product')
	se=datas('sellers')
	dat=datas('regi')
	product=f[p]
	seller=f[p]['seller_email']
	address=request.form['address']
	ads=dat[session['email']]['address'][address]
	delivary=request.form['paymentMethod']
	try:
		se[seller]['order'].update({p:product})
		se[seller]['order'][p].update({'delivary':delivary})
		se[seller]['order'][p].update({'address':ads})
		wri("sellers",se)
	except:
		se[seller].update({'order':{}})
		se[seller]['order'].update({p:product})
		se[seller]['order'][p].update({'delivary':delivary})
		se[seller]['order'][p].update({'address':ads})
		wri("sellers",se)

	if 'user' in session:
		return render_template("home_image_slider.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'],catagory=session['cata'],li=session['lip'],product=session['product'])
	else:
		return render_template("home_image_slider.html",dl=session['dl'],city=session['country'],catagory=session['cata'],li=session['lip'],product=session['product'])



@app.route('/seller_order', methods=['get','post'])
def seller_order():
	user=session['email']
	da=datas('sellers')
	dat=da[user]['order']
	if 'user' in session:
		return render_template("seller_order.html",dl=session['dl'],city=session['country'],user=session['user'],cart=session['cart'],dat=dat)
	else:
		return render_template("seller_order.html",dl=session['dl'],city=session['country'])



















#


if __name__ == '__main__':
       app.run(host="0.0.0.0",port=5000,debug=True)


'''
import imageio,os
o=[]
inp=input("Enter the images (separet wiht space) : ")
inp=inp.replace("'","")
images = inp.split(" ")
print(images)
for i in images:
	o.append(imageio.imread(i))
imageio.mimsave(f'{os.getcwd()}/movie.gif', o)
'''
