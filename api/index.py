from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, template_folder="templates")
app.secret_key = "coffee-point-secret"

# 고객 데이터 (메모리 저장)
customers = {}

# 메뉴
menu = {
	"1": {"name": "아메리카노", "price": 4500},
	"2": {"name": "카페라떼", "price": 5000},
	"3": {"name": "카푸치노", "price": 5500},
}


@app.route("/", methods=["GET"])
def home():
	phone = session.get("phone")
	message = session.pop("message", None)
	current_point = customers.get(phone, {}).get("point") if phone else None

	return render_template(
		"index.html",
		menu=menu,
		phone=phone,
		current_point=current_point,
		message=message,
	)


@app.route("/customer", methods=["POST"])
def customer():
	phone = request.form.get("phone", "").strip()
	register = request.form.get("register") == "y"

	if not phone:
		session["phone"] = None
		session["message"] = "전화번호를 입력해 주세요."
		return redirect(url_for("home"))

	if phone in customers:
		session["phone"] = phone
		session["message"] = f"{phone}번 고객님 환영 (포인트: {customers[phone]['point']}점)"
	else:
		if register:
			customers[phone] = {"point": 0}
			session["phone"] = phone
			session["message"] = "등록 완료!"
		else:
			session["phone"] = None
			session["message"] = "비회원으로 주문합니다."

	return redirect(url_for("home"))


@app.route("/order", methods=["POST"])
def order():
	choice = request.form.get("choice")
	phone = session.get("phone")

	if choice not in menu:
		session["message"] = "올바른 메뉴 번호를 선택해 주세요."
		return redirect(url_for("home"))

	item = menu[choice]
	result = [f"{item['name']} 주문완료! {item['price']}원"]

	if phone and phone in customers:
		earned = item["price"] // 10
		customers[phone]["point"] += earned
		result.append(f"+{earned}점 (누적: {customers[phone]['point']}점)")
	else:
		result.append("비회원은 포인트 적립 불가")

	session["message"] = " / ".join(result)
	return redirect(url_for("home"))


if __name__ == "__main__":
	app.run(debug=True)
