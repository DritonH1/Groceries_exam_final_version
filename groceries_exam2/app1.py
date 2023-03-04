import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('product.db')
c = conn.cursor()

# create the Product table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS Product
             (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
              name TEXT NOT NULL,
              quantity INTEGER NOT NULL,
              place TEXT NOT NULL)''')
conn.commit()

# create the Product table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS Porosia
             (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
              Product TEXT NOT NULL,
              quantity INTEGER NOT NULL,
              date INTEGER NOT NULL)''')
conn.commit()

def add_product(name, quantity, place):
    with conn:
        c.execute("INSERT INTO Product (name, quantity, place) VALUES (?, ?, ?)", (name, quantity, place))
        st.success(f"Product {name} added successfully")
        
# function to delete a product from the database
def delete_product(name):
    with conn:
        c.execute("DELETE FROM Product WHERE name=?", (name,))
        st.success(f"Product {name} deleted successfully")

# function to update a product in the database
def update_product(old_name, new_name, quantity, place):
    """
    Update a product in the Product table
    """
    with conn:
        c.execute('''UPDATE Product
                     SET name = ?, quantity = ?, place = ?
                     WHERE name = ?''',
                  (new_name, quantity, place, old_name))
        conn.commit()
        st.success(f"Product {old_name} has been updated to {new_name}!")

# function to display all products in the database
def view_all_products():
    df = pd.read_sql_query("SELECT * FROM Product", conn)
    return df

def add_order(Product, quantity, date):
    with conn:
        c.execute("INSERT INTO Porosia (Product, quantity, date) VALUES (?, ?, ?)", (Product, quantity, date))
        st.success(f"Order {Product} added successfully")

def delete_order(Product):
    with conn:
        c.execute("DELETE FROM Porosia WHERE Product=?", (Product,))
        st.success(f"order {Product} deleted successfully")
        

# function to display all orders in the database
def view_all_orders():
    df = pd.read_sql_query("SELECT * FROM Porosia", conn)
    return df


st.title("Product Management System")

# get user input for adding, deleting or updating a product
action = st.radio("Select an action:", ("Add Product", "Delete Product", "Update Product","Add Order","Delete Order","View Products"))

# if adding a product
if action == "Add Product":
    if st.button("View products"):
        df = view_all_products()
        st.dataframe(df)
    st.subheader("Add a Product")
    name = st.text_input("Name")
    quantity = st.number_input("Quantity", value=1, step=1)
    place = st.text_input("Place")
    
    if st.button("Add Product"):
        add_product(name, quantity, place)
        
# if deleting a product
elif action == "Delete Product":
    st.subheader("Delete a Product")
    df = view_all_products()
    st.dataframe(df)
    
    name = st.text_input("Enter the name of the product to delete")
    
    if st.button("Delete Product"):
        delete_product(name)
        
    st.write("")
    
# if updating a product
elif action == "Update Product":
    st.subheader("Update a Product")
    df = view_all_products()
    st.dataframe(df)
    
    old_name = st.text_input("Enter the name of the product to update")
    new_name = st.text_input("Enter the new name of the product")
    quantity = st.number_input("Enter the new quantity of the product", value=1, step=1)
    place = st.text_input("Enter the new place of the product")
    if st.button("Update Product"):
        update_product(old_name,new_name, quantity, place)
        
    st.write("")

elif action == "Add Order":
    st.subheader("Add a Order")
    Product = st.text_input("Name")
    quantity = st.number_input("Quantity", value=1, step=1)
    date = st.date_input("data")
    df = view_all_orders()
    st.dataframe(df)
    dv = view_all_products()
    st.dataframe(dv)
    
    if st.button("Add Order"):
        add_order(Product, quantity, date)

elif action == "Delete Order":
    st.subheader("Delete a Order")
    df = view_all_orders()
    st.dataframe(df)
    
    Product = st.text_input("Enter the name of the product to delete")
    
    if st.button("Delete Order"):
        delete_order(Product)

elif action=="View Products":
    df = view_all_products()
    st.dataframe(df)