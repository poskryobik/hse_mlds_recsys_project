import torch


MAX_LENGTH = 630
SOS_token = 0
EOS_token = 1


class NextBasket():
    """
        Класс интерфейса модели для инференса в API
    """
    def __init__(self, encoder, decoder, device,
                 prod_to_id, user_to_id, id_to_product,
                 top_product,
                 df, max_length=MAX_LENGTH):
        # Модели
        self.encoder = encoder
        self.decoder = decoder
        self.device = device
        self.encoder.eval()
        self.decoder.eval()
        # Кодировщики
        self.prod_to_id = prod_to_id
        self.user_to_id = user_to_id
        self.id_to_product = id_to_product
        self.df = df  # Датафрейм с последними 5 корзинами клиента
        self.max_length = max_length
        self.top_prod = top_product  # топ 100 продуктов

    def get_uid(self, user_id):
        """
            Кодирование пользователя в внутренний uid
        """
        return self.user_to_id.get(user_id, None)

    def get_user_baskets(self, uid):
        """
           Возвращает последовательность продуктов
        """
        sample = self.df[self.df["user_id"] == uid]["product_id"]
        ans = []
        for seq in sample:
            ans += list(seq)
        return ans

    def convert_seq(self, seq):
        """
            Перевод id продуктов во внутренний id
        """
        seq = [self.prod_to_id[val] for val in seq]
        return seq

    def evaluate(self, seq, k=10):
        with torch.inference_mode():
            input_tensor = self.convert_seq(seq)
            input_tensor = torch.tensor(input_tensor, dtype=torch.long,
                                        device=self.device).view(-1, 1)
            input_length = input_tensor.size()[0]
            encoder_hidden = self.encoder.initHidden()

            encoder_outputs = torch.zeros(self.max_length,
                                          self.encoder.hidden_size,
                                          device=self.device)

            for ei in range(input_length):
                encoder_output, encoder_hidden = self.encoder(input_tensor[ei],
                                                              encoder_hidden)
                encoder_outputs[ei] += encoder_output[0, 0]

            decoder_input = torch.tensor([[SOS_token]], device=self.device)
            decoder_hidden = encoder_hidden
            decoded_words = []

            for di in range(k):  # Количество слов
                decoder_output, decoder_hidden = self.decoder(
                    decoder_input, decoder_hidden, encoder_outputs)
                _, topi = decoder_output.data.topk(1)
                if topi.item() == EOS_token:
                    break
                else:
                    decoded_words.append(self.id_to_product[topi.item()])
                decoder_input = topi.squeeze().detach()

            return decoded_words

    def recommend(self, user_id, k=10):
        uid = self.get_uid(user_id=user_id)
        if uid is None:
            return  # Cold start
        seq = self.get_user_baskets(uid=uid)
        ans = self.evaluate(seq=seq, k=k)
        return ans

    def predict(self, users_to_recommend, k=10):
        """
            Рекомендации для нескольких пользователей
        """
        predictions = {}
        for uid in users_to_recommend:
            predictions[uid] = self.recommend(user_id=uid, k=k)
        return predictions

    def cold_start(self, cold_seq=None, k=10):
        """
            Функция холодного старта
            возвращает популярные продукты по убываюнию
        """
        if cold_seq is not None:
            return self.evaluate(seq=cold_seq, k=k)
        return self.top_prod[:k]
