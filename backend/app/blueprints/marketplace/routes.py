from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.item import Item
from app.blueprints.marketplace import marketplace_bp
from app.blueprints.marketplace.forms import ItemForm

@marketplace_bp.route('/')
@login_required
def index():
    items = Item.query.all()
    return render_template('marketplace/index.html', items=items)

@marketplace_bp.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            name=form.name.data, 
            description=form.description.data, 
            price=form.price.data, 
            seller_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Item listed for sale.', 'success')
        return redirect(url_for('marketplace.index'))
    return render_template('marketplace/sell.html', form=form)

@marketplace_bp.route('/buy/<int:item_id>')
@login_required
def buy(item_id):
    item = Item.query.get_or_404(item_id)
    # Implement purchase logic here
    flash(f'You have purchased {item.name}.', 'success')
    return redirect(url_for('marketplace.index'))
