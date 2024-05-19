server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /path/to/cert.pem;   # Путь к вашему SSL-сертификату
    ssl_certificate_key /path/to/key.pem;  # Путь к вашему ключу SSL

    location / {
        proxy_pass http://127.0.0.1:8000;  # Адрес, на котором слушает Gunicorn ваше приложение Django
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


