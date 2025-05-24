def bmi(hei:int,wei:int) -> float:
    return wei / (hei/100) ** 2

def warning(bmi:float) -> str:
    if bmi < 18.5 :         #不同funtion之間互相獨立，和主程式也獨立，所以可以取一樣的變數/參數名
        return "體重過輕"
    elif bmi < 24 :
        return "體重正常"
    elif bmi < 27 :
        return "過重"
    else: 
        return "肥胖"

def main():
    hei:int = int(input("輸入身高："))
    wei:int = int(input("輸入體重："))

    bmi_you = bmi(hei,wei)
    print(bmi_you)
    print(warning(bmi_you))

if __name__ == '__main__':
    main()