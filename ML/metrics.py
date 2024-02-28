import pandas as pd
import numpy as np


def precision_at_k(relevant, predicted, k: int = 10):
    """ 
        Функиця расчета Precision@k
        relevant - релевантные items для одного пользователя
        predicted - рекомендованные items для одного пользователя
    """
    return len(set(relevant[:k]) & set(predicted[:k]))/k 

def rel_item(relevant, predicted):
    """
        Функция рассчитывает количество релевантных Item
    """
    result = [0]*max(len(relevant), len(predicted))
    items = min(len(relevant), len(predicted))
    for i in range(items):
        result[i] = int(relevant[i] == predicted[i])
    return result  


def ap_at_k(relevant, predicted, k: int = 10):
    """ 
        Функция расчета AP@k
        relevant - релевантные items для одного пользователя
        predicted - рекомендованные items для одного пользователя
    """
    y_i = rel_item(relevant=relevant, predicted=predicted)
    p_at_i = [0]*k
    iter_cnt = min(len(relevant), k)
    for i in range(1, iter_cnt+1):
        p_at_i[i-1] = precision_at_k(relevant=relevant, predicted=predicted, k=i)
    return sum([y*p/k for y, p in zip(y_i, p_at_i)])

def map_at_k(relevant, predicted, k: int = 10):
    """ 
        Функция расчета MAP@k
        relevant список по всем пользователям с их релевантными items
        predicted список по всем пользователям с их рекомендованными items
    """
    users = len(relevant)
    sum_apk = 0
    for user in range(users):
        sum_apk += ap_at_k(relevant=relevant[user], predicted=predicted[user], k=k)
    return sum_apk/users


def nap_at_k(relevant, predicted, k: int = 10):
    """ 
        Функция расчета normalize AP@k
        relevant - релевантные items для одного пользователя
        predicted - рекомендованные items для одного пользователя
    """
    y_i = rel_item(relevant=relevant, predicted=predicted)
    p_at_i = [0]*k
    k = min(len(relevant), k)
    for i in range(1, k+1):
        p_at_i[i-1] = precision_at_k(relevant=relevant, predicted=predicted, k=i)
    return sum([y*p/k for y, p in zip(y_i, p_at_i)])

def mnap_at_k(relevant, predicted, k: int = 10):
    """ 
        Функция расчета MAP@k
        relevant список по всем пользователям с их релевантными items
        predicted список по всем пользователям с их рекомендованными items
    """
    users = len(relevant)
    sum_napk = 0
    for user in range(users):
        sum_napk += nap_at_k(relevant=relevant[user], predicted=predicted[user], k=k)
    return sum_napk/users


def hitrate_at_k(relevant, predicted, k: int = 10):
    """
        Функция расчета Hitrate@k
        relevant список по всем пользователям с их релевантными items
        predicted список по всем пользователям с их рекомендованными items
    """
    
    cnt_user = len(predicted) # Количество пользователей    
    cnt_valid_user = 0
    for user in range(cnt_user):
        cnt_valid_user += int(len(set(relevant[user][:k]) & set(predicted[user][:k])) > 0) 

    return cnt_valid_user/cnt_user


def ndsg_at_k(relevant, predicted, k: int = 10):
    """
        Функция расчета nDSG@k
        relevant - релевантные items для одного пользователя
        predicted - рекомендованные items для одного пользователя
    """
    idsg_at_k = sum([1/np.log2(k+1) for k in range(1, k+1)])
    k = min(len(relevant), k)
    dsg_at_k = 0
    for k in range(1, k+1):
        dsg_at_k += int(relevant[k-1] == predicted[k-1])/np.log2(k+1)
    return dsg_at_k/idsg_at_k