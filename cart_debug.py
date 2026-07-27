from app.db.database import SessionLocal
from app.models.cart import Cart
from app.models.cart_item import CartItem

session = SessionLocal()
try:
    carts = session.query(Cart).all()
    print('carts', [(c.id, c.user_id, len(c.items), [(i.product_id, i.quantity) for i in c.items]) for c in carts])
    items = session.query(CartItem).all()
    print('cart_items', [(i.id, i.cart_id, i.product_id, i.quantity) for i in items])
finally:
    session.close()
