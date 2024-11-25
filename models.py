from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FishProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fish_type = db.Column(db.String(80), nullable=False)
    origin = db.Column(db.String(120), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    nutritional_info = db.Column(db.Text, nullable=True)  # 新增的营养资讯字段

    def to_dict(self):
        return {
            'id': self.id,
            '魚種': self.fish_type,
            '產地': self.origin,
            '存貨數量': self.stock_quantity,
            '圖片URL': self.image_url,
            '營養資訊': self.nutritional_info
        }
nutritional_info = db.Column(db.Text, nullable=True)
