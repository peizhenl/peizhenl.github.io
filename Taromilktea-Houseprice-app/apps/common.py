#coding:utf -8
from flask import session, request, redirect
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import time
from functools import wraps

# get the datetime after specified days
def get_datetime_after(days):
    return datetime.now() + timedelta(days)
    
# def datetime_diff(datetime1, datetime2):
#     format = "%Y-%m-%d %H:%M:%S"
#     return not (datetime.strptime(datetime1.strftime(format), format) >
#                 datetime.strptime(datetime2.strftime(format), format))


# def sendMessage(host, port, sender, password, receiver, subject, content):
#     message = MIMEText(content, "plain", "utf-8")

#     message['Subject'] = subject
#     message['To'] = receiver
#     message['From'] = sender

#     smtp = smtplib.SMTP_SSL(host, port)
#     smtp.login(sender, password)
#     smtp.sendmail(sender, [receiver], message.as_string())
#     smtp.close()


def format_price(amount, currency=u'£'):
    return u'{1}{0:.2f}'.format(amount, currency)

# get the list length
def length(params):
    return len(params)

def load_filters(env):
    env.filters['length'] = length
    env.filters['format_price'] = format_price

# get file extension
def get_file_extension(filename):
    """
        get file extension
    """
    ext = ".jpg"
    if filename:
        ext = filename.split(".")[-1]
    return ".{}".format(ext)

# generate the order number
def get_order_code():
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[-7:]
    return order_no

# user login intercept
def login_require(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            session['redirect'] = request.path
            return redirect("/user/login.html")
    return decorator

# admin login interceptor
def admin_login_require(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'admin_id' in session:
            return func(*args, **kwargs)
        else:
            session['redirect'] = request.path
            return redirect("/admin/login.html")

    return decorator

if __name__ == "__main__":
    print(get_order_code())
