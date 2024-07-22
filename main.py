import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Цены на топливо
fuel_prices = {"Аи-95": 65.45, "Дизель": 52.65}
fuel_type = None
total_price = 0
current_payment = 0

# Создание главного окна
root = tk.Tk()
root.title("АЗС Терминал")
root.geometry("1920x1080")
root.config(bg="black")
root.resizable(False, False)

# Загрузка изображения для заднего фона
bg_image = Image.open("back.png")  # Укажите путь к вашему изображению
bg_image = bg_image.resize((1920, 1080))
bg_photo = ImageTk.PhotoImage(bg_image)

# Создание метки для отображения фонового изображения
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Экран автомата
screen_frame = tk.Frame(root, bg="light blue", width=740, height=400, bd=25, relief="sunken")
screen_frame.place(relx=0.219, rely=0.231 , anchor="center")
screen_frame.pack_propagate(False)

# Дополнительный фрейм для числовых кнопок и кнопок внесения наличных
number_button_frame = tk.Frame(root)
number_button_frame.place(relx=0.1, rely=0.6, anchor="center")

# Фрейм для кнопок внесения наличных
payment_button_frame = tk.Frame(root)
payment_button_frame.place(relx=0.3, rely=0.67, anchor="center")

# Создание числовых кнопок
def create_number_buttons():
    for i in range(1, 10):
        tk.Button(number_button_frame, text=str(i), font=("Impact", 15), command=lambda x=i: append_to_entry(str(x)), bg="gray", fg="black", bd=7, relief="raised", width=5, height=2).grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5)
    tk.Button(number_button_frame, text="0", font=("Impact", 15), command=lambda: append_to_entry("0"), bg="gray", fg="black", bd=7, relief="raised", width=5, height=2).grid(row=3, column=1, padx=5, pady=5)
    tk.Button(number_button_frame, text=".", font=("Impact", 15), command=lambda: append_to_entry("."), bg="gray", fg="black", bd=7, relief="raised", width=5, height=2).grid(row=3, column=0, padx=5, pady=5)
    tk.Button(number_button_frame, text="<-", font=("Impact", 15), command=backspace_entry, bg="gray", fg="black", width=5, bd=7, relief="raised", height=2).grid(row=3, column=2, padx=5, pady=5)

# Создание кнопки "Вернуться"
def returning():
    tk.Button(payment_button_frame, text="Вернуться", font=("Impact", 24), command=create_main_menu, bg="red", fg="black", bd=7, relief="raised", width=15).grid(row=2, columnspan=2)

# Создание кнопок внесения наличных
def create_payment_buttons():
    tk.Button(payment_button_frame, text="1000", font=("Courier", 14), command=lambda: add_payment(1000), bg="green", fg="light blue", bd=7, relief="raised", width=10).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(payment_button_frame, text="500", font=("Courier", 14), command=lambda: add_payment(500), bg="green", fg="light blue", bd=7, relief="raised", width=10).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(payment_button_frame, text="100", font=("Courier", 14), command=lambda: add_payment(100), bg="green", fg="light blue", bd=7, relief="raised", width=10).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(payment_button_frame, text="50", font=("Courier", 14), command=lambda: add_payment(50), bg="green", fg="light blue", bd=7, relief="raised", width=10).grid(row=1, column=1, padx=5, pady=5)

# Функция для создания главного меню
def create_main_menu():
    clear_screen()
    tk.Label(screen_frame, text="Выберите вид топлива", font=("Impact", 24), fg="black", bg="light blue").pack(pady=20)
    tk.Button(screen_frame, text="Аи-95 - 65.45 р.", font=("Courier", 28), command=select_ai98, bg="green", fg="light blue", width=20).pack(pady=10)
    tk.Button(screen_frame, text="Дизель - 52.65 р.", font=("Courier", 28), command=select_diesel, bg="green", fg="light blue", width=20).pack(pady=10)

# Функция для очистки экрана
def clear_screen():
    for widget in screen_frame.winfo_children():
        widget.destroy()

# Функции для выбора топлива
def select_ai98():
    global fuel_type
    fuel_type = "Аи-98"
    create_fuel_entry()

def select_diesel():
    global fuel_type
    fuel_type = "Дизель"
    create_fuel_entry()

# Функция для создания ввода объема топлива
def create_fuel_entry():
    clear_screen()
    tk.Label(screen_frame, text=f"Введите объем топлива для {fuel_type} (литр)", font=("Impact", 24), fg="black",
             bg="light blue").pack(pady=20)
    global entry_fuel
    entry_fuel = tk.Entry(screen_frame, font=("Courier", 18), width=10, justify='center')
    entry_fuel.pack(pady=10)
    tk.Button(screen_frame, text="Посчитать", font=("Courier", 18), command=calculate_price, bg="green",
              fg="light blue", width=20).pack(pady=10)


# Функции для управления вводом
def append_to_entry(char):
    current_text = entry_fuel.get()
    if char == "." and "." in current_text:
        return
    entry_fuel.insert(tk.END, char)


def backspace_entry():
    current_text = entry_fuel.get()
    if current_text:
        entry_fuel.delete(len(current_text) - 1, tk.END)


# Функция для расчета стоимости топлива
def calculate_price():
    try:
        liters = float(entry_fuel.get())
        global total_price
        total_price = liters * fuel_prices[fuel_type]
        show_payment_screen(total_price)
    except ValueError:
        show_error("Неправильный ввод! Пожалуйста, введите число.")


# Функция для отображения экрана оплаты
def show_payment_screen(price):
    clear_screen()
    global current_payment
    current_payment = 0
    tk.Label(screen_frame, text=f"С вас {int(price)} руб. {int(100 * round(price % 1, 2))} коп.", font=("Impact", 24),
             fg="red", bg="light blue").pack(pady=20)
    tk.Label(screen_frame, text="Оплата производится наличными, без сдачи.", font=("Courier", 18), fg="black",
             bg="light blue").pack(pady=10)
    tk.Label(screen_frame, text="Используйте купюры 1000, 500, 100, 50 руб.", font=("Courier", 18), fg="black",
             bg="light blue").pack(pady=10)
    global payment_label
    payment_label = tk.Label(screen_frame, text="Сумма: 0 руб.", font=("Impact", 24), fg="red", bg="light blue")
    payment_label.pack(pady=20)




# Функция для добавления оплаты
def add_payment(amount):
    global current_payment
    current_payment += amount
    payment_label.config(text=f"Сумма: {current_payment} руб.")
    if current_payment >= total_price:
        payment_label.config(fg="green")
        show_thank_you()


# Функция для отображения благодарственного сообщения
def show_thank_you():
    clear_screen()
    tk.Label(screen_frame, text="Спасибо за покупку!", font=("Impact", 45), fg="black", bg="light blue").pack(pady=150)

# Функция для отображения ошибки
def show_error(message):
    messagebox.showerror("Ошибка", message)


# Инициализация главного меню
create_main_menu()
create_number_buttons()
create_payment_buttons()
returning()
root.mainloop()