from datetime import datetime
from sqlalchemy.dialects.mysql import INTEGER
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql

app = Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:qqssb@liangc.me:3306/crawler"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asdasdasd'
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    publishDate = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    productId = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    view = db.Column(db.Integer, default=0, nullable=False)
    # 关系
    image = db.relationship("Image", backref="book")
    browsingHistory = db.relationship("BrowsingHistory", backref="books")
    orderItem = db.relationship("OrderItem", backref="books")
    shopping_cart_item_entity = db.relationship("shopping_cart_item_entity", backref="books")
    favoriteBook = db.relationship("userFavoriteBook", backref="books")


class Image(db.Model):
    __tablename__ = "book_image"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.TEXT, nullable=False)
    bookId = db.Column(db.Integer, db.ForeignKey("book.id"))
    type = db.Column(db.Enum("bigImage", "smallImage"))


class BrowsingHistory(db.Model):
    __tablename__ = "browsingHistory"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    bookId = db.Column(db.Integer, db.ForeignKey("book.id"))


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descriptionStar = db.Column(db.Integer, nullable=False)
    transportStar = db.Column(db.Integer, nullable=False)
    itemStar = db.Column(db.Integer, nullable=False)
    commentStr = db.Column(db.String(255), nullable=False)

    orderItem = db.relationship("OrderItem",backref="comment")


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    sumPrice = db.Column(db.Float, nullable=False)

    orderItem = db.relationship("OrderItem", backref="order")


class OrderItem(db.Model):
    __tablename__ = "orderItem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    count = db.Column(db.Integer, nullable=False)
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    orderId = db.Column(db.Integer, db.ForeignKey('order.id'))
    bookId = db.Column(db.Integer, db.ForeignKey("book.id"))
    status = db.Column(db.Enum('pendingPayment', 'pendingReceived', 'pendingComment', 'finish', 'cancel'),
                       nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    commentId = db.Column(db.Integer, db.ForeignKey('comment.id'))
    addressId = db.Column(db.Integer)


class post_comment_entity(db.Model):
    __tablename__ = "post_comment_entity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    likeCount = db.Column(db.Integer, default=0, nullable=False)
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    postId = db.Column(db.Integer, db.ForeignKey("post_entity.id"))
    parentCommentId = db.Column(db.Integer, db.ForeignKey("post_comment_entity.id"))
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    mpath = db.Column(db.String(255), default='')


class post_entity(db.Model):
    __tablename__ = "post_entity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    deltaContent = db.Column(db.TEXT, nullable=False)
    htmlContent = db.Column(db.TEXT, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    views = db.Column(db.Integer, default=0, nullable=False)

    post_comment_entity = db.relationship("post_comment_entity", backref="post_entitys")
    post_image_entity = db.relationship("post_image_entity", backref="post_entity")


class post_image_entity(db.Model):
    __tablename__ = "post_image_entity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey("post_entity.id"))
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)


class search_history(db.Model):
    __tablename__ = "search_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    searchName = db.Column(db.String(255), nullable=False, unique=True)
    searchTimes = db.Column(db.Integer, default=0, nullable=False)
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)


class Sessions(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expires = db.Column(INTEGER(unsigned=True), nullable=False)
    data = db.Column(db.Text(65536))


class shopping_cart_item_entity(db.Model):
    __tablename__ = "shopping_cart_item_entity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    bookId = db.Column(db.Integer, db.ForeignKey("book.id"))
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))


class user(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    email = db.Column(db.String(255), nullable=False)
    userName = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    browsingHistory = db.relationship("BrowsingHistory", backref="users")
    order = db.relationship("Order", backref="user")
    orderItem = db.relationship("OrderItem", backref="users")
    post_comment_entity = db.relationship("post_comment_entity", backref="user")
    post_entity = db.relationship("post_entity", backref="user")
    shopping_cart_item_entity = db.relationship("shopping_cart_item_entity", backref="users")
    address = db.relationship("userAddress", backref="user")
    favoriteBook = db.relationship("userFavoriteBook", backref="users")


class userAddress(db.Model):
    __tablename__ = "userAddress"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(255), nullable=False)
    isDefaultAddress = db.Column(db.Boolean, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    name = db.Column(db.String(255), nullable=False)
    phoneNumber = db.Column(db.String(255), nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=0)


class userFavoriteBook(db.Model):
    __tablename__ = "userFavoriteBook"
    id = db.Column(db.Integer, primary_key=True)
    bookId = db.Column(db.Integer, db.ForeignKey("book.id"))
    createDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    updateDate = db.Column(db.DATETIME(6), nullable=False, default=datetime.now)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
