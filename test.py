import json
import math
import random
from operator import itemgetter

from models import db, Book, user, userFavoriteBook, BrowsingHistory, Comment, post_comment_entity, Order, OrderItem, \
    Sessions, post_entity, shopping_cart_item_entity


def get_data1(user_id):
    book_list = list()
    user_set = set()
    rv_dict = dict()
    shopping_dict = dict()
    # 当前用户的购买记录
    try:
        orderItem = OrderItem.query.filter_by(userId=user_id)
    except:
        book_list = []
        return rv_dict
    # 获取评价过的书的列表
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


def get_data2():
    book_list = list()
    user_set = set()
    rv_dict = dict()
    try:
        orderItem = OrderItem.query.all()
    except:
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

def get_data3(user_id):
    pass


def preData(rv_dict):
    data = []
    for i in rv_dict.keys():
        for j in rv_dict[i].items():
            data.append((i, j[0], int(j[1])))
    return data


def splitData(data, k, seed, M=9):
    train, test = {}, {}
    random.seed(seed)
    for user, item, record in data:
        if random.randint(0, M) == k:
            test.setdefault(user, {})
            test[user][item] = record
        else:
            train.setdefault(user, {})
            train[user][item] = record
    return train

def UserSim(trainData):
    item_users = dict()
    for u,items in trainData.items():
        for i in items.keys():
            item_users.setdefault(i,set())
            if trainData[u][i]>0:
                item_users[i].add(u)
    count = dict()
    user_item_count = dict()
    for i,users in item_users.items():
        for u in users:
            user_item_count.setdefault(u,0)
            user_item_count[u]+=1
            count.setdefault(u,{})
            for v in users:
                count[u].setdefault(v,0)
                if u == v:
                    continue
                count[u][v] += 1/math.log(1+len(users))
    #构建相似度矩阵
    userSim = dict()
    for u,related_users in count.items():
        userSim.setdefault(u,{})
        for v,cuv in related_users.items():
            if u ==v :
                continue
            userSim[u].setdefault(v,0.0)
            userSim[u][v] = cuv/math.sqrt(user_item_count[u]*user_item_count[v])
        json.dump(userSim,open('user_sim.json','w'))
    return userSim

def recommend(trainData,userSim,user):
    result = dict()
    have_score_items = trainData.get(user,{})
    for v,wuv in sorted(userSim[user].items(), key=lambda x:x[1],reverse=True):
        for i,rvi in trainData[v].items():
            if i in have_score_items:
                continue
            result.setdefault(i,0)
            result[i] += wuv*rvi
    return dict(sorted(result.items(),key=lambda x:x[1],reverse=True))

if __name__ == "__main__":
    rv_dict = get_data2()
    data = preData(rv_dict)
    trainData = splitData(data,3,17)
    userSim = UserSim(trainData)
    result = recommend(trainData,userSim,5)
    print("result is {}".format(result))

