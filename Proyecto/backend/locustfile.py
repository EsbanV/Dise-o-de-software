from locust import HttpUser, task, between

class FinanzasUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Registro y login de un usuario de prueba
        self.client.post("/usuario/registro", json={
            "email": "test@example.com",
            "password": "1234"
        })
        resp = self.client.post("/usuario/login", json={
            "email": "test@example.com",
            "password": "1234"
        })
        self.token = resp.json().get("access_token", "")

    @task(5)
    def ver_dashboard(self):
        self.client.get(
            "/dashboard",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(3)
    def nueva_transaccion(self):
        self.client.post(
            "/transaccion",
            json={"monto": 50, "tipo": "gasto", "categoria_id": 1},
            headers={"Authorization": f"Bearer {self.token}"}
        )
