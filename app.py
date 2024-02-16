# app.py
import logging
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Database connection
db = pymysql.connect(port=3306, host='localhost', user='root', password='password', db='prod_ajax', cursorclass=pymysql.cursors.DictCursor)

# Form for adding/editing a product
class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Submit')

# Routes
@app.route('/')
def index():
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM products_ajax')
            products = cursor.fetchall()
        return render_template('index.html', products=products)
    except Exception as e:
        logging.error('Error fetching products: {}'.format(str(e)))
        return 'An error occurred while fetching products.', 500

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        try:
            with db.cursor() as cursor:
                cursor.execute('INSERT INTO products_ajax (name, description, price) VALUES (%s, %s, %s)', (form.name.data, form.description.data, form.price.data))
                db.commit()
            logging.info('Product added: {}'.format(form.name.data))
            return jsonify({'success': True})
        except Exception as e:
            logging.error('Error adding product: {}'.format(str(e)))
            return jsonify({'error': 'An error occurred while adding the product.'}), 500
    return render_template('add_product.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM products_ajax WHERE id = %s', (id,))
            product = cursor.fetchone()
    except Exception as e:
        logging.error('Error fetching product for editing: {}'.format(str(e)))
        return 'An error occurred while fetching the product for editing.', 500
    
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        try:
            with db.cursor() as cursor:
                cursor.execute('UPDATE products_ajax SET name = %s, description = %s, price = %s WHERE id = %s', (form.name.data, form.description.data, form.price.data, id))
                db.commit()
            logging.info('Product edited: {}'.format(form.name.data))
            return jsonify({'success': True})
        except Exception as e:
            logging.error('Error editing product: {}'.format(str(e)))
            return jsonify({'error': 'An error occurred while editing the product.'}), 500
    return render_template('edit_product.html', form=form, product=product)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    try:
        with db.cursor() as cursor:
            cursor.execute('DELETE FROM products_ajax WHERE id = %s', (id,))
            db.commit()
        logging.info('Product deleted with ID: {}'.format(id))
        return jsonify({'success': True})
    except Exception as e:
        logging.error('Error deleting product: {}'.format(str(e)))
        return jsonify({'error': 'An error occurred while deleting the product.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
