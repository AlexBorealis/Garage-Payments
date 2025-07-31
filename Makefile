# Определение переменных
IMAGE_NAME = garage-payments
TAG = latest

# Сборка образа
build:
	podman build -t $(IMAGE_NAME):$(TAG) .

# Запуск контейнера
run:
	podman run --rm -it \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/output:/app/result \
		$(IMAGE_NAME):$(TAG)

# Остановка и удаление контейнеров
clean-containers:
	podman container prune -f

# Удаление образа
clean-images:
	podman rmi $(IMAGE_NAME):$(TAG)

# Полная очистка
clean: clean-containers clean-images

# Локальный запуск
local:
	PYTHONPATH=$(PWD) python3 src/garage_payments/main.py