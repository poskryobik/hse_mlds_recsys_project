import pandas as pd
import numpy as np
import gdown
import scipy.sparse as sps
from metrics import hitrate_at_k

# Порог для отсечения редко встречающихся продуктов
N = 15
# Загрузка тестовых данных
gdown.download(url="https://drive.google.com/uc?export=download&id=1Ud6jFto6e7FW5y0LxxwX8afpmTrvA0u-",
               output="test_transacrion_df.csv",
               quiet=False)
# Загрузка датафрейма с рейтингами
gdown.download(url="https://drive.google.com/uc?export=download&id=1epGrpzB8BEC2t5Od3hrL3x07B1VZIm3c",
               output="ratings.csv",
               quiet=False)
test_all_df = pd.read_csv("test_transacrion_df.csv", index_col=0)
rating_df = pd.read_csv("ratings.csv", index_col=0)
# Оставляем только продукты которые встречались больше N раз
top_product = np.array(rating_df.groupby(['product_id'],
                                         as_index=False)['rating']
                       .count().query(f'rating > {N}')['product_id'])
rating_df = rating_df[rating_df['product_id'].isin(top_product)]
# Кодировщик пользователей
user2id = {k: v for v, k in enumerate(rating_df["user_id"].unique())}
id2user = {k: v for v, k in user2id.items()}
# Кодировка items
item2id = {k: v for v, k in enumerate(sorted(
    rating_df['product_id'].unique()))}
id2item = {k: v for v, k in item2id.items()}
# Кодирование пользователей
rating_df['user_id'] = rating_df["user_id"].apply(lambda x: user2id[x])
test_all_df['user_id'] = (
    test_all_df["user_id"].apply(lambda x: user2id.get(x, 999999)))
# Кодирование продуктов
rating_df['product_id'] = rating_df['product_id'].apply(lambda x: item2id[x])
test_all_df['product_id'] = (
    test_all_df['product_id'].apply(lambda x: item2id.get(x, -1)))
# Удаление повторяющихся покупок пользователем в тесте
test_all_df = test_all_df.drop_duplicates(subset=['user_id', 'product_id'],
                                          keep='first')
# Подготовка матрицы интеракций
matrix = sps.coo_matrix(
    (np.ones(rating_df.shape[0]),
     (rating_df['user_id'], rating_df['product_id'])),
    shape=(rating_df["user_id"].nunique(), rating_df["product_id"].nunique()))


class EASE():
    """
        EASE
        Reference:
            Harald Steck. "Embarrassingly Shallow Autoencoders for Sparse Data"
            in WWW 2019.
    """
    def __init__(self, encoder, rating_df=None, model=None):
        if model is not None:
            self.model = model
            self.encoder = encoder
        self.rating_df = rating_df

    def predict(self, users_to_recommend: list, k: int = 10):
        """
            Вычисление рекомендаций для несколькиъ пользователей
        """
        predictions = {}
        for uid in users_to_recommend:
            predictions[uid] = self.recommend(uid=uid, k=k)
        return predictions

    def cold_start(self):
        """
            Функция холодного старта
            возвращает популярные продукты по убываюнию
        """
        if self.rating_df is None:
            return None
        return np.argsort(
            np.array(self.rating_df.groupby("product_id")["rating"].sum())
            )[::-1]

    def recommend(self, uid: int, k: int):
        """
            Рекомендации
        """
        uid = self.encoder.get(uid, -1)
        if uid == -1:
            return self.cold_start()[:k]
        # Покупки пользователя
        interact = (
            self.rating_df[self.rating_df['user_id'] == uid]['product_id']
            .to_list())
        # Составляем вектор интеракций человека
        vector = np.zeros(len(item2id))
        vector[interact] = 1
        vector = sps.csr_matrix(vector)
        preds = np.array(vector.dot(self.model))[0]
        ranks = np.argsort(-preds)
        return list(ranks[:k])

    def fit(self, X, reg_weight=100):
        """
            Обучаем конечную модель
        """
        # gram matrix
        G = X.T @ X
        G += reg_weight * sps.identity(G.shape[0]).astype(np.float32)
        # convert to dense because inverse will be dense
        G = G.todense()
        # invert. this takes most of the time
        P = np.linalg.inv(G)
        self.model = P / (-np.diag(P))
        # zero out diag
        np.fill_diagonal(self.model, 0.)


# Для ускорения расчета метрик, перевод в CSC
X = matrix.tocsc()
# Пользователи с их релевантными покупками
relevant = (test_all_df[test_all_df["user_id"].isin(user2id.keys())]
            .sort_values(by=["user_id", "add_to_cart_order"])
            .groupby(['user_id'])
            .agg({'product_id': 'unique'})['product_id'].to_list())
# Подбор коэффициента регуляризации в EASE
grid_param = [100, 10, 1]
best_metric = 0
for reg_weight in grid_param:
    model = EASE(encoder=user2id, rating_df=rating_df)
    model.fit(matrix, reg_weight=reg_weight)
    # Предсказание модели
    predict = []
    ans = np.array(X.dot(model.model))
    for i in range(X.shape[0]):
        predict.append(np.argsort(-ans[i])[:10])
    metric_val = hitrate_at_k(predicted=predict, relevant=relevant)
    print(f"reg_weight: {reg_weight}, metric_val: {metric_val}")
