#import bmi_calculate #導入module
from edu.bmi_calculate import bmi as a1 #這個pacakage（edu）的moudule（bmi_calculate）裡的function（bmi）叫a1
from edu.bmi_calculate import warning as a2

def main():
    hei:int = int(input("輸入身高："))
    wei:int = int(input("輸入體重："))

    #bmi = bmi_calculate.bmi #呼叫module裡的function
    #warning = bmi_calculate.warning #呼叫module裡的funtion
    bmi = a1
    warning =a2

    bmi_you = a1(hei,wei)
    print(bmi_you)
    print(a2(bmi_you))

if __name__ == '__main__':
    main()