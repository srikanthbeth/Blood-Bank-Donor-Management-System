from datetime import date, timedelta


def create_inventory(client, staff_headers):
    client.post(
        "/inventory",
        json={
            "blood_group": "O+",
            "units_available": 20,
            "expiry_date": (date.today() + timedelta(days=30)).isoformat(),
            "storage_location": "Freezer A"
        },
        headers=staff_headers
    )


def test_create_request(client, staff_headers):

    create_inventory(client, staff_headers)

    response = client.post(
        "/requests",
        json={
            "hospital_name": "Apollo Hospital",
            "blood_group": "O+",
            "units_required": 5,
            "request_date": date.today().isoformat(),
            "status": "Pending"
        },
        headers=staff_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Pending"


def test_get_requests(client, staff_headers):

    create_inventory(client, staff_headers)

    client.post(
        "/requests",
        json={
            "hospital_name": "Apollo Hospital",
            "blood_group": "O+",
            "units_required": 5,
            "request_date": date.today().isoformat(),
            "status": "Pending"
        },
        headers=staff_headers
    )

    response = client.get(
        "/requests",
        headers=staff_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_request_by_id(client, staff_headers):

    create_inventory(client, staff_headers)

    client.post(
        "/requests",
        json={
            "hospital_name": "Yashoda",
            "blood_group": "O+",
            "units_required": 4,
            "request_date": date.today().isoformat(),
            "status": "Pending"
        },
        headers=staff_headers
    )

    response = client.get(
        "/requests/1",
        headers=staff_headers
    )

    assert response.status_code == 200
    assert response.json()["hospital_name"] == "Yashoda"


def test_approve_request_updates_inventory(client, staff_headers):

    create_inventory(client, staff_headers)

    client.post(
        "/requests",
        json={
            "hospital_name": "Care Hospital",
            "blood_group": "O+",
            "units_required": 5,
            "request_date": date.today().isoformat(),
            "status": "Pending"
        },
        headers=staff_headers
    )

    response = client.put(
        "/requests/1",
        json={
            "status": "Approved"
        },
        headers=staff_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Approved"

    inventory = client.get(
        "/inventory",
        headers=staff_headers
    )

    assert inventory.json()[0]["units_available"] == 15


def test_insufficient_stock(client, staff_headers):

    client.post(
        "/inventory",
        json={
            "blood_group": "A+",
            "units_available": 2,
            "expiry_date": (date.today() + timedelta(days=30)).isoformat(),
            "storage_location": "Freezer B"
        },
        headers=staff_headers
    )

    client.post(
        "/requests",
        json={
            "hospital_name": "Apollo",
            "blood_group": "A+",
            "units_required": 5,
            "request_date": date.today().isoformat(),
            "status": "Pending"
        },
        headers=staff_headers
    )

    response = client.put(
        "/requests/1",
        json={
            "status": "Approved"
        },
        headers=staff_headers
    )

    assert response.status_code == 400
    assert "Insufficient" in response.json()["detail"]