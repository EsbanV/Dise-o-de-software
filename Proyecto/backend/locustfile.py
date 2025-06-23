from locust import HttpUser, TaskSet, task, between
import random
import string

def random_email():
    return f"user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}@test.com"

class UserBehavior(TaskSet):
    def on_start(self):
        # 1) Registro
        self.email = random_email()
        self.password = "Password123"
        reg_data = {
            "nombre": "LocustUser",
            "correo": self.email,
            "password": self.password
        }
        with self.client.post("/registro", data=reg_data, catch_response=True) as resp:
            if resp.status_code != 200 and resp.status_code != 302:
                resp.failure(f"Registro falló: {resp.status_code}")
        
        # 2) Login
        login_data = {"correo": self.email, "password": self.password}
        with self.client.post("/login", data=login_data, catch_response=True) as resp:
            if resp.status_code != 200 and resp.status_code != 302:
                resp.failure(f"Login falló: {resp.status_code}")

    @task(3)
    def view_dashboard(self):
        # GET a la ruta raíz: muestra el dashboard HTML
        with self.client.get("/", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Dashboard falló: {resp.status_code}")

    @task(2)
    def new_transaction(self):
        # POST a la ruta de transacciones_vista
        # Se usa categoria_id=1 como ejemplo
        params = {"categoria_id": 1}
        form = {"monto": str(round(random.uniform(1, 100), 2))}
        with self.client.post("/transacciones_vista", params=params, data=form, catch_response=True) as resp:
            # Tras un POST exitoso redirige (302) de vuelta al mismo endpoint
            if resp.status_code not in (200, 302):
                resp.failure(f"Registrar transacción falló: {resp.status_code}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
