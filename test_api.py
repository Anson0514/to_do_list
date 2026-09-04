import unittest
from fastapi.testclient import TestClient
from main2 import app


class ItemApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_crud_flow(self):
        create_response = self.client.post("/items", json={"name": "Laptop", "price": 999.99})
        self.assertEqual(create_response.status_code, 201)
        body = create_response.json()
        self.assertIn("id", body)
        item_id = body["id"]

        get_response = self.client.get(f"/items/{item_id}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["name"], "Laptop")

        update_response = self.client.put(f"/items/{item_id}", json={"name": "Laptop Pro", "price": 1299.99})
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["name"], "Laptop Pro")

        delete_response = self.client.delete(f"/items/{item_id}")
        self.assertEqual(delete_response.status_code, 200)

        missing_response = self.client.get(f"/items/{item_id}")
        self.assertEqual(missing_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
