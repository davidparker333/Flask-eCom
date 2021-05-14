from app import create_app, db
#from app.blueprints.auth.models import User
#from app.blueprints.shop.models import Cart, Product

app = create_app()
# @app.shell_context_processor
# def make_shell_content():
#     return {'User' : User, 'Cart' : Cart, 'db' : db, 'Product' : Product}