from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FishProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fish_type = db.Column(db.String(80), nullable=False)
    origin = db.Column(db.String(120), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    nutritional_info = db.Column(db.Text, nullable=True)  # 新增的營養資訊字段
    price_per_kg = db.Column(db.Float, nullable=False)  # 新增每斤價格欄位

    def to_dict(self):
        return {
            'id': self.id,
            '魚種': self.fish_type,
            '產地': self.origin,
            '存貨數量': self.stock_quantity,
            '圖片URL': self.image_url,
            '營養資訊': self.nutritional_info,
            '每斤價格': self.price_per_kg  # 將每斤價格加入字典
        }

nutritional_info = db.Column(db.Text, nullable=True)
