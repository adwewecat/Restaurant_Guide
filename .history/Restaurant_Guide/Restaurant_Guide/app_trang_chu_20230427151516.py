import email
from http.client import OK
import re
from unicodedata import name
from flask import render_template , request , Markup , url_for , redirect , session, sessions,send_file
import os
from Restaurant_Guide import app
# from datetime import datetime, timedelta
from flask_ckeditor import CKEditor
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from flask_ckeditor import CKEditor
from flask_mail import Mail, Message
import sqlite3
from sqlalchemy import create_engine
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import pymysql.cursors
from Restaurant_Guide.thu_vien.xu_ly_3L import *
# from GGG.thu_vien.connection import *
import socket  
from Restaurant_Guide.thu_vien.connection import *
import datetime

#upload_folder = app.static_folder
#app.config['UPLOAD_FOLDER'] = upload_folder
from io import BytesIO

import sqlite3
import openpyxl

from PIL import Image
from redmail import outlook
import random
import string

# upload_folder = app.static_folder
#upload_folder = '/GGG HCM/DUNG_IT/South_file_management/South_File_Managerment/static/images'
upload_folder = '../Restaurant_Guide/Restaurant_Guide/static/luu_file_memo'
# upload_folder = '/LAPTRINH/South_file_management/South_File_Managerment/static/images'
app.config['UPLOAD_FOLDER'] = upload_folder


ComputerName = socket.gethostname()    
IP_Address = socket.gethostbyname(ComputerName)    
# print("Your Computer Name is:" + hostname)    
# print("Your Computer IP_Address is:" + IPAddr)

Dangnhapthatbai = ""


def get_random_string():
    length=110
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# =========================================Start TRANG CHỦ==============================================
# =========================================Start TRANG CHỦ==============================================
@app.route("/", methods=["GET", "POST"])
def index():

    if session.get('session_username_19') is not None:
        username = session['session_username_19']
        # print(username)
        quyen = session['session_quyen_19'] 
        fullname = session['session_fullname_19'] 

        # Trang ADMIN
        if quyen == "1":           
            return redirect(url_for('admin')) 

        else:
            Dangnhapthatbai = "Sai User Hoặc Mật Khẩu, Vui Lòng Thử Lại"
            return render_template('login.html',DANGNHAP = Dangnhapthatbai)  



    if request.form.get("pass"):
        username = request.form.get("username").lower()
        passw = request.form.get("pass")

        save_account = request.form.get("save_account")
        
        if save_account == "yes":
            session.permanent = True
        else:
            session.permanent = False


        if username =='admin' and passw =='admin9528077':
            active = 'True'
            quyen = '1'
            fullname = 'Administrator'           
        else:
            xu_ly_dang_nhap = XU_LY_DANG_NHAP(username,passw)
            fullname = xu_ly_dang_nhap[0]
            quyen = str(xu_ly_dang_nhap[1])
            active = str(xu_ly_dang_nhap[2])


        if active == "True":
            session['session_username_19'] = username
            session['session_quyen_19'] = quyen
            session['session_fullname_19'] = fullname
                  
            Dangnhapthatbai=''
            if quyen == "1":
                return redirect(url_for('admin')) 

            # Trang APP
            if quyen == "2":           
                return redirect(url_for('ticket')) 

            else:
                Dangnhapthatbai = "User Chưa Được Phân Quyền vui lòng check lại"
                return render_template('login.html',DANGNHAP = Dangnhapthatbai, USER = username , PASS = passw)                             
        elif active == "False":
            Dangnhapthatbai = "User Đã Bị Tắt Kích Hoạt"
            return render_template('login.html',DANGNHAP = Dangnhapthatbai, USER = username , PASS = passw) 
        elif active == "-1":
            Dangnhapthatbai = "User hoặc Pass Không Chính Xác"
            return render_template('login.html',DANGNHAP = Dangnhapthatbai, USER = username , PASS = passw)   
            

    return redirect(url_for('dashboard'))
# =========================================END TRANG CHỦ=====================================================
# =========================================END TRANG CHỦ=====================================================




# ===========================ĐĂNG Xuat Start=====================================
# ===========================ĐĂNG Xuat Start=====================================
@app.route('/dang-xuat', methods=['GET', 'POST'])
def dang_xuat():

    session.pop('session_username_19', None)
    session.pop('session_quyen_19', None)
    session.pop('session_fullname_19', None)

    return redirect(url_for('index'))
    # return render_template('login.html',USER = user1 , PASS = pass1)
# ===========================ĐĂNG Xuat END=====================================
# ===========ĐĂNG Xuat END===================




# =========================== Trang Chủ dashboard Start=====================================
# =========================== Trang Chủ dashboard Start=====================================
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    huongdan_list =''
    thuongxuyen_list = ''
    khac_list = ''
    doitac_list = ''

    connection_2014 = connect_SQL_Web_NH_172_16_8_19()
    conn_2014 = connection_2014.cursor()
    sql = "SELECT id,APPNAME,LINK,HOTLINE,CLASSIFY,LOGO_APP,NOTE,IS_HUONGDAN FROM dbo.THONGTIN_APP_ALL WHERE ACTIVE='1'"
    conn_2014.execute(sql,)
    danh_sach = conn_2014.fetchall()              
    if danh_sach is not None:
        for item in danh_sach:
            id =item[0]
            appname =item[1]
            link =item[2]
            if link is None or link =='':
                link ='#'
            hotline =item[3]
            classify =item[4]
            logo =item[5]
            note =item[6]
            is_huongdan = item[7]

            if is_huongdan == 'True':
                huongdan_list +='''
                                <a href="/huongdan_app/'''+str(id)+'''" class="col-sm-6 col-xl-3" title="'''+str(hotline)+'''" target="_blank"> 
                                    <div class="bg-secondary rounded d-flex align-items-center justify-content-between p-4">
                                        <i class="'''+str(logo)+''' text-primary" style="color: #DBAC17;"></i>
                                        <div class="ms-3">
                                            <p class="mb-2">'''+str(appname)+'''</p>
                                            <h6 class="mb-0" >'''+str(note)+'''</h6>
                                        </div>
                                    </div>
                                </a>
                            '''
            if classify == 'thuong_xuyen': 
                thuongxuyen_list += '''
                                        <tr>
                                            <td>'''+str(appname)+'''</td>
                                            <td><a href="'''+str(link)+'''" class="col-sm-6 col-xl-3" target="_blank">Link truy cập</a></td>
                                            <td>'''+str(hotline)+'''</td>
                                        </tr>
                                    '''
            elif classify == 'khac': 
                khac_list += '''
                                        <tr>
                                            <td>'''+str(appname)+'''</td>
                                            <td><a href="'''+str(link)+'''" class="col-sm-6 col-xl-3" target="_blank">Link truy cập</a></td>
                                            <td>'''+str(hotline)+'''</td>
                                        </tr>
                                    '''
            elif classify =='doi_tac':
                doitac_list += '''
                                        <tr>
                                            <td>'''+str(appname)+'''</td>
                                            <td><a href="'''+str(link)+'''" class="col-sm-6 col-xl-3" target="_blank">Link truy cập</a></td>
                                            <td>'''+str(hotline)+'''</td>
                                        </tr>
                                    '''





    return render_template('QUAN_TRI/index.html',HUONGDAN_LIST = Markup(huongdan_list),THUONGXUYEN_LIST = Markup(thuongxuyen_list),KHAC_LIST = Markup(khac_list),DOITAC_LIST = Markup(doitac_list))
    # return render_template('login.html',USER = user1 , PASS = pass1)
# =========================== Trang Chủ dashboard END=====================================
# =========== Trang Chủ dashboard END===================




# =========================== Dashboard Start=====================================
# =========================== Dashboard Start=====================================
@app.route('/table', methods=['GET', 'POST'])
def table():


    return render_template('QUAN_TRI/table.html') 
    # return render_template('login.html',USER = user1 , PASS = pass1)
# =========================== Dashboard END=====================================
# =========================== Dashboard END=====================================






# =========================== Hướng Dẫn App Start=====================================
# =========================== Hướng Dẫn App Start=====================================
@app.route('/huongdan_app/<key_app>', methods=['GET', 'POST'])
def huongdan_app(key_app):
    connection_2014 = connect_SQL_Web_NH_172_16_8_19()
    conn_2014 = connection_2014.cursor()
    sql = "SELECT id,TACVU_CHINH,TACVU_PHU,FILE_DINHKEM,TENKHONGDAU_LON,TENKHONGDAU_NHO,VERSION_APP,NOTE,TEN_FILE FROM dbo.HUONGDAN_CHUNG_APP WHERE ID_APP_ALL='"+str(key_app)+"' AND ACTIVE='1' ORDER BY NGAY_INSERT"
    sql1 = str(sql)
    conn_2014.execute(sql1,)
    danh_sach = conn_2014.fetchall() 
    danhsach_html = ''  
    print(danh_sach)           
    if len(danh_sach) != 0:
        soluong_gomcot = len(danh_sach)
        soluong_chieucao = 45 *int(soluong_gomcot)
        for item in danh_sach:
            id =item[0]    
            tacvu_chinh = item[1]
            tacvu_phu = item[2]
            file_dinhkem = item[3]
            tenkhongdau_lon = item[4]
            tenkhongdau_nho = item[5]
            version_app = item[6]
            note = item[7]
            ten_file = item[8]
            danhsach_html += '''
                        <tr>
                            <td class="chinhlai_input_the_td"><input name="tacvu_chinh" id="'''+str(id)+'''" class="input_table" name='tacvu_chinh' value="'''+str(tacvu_chinh)+'''" onblur="iWillCallWhenBlur(this)"></td>
                            <td class="chinhlai_input_the_td"><input name="tacvu_chinh" id="'''+str(id)+'''"  class="input_table" value="'''+str(tacvu_phu)+'''" onblur="iWillCallWhenBlur(this)"></td>
                            <td class="chinhlai_input_the_td"><a href="link/to/your/download/file" download>'''+str(ten_file)+'''</a></td>
                            <td class="chinhlai_input_the_td"><input name="tacvu_chinh" id="'''+str(id)+'''"  class="input_table" value="'''+str(version_app)+'''" onblur="iWillCallWhenBlur(this)"></td>
                           
                            <td class="chinhlai_input_the_td"><select style="width: 100%; height: 45px; border: 0; padding-left: 15px;" name="TRANGTHAI" id="'''+str(id)+'''" onblur="iWillCallWhenBlur(this)">
                                <option label="Tắt Kích Hoạt">0</option>
                                <option label="Kích Hoạt">1</option>
                            </select></td>

                            <td class="chinhlai_input_the_td" hidden>'''+str(tenkhongdau_lon)+'''</td>
                            <td class="chinhlai_input_the_td" hidden>'''+str(tenkhongdau_nho)+'''</td>
                            <td class="chinhlai_input_the_td" hidden>'''+str(tacvu_chinh)+'''</td>
                            <td class="chinhlai_input_the_td" hidden>'''+str(tacvu_phu)+'''</td>
                            <td class="chinhlai_input_the_td" hidden>'''+str(ten_file)+'''</td>
                            <td class="chinhlai_input_the_td" hidden>'''+str(id)+'''</td>
                        </tr>
                        '''

    return render_template('QUAN_TRI/huongdan_app.html',DANHSACH_HTML = Markup(danhsach_html)) 
    # return render_template('login.html',USER = user1 , PASS = pass1)
# =========================== Hướng Dẫn App END=====================================
# =========== Hướng Dẫn App END===================



# =========================== Update Hướng Dẫn App Start=====================================
# =========================== Update Hướng Dẫn App Start=====================================
@app.route('/update_huongdan_app', methods=['GET', 'POST'])
def update_huongdan_app():
    import unidecode
    connection_2014 = connect_SQL_Web_NH_172_16_8_19()
    conn_2014 = connection_2014.cursor()
    giatri = request.form.get('gia_tri') 
    catchuoi = giatri.split("@@@")
    giatri_update = (catchuoi[0])
    cotcanupdate = (catchuoi[1])
    id_update = (catchuoi[2])

    # Bỏ dấu trong chuỗi
    giatri_update_khongdau = unidecode.unidecode(giatri_update)
    if cotcanupdate =='TACVU_CHINH':
        sql ="UPDATE dbo.HUONGDAN_CHUNG_APP SET "+str(cotcanupdate)+" = '"+str(giatri_update)+"',TENKHONGDAU_LON ='"+str(giatri_update_khongdau)+"' WHERE id='"+str(id_update)+"'"
        sql1 = str(sql)
        conn_2014.execute(sql1,)
        conn_2014.commit()   
    if cotcanupdate =='TACVU_PHU':
        sql ="UPDATE dbo.HUONGDAN_CHUNG_APP SET "+str(cotcanupdate)+" = '"+str(giatri_update)+"',TENKHONGDAU_NHO ='"+str(giatri_update_khongdau)+"' WHERE id='"+str(id_update)+"'"
        sql1 = str(sql)
        conn_2014.execute(sql1,)
        conn_2014.commit() 
        print('OK TACVU_PHU')    
    else:
        sql ="UPDATE dbo.HUONGDAN_CHUNG_APP SET "+str(cotcanupdate)+" = '"+str(giatri_update)+"' WHERE id='"+str(id_update)+"'"
        sql1 = str(sql)
        conn_2014.execute(sql1,)
        conn_2014.commit() 
        print('OK Khác') 
    return 'ok'
    # return render_template('login.html',USER = user1 , PASS = pass1)
# =========================== Update Hướng Dẫn App END=====================================
# =========== Update Hướng Dẫn App END===================






# ===========================ĐĂNG Xuat Start=====================================
# ===========================ĐĂNG Xuat Start=====================================
@app.route('/doimatkhau', methods=['GET', 'POST'])
def doimatkhau():
    if session.get('session_username') is not None:
        thongbao_admin=''
        username = session['session_username']
        quyen = session['session_quyen']
        fullname = session['session_fullname']
        if request.form.get('pass_old'):
            pass_old=request.form.get('pass_old').strip()
            pass_new=request.form.get('pass_new').strip()
            pass_new1=request.form.get('pass_new1').strip()
            if pass_new == pass_new1:
                connection_2014 = connect_database_SQL_2014()
                conn_2014 = connection_2014.cursor()
                sql = "SELECT TOP 1 id FROM LIST_USER WHERE pass=? AND user_name1 = ?"
                conn_2014.execute(sql,(pass_old,username))
                danh_sach = conn_2014.fetchall()  
                check_matkhau_old ='-1'              
                if danh_sach is not None:
                    for ten in danh_sach:
                        check_matkhau_old =ten[0]
                    
                if check_matkhau_old == '-1':
                    thongbao_admin = '''
                    <div class="alert alert-danger" style="width:1050px;margin-left: 60px">
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                    Mật Khẩu Cũ : <strong> Không </strong> Đúng
                    </div>
                    '''  
                else:
                    now = datetime.datetime.today()
                    time_hientai = now.strftime("%Y-%m-%d %H:%M:%S")              
                    sql1 ="UPDATE dbo.LIST_USER SET pass=? WHERE user_name1=?"
                    conn_2014.execute(sql1,(pass_new,username))
                    sql_logs = "INSERT dbo.LOGS(manhinh,chucnang,user_thuchien,noidung,ngay_insert,active)\
                                            VALUES(N'User_DOI_PASS',   N'USER_RESET_PASS', ? , ? ,?, 1)"
                    noidung_logs =" Pass Cũ : "+str(pass_old)+" - Pass Mới : "+str(pass_new)
                    conn_2014.execute(sql_logs,(username,noidung_logs,time_hientai))
                    conn_2014.commit()
                    thongbao_admin = '''<div class="alert alert-success alert-dismissible">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                        Reset Pass Thành Công
                                </div>'''                     
            else:
                thongbao_admin = '''
                    <div class="alert alert-danger" style="width:1050px;margin-left: 60px">
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                    Pass Mới và Pass Nhập Lại : <strong> Không </strong> Khớp
                    </div>
                    '''  
        chuoi_html_dang_xuat = CHUOI_HTML_DANG_XUAT(fullname)

        return render_template('doimatkhau.html',THONGBAO_ADMIN = Markup(thongbao_admin),USER1 = chuoi_html_dang_xuat)

    return redirect(url_for('index'))
    # return render_template('login.html',USER = user1 , PASS = pass1)
# ===========================ĐĂNG Xuat END=====================================
# ===========ĐĂNG Xuat END===================



# ===========================ĐĂNG Xuat Start=====================================
# ===========================ĐĂNG Xuat Start=====================================
@app.route('/<_key_reset>', methods=['GET', 'POST'])
def quen_matkhau(_key_reset):
    thongbao_admin=''
    _id ='-1'
    mail=''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    sql = "SELECT id,email FROM dbo.QUEN_PASS where key_reset=? AND active='1'"
    conn_2014.execute(sql,str(_key_reset))
    danh_sach = conn_2014.fetchall()             
    if danh_sach is not None:
        for item in danh_sach:
            _id =item[0]
            email =item[1]
        if _id =='-1':
            error ='<h1 style="width:100%;">Link Không Tồn Tại Hoặc Đã Hết Hạn</h1>'
            return render_template('404.html',ERROR = Markup(error),)
        else:   
            if request.form.get('pass_new'):
                passnew = request.form.get('pass_new').strip()  
                pass_new1=request.form.get('pass_new1').strip()  
                if passnew == pass_new1:            
                    sql1 ="UPDATE dbo.LIST_USER SET pass=? WHERE email=?"
                    sql2="UPDATE dbo.QUEN_PASS SET active=0 WHERE key_reset=?"
                    conn_2014.execute(sql1,(passnew,email))
                    conn_2014.execute(sql2,(_key_reset))
                    conn_2014.commit()
                    thongbao_admin = '''<div class="alert alert-success alert-dismissible">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                        Reset Pass Thành Công
                                </div>'''
                    return render_template('quen_matkhau.html',THONGBAO_ADMIN = Markup(thongbao_admin),)          
                else:
                    thongbao_admin = '''<div class="alert alert-danger alert-dismissible">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                        Pass Nhập Lại Không Khớp
                                </div>'''                    

            return render_template('quen_matkhau.html',THONGBAO_ADMIN = Markup(thongbao_admin),)


    return render_template('404.html',ERROR = Markup(error),)
    # return render_template('login.html',USER = user1 , PASS = pass1)
# ===========================ĐĂNG Xuat END=====================================
# ===========ĐĂNG Xuat END===================






# =========================== Check User đã tồn tại chưa Start=====================================
# =========================== Check User đã tồn tại chưa Start=====================================
@app.route("/Check_user_da_ton_tai_hay_chua", methods = ["POST","GET"])
def Check_user_da_ton_tai_hay_chua():
    user=request.form.get('gia_tri')
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    sql = "SELECT user_name1 FROM dbo.LIST_USER WHERE user_name1 = ?"
    conn_2014.execute(sql,(user))
    danh_sach = conn_2014.fetchall()

    check1 = '-1'
    if danh_sach is not None:
        for ten in danh_sach:
            check1 = ten[0]
            print(check1)
    # print(check1)
    if check1 == user:
        check = 'User Name:(*) <span id="check_user_span" style="color: red;">User Đã tồn tại trên hệ thống</span>'
    else:
        check = 'User Name:(*) <span id="check_user_span" style="color: #0b891b;">User Hợp Lệ</span>'

    return check
# =========================== Check User đã tồn tại chưa END=====================================
# ===========  Check User đã tồn tại chưa END===================






# =========================================Start Admin Trang Chủ User=========================
# =========================================Start Admin Trang Chủ User=========================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if session.get('session_username') is not None:
        thongbao_admin=''
        username = session['session_username']
        quyen = session['session_quyen']
        fullname = session['session_fullname'] 

    # Trang ADMIN
        if quyen == '1':
            chuoi_html_dang_xuat = CHUOI_HTML_DANG_XUAT(fullname)
            chuoi_html_user_list = CHUOI_HTML_DANH_SACH_USER_LIST()
            chuoi_html_danh_sach_quyen = HTML_LIST_DANH_SACH_QUYEN_HIEN_TAI()
            chuoi_html_danh_sach_quyen_mo_rong = HTML_LIST_DANH_SACH_QUYEN_MO_RONG_HIEN_TAI()
            # print(chuoi_html_danh_sach_quyen_mo_rong)

            # Reset Pass - Strat
            if request.form.get("update_pass"):
                now = datetime.datetime.today()
                time_hientai = now.strftime("%Y-%m-%d %H:%M:%S")               
                update_pass = request.form.get("update_pass").strip()
                _id_update_pass = request.form.get("_id_update_pass").strip()
                user_name_update_pass = request.form.get("user_name_update_pass").strip()
                connection_2014 = connect_database_SQL_2014()
                conn_2014 = connection_2014.cursor() 
                sql1 ="UPDATE dbo.LIST_USER SET pass=? WHERE id=? \
                "
                conn_2014.execute(sql1,(update_pass,_id_update_pass))
                sql_logs = "INSERT dbo.LOGS(manhinh,chucnang,user_thuchien,noidung,ngay_insert,active)\
                                        VALUES(N'Admin',   N'Reset Pass', ? , ? , ? , 1)"
                noidung_logs ="Reset Pass : *********** - User : "+str(user_name_update_pass)

                conn_2014.execute(sql_logs,(username,noidung_logs,time_hientai))
                conn_2014.commit()
                thongbao_admin = '''<div class="alert alert-success alert-dismissible">\
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                    User : <strong>'''+str(user_name_update_pass)+'''</strong> Đã Reset PassW Thành Công
                            </div>'''                                      
                conn_2014.close()
                chuoi_html_user_list = CHUOI_HTML_DANH_SACH_USER_LIST()
                chuoi_html_danh_sach_quyen = HTML_LIST_DANH_SACH_QUYEN_HIEN_TAI()
                chuoi_html_danh_sach_quyen_mo_rong = HTML_LIST_DANH_SACH_QUYEN_MO_RONG_HIEN_TAI()            
            # Reset Pass - End


            # Update User - Start
            if request.form.get("_id_update"):
                now = datetime.datetime.today()
                time_hientai = now.strftime("%Y-%m-%d %H:%M:%S")            
                _id_update = request.form.get("_id_update")
                user_update = request.form.get("user_update").strip()
                full_name_update = request.form.get("full_name_update").strip()
                email_update = request.form.get("email_update").strip()
                manv_update = request.form.get("manv_update").strip()
                active_update = request.form.get("active_update")
                phanquyen_update = request.form.get("phanquyen_update").strip()
                phanquyen_morong_update = str(request.form.get("phanquyen_morong_update"))
                if phanquyen_morong_update =='None':
                    phanquyen_morong_update = 0
                connection_2014 = connect_database_SQL_2014()
                conn_2014 = connection_2014.cursor() 
                sql1 ="UPDATE dbo.LIST_USER SET full_name=? ,email=?, manv=?, ngay_update=?,phanquyen=?,quyen_mo_rong=?,active=? WHERE id=? \
                "
                conn_2014.execute(sql1,(full_name_update,email_update,manv_update,time_hientai,phanquyen_update,phanquyen_morong_update,active_update,_id_update))
                sql_logs = "INSERT dbo.LOGS(manhinh,chucnang,user_thuchien,noidung,ngay_insert,active)\
                                        VALUES(N'Admin',   N'Update_user', ? , ? , ? , 1)"
                noidung_logs ="User : "+str(user_update)+" - Full Name : "+str(full_name_update)+" - Email : "+str(email_update)+" - Mã Nhân Viên : "+str(manv_update)+" - Phân Quyền : "+str(phanquyen_update)+" - Active : "+str(active_update)+" - Phân Quyền Mở Rộng : "+str(phanquyen_morong_update)

                conn_2014.execute(sql_logs,(username,noidung_logs,time_hientai))
                conn_2014.commit()
                thongbao_admin = '''<div class="alert alert-success alert-dismissible">\
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                    User : <strong>'''+str(user_update)+'''</strong> Đã Update Thành Công
                            </div>'''                                      
                conn_2014.close()
                chuoi_html_user_list = CHUOI_HTML_DANH_SACH_USER_LIST()
                chuoi_html_danh_sach_quyen = HTML_LIST_DANH_SACH_QUYEN_HIEN_TAI()
                chuoi_html_danh_sach_quyen_mo_rong = HTML_LIST_DANH_SACH_QUYEN_MO_RONG_HIEN_TAI()
            # Update User - End


            # Insert User - Start
            if request.form.get("user_insert"):
                now = datetime.datetime.today()
                time_hientai = now.strftime("%Y-%m-%d %H:%M:%S")
                # s2 = now.strftime("%Y%m%d%H%M%S")             
                user_insert = request.form.get("user_insert").strip().lower()
                pass_insert = request.form.get("pass_insert").strip()
                full_name_insert = request.form.get("full_name_insert").strip()
                email_insert = request.form.get("email_insert").strip()
                manv_insert = request.form.get("manv_insert").strip()
                phanquyen_insert = request.form.get("phanquyen_insert")
                phanquyen_morong_insert = str(request.form.get("phanquyen_morong_insert"))
                active_insert = request.form.get("active_insert")

                check_user_hop_le = CHECK_USER_MAIL(user_insert,email_insert)
                if check_user_hop_le == '0' or user_insert == 'admin':
                    thongbao_admin = '''
                        <div class="alert alert-danger" style="width:1050px;margin-left: 60px">
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                        User : <strong>'''+str(user_insert)+''' </strong> Hoặc Mail : <strong>'''+str(email_insert)+''' </strong> Đã Tồn Tại
                        </div>
                        '''  
                elif check_user_hop_le == '1':
                    if phanquyen_morong_insert =='None':
                        phanquyen_morong_insert = 0
                    connection_2014 = connect_database_SQL_2014()
                    conn_2014 = connection_2014.cursor() 
                    sql1 ="INSERT INTO LIST_USER (user_name1,pass,full_name,email,manv,ngay_insert,phanquyen,active,quyen_mo_rong)\
                                VALUES(?,?,?,?,?,?,?,?,?)\
                    "
                    conn_2014.execute(sql1,(user_insert,pass_insert,full_name_insert,email_insert,manv_insert,time_hientai,phanquyen_insert,active_insert,phanquyen_morong_insert))
                    sql_logs = "INSERT dbo.LOGS(manhinh,chucnang,user_thuchien,noidung,ngay_insert,active)\
                                            VALUES(N'Admin',   N'Insert_user', ? , ? ,?, 1)"
                    noidung_logs =" User : "+str(user_insert)+" - Full Name : "+str(full_name_insert)+" - Email : "+str(email_insert)+" - Mã Nhân Viên : "+str(manv_insert)+" - Phân Quyền : "+str(phanquyen_insert)+" - Active : "+str(active_insert)+" - Phân Quyền Mở Rộng : "+str(phanquyen_morong_insert)

                    conn_2014.execute(sql_logs,(username,noidung_logs,time_hientai))
                    conn_2014.commit()
                    thongbao_admin = '''<div class="alert alert-success alert-dismissible">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                        User : <strong>'''+str(user_insert)+'''</strong> Đã Thêm Thành Công
                                </div>'''                                      
                    conn_2014.close()
                    chuoi_html_user_list = CHUOI_HTML_DANH_SACH_USER_LIST()
                    chuoi_html_danh_sach_quyen = HTML_LIST_DANH_SACH_QUYEN_HIEN_TAI()
                    chuoi_html_danh_sach_quyen_mo_rong = HTML_LIST_DANH_SACH_QUYEN_MO_RONG_HIEN_TAI()
            # Insert User - End
        
        
        else:
            return redirect(url_for('index'))
        
    
        return render_template('QUAN_TRI/index.html',USER1 = chuoi_html_dang_xuat,LIST_USER = Markup(chuoi_html_user_list),DANH_SACH_QUYEN = Markup(chuoi_html_danh_sach_quyen),DANH_SACH_QUYEN_MO_RONG = Markup(chuoi_html_danh_sach_quyen_mo_rong),THONGBAO_ADMIN = Markup(thongbao_admin))
    return redirect(url_for('index'))
# =========================================END Admin Trang Chủ User===========
# =========================================END Admin Trang Chủ User===========




# =========================================Start Nhóm Quyền Detail=========================
# =========================================Start Nhóm Quyền Detail=========================
@app.route("/list_nhomquyen", methods=["GET", "POST"])
def list_nhomquyen():
    if session.get('session_username') is not None:
        thongbao_admin=''
        username = session['session_username']
        quyen = session['session_quyen']
        fullname = session['session_fullname'] 

    # Trang ADMIN
        if quyen == '1':
            chuoi_html_dang_xuat = CHUOI_HTML_DANG_XUAT(fullname)
            chuoi_html_list_nhomquyen = CHUOI_HTML_LIST_NHOMQUYEN()

            if request.form.get('tenquyen_insert'):
                now = datetime.datetime.today()
                time_hientai = now.strftime("%Y-%m-%d %H:%M:%S")            
                tenquyen_insert = request.form.get("tenquyen_insert").strip().upper()
                noidung_insert = request.form.get("noidung_insert").strip()
                active_insert = request.form.get("active_insert")

                check_tenquyen_hop_le = CHECK_TEN_QUYEN(tenquyen_insert)
                if check_tenquyen_hop_le == '0':
                    thongbao_admin = '''
                        <div class="alert alert-danger" style="width:1050px;margin-left: 60px">
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                        Quyền : <strong>'''+str(tenquyen_insert)+''' </strong> Đã Tồn Tại
                        </div>
                        '''  
                elif check_tenquyen_hop_le == '1':
                    connection_2014 = connect_database_SQL_2014()
                    conn_2014 = connection_2014.cursor() 
                    sql1 ="INSERT dbo.LV_QUYEN(tenquyen,noidung,active)VALUES(?,?,?)"
                    conn_2014.execute(sql1,(tenquyen_insert,noidung_insert,active_insert))
                    sql_logs = "INSERT dbo.LOGS(manhinh,chucnang,user_thuchien,noidung,ngay_insert,active)\
                                            VALUES(N'Admin_quyenmo_rong',   N'Insert_Nhomquyen_morong', ? , ? ,?, 1)"
                    noidung_logs =" Tên Quyền : "+str(tenquyen_insert)+" - Nội Dung : "+str(noidung_insert)+" - Trạng thái : "+str(active_insert)

                    conn_2014.execute(sql_logs,(username,noidung_logs,time_hientai))
                    conn_2014.commit()
                    thongbao_admin = '''<div class="alert alert-success alert-dismissible">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                        Nhóm Quyền Mở Rộng : <strong>'''+str(tenquyen_insert)+'''</strong> Đã Thêm Thành Công
                                </div>''' 

                    sql001 = "SELECT TOP 1 id FROM dbo.LV_QUYEN WHERE tenquyen=? "   
                    conn_2014.execute(sql001,tenquyen_insert)  
                    danh_sach = conn_2014.fetchall()   
                    if danh_sach is not None:
                        for item in danh_sach:  
                            sql002 = '''
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'view_ipwan', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'insert_ipwan', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'update_ipwan', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'view_sys', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'insert_sys', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'update_sys', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'view_ftth', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'insert_ftth', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'update_ftth', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'view_pass_mail', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'insert_pass_mail', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'update_pass_mail', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'view_code_photo', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'insert_code_photo', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'update_code_photo', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'view_ext_rsc', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'insert_ext_rsc', 0)
                                INSERT INTO dbo.PHANQUYEN_DETAIL(id_quyen,chucnang,active)VALUES('''+str(item[0])+''',N'update_ext_rsc', 0)
                            ''' 
                            sql003 = sql002
                            conn_2014.execute(sql003,)
                            conn_2014.commit()                            
                    conn_2014.close()
                    chuoi_html_list_nhomquyen = CHUOI_HTML_LIST_NHOMQUYEN()                




            if request.form.get('_id_update'):
                now = datetime.datetime.today()
                time_hientai = now.strftime("%Y-%m-%d %H:%M:%S")  
                _id_update = request.form.get("_id_update").strip()       
                tenquyen_update = request.form.get("tenquyen_update").strip().upper()
                noidung_update = request.form.get("noidung_update").strip()
                active_update = request.form.get("active_update")

                connection_2014 = connect_database_SQL_2014()
                conn_2014 = connection_2014.cursor() 
                sql1 ="UPDATE dbo.LV_QUYEN SET noidung=?, active=? WHERE id=?"
                conn_2014.execute(sql1,(noidung_update,active_update,_id_update))
                sql_logs = "INSERT dbo.LOGS(manhinh,chucnang,user_thuchien,noidung,ngay_insert,active)\
                                        VALUES(N'Admin_quyenmo_rong',   N'Update_Nhomquyen_morong', ? , ? ,?, 1)"
                noidung_logs =" Tên Quyền : "+str(tenquyen_update)+" - Nội Dung : "+str(noidung_update)+" - Trạng thái : "+str(active_update)

                conn_2014.execute(sql_logs,(username,noidung_logs,time_hientai))
                conn_2014.commit()
                thongbao_admin = '''<div class="alert alert-success alert-dismissible">\
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                    Nhóm Quyền Mở Rộng : <strong>'''+str(tenquyen_update)+'''</strong> Đã Update Thành Công
                            </div>'''                                      
                conn_2014.close()
                chuoi_html_list_nhomquyen = CHUOI_HTML_LIST_NHOMQUYEN()  


            
            return render_template('QUAN_TRI/nhomquyen.html',USER1 = chuoi_html_dang_xuat,LIST_NHOMQUYEN = Markup(chuoi_html_list_nhomquyen),THONGBAO_ADMIN = Markup(thongbao_admin))
    return redirect(url_for('index'))
# =========================================END Nhóm Quyền Detail===========
# =========================================END Nhóm Quyền Deatail===========









