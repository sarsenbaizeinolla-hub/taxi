import psycopg2

# Функция подключения
def connect_db():
    return psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="123456789", # Сюда впиши свой пароль от базы
        host="localhost", 
        port="12345" # Проверь порт, обычно 5432
    )

# Функция для добавления поездки и оценки (Задание №1)
def add_ride(driver_id, client_id, score):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO rides (driver_id, client_id, score) VALUES (%s, %s, %s)",
            (driver_id, client_id, score)
        )
        conn.commit()
        print(f"Успех: Поездка завершена. Оценка {score} поставлена.")
    except Exception as e:
        print(f"Ошибка при добавлении поездки: {e}")
    finally:
        cur.close()
        conn.close()

# Основной блок запуска "Приложения"
if __name__ == "__main__":
    print("--- ПРИЛОЖЕНИЕ ТАКСИ ЗАПУЩЕНО ---")
    try:
        # 1. Имитируем вызов такси и оценку
        # (Водитель №1 получает оценку 5 от Клиента №1)
        add_ride(1, 1, 5)
        
        # 2. Проверяем, как сработал ТРИГГЕР в базе
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT name, rating FROM drivers WHERE id = 1")
        driver_data = cur.fetchone()
        
        print(f"\nДанные из базы после работы триггера:")
        print(f"Водитель: {driver_data[0]}")
        print(f"Автоматический рейтинг: {driver_data[1]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Ошибка соединения: {e}")
        print("Проверь пароль и запущен ли pgAdmin!")