import json
import math
import random
import numpy as np

from flask import Flask, redirect, request, jsonify, session
from models import db, Book, user, userFavoriteBook, BrowsingHistory, Comment, post_comment_entity, Order, OrderItem, \
    Sessions, post_entity, shopping_cart_item_entity

app = Flask(__name__)
app.secret_key = "sdasofgivcsapofu"

app.route("/post")
def doRecommend(rv_dict,):
    rv_dict = get_data()
    data = preData(rv_dict)
    trainData = splitData(data, 2, 17)
    userSim = UserSim(trainData)
    result = recommend(trainData, userSim, 4)

    user_id = session.get("userId")
    if user_id is not None:
        return jsonify(result=result)

def get_data():
    dicc = dict()
    user_set = set()
    post_list = post_comment_entity.query.all()
    for item in post_list:
        user_set.add(item.userId)
    for i in user_set:
        dicc1 = dict()
        post_set = set()
        post_user_list = post_comment_entity.query.filter_by(userId=i)
        for item in post_user_list:
            post_set.add(item.postId)
            for j in post_set:
                dicc1[j] = post_comment_entity.query.filter_by(postId=j).count()
        dicc[i] = dicc1
    return dicc


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
    for u, items in trainData.items():
        for i in items.keys():
            item_users.setdefault(i, set())
            if trainData[u][i] > 0:
                item_users[i].add(u)
    count = dict()
    user_item_count = dict()
    for i, users in item_users.items():
        for u in users:
            user_item_count.setdefault(u, 0)
            user_item_count[u] += 1
            count.setdefault(u, {})
            for v in users:
                count[u].setdefault(v, 0)
                if u == v:
                    continue
                count[u][v] += 1 / math.log(1 + len(users))
    # 构建相似度矩阵
    userSim = dict()
    for u, related_users in count.items():
        userSim.setdefault(u, {})
        for v, cuv in related_users.items():
            if u == v:
                continue
            userSim[u].setdefault(v, 0.0)
            userSim[u][v] = cuv / math.sqrt(user_item_count[u] * user_item_count[v])
        json.dump(userSim, open('post_user_sim.json', 'w'))
    return userSim


def recommend(trainData, userSim, user):
    result = dict()
    have_score_items = trainData.get(user, {})
    for v, wuv in sorted(userSim[user].items(), key=lambda x: x[1], reverse=True):
        for i, rvi in trainData[v].items():
            if i in have_score_items:
                continue
            result.setdefault(i, 0)
            result[i] += wuv * rvi
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

