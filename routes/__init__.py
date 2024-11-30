from routes.dashboard.product_routes import product_bp
from routes.dashboard.category_routes import category_bp
from routes.dashboard.unit_routes import unit_bp
from routes.dashboard.brand_routes import brand_bp
from routes.dashboard.tag_routes import tag_bp

def register_routes(app):
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(unit_bp)
    app.register_blueprint(brand_bp)
    app.register_blueprint(tag_bp)
