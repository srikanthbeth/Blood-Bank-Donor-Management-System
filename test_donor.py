def test_create_donor(client, admin_headers):

    response = client.post(
        "/donors",
        json={
            "name": "Rahul",
            "age": 25,
            "blood_group": "O+",
            "phone": "9876543210",
            "city": "Hyderabad",
            "last_donation_date": "2026-01-01",
            "is_eligible": True,
            "user_id": None
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    assert response.json()["name"] == "Rahul"


def test_get_all_donors(client, admin_headers):

    client.post(
        "/donors",
        json={
            "name": "Rahul",
            "age": 25,
            "blood_group": "O+",
            "phone": "9876543210",
            "city": "Hyderabad",
            "last_donation_date": "2026-01-01",
            "is_eligible": True,
            "user_id": None
        },
        headers=admin_headers
    )

    response = client.get(
        "/donors",
        headers=admin_headers
    )

    assert response.status_code == 200

    assert len(response.json()) == 1


def test_get_donor_by_id(client, admin_headers):

    client.post(
        "/donors",
        json={
            "name": "Rahul",
            "age": 25,
            "blood_group": "A+",
            "phone": "9999999999",
            "city": "Hyderabad",
            "last_donation_date": "2026-01-01",
            "is_eligible": True,
            "user_id": None
        },
        headers=admin_headers
    )

    response = client.get(
        "/donors/1",
        headers=admin_headers
    )

    assert response.status_code == 200

    assert response.json()["id"] == 1


def test_update_donor(client, admin_headers):

    client.post(
        "/donors",
        json={
            "name": "Rahul",
            "age": 25,
            "blood_group": "B+",
            "phone": "8888888888",
            "city": "Hyderabad",
            "last_donation_date": "2026-01-01",
            "is_eligible": True,
            "user_id": None
        },
        headers=admin_headers
    )

    response = client.put(
        "/donors/1",
        json={
            "city": "Vijayawada"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    assert response.json()["city"] == "Vijayawada"


def test_delete_donor(client, admin_headers):

    client.post(
        "/donors",
        json={
            "name": "Rahul",
            "age": 25,
            "blood_group": "AB+",
            "phone": "7777777777",
            "city": "Hyderabad",
            "last_donation_date": "2026-01-01",
            "is_eligible": True,
            "user_id": None
        },
        headers=admin_headers
    )

    response = client.delete(
        "/donors/1",
        headers=admin_headers
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Donor deleted successfully"


def test_duplicate_phone(client, admin_headers):

    donor = {
        "name": "Rahul",
        "age": 25,
        "blood_group": "O+",
        "phone": "9000000000",
        "city": "Hyderabad",
        "last_donation_date": "2026-01-01",
        "is_eligible": True,
        "user_id": None
    }

    client.post(
        "/donors",
        json=donor,
        headers=admin_headers
    )

    response = client.post(
        "/donors",
        json=donor,
        headers=admin_headers
    )

    assert response.status_code == 400


def test_invalid_age(client, admin_headers):

    response = client.post(
        "/donors",
        json={
            "name": "Rahul",
            "age": 16,
            "blood_group": "O+",
            "phone": "9111111111",
            "city": "Hyderabad",
            "last_donation_date": "2026-01-01",
            "is_eligible": True,
            "user_id": None
        },
        headers=admin_headers
    )

    assert response.status_code == 422