from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, FishProduct
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fish.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 删除旧的数据库文件
if os.path.exists('fish.db'):
    os.remove('fish.db')

with app.app_context():
    db.create_all()
    # 添加初始数据
    if not FishProduct.query.first():
        sample_fishes = [
            FishProduct(
                fish_type='鯖魚',
                origin='日本',
                stock_quantity=50,
                image_url='/static/images/mackerel.jpg',
                nutritional_info='抗癌、預防失智',
                price_per_kg=100.0  # 每斤價格設定為 100
            ),
            FishProduct(
                fish_type='鮭魚',
                origin='挪威',
                stock_quantity=20,
                image_url='/static/images/salmon.jpg',
                nutritional_info='富含Omega-3脂肪酸、維生素D，以及優質蛋白質，有助調節生理機能、促進新陳代謝',
                price_per_kg=250.0  # 每斤價格設定為 250
            ),
            FishProduct(
                fish_type='鯛魚',
                origin='台灣',
                stock_quantity=100,
                image_url='/static/images/sea_bream.jpg',
                nutritional_info='魚肉蛋白纖維細，咀嚼後好消化吸收。而且鯛魚的蛋白質能提供人體無法合成的9種必需胺基酸，幫助人體肌肉生長及合成免疫蛋白，有助於維持免疫力，而攝取蛋白質能增加飽足感並降低食慾，對於減肥、維持體重的人來說，幫助很大',
                price_per_kg=180.0  # 每斤價格設定為 180
            ),
            FishProduct(
                fish_type='牡蠣',
                origin='台灣王功',
                stock_quantity=80,
                image_url='/static/images/oyster.jpg',
                nutritional_info='補鈣',
                price_per_kg=300.0  # 每斤價格設定為 300
            ),
        ]
        db.session.bulk_save_objects(sample_fishes)
        db.session.commit()

# RESTful API 部分（保持不变）

# 创建鱼产
@app.route('/api/fish', methods=['POST'])
def create_fish():
    data = request.get_json()
    new_fish = FishProduct(
        fish_type=data.get('魚種'),
        origin=data.get('產地'),
        stock_quantity=data.get('存貨數量'),
        image_url=data.get('圖片URL'),
        nutritional_info=data.get('營養資訊'),
        price_per_kg=data.get('每斤價格')  # 新增每斤價格欄位
    )
    db.session.add(new_fish)
    db.session.commit()
    return jsonify(new_fish.to_dict()), 201

# 读取所有鱼产
@app.route('/api/fish', methods=['GET'])
def get_fishes():
    fishes = FishProduct.query.all()
    return jsonify([fish.to_dict() for fish in fishes])

# 读取单个鱼产
@app.route('/api/fish/<int:fish_id>', methods=['GET'])
def get_fish(fish_id):
    fish = FishProduct.query.get_or_404(fish_id)
    return jsonify(fish.to_dict())

# 更新鱼产
@app.route('/api/fish/<int:fish_id>', methods=['PUT'])
def update_fish(fish_id):
    data = request.get_json()
    fish = FishProduct.query.get_or_404(fish_id)
    fish.fish_type = data.get('魚種', fish.fish_type)
    fish.origin = data.get('產地', fish.origin)
    fish.stock_quantity = data.get('存貨數量', fish.stock_quantity)
    fish.image_url = data.get('圖片URL', fish.image_url)
    fish.nutritional_info = data.get('營養資訊', fish.nutritional_info)
    fish.price_per_kg = data.get('每斤價格', fish.price_per_kg)  # 更新每斤價格
    db.session.commit()
    return jsonify(fish.to_dict())

# 删除鱼产
@app.route('/api/fish/<int:fish_id>', methods=['DELETE'])
def delete_fish(fish_id):
    fish = FishProduct.query.get_or_404(fish_id)
    db.session.delete(fish)
    db.session.commit()
    return '', 204

# 前端页面部分

@app.route('/')
def index():
    fishes = FishProduct.query.all()
    return render_template('index.html', fish_products=fishes)

@app.route('/fish/<int:fish_id>')
def fish_detail(fish_id):
    fish = FishProduct.query.get_or_404(fish_id)
    return render_template('fish_detail.html', fish=fish)

# 新增訂購資訊頁面
@app.route('/order_info')
def order_info():
    return render_template('order_info.html')

if __name__ == '__main__':
    # 使用 Flask 內建的開發伺服器來運行應用
    app.run(host='0.0.0.0', port=5000, debug=True)
