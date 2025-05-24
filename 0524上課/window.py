import tkinter as tk
import bmi_calculate

def calculate_bmi():
    try:
        hei = int(entry_height.get())
        wei = int(entry_weight.get())
        bmi = bmi_calculate.bmi(hei, wei)
        warning_msg = bmi_calculate.warning(bmi)
        label_result.config(text=f"BMI: {bmi:.2f}")
        # 根據警告訊息設定顏色
        if warning_msg == "體重正常":
            label_warning.config(text=warning_msg, fg="black")
        else:
            label_warning.config(text=warning_msg, fg="red")
    except ValueError:
        label_result.config(text="請輸入正確的數字")
        label_warning.config(text="", fg="red")
        
window = tk.Tk()
window.title("BMI 計算器")

tk.Label(window, text="身高（公分）:").grid(row=0, column=0, padx=10, pady=5)
entry_height = tk.Entry(window)
entry_height.grid(row=0, column=1, padx=10, pady=5)

tk.Label(window, text="體重（公斤）:").grid(row=1, column=0, padx=10, pady=5)
entry_weight = tk.Entry(window)
entry_weight.grid(row=1, column=1, padx=10, pady=5)

btn_calculate = tk.Button(window, text="計算 BMI", command=calculate_bmi)
btn_calculate.grid(row=2, column=0, columnspan=2, pady=10)

label_result = tk.Label(window, text="")
label_result.grid(row=3, column=0, columnspan=2)

label_warning = tk.Label(window, text="", fg="red")
label_warning.grid(row=4, column=0, columnspan=2)

window.mainloop()