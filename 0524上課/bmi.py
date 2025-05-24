import bmi_calculate #導入module

def main():
    hei:int = int(input("輸入身高："))
    wei:int = int(input("輸入體重："))

    bmi = bmi_calculate.bmi #呼叫module裡的function
    warning = bmi_calculate.warning #呼叫module裡的funtion

    bmi_you = bmi(hei,wei)
    print(bmi_you)
    print(warning(bmi_you))

if __name__ == '__main__':
    main()