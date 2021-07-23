import pymysql
menu_list = {'아메리카노': 2000, '카페 라떼': 2500, '바닐라 라떼': 3000, '초코 라떼': 4000, '망고 스무디': 5000}

conn = 0
curs = 0


def db_connect():
    """DB 연결 함수"""
    global conn, curs
    try:
        conn = pymysql.connect(host='host', user='user', password='password',
                               db='db', charset='utf8')
    except:
        print("DB 연결을 실패했습니다.")
        return False
    curs = conn.cursor(pymysql.cursors.DictCursor)
    return True


def show_menu():
    """메뉴판 조회 함수"""
    print("*******************************")
    global menu_list
    for menu, price in menu_list.items():
        print(f"{menu} : {price}원")
    print("*******************************")


def order():
    """음료명과 수량을 입력 받아 딕셔너리로 반환하는 함수"""
    global menu_list
    order_list = {}
    while True:
        myorder = input("음료를 주문하세요(주문이 완료되었다면 0을 입력하세요) : ")
        if myorder in menu_list:
            try:
                drink_number = int(input("주문하실 음료 개수를 입력하세요 :"))
            except ValueError:
                print("올바르지 않은 형식입니다. 다시 주문해주세요.")
                continue
            else:
                order_list[myorder] = drink_number
        elif myorder == "0":
            print("주문을 종료합니다")
            break
        else:
            print("주문하신 음료가 메뉴에 없습니다.")

    print("**********<주문내역>*************")
    for menu, cnt in order_list.items():
        print(f"{menu}  -  {cnt}잔")
    print("*******************************")
    return order_list


def check_member():
    """DB에 등록된 회원인지 확인하는 함수"""
    member_info = input('전화번호(회원 정보)를 입력하세요 : ')
    sql = f'select m_number from member_t where m_number = "{member_info}"'
    curs.execute(sql)
    row = curs.fetchone()
    if row == None:
        return False
    return member_info


def add_point(total, m_number):
    """등급별 적립율과 주문금액 계산해서 포인트를 적립하는 함수"""
    sql = f'select rate, m_point from member_t,grade_t where member_t.grade = grade_t.grade and m_number = "{m_number}"'
    curs.execute(sql)
    row = curs.fetchone()

    rate = row['rate']
    m_point = row['m_point']
    plus_point = total * rate
    update_point = int(m_point + plus_point)
    sql_ = f'update member_t set m_point = {update_point} where m_number = "{m_number}"'
    curs.execute(sql_)

    return update_point


def use_point(m_number):
    """포인트의 전체 금액을 사용하는 함수"""
    sql = f'select m_point from member_t where m_number = "{m_number}"'
    curs.execute(sql)
    row = curs.fetchone()
    if row == None:
        return None
    else:
        point = row['m_point']
    sql_ = f'update member_t set m_point = 0 where m_number = "{m_number}"'
    curs.execute(sql_)

    return point


def register_member():
    """회원 등록 함수"""
    name = input("이름을 입력해주세요 > ")
    number = input("핸드폰 번호를 입력해주세요 > ")
    try:
        if len(number) != 11:
            raise ValueError
        check_number = int(number)
    except ValueError:
        print("잘못된 형식입니다. 다시 입력해주세요.")
        return None
    else:
        sql = f'select name from member_t where m_number = "{number}"'
        curs.execute(sql)
        row = curs.fetchone()

    if not row:
        # 입력받은 정보와 일치하는 회원이 없는 경우 등록(db에 업데이트)
        sql = f'insert into member_t (name, m_number) values ( "{name}", "{number}" )'
        curs.execute(sql)
        conn.commit()
        return True
    else:
        # 등록되어 있는 경우
        print("이미 등록된 회원입니다.")
        return False


def show_receipt(order_list, use_check=False, point=0, number=None):
    """주문 내역 및 잔여 포인트 출력 함수"""
    print("주문 목록 확인해주세요")
    print("주문하신 음료 목록입니다.")
    print("************************")
    for menu, cnt in order_list.items():
        print(f"{menu}  -  {cnt}잔")

    total = total_price(order_list)
    if use_check:
        total -= int(point)
        point = 0

    if total < 0:
        total = 0

    print("총 금액은 ", total, "원 입니다.")
    if number != None:
        print("잔여 포인트는 ", point, "입니다.")
    print("************************")


def total_price(order_dict):
    """총 주문 금액 구하는 함수"""
    total = 0
    for drink, cnt in order_dict.items():
        cnt = int(cnt)
        total += menu_list[drink] * cnt

    return total


def point(number):
    """포인트 조회 함수"""
    sql = f'select name, m_point from member_t where m_number = "{number}"'
    curs.execute(sql)
    row = curs.fetchone()
    print("현재 포인트 : ", row['m_point'])


def db_close():
    """DB 연결 해제 함수"""
    curs.close()
    conn.close()