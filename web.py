from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB = "database.db"

def get_orders(status=None):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    if status:
        cur.execute("SELECT * FROM orders WHERE status=?", (status,))
    else:
        cur.execute("SELECT * FROM orders")

    data = cur.fetchall()
    conn.close()
    return data


def get_order(order_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
    row = cur.fetchone()

    conn.close()
    return row


def update_status(order_id, status):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    UPDATE orders SET status=? WHERE order_id=?
    """, (status, order_id))

    conn.commit()
    conn.close()


@app.route("/")
def index():
    status = request.args.get("status")
    orders = get_orders(status)
    return render_template("index.html", orders=orders)


@app.route("/order/<int:order_id>")
def order(order_id):
    order = get_order(order_id)
    return render_template("order.html", order=order)


@app.route("/update/<int:order_id>/<status>")
def update(order_id, status):
    update_status(order_id, status)
    return redirect("/")


if __name__ == "__main__":
    print("🌐 Web running http://127.0.0.1:5000")
    app.run(debug=True)