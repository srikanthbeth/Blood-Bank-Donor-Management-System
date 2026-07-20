from datetime import date, timedelta


def setup_data(client, admin_headers, staff_headers):

    client.post(
        "/donors",
        json={
            "name": "Rahul",
            "age": 25,
            "blood_group": "O+",
            "phone": "9999999999",
            "city": "Hyderabad",
            "last_donation_date": "2026-01-01",
            "is_eligible": True,
            "user_id": None
        },
        headers=admin_headers
    )

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

    client.post(
        "/requests",
        json={
            "hospital_name": "Apollo",
            "blood_group": "O+",
            "units_required": 5,
            "request_date": date.today().isoformat(),
            "status": "Pending"
        },
        headers=staff_headers
    )


def test_search_donors(client, admin_headers, staff_headers):

    setup_data(client, admin_headers, staff_headers)

    response = client.get(
    "/reports/donors",
    params={"blood_group": "O+"},
    headers=admin_headers
)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_requests(client, admin_headers, staff_headers):

    setup_data(client, admin_headers, staff_headers)

    response = client.get(
        "/reports/requests?status=Pending",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_inventory_report(client, admin_headers, staff_headers):

    setup_data(client, admin_headers, staff_headers)

    response = client.get(
        "/reports/inventory",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()[0]["blood_group"] == "O+"


def test_pagination(client, admin_headers, staff_headers):

    setup_data(client, admin_headers, staff_headers)

    response = client.get(
        "/reports/donors?page=1&limit=1",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1