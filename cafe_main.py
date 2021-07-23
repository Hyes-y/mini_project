import cafe_function as cf

cf.db_connect()

while True:

    print("반갑습니다. 스타벅스입니다!")
    # 메뉴 리스트 조회
    cf.show_menu()

    # 주문 받을 함수 호출
    order_list = cf.order()
    if len(order_list) == 0:
        print("주문이 올바르지 않습니다. 다시 주문해주세요")
        continue

    total = cf.total_price(order_list)
    regi_check = False         # 미등록 회원인경우 True
    use_check = False           # 포인트 사용하는 경우 True
    while True:
        n = input("회원이신가요? [y/n] > ")
        if n != 'y' and n != 'n':
            print("다시 입력해주세요")
            continue
        elif n == 'y':
            # 입력 받은 번호로 등록된 회원인지 확인
            number = cf.check_member()
            if number:
                while True:
                    cf.point(number)
                    print("1.포인트 적립\n2.포인트 사용")
                    n = input("해당하는 숫자를 눌러주세요 > ")
                    if n != '1' and n != '2':
                        print("다시 입력해주세요!")
                        continue
                    elif n == '1':
                        point = cf.add_point(total, number)
                        break
                    else:
                        point = cf.use_point(number)
                        use_check = True
                        break
                break
            else:
                print("등록 되어 있지 않습니다.")
                regi_check = True
        else:
            regi_check = True
            break

    while regi_check:
        n = input("회원 등록하시겠습니까? [y/n] > ")
        point = None
        if n != 'y' and n != 'n':
            print("다시 입력해주세요")
            continue
        elif n == 'y':
            if not cf.register_member():
                continue
            break
        else:
            break

    # 주문 내역 및 적립금(회원인 경우) 출력
    if regi_check:
        cf.show_receipt(order_list)
    else:
        cf.show_receipt(order_list, use_check, point, number)

    while True:
        n = input("결제하시겠습니까? [y/n] > ")
        if n != 'y' and n != 'n':
            print("정확하게 입력해주세요!")
            continue
        elif n == 'y':
            print("감사합니다.")
            cf.conn.commit()
            break
        else:
            print("주문이 초기화됩니다. 감사합니다.")
            break

    cf.db_close()
    break

