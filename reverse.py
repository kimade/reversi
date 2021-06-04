import numpy as np
import sys
import copy


class reverse:
    # 初期設定
    column = np.arange(1, 9)  # 行のインデックス
    row = np.arange(1, 9)  # 列のインデックス
    board = np.array([["×"] * 8] * 8)  # 盤面  # 石を置いていないところは×で表記する
    # 初期配置
    board[3, 3] = "○"
    board[3, 4] = "●"
    board[4, 4] = "○"
    board[4, 3] = "●"
    board_copy = copy.deepcopy(board)

    def __init__(self):
        # 先攻・後攻の決定
        print("先攻(黒:○)の名前を入力してください")
        self.former = input()
        print("後攻(白:●)の名前を入力してください")
        self.later = input()
        self.print_board()
        print("入力は以下のようにしてください")
        print("例：3 4　(3行4列におきたいとき)")
        self.turn = "○"  # 先攻:○, 後攻:●として管理

    def put_stone(self):
        print()
        if self.turn == "○":
            print(self.former + "(黒:○)のターンです。")
        else:
            print(self.later + "(白:●)のターンです。")
        print("どこに石をおきますか")
        while 1:
            try:
                c, r = map(int, input().split())
                if not ((1 <= c <= 8) and (1 <= r <= 8)):
                    print("不正な入力です。もう一度お願いします。")
                else:
                    break

            except:  # 数字以外の入力や3つ以上の引数がきたとき
                print("不正な入力です。もう一度お願いします。")

        if self.search(c, r):  # 石を置けるならば置く
            if self.turn == "●":
                self.turn = "○"  # turnの交代
            else:
                self.turn = "●"  # turnの交代
        else:  # 置けない時にはもう一度処理をやり直す
            print("そこに石を置くことはできません。もう一度石を置く場所を選び直してください。")
            self.put_stone()

    def search(self, c, r):  # 置ける場所を確認する関数 置けるならばTrueを返し、ダメならFalseを返す
        if self.board[c - 1, r - 1] != "×":  # 石が置いてあるかどうかの確認
            return False  # 石が置いてあったらFalseを返す
        else:  # ひっくり返せる石があるかどうかの確認
            self.board = self.board_copy.copy()  # 盤面に同期
            A = self.check_vertical(c, r, rvs=True)
            self.board = self.board_copy.copy()  # 盤面に同期
            B = self.check_side(c, r, rvs=True)
            self.board = self.board_copy.copy()  # 盤面に同期
            C = self.check_diagonal(c, r, rvs=True)
            self.board = self.board_copy.copy()  # 盤面に同期

            if (A or B or C) == False:  # 縦・横・斜めのどこにも置けない時にはFalseを返す
                return False
            else:  # どこかにおけたら続行する
                self.board = self.board_copy
                return True

    def check_vertical(self, c, r, rvs=True):  # 縦にひっくり返せるかのチェック ひっくり返せたらひっくり返してTrue、だめならFalseを返す
        c_v = c - 1
        r_v = r - 1
        if c_v == 0:  # 上端の場合
            if (self.board[c_v + 1, r_v] == self.turn) or (self.board[c_v + 1, r_v] == "×"):  # 下が自分と同じ色か×だったらOUT
                return False
            else:  # 下に違う色がある時
                if rvs:
                    self.board_copy[c_v, r_v] = self.turn  # 指定の場所に石を置く
                for i in range(c_v + 1, len(self.column)):  # 一番下まで確認して
                    if self.board[i, r_v] == "×":
                        break
                    if self.board[i, r_v] != self.turn:
                        if rvs:  # ひっくり返す
                            self.board_copy[i, r_v] = self.turn
                        else:  # ひっくり返さない
                            continue
                    elif self.board[i, r_v] == self.turn:  # 同じ色があったらTrue
                        return True
                self.board_copy = self.board  # ひっくり返せない時にはcopyを更新しない
                return False

        elif c_v == 7:  # 下端の場合
            if (self.board[c_v - 1, r_v] == self.turn) or (self.board[c_v - 1, r_v] == "×"):  # 上が自分と同じ色か×だったらOUT
                return False
            else:
                if rvs:
                    self.board_copy[c_v, r_v] = self.turn  # 指定の場所に石を置く
                for i in range(c_v - 1, -1, -1):  # 一番上まで確認して
                    if self.board[i, r_v] == "×":
                        break
                    if self.board[i, r_v] != self.turn:
                        if rvs:  # ひっくり返す
                            self.board_copy[i, r_v] = self.turn
                        else:  # ひっくり返さない
                            continue
                    elif self.board[i, r_v] == self.turn:  # 同じ色があったらTrue
                        return True
                self.board_copy = self.board  # ひっくり返せない時にはcopyを更新しない
                return False

        else:  # 上端でも下端でもない場合
            if (self.board[c_v - 1, r_v] == self.turn) and (
                    self.board[c_v + 1, r_v] == self.turn):  # 上下が自分の色と同じ色だったらOUT
                return False
            if (self.board[c_v - 1, r_v] == "×") and (self.board[c_v + 1, r_v] == "×"):  # 上下ともに×でもOUT
                return False
            # 下の確認
            under = False  # 下をまだひっくり返していない
            if (self.board[c_v + 1, r_v] != self.turn) and (self.board[c_v + 1, r_v] != "×"):  # 下が自分と違う色だった場合
                if rvs:
                    self.board_copy[c_v, r_v] = self.turn  # 指定の場所に石を置く
                for i in range(c_v + 1, len(self.column)):  # 一番下まで確認して
                    if self.board[i, r_v] == "×":
                        self.board_copy = self.board
                        break
                    if self.board[i, r_v] != self.turn:
                        if rvs:
                            self.board_copy[i, r_v] = self.turn
                        else:
                            continue
                    elif self.board[i, r_v] == self.turn:  # 同じ色があったらひっくり返せるのでflag=Trueに
                        under = True
                        break

            # 上の確認
            top = False
            if (self.board[c_v - 1, r_v] != self.turn) and (self.board[c_v - 1, r_v] != "×"):  # 上が自分と違う色だった場合
                if rvs:
                    self.board_copy[c_v, r_v] = self.turn  # 指定の場所に石を置く
                for i in range(c_v - 1, -1, -1):  # 一番上まで確認して
                    if self.board[i, r_v] == "×":
                        self.board_copy = self.board
                        break
                    if self.board[i, r_v] != self.turn:
                        if rvs:
                            self.board_copy[i, r_v] = self.turn
                        else:
                            continue
                    elif self.board[i, r_v] == self.turn:  # 同じ色があったらひっくり返せるのでflag=Trueに
                        top = True
                        break

            if top or under:  # 上か下どっちかひっくり返している
                return True
            else:
                return False

    def check_side(self, c, r, rvs=True):  # 横にひっくり返せるかのチェック ひっくり返せたらひっくり返してTrue、だめならFalseを返す
        c_s = c - 1
        r_s = r - 1

        if r_s == 0:  # 左端の場合
            if (self.board[c_s, r_s + 1] == self.turn) or (self.board[c_s, r_s + 1] == "×"):  # 右が自分と同じ色か×だったらOUT
                return False
            else:  # 右に違う色がある時
                if rvs:
                    self.board_copy[c_s, r_s] = self.turn  # 指定の場所に石を置く
                for i in range(r_s + 1, len(self.row)):  # 一番右まで確認して
                    if self.board[c_s, i] == "×":
                        break
                    if self.board[c_s, i] != self.turn:
                        if rvs:
                            self.board_copy[c_s, i] = self.turn
                        else:
                            continue
                    elif self.board[c_s, i] == self.turn:  # 同じ色があったらひっくり返せるのでflag=Trueに
                        return True
                self.board_copy = self.board
                return False

        elif r_s == 7:  # 右端の場合
            if (self.board[c_s - 1, r_s] == self.turn) or (self.board[c_s, r_s - 1] == "×"):  # 左が自分と同じ色か×だったらOUT
                return False
            else:
                if rvs:
                    self.board_copy[c_s, r_s] = self.turn  # 指定の場所に石を置く
                for i in range(r_s - 1, -1, -1):  # 一番右まで確認して
                    if self.board[c_s, i] == "×":
                        break
                    if self.board[c_s, i] != self.turn:
                        if rvs:
                            self.board_copy[c_s, i] = self.turn
                        else:
                            continue
                    elif self.board[c_s, i] == self.turn:  # 同じ色があったらひっくり返せるのでflag=Trueに
                        return True
                self.board_copy = self.board
                return False

        else:  # 右端でも左端でもない場合
            if (self.board[r_s, r_s - 1] == self.turn) and (
                    self.board[c_s, r_s + 1] == self.turn):  # 左右が自分の色と同じ色だったらOUT
                return False
            if (self.board[c_s, r_s - 1] == "×") and (self.board[c_s, r_s + 1] == "×"):  # 左右ともに×でもOUT
                return False
            # 右の確認
            right = False  # 右をまだひっくり返していない
            if (self.board[c_s, r_s + 1] != self.turn) and (self.board[c_s, r_s + 1] != "×"):  # 右が自分と違う色だった場合
                if rvs:
                    self.board_copy[c_s, r_s] = self.turn  # 指定の場所に石を置く
                for i in range(r_s + 1, len(self.row)):  # 一番右まで確認して
                    if self.board[c_s, i] == "×":
                        self.board_copy = self.board
                        break
                    if self.board[c_s, i] != self.turn:
                        if rvs:
                            self.board_copy[c_s, i] = self.turn
                        else:
                            continue
                    elif self.board[c_s, i] == self.turn:  # 同じ色があったらひっくり返せるのでflag=Trueに
                        right = True
                        break
            # 左の確認
            left = False
            if (self.board[c_s, r_s - 1] != self.turn) and (self.board[c_s, r_s - 1] != "×"):  # 左が自分と違う色だった場合
                if rvs:
                    self.board_copy[c_s, r_s] = self.turn  # 指定の場所に石を置く
                for i in range(r_s - 1, -1, -1):  # 一番左まで確認して
                    if self.board[c_s, i] == "×":
                        self.board_copy = self.board
                        break
                    if self.board[c_s, i] != self.turn:
                        if rvs:
                            self.board_copy[c_s, i] = self.turn
                        else:
                            continue
                    elif self.board[c_s, i] == self.turn:  # 同じ色があったらひっくり返せるのでflag=Trueに
                        left = True
                        break

            if (left or right):  # 上か下どっちかひっくり返している
                return True
            else:
                return False

    def check_diagonal(self, c, r, rvs=True):  # 斜めにひっくり返せるかのチェック ひっくり返せたらひっくり返してTrue、だめならFalseを返す
        c_d = c - 1
        r_d = r - 1

        # TODO:角のひっくり返し方の実装
        if c_d == 0:
            if r_d == 0:  # 左上の角
                if (self.board[c_d + 1, r_d + 1] == self.turn) or (self.board[c_d + 1, r_d + 1] == "×"):
                    return False
                for i in range(1, len(self.column)):
                    if (self.board[i, i] == "×"):
                        break
                    if (self.board[i, i] != self.turn):
                        if rvs:
                            self.board[i, i] = self.turn
                        else:
                            continue
                    elif self.board[i, i] == self.turn:
                        return True
                self.board_copy = self.board
                return False

            elif r_d == 7:  # 右上の角
                if (self.board[c_d + 1, r_d - 1] == self.turn) or (self.board[c_d + 1, r_d - 1] == "×"):
                    return False
                for i in range(1, len(self.column)):
                    if (self.board[i, 7 - i] == "×"):
                        break
                    if (self.board[i, 7 - i] != self.turn):
                        if rvs:
                            self.board[i, 7 - i] = self.turn
                        else:
                            continue
                    elif self.board[i, 7 - i] == self.turn:
                        return True
                self.board_copy = self.board
                return False

        elif c_d == 7:
            if r_d == 0:  # 左下の角
                if (self.board[c_d - 1, r_d + 1] == self.turn) or (self.board[c_d - 1, r_d + 1] == "×"):
                    return False
                for i in range(1, len(self.column)):
                    if (self.board[7 - i, i] == "×"):
                        break
                    if (self.board[7 - i, i] == self.turn):
                        if rvs:
                            self.board[7 - i, i] = self.turn
                        else:
                            continue
                    elif self.board[7 - i, i] == self.turn:
                        return True
                self.board_copy = self.board
                return False

            elif r_d == 7:  # 右下の角
                if (self.board[c_d - 1, r_d - 1] == self.turn) or (self.board[c_d - 1, r_d - 1] == "×"):
                    return False
                for i in range(1, len(self.column)):
                    if (self.board[7 - i, 7 - i] == "×"):
                        break
                    if (self.board[7 - i, 7 - i] != self.turn):
                        if rvs:
                            self.board[7 - i, 7 - i] = self.turn
                        else:
                            continue
                    elif self.board[7 - i, 7 - i] == self.turn:
                        return True
                self.board_copy = self.board
                return False

        # TODO:端のひっくり返し方の実装
        if c_d == 0:
            a = ((self.board[c_d + 1, r_d + 1] == self.turn) or (self.board[c_d + 1, r_d + 1] == "×"))
            b = ((self.board[c_d + 1, r_d - 1] == self.turn) or (self.board[c_d + 1, r_d - 1] == "×"))
            if (a and b):
                return False
            # 左斜め下
            down_l = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d + i, r_d - i] == "×":
                        break
                    if self.board[c_d + i, r_d - i] != self.turn:
                        if rvs:
                            self.board_copy[c_d + i, r_d - i] = self.turn
                        else:
                            continue
                    elif self.board[c_d + i, r_d - i] == self.turn:
                        down_l = True
                        break
                except:
                    break
            if down_l == False:  # ひっくり返せない時
                self.board_copy = self.board

            # 右斜め下
            down_r = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d + i, r_d + i] == "×":
                        break
                    if self.board[c_d + i, r_d + i] != self.turn:
                        if rvs:
                            self.board_copy[c_d + i, r_d + i] = self.turn
                        else:
                            continue
                    elif self.board[c_d + i, r_d + i] == self.turn:
                        down_r = True
                        break
                except:
                    break
            if down_r == False:  # ひっくり返せない時
                self.board_copy = self.board

            if down_l or down_r:
                return True
            else:
                return False

        elif c_d == 7:
            a = ((self.board[c_d - 1, r_d - 1] == self.turn) or (self.board[c_d - 1, r_d - 1] == "×"))
            b = ((self.board[c_d - 1, r_d + 1] == self.turn) or (self.board[c_d - 1, r_d + 1] == "×"))
            if (a and b):
                return False
            # 左斜め上
            up_l = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d - i, r_d - i] == "×":
                        break
                    if self.board[c_d - i, r_d - i] != self.turn:
                        if rvs:
                            self.board_copy[c_d - i, r_d - i] = self.turn
                        else:
                            continue
                    elif self.board[c_d - i, r_d - i] == self.turn:
                        up_l = True
                        break
                except:
                    break
            if up_l == False:  # ひっくり返せない時
                self.board_copy = self.board

            # 右斜め上
            up_r = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d - i, r_d + i] == "×":
                        break
                    if self.board[c_d - i, r_d + i] != self.turn:
                        if rvs:
                            self.board_copy[c_d - i, r_d + i] = self.turn
                        else:
                            continue
                    elif self.board[c_d - i, r_d + i] == self.turn:
                        up_r = True
                        break
                except:
                    break
            if up_r == False:  # ひっくり返せない時
                self.board_copy = self.board

            if up_l or up_r:
                return True
            else:
                return False

        if r_d == 0:
            a = ((self.board[c_d + 1, r_d + 1] == self.turn) or (self.board[c_d + 1, r_d + 1] == "×"))
            b = ((self.board[c_d - 1, r_d + 1] == self.turn) or (self.board[c_d - 1, r_d + 1] == "×"))
            if (a and b):
                return False
            # 右斜め上
            up_r = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d - i, r_d + i] == "×":
                        break
                    if self.board[c_d - i, r_d + i] != self.turn:
                        if rvs:
                            self.board_copy[c_d - i, r_d + i] = self.turn
                        else:
                            continue
                    elif self.board[c_d - i, r_d + i] == self.turn:
                        up_r = True
                        break
                except:
                    break
            if up_r == False:  # ひっくり返せない時
                self.board_copy = self.board

            # 右斜め下
            down_r = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d + i, r_d + i] == "×":
                        break
                    if self.board[c_d + i, r_d + i] != self.turn:
                        if rvs:
                            self.board_copy[c_d + i, r_d + i] = self.turn
                        else:
                            continue
                    elif self.board[c_d + i, r_d + i] == self.turn:
                        down_r = True
                        break
                except:
                    break
            if down_r == False:  # ひっくり返せない時
                self.board_copy = self.board

            if up_r or down_r:
                return True
            else:
                return False


        elif r_d == 7:
            a = ((self.board[c_d + 1, r_d - 1] == self.turn) or (self.board[c_d + 1, r_d - 1] == "×"))
            b = ((self.board[c_d - 1, r_d - 1] == self.turn) or (self.board[c_d - 1, r_d - 1] == "×"))
            if (a and b):
                return False

            # 左斜め上
            up_l = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d - i, r_d - i] == "×":
                        break
                    if self.board[c_d - i, r_d - i] != self.turn:
                        if rvs:
                            self.board_copy[c_d - i, r_d - i] = self.turn
                        else:
                            continue
                    elif self.board[c_d - i, r_d - i] == self.turn:
                        up_l = True
                        break
                except:
                    break
            if up_l == False:  # ひっくり返せない時
                self.board_copy = self.board

            # 左斜め下
            down_l = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d + i, r_d - i] == "×":
                        break
                    if self.board[c_d + i, r_d - i] != self.turn:
                        if rvs:
                            self.board_copy[c_d + i, r_d - i] = self.turn
                        else:
                            continue
                    elif self.board[c_d + i, r_d - i] == self.turn:
                        down_l = True
                        break
                except:
                    break
            if down_l == False:  # ひっくり返せない時
                self.board_copy = self.board

            if up_l or down_l:
                return True
            else:
                return False

        # TODO:どれでもない時のひっくり返し方の実装
        else:
            A = ((self.board[c_d + 1, r_d - 1] == self.turn) or (self.board[c_d + 1, r_d - 1] == "×"))
            B = ((self.board[c_d - 1, r_d - 1] == self.turn) or (self.board[c_d - 1, r_d - 1] == "×"))
            C = ((self.board[c_d + 1, r_d + 1] == self.turn) or (self.board[c_d + 1, r_d + 1] == "×"))
            D = ((self.board[c_d - 1, r_d + 1] == self.turn) or (self.board[c_d - 1, r_d + 1] == "×"))
            if (A and B and C and D):  # どこにも置けないなら
                return False

            # 左斜め上
            up_l = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d - i, r_d - i] == "×":
                        break
                    if self.board[c_d - i, r_d - i] != self.turn:
                        if rvs:
                            self.board_copy[c_d - i, r_d - i] = self.turn
                        else:
                            continue
                    elif self.board[c_d - i, r_d - i] == self.turn:
                        up_l = True
                        break
                except:
                    break
            if up_l == False:  # ひっくり返せない時
                self.board_copy = self.board

            # 左斜め下
            down_l = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d + i, r_d - i] == "×":
                        break
                    if self.board[c_d + i, r_d - i] != self.turn:
                        if rvs:
                            self.board_copy[c_d + i, r_d - i] = self.turn
                        else:
                            continue
                    elif self.board[c_d + i, r_d - i] == self.turn:
                        down_l = True
                        break
                except:
                    break
            if down_l == False:  # ひっくり返せない時
                self.board_copy = self.board

            # 右斜め上
            up_r = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d - i, r_d + i] == "×":
                        break
                    if self.board[c_d - i, r_d + i] != self.turn:
                        if rvs:
                            self.board_copy[c_d - i, r_d + i] = self.turn
                        else:
                            continue
                    elif self.board[c_d - i, r_d + i] == self.turn:
                        up_r = True
                        break
                except:
                    break
            if up_r == False:  # ひっくり返せない時
                self.board_copy = self.board

            # 右斜め下
            down_r = False
            if rvs:
                self.board_copy[c_d, r_d] = self.turn
            for i in range(1, len(self.column)):
                try:
                    if self.board[c_d + i, r_d + i] == "×":
                        break
                    if self.board[c_d + i, r_d + i] != self.turn:
                        if rvs:
                            self.board_copy[c_d + i, r_d + i] = self.turn
                        else:
                            continue
                    elif self.board[c_d + i, r_d + i] == self.turn:
                        down_r = True
                        break
                except:
                    break
            if down_r == False:  # ひっくり返せない時
                self.board_copy = self.board

            if (up_r) or (down_r) or (up_l) or (up_r):
                return True
            else:
                return False

    def judge(self):  # 終局判定をする関数
        for i in range(len(self.column)):
            for j in range(len(self.row)):
                if self.board[i, j] != "×":  # 置いてあるところは無視する
                    continue
                A = self.check_vertical(i + 1, j + 1, rvs=False)
                B = self.check_side(i + 1, j + 1, rvs=False)
                C = self.check_diagonal(i + 1, j + 1, rvs=False)
                if (A or B or C):  # どこかひとつでも置けるのであればまだ終局でないのでreturnする
                    return  # まだ続ける
        self.count_stone()  # どこにも置けないのであればFalseを返して対局を終了する
        sys.exit()

    def count_stone(self):  # 石の数を数えて勝敗を決める関数
        cnt_black = 0
        cnt_white = 0
        for i in range(len(self.column)):
            for j in range(len(self.row)):
                if self.board[i, j] == "●":
                    cnt_black += 1
                elif self.board[i, j] == "○":
                    cnt_white += 1
        print("対局終了")
        if cnt_black > cnt_white:
            print("勝者は" + self.former + "です。")
        elif cnt_white > cnt_black:
            print("勝者は" + self.later + "です。")
        else:
            print("黒と白が同数なため引き分けです。")

    def print_board(self):  # 盤面を表示する関数
        print(" ", *self.column)
        for i in range(len(self.column)):
            print(self.row[i], *(self.board[i]))

    def play(self):  # 試合を実行する関数
        while 1:
            self.put_stone()
            self.print_board()
            self.judge()
