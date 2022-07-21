from apps.db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import datetime as dt
from apps.common import get_datetime_after

# User model
class User(db.Model):

    __tablename__ = 't_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100))
    _password = db.Column(db.String(200))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    avatar = db.Column(db.String(500))
    is_admin = db.Column(db.SmallInteger, default=0)
    create_at = db.Column(db.DateTime, default=dt.datetime.now)
    update_at = db.Column(db.DateTime, default=dt.datetime.now)

    user_orders = db.relationship("Order", backref="order_user", lazy=True)

    # getter method，it could access the password by dot.password instead of adding
    # bracket
    @property
    def password(self):
        return self._password

    # setter method
    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    # password validate
    def check_password(self, origin_password):
        return check_password_hash(self.password, origin_password)
    

    def keys(self):
        return ['id', 'username', 'first_name', 'second_name', 'gender', 'phone', 'avatar', 'is_admin', 'create_at', 'update_at']

    def __getitem__(self, item):
        return getattr(self, item)

# Good category model
class GoodCategory(db.Model):

    __tablename__ = 't_good_category'

    def __init__(self, name, description):
        self.name = name
        self.description = description

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300))
    description = db.Column(db.String(100))
    create_at = db.Column(db.DateTime, default=dt.datetime.now)
    update_at = db.Column(db.DateTime, default=dt.datetime.now)

    def keys(self):
        return ['id', 'name', 'description', 'create_at', 'update_at']

    def __getitem__(self, item):
        return getattr(self, item)

# Good model
class Good(db.Model):

    __tablename__ = 't_good'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    good_category_id = db.Column(db.Integer,
                                 db.ForeignKey('t_good_category.id'),
                                 nullable=False)
    name = db.Column(db.String(300))
    description = db.Column(db.Text, default='')
    price = db.Column(db.DECIMAL(20, 2), nullable=False, default=0.0)
    discout_rate = db.Column(db.DECIMAL(10, 3), default=1.0)
    stock = db.Column(db.Integer, default=0)
    purchase_number = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    can_refund = db.Column(db.SmallInteger, default=0)
    status = db.Column(db.SmallInteger, default=0)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    category = db.relationship('GoodCategory', backref='good_category', lazy=True)

    transaction_records = []

    def keys(self):
        return ['id', 'good_category_id', 'name', 'description', 'price', 'discout_rate', 'stock', 'purchase_number', 'image_url', 'can_refund', 'status', 'create_at', 'update_at', 'transaction_records']

    def __getitem__(self, item):
        return getattr(self, item)

# Cart model
class Cart(db.Model):

    __tablename__ = 't_cart'

    def __init__(self, user_id, good_id, quantity):
        self.user_id = user_id
        self.good_id = good_id
        self.quantity = quantity

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,
                           db.ForeignKey('t_user.id'),
                           nullable=False)
    good_id = db.Column(db.Integer,
                           db.ForeignKey('t_good.id'),
                           nullable=False)
    quantity = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=dt.datetime.now)
    update_at = db.Column(db.DateTime, default=dt.datetime.now)

    user = db.relationship('User', backref='user', uselist=False)
    good = db.relationship('Good', backref='cart_good', uselist=False)

    def keys(self):
        return ['id', 'user_id', 'good_id', 'quantity', 'create_at', 'update_at']

    def __getitem__(self, item):
        return getattr(self, item)

# order item model
class OrderItem(db.Model):

    __tablename__ = 't_order_item'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer,
                           db.ForeignKey('t_order.id'),
                           nullable=False)
    good_id = db.Column(db.Integer,
                          db.ForeignKey('t_good.id'),
                          nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit_price = db.Column(db.DECIMAL(20, 2), default=0.0)
    good_price = db.Column(db.DECIMAL(20, 2), default=0.0)
    create_at = db.Column(db.DateTime, default=dt.datetime.now)
    update_at = db.Column(db.DateTime, default=dt.datetime.now)

    # order = db.relationship('Order', backref='order')
    good = db.relationship('Good', backref='good_order_item')

    def keys(self):
        return ['id', 'order_id', 'good_id', 'quantity', 'create_at', 'update_at']

    def __getitem__(self, item):
        return getattr(self, item)

# Order model
class Order(db.Model):

    __tablename__ = 't_order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    pay_price = db.Column(db.DECIMAL(20, 2))
    # the status whether the goods price had been paid, 0 unpaid,1 paid
    pay_status = db.Column(db.Integer, default=0)
    is_refund = db.Column(db.SmallInteger, default=0)
    create_at = db.Column(db.DateTime, default=datetime.now)
    # By default, set the expired datetime to 7 days
    expire_at = db.Column(db.DateTime, default=get_datetime_after(7))
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    orderItems = db.relationship('OrderItem', backref='items_order', lazy='dynamic', cascade="save-update, merge, delete")
    receiptInfo = db.relationship('ReceiptInfo', backref='receipt_info_order', cascade="delete")
    paymentInfo = db.relationship('PaymentInfo', backref='payment_info_order', cascade="delete")
    refundInfo = db.relationship('RefundInfo', backref='refund_info', cascade="delete", uselist=False)
    

    def keys(self):
        return ['id', 'good_number', 'user_id',
                'pay_price', 'pay_status', 'expire_at'
                'create_datetime', 'update_datetime']

    def __getitem__(self, item):
        return getattr(self, item)

# user address
class UserAddress(db.Model):
    __tablename__ = 't_user_address'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)
    consignee_name = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    remark = db.Column(db.String)
    is_default = db.Column(db.SmallInteger)
    create_at = db.Column(db.DateTime, default=dt.datetime.now)
    update_at = db.Column(db.DateTime, default=dt.datetime.now)

    user = db.relationship('User', backref='user_address')

    def keys(self):
        return ['id', 'user_id', 'consignee_name', 'address', 'phone', 'remark', 'is_default', 'create_at', 'update_at']

    def __getitem__(self, item):
        return getattr(self, item)

# receipt information model
class ReceiptInfo(db.Model):

    __tablename__ = 't_receipt_info'

    def __init__(self, order_id, user_address_id):
        self.order_id = order_id
        self.user_address_id = user_address_id

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer,db.ForeignKey('t_order.id'),nullable=False)
    user_address_id = db.Column(db.Integer, db.ForeignKey('t_user_address.id'), nullable=False)
    create_at = db.Column(db.DateTime, default=dt.datetime.now)
    update_at = db.Column(db.DateTime, default=dt.datetime.now)

    # order = db.relationship('Order', backref='good_order')
    userAddress = db.relationship('UserAddress', backref='receipt_info_address')

    def keys(self):
        return ['id', 'order_id', 'user_address_id', 'create_at', 'update_at']

    def __getitem__(self, item):
        return getattr(self, item)

# payment information model
class PaymentInfo(db.Model):

    __tablename__ = 't_payment_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer,
                         db.ForeignKey('t_order.id'),
                         nullable=False)
    card_no = db.Column(db.String)
    remark = db.Column(db.String)
    create_at = db.Column(db.DateTime, default=dt.datetime.now)
    update_at = db.Column(db.DateTime, default=dt.datetime.now)

    # payment_order = db.relationship('Order', backref='payment_order')

    def keys(self):
        return ['id', 'order_id', 'card_no', 'remark', 'create_at', 'update_at']

    def __getitem__(self, item):
        return getattr(self, item)

# refund 
class RefundInfo(db.Model):

    __tablename__ = 't_refund_info'

    def __init__(self, order_id, refund_reason):
        self.order_id = order_id
        self.refund_reason = refund_reason

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer,db.ForeignKey('t_order.id'),nullable=False)
    refund_reason = db.Column(db.String)
    is_approve = db.Column(db.SmallInteger, default=0)
    refund_at = db.Column(db.DateTime, default=dt.datetime.now)
    update_at = db.Column(db.DateTime, default=dt.datetime.now)

    refund_order = db.relationship('Order', backref='refund_order')

    def keys(self):
        return ['id', 'order_id', 'refund_reason', 'is_approve', 'create_at', 'update_at']

    def __getitem__(self, item):
        return getattr(self, item)


