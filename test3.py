import json
import math
import random
# import numpy as np
from operator import itemgetter

from models import db, Book, user, userFavoriteBook, BrowsingHistory, Comment, post_comment_entity, Order, OrderItem, \
    Sessions, post_entity, shopping_cart_item_entity


def get_data2():
    book_list = list()
    user_set = set()
    rv_dict = dict()
    try:
        orderItem = OrderItem.query.all()
    except Exception:
        book_list = []
        return rv_dict
    for i in orderItem:
        book_list.append(i.bookId)
    # 通过书去找所有买过这本书的订单
    for book in book_list:
        oi = OrderItem.query.filter_by(bookId=book)
        # 将订单上的用户添加到用户集
        for i in oi:
            user_set.add(i.userId)

    for user in user_set:
        book_set = set()
        rv_item_dict = {}
        ois = OrderItem.query.filter(OrderItem.userId == user and OrderItem.status == 'finish')
        for item in ois:
            book_set.add(item.bookId)
            comment_id = item.commentId
            comments = Comment.query.filter(Comment.id == comment_id)
            for i in comments:
                rv_item_dict[item.bookId] = i.itemStar
        rv_dict[user] = rv_item_dict
        # shopping_dict[user] = tuple(book_set)
    return rv_dict


def ItemSim(rv_dict):
    itemSim = dict()
    item_user_count = dict()
    count = dict()
    for user, item in rv_dict.items():
        for i in item.keys():
            item_user_count.setdefault(i, 0)
            if rv_dict[user][i] > 0.0:
                item_user_count[i] += 1
            for j in item.keys():
                count.setdefault(i, {}).setdefault(j, 0)
                if (
                        rv_dict[user][i] > 0.0
                        and rv_dict[user][j] > 0.0
                        and i != j
                ):
                    count[i][j] += 1
    for i, related_items in count.items():
        itemSim.setdefault(i, dict())
        for j, cuv in related_items.items():
            itemSim[i].setdefault(j, 0)
            itemSim[i][j] = cuv / item_user_count[i]
    return itemSim


# def preUserScore(rv_dict,itemSim,userA,item):
#     score = 0.0
#     for item1 in itemSim[item].keys():
#         if item1 != item:
#             score += (itemSim[item][item1]*
#                       rv_dict[userA][int(item1)])
#     return score

def recommend(rv_dict, itemSim, userA):
    result = dict()
    u_items = rv_dict.get(userA, {})
    for i, pi in u_items.items():
        for j, wj in sorted(itemSim[i].items(), key=lambda x: x[1], reverse=True):
            if j in u_items:
                continue
            result.setdefault(j, 0)
            result[j] += pi * wj
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    # user_item_score_dict = dict()
    # for item in rv_dict[userA].keys():
    #     user_item_score_dict[item] = preUserScore(rv_dict,itemSim,userA,item)
    # return user_item_score_dict


if __name__ == "__main__":
    rv_dict = get_data2()
    itemSim = ItemSim(rv_dict)
    result = recommend(rv_dict, itemSim, 4)
    print("result is {}".format(result))
