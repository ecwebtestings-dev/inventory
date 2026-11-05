
import os
from datetime import date
from decimal import Decimal, InvalidOperation
import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv


# CREATE THE FLASK APPLICATION
app = Flask(__name__)

# LOAD ENVIRONMENT VARIABLES FROM .env FILE
load_dotenv()  

app.secret_key = os.getenv("SECRET_KEY", "Secret")


# DATABASE CONFIGURATION
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),       
    "user": os.getenv("DB_USER", "root"),             
    "password": os.getenv("DB_PASSWORD", ""),         
    "database": os.getenv("DB_NAME", "inventory_db"), 
}

# ESTABLISH A DATABASE CONNECTION
def get_db():
    return mysql.connector.connect(**DB_CONFIG)


#REUSABLE FUNCTION TO EXECUTE SQL QUERIES
def query(sql, params=(), fetch="all", commit=False):
    conn = get_db()
    try:

        # CREATE A CURSOR THAT RETURNS DATABASE RECORDS AS DICTIONARIES
        cur = conn.cursor(dictionary=True)

        # EXECUTE THE SQL STATEMENT WITH ITS PARAMETERS
        cur.execute(sql, params)

        # CHECK WHETHER THE QUERY SHOULD SAVE CHANGES TO THE DATABASE
        if commit:
            # SAVE THE CHANGES PERMANENTLY
            conn.commit()
            # RETURN THE ID OF THE LAST INSERTED RECORD
            return cur.lastrowid
        # RETURN ONE RECORD OR ALL RECORDS DEPENDING ON THE FETCH VALUE
        return cur.fetchone() if fetch == "one" else cur.fetchall()
    finally:
        conn.close()


# VALIDATE PRODUCT INFORMATION SUBMITTED THROUGH THE FORM
def validate(form):

    # CREATE AN EMPTY LIST TO STORE VALIDATION ERRORS
    errors = []
    # GET PRODUCT NAME, CATEGORY AND SUPPLIER FROM THE FORM
    # STRIP() REMOVES UNNECESSARY SPACES AT THE BEGINNING AND END
    name = form.get("product_name", "").strip()
    category = form.get("category", "").strip()
    supplier = form.get("supplier", "").strip()

    # CHECK WHETHER THE REQUIRED TEXT FIELDS ARE EMPTY
    if not name:
        errors.append("Product name is required.")

    if not category:
        errors.append("Category is required.")

    if not supplier:
        errors.append("Supplier is required.")

    # VALIDATE THE UNIT PRICE
    try:

        # CONVERT THE PRICE INTO A DECIMAL NUMBER
        price = Decimal(form.get("unit_price", ""))

        # ENSURE THAT THE PRICE IS NOT NEGATIVE
        if price < 0:
            raise ValueError

    except (InvalidOperation, ValueError):

        # ADD AN ERROR IF THE PRICE IS INVALID OR NEGATIVE
        errors.append("Unit price must be a number of 0 or more.")

        # SET PRICE TO NONE BECAUSE THE INPUT WAS INVALID
        price = None


    # CREATE A REUSABLE FUNCTION TO VALIDATE WHOLE NUMBERS
    def non_negative_int(field, label):

        try:

            # CONVERT THE FORM VALUE INTO AN INTEGER
            value = int(form.get(field, ""))

            # ENSURE THAT THE VALUE IS NOT NEGATIVE
            if value < 0:
                raise ValueError

            # RETURN THE VALID INTEGER
            return value

        except ValueError:

            # ADD AN ERROR IF THE VALUE IS INVALID
            errors.append(
                f"{label} must be a whole number of 0 or more."
            )

            # RETURN NONE IF VALIDATION FAILS
            return None


    # VALIDATE QUANTITY IN STOCK
    qty = non_negative_int(
        "quantity_in_stock",
        "Quantity in stock"
    )

    # VALIDATE REORDER LEVEL
    reorder = non_negative_int(
        "reorder_level",
        "Reorder level"
    )


    # COLLECT ALL VALIDATED PRODUCT INFORMATION IN A DICTIONARY
    data = {
        "product_name": name,
        "category": category,
        "supplier": supplier,
        "unit_price": price,
        "quantity_in_stock": qty,
        "reorder_level": reorder,
    }

    # RETURN THE VALIDATED DATA AND ANY ERRORS FOUND
    return data, errors



# READ AND FILTER PRODUCTS FROM THE DATABASE
@app.route("/")
def index():

    # GET THE SEARCH VALUE FROM THE URL
    # IF NO SEARCH VALUE EXISTS, USE AN EMPTY STRING
    search = request.args.get("q", "").strip()

    # CHECK WHETHER THE USER REQUESTED LOW-STOCK PRODUCTS
    # THIS IS TRUE WHEN THE URL CONTAINS ?low=1
    low_only = request.args.get("low") == "1"


    # START THE SQL QUERY BY SELECTING ALL PRODUCTS
    # WHERE 1=1 MAKES IT EASY TO ADD MORE CONDITIONS USING AND
    sql = "SELECT * FROM product WHERE 1=1"

    # CREATE AN EMPTY LIST TO HOLD SQL QUERY PARAMETERS
    params = []


    # CHECK WHETHER THE USER ENTERED A SEARCH TERM
    if search:

        # SEARCH PRODUCTS BY NAME, CATEGORY OR SUPPLIER
        sql += """
            AND (
                product_name LIKE %s
                OR category LIKE %s
                OR supplier LIKE %s
            )
        """

        # ADD THE SEARCH VALUE TO ALL THREE SEARCH CONDITIONS
        # PERCENT SIGNS ALLOW PARTIAL MATCHING
        params += [f"%{search}%"] * 3


    # FILTER PRODUCTS WHOSE QUANTITY IS AT OR BELOW REORDER LEVEL
    if low_only: sql += " AND quantity_in_stock <= reorder_level"


    # ARRANGE PRODUCTS ALPHABETICALLY BY PRODUCT NAME
    sql += " ORDER BY product_name"


    # EXECUTE THE PRODUCT QUERY AND RETRIEVE THE RESULTS
    products = query(sql, params)


    # CALCULATE INVENTORY SUMMARY INFORMATION
    summary = query(
        """
        SELECT

            # COUNT THE TOTAL NUMBER OF PRODUCTS
COUNT(*) AS total,

            # COUNT PRODUCTS WHOSE STOCK IS AT OR BELOW REORDER LEVEL
            COALESCE(
                SUM(quantity_in_stock <= reorder_level), 0
            ) AS low,

            # CALCULATE THE TOTAL VALUE OF ALL STOCK
            COALESCE(
                SUM(unit_price * quantity_in_stock), 0
            ) AS value

        FROM product
        """,
        fetch="one",
    )


    # DISPLAY THE DASHBOARD AND PASS THE DATABASE RESULTS TO HTML
    return render_template(
        "index.html",
        products=products,
        summary=summary,
        search=search,
        low_only=low_only
    )



# CREATE PRODUCT
@app.route("/add", methods=["GET", "POST"])
def add_product():

    # CHECK WHETHER THE USER HAS SUBMITTED THE ADD PRODUCT FORM
    if request.method == "POST":

        # VALIDATE ALL INFORMATION SUBMITTED THROUGH THE FORM
        data, errors = validate(request.form)


        # CHECK WHETHER VALIDATION FOUND ANY ERRORS
        if errors:

            # DISPLAY EACH ERROR MESSAGE TO THE USER
            for error in errors:
                flash(error, "error")

            # RETURN TO THE ADD PRODUCT PAGE
            # PRESERVE THE INFORMATION THE USER ALREADY ENTERED
            return render_template(
                "add_product.html",
                product=request.form
            )


        # INSERT THE NEW PRODUCT INTO THE DATABASE
        query(
            """
            INSERT INTO product (
                product_name,
                category,
                supplier,
                unit_price,
                quantity_in_stock,
                reorder_level,
                date_added
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,

            # PROVIDE THE VALUES FOR THE SQL PLACEHOLDERS
            (
                data["product_name"],
                data["category"],
                data["supplier"],
                data["unit_price"],
                data["quantity_in_stock"],
                data["reorder_level"],
                date.today()
            ),

            # COMMIT TRUE SAVES THE NEW PRODUCT TO MYSQL
            commit=True
        )


        # DISPLAY A SUCCESS MESSAGE AFTER ADDING THE PRODUCT
        flash("Product added successfully.", "success")

        # REDIRECT THE USER TO THE MAIN DASHBOARD
        return redirect(url_for("index"))


    # IF THE USER JUST OPENED THE PAGE USING GET,
    # DISPLAY AN EMPTY ADD PRODUCT FORM
    return render_template("add_product.html", product={})



# UPDATE PRODUCT
@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    # FIND THE PRODUCT USING ITS UNIQUE PRODUCT ID
    product = query(
        "SELECT * FROM product WHERE product_id = %s",
        (product_id,),
        fetch="one"
    )


    # CHECK WHETHER THE REQUESTED PRODUCT EXISTS
    if not product:

        # DISPLAY AN ERROR MESSAGE IF THE PRODUCT DOES NOT EXIST
        flash("Product not found.", "error")

        # RETURN THE USER TO THE DASHBOARD
        return redirect(url_for("index"))


    # CHECK WHETHER THE USER HAS SUBMITTED THE EDIT FORM
    if request.method == "POST":

        # VALIDATE THE UPDATED PRODUCT INFORMATION
        data, errors = validate(request.form)


        # CHECK WHETHER THE UPDATED INFORMATION CONTAINS ERRORS
        if errors:

            # DISPLAY ALL VALIDATION ERROR MESSAGES
            for error in errors:
                flash(error, "error")


            # COPY THE SUBMITTED FORM INFORMATION INTO A DICTIONARY
            merged = dict(request.form)

            # PRESERVE THE PRODUCT ID
            merged["product_id"] = product_id

            # PRESERVE THE ORIGINAL DATE THE PRODUCT WAS ADDED
            merged["date_added"] = product["date_added"]


            # RETURN TO THE EDIT PAGE WITH THE USER'S ENTERED VALUES
            return render_template(
                "edit_product.html",
                product=merged
            )


        # UPDATE THE EXISTING PRODUCT IN THE DATABASE
        query(
            """
            UPDATE product
            SET
                product_name = %s,
                category = %s,
                supplier = %s,
                unit_price = %s,
                quantity_in_stock = %s,
                reorder_level = %s
            WHERE product_id = %s
            """,

            # PROVIDE THE NEW VALUES AND THE ID OF THE PRODUCT TO UPDATE
            (
                data["product_name"],
                data["category"],
                data["supplier"],
                data["unit_price"],
                data["quantity_in_stock"],
                data["reorder_level"],
                product_id
            ),

            # COMMIT TRUE SAVES THE UPDATED INFORMATION
            commit=True
        )


        # DISPLAY A SUCCESS MESSAGE
        flash("Product updated successfully.", "success")

        # RETURN THE USER TO THE DASHBOARD
        return redirect(url_for("index"))


    # IF THE USER JUST OPENED THE EDIT PAGE,
    # DISPLAY THE EXISTING PRODUCT INFORMATION IN THE FORM
    return render_template(
        "edit_product.html",
        product=product
    )



# DELETE PRODUCT
@app.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):

    # DELETE THE PRODUCT THAT MATCHES THE PROVIDED PRODUCT ID
    query(
        "DELETE FROM product WHERE product_id = %s",
        (product_id,),
        commit=True
    )

    # DISPLAY A SUCCESS MESSAGE
    flash("Product deleted.", "success")

    # REDIRECT THE USER TO THE DASHBOARD
    return redirect(url_for("index"))



# CHECK WHETHER THIS FILE IS BEING RUN DIRECTLY
if __name__ == "__main__":

    # START THE FLASK DEVELOPMENT SERVER
    # DEBUG TRUE ENABLES DEBUGGING AND AUTOMATIC RELOADING
    app.run(debug=True)
