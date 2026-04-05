-- Удаляем старые таблицы, если они были, чтобы не было ошибок
DROP TABLE IF EXISTS rides;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS clients;

-- 1. Создаем таблицы
CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    rating NUMERIC(3, 2) DEFAULT 0
);

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE rides (
    id SERIAL PRIMARY KEY,
    driver_id INT REFERENCES drivers(id),
    client_id INT REFERENCES clients(id),
    score INT CHECK (score >= 1 AND score <= 5)
);

-- 2. Функция для автоматического пересчета рейтинга (PL/pgSQL)
CREATE OR REPLACE FUNCTION update_driver_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE drivers
    SET rating = (SELECT AVG(score) FROM rides WHERE driver_id = NEW.driver_id)
    WHERE id = NEW.driver_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 3. Триггер, который запускает функцию после каждой оценки
CREATE TRIGGER after_ride_insert
AFTER INSERT ON rides
FOR EACH ROW EXECUTE FUNCTION update_driver_rating();

-- Добавим одного водителя и клиента для теста
INSERT INTO drivers (name) VALUES ('Мухаммад');
INSERT INTO clients (name) VALUES ('Тестовый Клиент');