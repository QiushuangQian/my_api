from models import db, Book, user, userFavoriteBook, BrowsingHistory, Comment, post_comment_entity, Order, OrderItem, \
    Sessions, post_entity, shopping_cart_item_entity


orderItem = OrderItem.query.filter_by(userId=4)
for i in orderItem:
    print(i.bookId)
    print(i.commentId)