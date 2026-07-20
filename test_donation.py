from datetime import date, timedelta


def setup_donor(client, admin_headers):

    client.post(
        "/donors",
        json={
            "name": "Rahul",
            "age": 25,
            "blood_group": "O+",
            "phone": "9999999999",
            "city": "Hyderabad",
            "last_donation_date": "2025-01-01",
            "is_eligible": True,
            "user_id": None
        },
        headers=admin_headers
    )


def test_create_donation(client, admin_headers):

    setup_donor(client, admin_headers)

    response = client.post(
        "/donations",
        json={
            "donor_id": 1,
            "blood_group": "O+",
            "units_donated": 2,
            "donation_date": date.today().isoformat()
        },
        headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()["units_donated"] == 2


def test_90_day_rule(client, admin_headers):

    setup_donor(client, admin_headers)

    client.post(
        "/donations",
        json={
            "donor_id": 1,
            "blood_group": "O+",
            "units_donated": 2,
            "donation_date": date.today().isoformat()
        },
        headers=admin_headers
    )

    response = client.post(
        "/donations",
        json={
            "donor_id": 1,
            "blood_group": "O+",
            "units_donated": 1,
            "donation_date": (date.today() + timedelta(days=10)).isoformat()
        },
        headers=admin_headers
    )

    assert response.status_code == 400