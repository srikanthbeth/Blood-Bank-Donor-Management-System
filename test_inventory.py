from datetime import date, timedelta


def test_create_inventory(client, staff_headers):

    response = client.post(
        "/inventory",
        json={
            "blood_group": "O+",
            "units_available": 10,
            "expiry_date": (date.today() + timedelta(days=30)).isoformat(),
            "storage_location": "Freezer A"
        },
        headers=staff_headers
    )

    assert response.status_code == 200
    assert response.json()["blood_group"] == "O+"


def test_get_inventory(client, staff_headers):

    client.post(
        "/inventory",
        json={
            "blood_group": "A+",
            "units_available": 20,
            "expiry_date": (date.today() + timedelta(days=30)).isoformat(),
            "storage_location": "Freezer B"
        },
        headers=staff_headers
    )

    response = client.get(
        "/inventory",
        headers=staff_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_inventory(client, staff_headers):

    client.post(
        "/inventory",
        json={
            "blood_group": "B+",
            "units_available": 5,
            "expiry_date": (date.today() + timedelta(days=30)).isoformat(),
            "storage_location": "Freezer C"
        },
        headers=staff_headers
    )

    response = client.put(
        "/inventory/1",
        json={
            "units_available": 15
        },
        headers=staff_headers
    )

    assert response.status_code == 200
    assert response.json()["units_available"] == 15


def test_expired_inventory(client, staff_headers):

    response = client.post(
        "/inventory",
        json={
            "blood_group": "AB+",
            "units_available": 10,
            "expiry_date": (date.today() - timedelta(days=1)).isoformat(),
            "storage_location": "Freezer D"
        },
        headers=staff_headers
    )

    assert response.status_code == 400