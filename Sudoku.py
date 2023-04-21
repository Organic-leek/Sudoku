import pytesseract
import time
import pyautogui


def dfs(n):
    if n == len(valid):
        print('完成')
        return True
    i, j = valid[n]
    res = nums - line[i] - col[j] - block[i // 3][j // 3]
    if not res: return False
    for k in res:
        line[i].add(k)
        col[j].add(k)
        block[i // 3][j // 3].add(k)
        board[i][j] = k
        if dfs(n + 1): return True
        line[i].remove(k)
        col[j].remove(k)
        block[i // 3][j // 3].remove(k)


def Sudoku_locate():
    xy1 = pyautogui.locateOnScreen(r"img1.png", confidence=0.95)
    xy2 = pyautogui.locateOnScreen(r"img2.png", confidence=0.95)
    x1, y1 = pyautogui.center(xy1)
    x2, y2 = pyautogui.center(xy2)
    im = pyautogui.screenshot()
    im = im.crop([x1, y1 + 5, x2, y2])
    height = (y2 - y1) / 9
    wide = (x2 - x1) / 9
    im = im.convert('L')
    table = []
    for i in range(256):
        if i > 156:
            table.append(0)
        else:
            table.append(1)
    im = im.point(table, '1')
    im.show()
    sudoku = [['.'] * 9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            om = im.crop([wide * j + 2, height * i+2, wide * (j + 1) - 5, height * (i + 1) - 6])
            string = pytesseract.image_to_string(om, config='--psm 6', lang="eng")

            if string:
                sudoku[i][j] = string[0]
    return sudoku, x1, y1, height, wide


while True:
    time.sleep(0.5)
    try:
        board, x1, y1, height, wide = Sudoku_locate()
        print(board)
        break
    except Exception as e:
        print(e)

nums = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
col = [set() for _ in range(9)]
line = [set() for _ in range(9)]
block = [[set() for _a in range(3)] for _b in range(3)]
valid = []

for i in range(9):
    for j in range(9):
        a = board[i][j]
        if a == '.':
            valid.append((i, j))
        else:
            line[i].add(a)
            col[j].add(a)
            block[i // 3][j // 3].add(a)
dfs(0)
for i in range(9):
    for j in range(9):
        a = board[i][j]
        if a == '.':
            print('该数独不可解')
            break
for i, j in valid:
    pyautogui.click([x1 + wide * (j + 0.5), y1 + height * (i + 0.5)])
    pyautogui.typewrite(board[i][j])
