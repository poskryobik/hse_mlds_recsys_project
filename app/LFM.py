import pandas as pd
import numpy as np
from lightfm import LightFM
from tqdm import tqdm




class LFM():

    def __init__(self, encoder, rating_df=None, model=None):
        if model is None:
            self.model = LightFM(no_components=10,
                                loss='warp', 
                                random_state=42, 
                                learning_rate=0.01)
        else:
            self.model = model
        self.encoder = encoder
        self.rating_df = rating_df

    def predict(self, users_to_recommend: list, k: int = 10):
        """
            Рекомендации для нескольких пользователей
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
        return np.argsort(np.array(self.rating_df.groupby("product_id")["rating"].sum()))[::-1]



    def recommend(self,uid: int, k: int):
        """
            Расчет рекомендаций
        """
        # Если ранее такого пользователя не было, то применяется холодный старт
        try:
            uid = self.encoder.transform(np.array([uid]))[0]
        except:
            return self.cold_start()[:k]
        
        items = sorted(self.rating_df['product_id'].unique())
        scores = self.model.predict(user_ids=[uid]*len(items), 
                                    item_ids=items)
        predict = np.array(items)[np.argsort(-scores)][:k]
        return predict.tolist()
        
    def fit(self, train_sparse, epochs, rounds, num_threads=60):
        for rounds in tqdm(range(rounds)): 
            self.model.fit_partial(train_sparse, 
                            sample_weight=train_sparse, 
                            epochs=epochs, 
                            num_threads=num_threads)
